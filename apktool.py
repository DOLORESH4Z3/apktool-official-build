#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import requests
from packaging.version import Version

APKTOOL_WRAPPER_URL = (
    "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool"
)

BITBUCKET_DOWNLOADS_API = (
    "https://api.bitbucket.org/2.0/repositories/iBotPeaches/apktool/downloads"
)

INSTALL_DIR = "/usr/local/bin"
WRAPPER_PATH = os.path.join(INSTALL_DIR, "apktool")
JAR_PATH = os.path.join(INSTALL_DIR, "apktool.jar")
TMP_DIR = "/tmp/apktool_install"


# ---------------- helpers ----------------

def require_root():
    if os.geteuid() != 0:
        print("[-] Run this script with sudo/root")
        sys.exit(1)


def run(cmd):
    print(f"[+] {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def download(url, dest):
    print(f"[+] Downloading: {url}")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(dest, "wb") as f:
        f.write(r.content)


# ---------------- apktool logic ----------------

def get_latest_apktool_jar_url():
    print("[*] Fetching latest apktool version from Bitbucket")

    r = requests.get(BITBUCKET_DOWNLOADS_API, timeout=20)
    r.raise_for_status()

    jars = []

    for item in r.json()["values"]:
        name = item["name"]
        if name.startswith("apktool_") and name.endswith(".jar"):
            version = name.replace("apktool_", "").replace(".jar", "")
            jars.append((Version(version), item["links"]["self"]["href"]))

    if not jars:
        raise RuntimeError("No apktool JARs found on Bitbucket")

    jars.sort(reverse=True)
    latest_version, latest_url = jars[0]

    print(f"[+] Latest version detected: {latest_version}")
    return latest_url, latest_version


def install_apktool():
    os.makedirs(TMP_DIR, exist_ok=True)

    wrapper_tmp = os.path.join(TMP_DIR, "apktool")
    jar_tmp = os.path.join(TMP_DIR, "apktool.jar")

    latest_jar_url, version = get_latest_apktool_jar_url()

    download(APKTOOL_WRAPPER_URL, wrapper_tmp)
    download(latest_jar_url, jar_tmp)

    print("[*] Installing into /usr/local/bin")
    shutil.move(wrapper_tmp, WRAPPER_PATH)
    shutil.move(jar_tmp, JAR_PATH)

    print("[*] Setting executable permissions")
    os.chmod(WRAPPER_PATH, 0o755)
    os.chmod(JAR_PATH, 0o755)

    shutil.rmtree(TMP_DIR)

    return version


def verify():
    print("[*] Verifying installation")
    run(["apktool", "--version"])


# ---------------- main ----------------

def main():
    require_root()
    version = install_apktool()
    verify()
    print(f"\n[✓] Apktool {version} installed cleanly from official source")


if __name__ == "__main__":
    main()
