import subprocess
import os
import socket

host = socket.gethostname()
ipv4 = socket.gethostbyname_ex(host)[2][-1]
print(ipv4)

# os.chdir("D:/Python Programs/NAS-FastAPI")
# subprocess.run(["uvicorn", "main:app", "--host", ipv4, "--port", "8000"])