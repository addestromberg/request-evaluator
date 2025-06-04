# scripts/pack.py

import subprocess
import sys

def main():
    cmd = [
        "OctoBot", "tentacles",
        "--pack",
        "../pack/request_tentacle.zip",
        "--directory",
        "src/",
    ]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)