# ============================================================
# Minecraft-style voxel demo - chunked, greedy-meshed terrain
# ============================================================

import json
import os
import random

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise

# ------------------------------------------------------------
# Settings loading (with safe fallback defaults)
# ------------------------------------------------------------

DEFAULT_SETTINGS = {
    "WORLD_SIZE": 8,
    "HEIGHT_MIN": 5,
    "HEIGHT_MAX": 8,
    "FREQUENCY": 0.1,
    "CHUNK_SIZE": 10,
    "SEED": None
}

def load_settings(path="Settings.json"):
    settings = dict(DEFAULT_SETTINGS)
    try:
        with open(path, "r") as f:
            loaded = json.load(f)
        settings.update({k: v for k, v in loaded.items() if k in DEFAULT_SETTINGS})
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[Settings] Could not load {path} ({e}); using defaults.")
    return settings

SETTINGS = load_settings()
WORLD_SIZE = SETTINGS["WORLD_SIZE"]
HEIGHT_MIN = SETTINGS["HEIGHT_MIN"]
HEIGHT_MAX = SETTINGS["HEIGHT_MAX"]
FREQUENCY = SETTINGS["FREQUENCY"]
CHUNK_SIZE = SETTINGS["CHUNK_SIZE"]
SEED = SETTINGS["SEED"] if SETTINGS["SEED"] is not None else random.randint(0, 1000)

# Vertical range meshing considers per chunk (allows building above terrain).
WORLD_HEIGHT_LIMIT = HEIGHT_MAX + 30

# ------------------------------------------------------------
# App / world basics
# ------------------------------------------------------------

app = Ursina()
player = FirstPersonController()
camera.clip_plane_far = 20

Sky()

BLOCK_TEXTURES = ["grass.jpg", "dirt.jpg", "stone.jpeg", "iron.jpg", "bedrock.jpg"]
TEX_ID = {name: i for i, name in enumerate(BLOCK_TEXTURES)}
ID_TEX = {i: name for name, i in TEX_ID.items()}
BEDROCK_ID = TEX_ID["bedrock.jpg"]

# ------------------------------------------------------------
# World data (sparse, shared across chunks)
# key: (x, y, z) -> texture_id (int)
# ------------------------------------------------------------

block_data = {}       # (x,y,z) -> texture_id
bedrock_positions = set()
chunk_entities = {}   # (cx, cz) -> list of Entities (one per texture present)
block_active = [BLOCK_TEXTURES[0]]  # currently selected block name, or None if slot empty

noise_height = PerlinNoise(octaves=1, seed=SEED)
noise_height2 = PerlinNoise(octaves=1, seed=SEED + 1000)
noise_thickness = PerlinNoise(octaves=1, seed=SEED + 2000)


def fbm_height(x, z):
    """3-octave fractal Brownian motion for more natural terrain than raw Perlin."""
    total = 0.0
    max_val = 0.0
    amplitude = 1.0
    freq = 1.0
    sources = [noise_height, noise_height2, noise_height]
    for i in range(3):
        total += sources[i]([x * FREQUENCY * freq, z * FREQUENCY * freq]) * amplitude
        max_val += amplitude
        amplitude *= 0.5
        freq *= 2
    return total / max_val  # roughly -1..1


def get_height(x, z):
    n = fbm_height(x, z)
    height = int((n + 1) / 2 * (HEIGHT_MAX - HEIGHT_MIN) + HEIGHT_MIN)
    return max(HEIGHT_MIN, min(HEIGHT_MAX, height))


def get_stone_thickness(x, z, total):
    n = noise_thickness([x * FREQUENCY, z * FREQUENCY])  # -1..1
    frac = (n + 1) / 2
    lo, hi = 5, max(5, min(9, total - 2))
    if hi < lo:
        return lo
    return int(lo + frac * (hi - lo))


def world_to_chunk(x, z):
    return (x // CHUNK_SIZE, z // CHUNK_SIZE)


def generate_world():
    for x in range(-WORLD_SIZE, WORLD_SIZE):
        for z in range(-WORLD_SIZE, WORLD_SIZE):
            height = get_height(x, z)
            total = height - 2
            stone_thickness = get_stone_thickness(x, z, total)
            dirt_thickness = max(0, total - stone_thickness)

            block_data[(x, 0, z)] = BEDROCK_ID
            bedrock_positions.add((x, 0, z))

            for y in range(1, 1 + stone_thickness):
                block_data[(x, y, z)] = TEX_ID["stone.jpeg"]

            for y in range(1 + stone_thickness, 1 + stone_thickness + dirt_thickness):
                block_data[(x, y, z)] = TEX_ID["dirt.jpg"]

            block_data[(x, height - 1, z)] = TEX_ID["grass.jpg"]

# ------------------------------------------------------------
# Greedy meshing (per chunk, per axis, per direction, per texture)
# ------------------------------------------------------------

# axis 0 = x, 1 = y, 2 = z
def build_chunk_mesh(cx, cz):
    x0, z0 = cx * CHUNK_SIZE, cz * CHUNK_SIZE
    dims = [CHUNK_SIZE, WORLD_HEIGHT_LIMIT, CHUNK_SIZE]
    origin = [x0, 0, z0]

    def block_at(wx, wy, wz):
        return block_data.get((wx, wy, wz))

    # Separate geometry buffers per texture id, since each texture needs its
    # own Entity/Mesh to tile correctly (no shared atlas -> no UV stretching).
    buffers = {}  # tex_id -> {'verts':[], 'uvs':[], 'tris':[], 'offset':0}

    def buf_for(tex):
        if tex not in buffers:
            buffers[tex] = {'verts': [], 'uvs': [], 'tris': [], 'offset': 0}
        return buffers[tex]

    for axis in range(3):
        u_axis = (axis + 1) % 3
        v_axis = (axis + 2) % 3
        du, dv, da = dims[u_axis], dims[v_axis], dims[axis]

        for direction in (1, -1):
            for d in range(da):
                mask = [[None] * dv for _ in range(du)]
                any_face = False
                for uu in range(du):
                    for vv in range(dv):
                        pos = [0, 0, 0]
                        pos[axis] = d
                        pos[u_axis] = uu
                        pos[v_axis] = vv
                        wx, wy, wz = pos[0] + origin[0], pos[1] + origin[1], pos[2] + origin[2]
                        cur = block_at(wx, wy, wz)
                        if cur is None:
                            continue
                        npos = pos[:]
                        npos[axis] += direction
                        nwx = npos[0] + origin[0]
                        nwy = npos[1] + origin[1]
                        nwz = npos[2] + origin[2]
                        if block_at(nwx, nwy, nwz) is None:
                            mask[uu][vv] = cur
                            any_face = True

                if not any_face:
                    continue

                visited = [[False] * dv for _ in range(du)]
                for uu in range(du):
                    for vv in range(dv):
                        if mask[uu][vv] is None or visited[uu][vv]:
                            continue
                        tex = mask[uu][vv]

                        w = 1
                        while vv + w < dv and mask[uu][vv + w] == tex and not visited[uu][vv + w]:
                            w += 1

                        h = 1
                        stop = False
                        while uu + h < du and not stop:
                            for k in range(w):
                                if mask[uu + h][vv + k] != tex or visited[uu + h][vv + k]:
                                    stop = True
                                    break
                            if not stop:
                                h += 1

                        for hh in range(h):
                            for ww in range(w):
                                visited[uu + hh][vv + ww] = True

                        plane = d + 1 if direction == 1 else d
                        p0 = [0, 0, 0]; p0[axis] = plane; p0[u_axis] = uu;     p0[v_axis] = vv
                        p1 = [0, 0, 0]; p1[axis] = plane; p1[u_axis] = uu + h; p1[v_axis] = vv
                        p2 = [0, 0, 0]; p2[axis] = plane; p2[u_axis] = uu + h; p2[v_axis] = vv + w
                        p3 = [0, 0, 0]; p3[axis] = plane; p3[u_axis] = uu;     p3[v_axis] = vv + w

                        quad = [
                            (p[0] + origin[0] - 0.5, p[1] + origin[1] - 0.5, p[2] + origin[2] - 0.5)
                            for p in (p0, p1, p2, p3)
                        ]
                        # UVs measured in block units (not 0..1) so the texture
                        # tiles once per block across the merged quad via the
                        # texture's natural repeat wrap, instead of stretching.
                        quad_uvs = [(0, 0), (h, 0), (h, w), (0, w)]

                        if direction == -1:
                            quad = [quad[0], quad[3], quad[2], quad[1]]
                            quad_uvs = [quad_uvs[0], quad_uvs[3], quad_uvs[2], quad_uvs[1]]

                        b = buf_for(tex)
                        b['verts'].extend(quad)
                        b['uvs'].extend(quad_uvs)
                        off = b['offset']
                        # NOTE: winding is intentionally reversed from the "natural"
                        # outward-normal order (offset,offset+2,offset+1 instead of
                        # offset,offset+1,offset+2). Ursina's MeshCollider builds its
                        # CollisionPolygon per triangle with reversed vertex order
                        # internally, which flips it again -- net result is a
                        # collision polygon that actually faces outward, so mouse
                        # raycasts from outside the block hit it. Rendering is
                        # unaffected since the entity is double_sided.
                        b['tris'].extend([off, off + 2, off + 1, off, off + 3, off + 2])
                        b['offset'] += 4

    if not buffers:
        return []

    entities = []
    for tex, b in buffers.items():
        mesh = Mesh(vertices=b['verts'], uvs=b['uvs'], triangles=b['tris'], mode='triangle')
        ent = Entity(
            model=mesh,
            texture=f'Assets/{ID_TEX[tex]}',
            collider='mesh',
            position=(0, 0, 0),
            color=color.white
        )
        ent.double_sided = True  # Entity-level property; fixes rendering AND
        ent.is_chunk = True
        entities.append(ent)

    return entities


def rebuild_chunk(cx, cz):
    key = (cx, cz)
    if key in chunk_entities:
        for ent in chunk_entities[key]:
            destroy(ent)
        del chunk_entities[key]
    entities = build_chunk_mesh(cx, cz)
    if entities:
        chunk_entities[key] = entities


def rebuild_all_chunks():
    for entities in chunk_entities.values():
        for ent in entities:
            destroy(ent)
    chunk_entities.clear()

    touched = set()
    for (x, y, z) in block_data:
        touched.add(world_to_chunk(x, z))
    for cx, cz in touched:
        rebuild_chunk(cx, cz)


def chunks_touched_by_block(pos):
    """A block can expose/hide faces in its own chunk and any neighbor chunk
    it borders, so all chunks touching its 6 neighbors need a rebuild."""
    x, y, z = pos
    coords = {world_to_chunk(x, z)}
    for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
        coords.add(world_to_chunk(x + dx, z + dz))
    return coords

# ------------------------------------------------------------
# Hotbar GUI: slots bound to 1-9 and 0 (=slot 10)
# ------------------------------------------------------------

HOTBAR_SLOTS = 10
HOTBAR_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
# Slots 1-4 pre-filled; rest start empty. Bedrock intentionally excluded (unplaceable).
HOTBAR_CONTENTS = [
    "grass.jpg", "dirt.jpg", "stone.jpeg", "iron.jpg",
    None, None, None, None, None, None
]

selected_slot = 0
slot_backgrounds = []
slot_icons = []

def build_hotbar():
    slot_size = 0.08
    spacing = 0.09
    start_x = -(spacing * (HOTBAR_SLOTS - 1)) / 2

    for i in range(HOTBAR_SLOTS):
        x_pos = start_x + i * spacing
        bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.gray,
            scale=slot_size,
            position=(x_pos, -0.45),
            z=1
        )
        slot_backgrounds.append(bg)

        icon = None
        tex_name = HOTBAR_CONTENTS[i]
        if tex_name:
            icon = Entity(
                parent=bg,
                model='quad',
                texture=f'Assets/{tex_name}',
                scale=0.65,  # smaller than bg so the grey border stays visible
                z=-0.01
            )
        slot_icons.append(icon)

    update_hotbar_selection()


def update_hotbar_selection():
    for i, bg in enumerate(slot_backgrounds):
        bg.color = color.white if i == selected_slot else color.gray
        bg.scale = 0.095 if i == selected_slot else 0.08


def select_slot(i):
    global selected_slot, block_active
    selected_slot = i
    tex_name = HOTBAR_CONTENTS[i]
    block_active.clear()
    if tex_name:
        block_active.append(tex_name)
    update_hotbar_selection()

# ------------------------------------------------------------
# Input handling
# ------------------------------------------------------------

def input(key):
    if key == 'shift':
        player.speed *= 1.5
    if key in ('left shift up', 'right shift up'):
        player.speed /= 1.5
    if key == 'c':
        player.speed /= 2
        player.camera_pivot.y = 1.5
    if key == 'c up':
        player.speed *= 2
        player.camera_pivot.y = 2

    if key == 'escape':
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.locked

    if key in HOTBAR_KEYS:
        select_slot(HOTBAR_KEYS.index(key))

    if key not in ('right mouse down', 'left mouse down'):
        return

    hit = mouse.hovered_entity
    if not hit or not getattr(hit, 'is_chunk', False) or mouse.world_point is None:
        return

    # Derive the block position from the mouse hit point + surface normal,
    # since faces now belong to merged chunk meshes rather than per-block entities.
    normal = mouse.normal
    if normal is None:
        return
    hit_point = mouse.world_point

    if key == 'right mouse down':
        place_pos = (
            round(hit_point.x + normal[0] * 0.5),
            round(hit_point.y + normal[1] * 0.5),
            round(hit_point.z + normal[2] * 0.5),
        )
        if place_pos not in block_data and block_active:
            tex_name = block_active[0]
            block_data[place_pos] = TEX_ID[tex_name]
            for cx, cz in chunks_touched_by_block(place_pos):
                rebuild_chunk(cx, cz)

    elif key == 'left mouse down':
        break_pos = (
            round(hit_point.x - normal[0] * 0.5),
            round(hit_point.y - normal[1] * 0.5),
            round(hit_point.z - normal[2] * 0.5),
        )
        if break_pos in bedrock_positions:
            print("Bedrock is unbreakable!")
            return
        if break_pos in block_data:
            del block_data[break_pos]
            for cx, cz in chunks_touched_by_block(break_pos):
                rebuild_chunk(cx, cz)

# ------------------------------------------------------------
# Player / runtime
# ------------------------------------------------------------

def player_initialise():
    spawn_height = get_height(0, 0) + 1.5
    player.position = (0, spawn_height, 0)
    player.speed = 6
    player.jump_height = 1.5
    player.camera_pivot.y = 2


generate_world()
rebuild_all_chunks()
build_hotbar()
player_initialise()
app.run()