import urllib.request
import ssl
import subprocess
import time
import os
import signal
import sys

# Ignore SSL warnings
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("Starting server...")
# Start server using the venv
server_process = subprocess.Popen(
    ["./venv/bin/python3", "main.py"],
    cwd="/home/daniel/CODING/python-protocol/web",
    # We let stdout go to console so we can might see rich output in the recording/logs if captured, 
    # but strictly for this script we might want to capture it to check for errors.
    # checking stdout for "Error" string might be good.
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT 
)

time.sleep(3) # Wait for startup

try:
    print("Testing GET / ...")
    with urllib.request.urlopen("https://localhost:8443/", context=ctx) as response:
        print(f"Status: {response.status}")
        if response.status != 200:
            raise Exception("GET / failed")

    print("Testing POST /api/sendMessage ...")
    req = urllib.request.Request(
        "https://localhost:8443/api/sendMessage",
        data="Verification Message".encode('utf-8'),
        method="POST"
    )
    with urllib.request.urlopen(req, context=ctx) as response:
        print(f"Status: {response.status}")
        body = response.read().decode('utf-8')
        print(f"Body: {body}")
        if "added to the list" not in body:
            raise Exception("POST failed")

    print("VERIFICATION SUCCESSFUL")

except Exception as e:
    print(f"VERIFICATION FAILED: {e}")
    sys.exit(1)

finally:
    print("Killing server...")
    if server_process.poll() is None:
        server_process.terminate()
        try:
            outs, _ = server_process.communicate(timeout=2)
            print("Server Output:\n", outs.decode('utf-8', errors='replace'))
        except:
            server_process.kill()
    else:
        print("Server already dead.")
        outs, _ = server_process.communicate()
        print("Server Output:\n", outs.decode('utf-8', errors='replace'))
