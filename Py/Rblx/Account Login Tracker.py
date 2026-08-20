def installdepsfunc(content):
    """
    Install dependencies for the project.
    
    pass in a raw string literal as file content.
    """
    import os
    import subprocess
    content = "python -m pip install " + content

    def makefile(path, name, contents):
        """
        Create a .bat file with the given contents.
        path     : directory where the file will be created
        name     : filename (without extension, or with .bat)
        contents : string containing batch commands

        also returns path to the new file
        """
        # Ensure the directory exists
        os.makedirs(path, exist_ok=True)
        
        # Add .bat extension if not present
        if not name.endswith('.bat'):
            name += '.bat'
        
        full_path = os.path.join(path, name)
        
        with open(full_path, 'w') as f:
            f.write("python -m pip install --upgrade pip\n" + contents)
        
        return full_path
    def runfile(full_path):
        """
        Executes a file from "path" given
        """
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"File not found: {full_path}")
        
        # Run the batch file and wait for completion
        result = subprocess.run(full_path, shell=True, capture_output=True, text=True)
        return result
    def delfile(full_path):
        """
        Deletes a file from "path" given
        """
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            print(f"Warning: {full_path} dosen't exist.")

    # 1. Create file
    print("[Deps Installer] Creating File...")
    file_path = makefile(r"C:\Users\Public\Temp", "install_deps.bat", content)

    # 2. run dat
    print("[Deps Installer] Running File...")
    try:
        result = runfile(file_path)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running batch: {e}")
        
    # 3. delete it :3
    print("[Deps Installer] Finished.")
    delfile(file_path)
    subprocess.call('cls', shell=True) # cls for windwos

installdepsfunc(r"requests")

import requests
import time
from datetime import datetime
import re
import os

# ============= Configs =============
USER_ID = re.sub(r'[^0-9]', '', input("Enter Target (Profile Link) or (UserID) : ") )   # Change this to the user you want to monitor
POLL_INTERVAL = 30     # Seconds between checks (recommended 30)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, f"OnlineLogs [{USER_ID}].txt")
# ===================================

PRESENCE_URL = "https://presence.roproxy.com/v1/presence/users"

# Mapping of Roblox presence codes to labels
PRESENCE_LABELS = {
    0: "Offline",
    1: "Online",
    2: "In-game",
    3: "Studio"
}

def get_presence(user_id):
    """Return the presence label (string) or None on error."""
    try:
        payload = {"userIds": [user_id]}
        response = requests.post(PRESENCE_URL, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("userPresences"):
                code = data["userPresences"][0]["userPresenceType"]
                return PRESENCE_LABELS.get(code, "Unknown")
        else:
            print(f"[WARN] API returned {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

def log_session(start_time, end_time, state_label):
    """Append a session to the log file in the requested format."""
    with open(LOG_FILE, "a") as f:
        start_str = start_time.strftime("%I:%M %p").lower()
        end_str = end_time.strftime("%I:%M %p").lower()
        date_str = start_time.strftime("%d/%m/%Y")  # e.g., 16/07/2026
        f.write(f"{start_str} - {end_str} ( d/m/y - {date_str} ) [{state_label}],\n")
    print(f"[LOG] {start_str} - {end_str} ( d/m/y - {date_str} ) [{state_label}]")

def main():
    print("\033[H\033[J", end="")  # Clears screen and moves cursor to top-left
    print(f"Monitoring user {USER_ID} every {POLL_INTERVAL}s...")
    print(f"Logging to: {LOG_FILE}")
    print("Press Ctrl+C to stop.\n")

    current_state = None      # Last known state label (or None at start)
    session_start = None      # Start time of the current non-offline session

    while True:
        try:
            new_state = get_presence(USER_ID)
            if new_state is None:
                time.sleep(POLL_INTERVAL)
                continue

            now = datetime.now()

            # --- State change logic ---
            if new_state == "Offline":
                # If we were in a non-offline session, close it
                if session_start is not None:
                    log_session(session_start, now, current_state)
                    session_start = None
                # Update current state (even if it was already Offline)
                current_state = "Offline"

            else:  # new_state is one of: Online, In-game, Studio
                if session_start is None:
                    # We were offline – start a new session
                    session_start = now
                    current_state = new_state
                    print(f"[START] {new_state} at {now.strftime('%I:%M %p')}")
                elif new_state != current_state:
                    # State changed from one non-offline to another (e.g. Online → In-game)
                    log_session(session_start, now, current_state)
                    session_start = now
                    current_state = new_state
                    print(f"[SWITCH] {new_state} at {now.strftime('%I:%M %p')}")
                # else: same state, nothing to do

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\n[STOPPED] Monitoring ended.")
            # If a session is still open, log it with the current time as end
            if session_start is not None:
                log_session(session_start, datetime.now(), current_state)
                print("[WARN] Final session was still active – logged with current time.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
