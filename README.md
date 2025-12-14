# 🤖 apktool clean rebuild 
Fix broken APK recompilation by installing a clean, upstream Apktool instead of distro-patched versions.

### ⚠️ Important Notes

* If Apktool was previously installed from your Linux distribution (APT), it may cause APK recompilation issues.

* This script installs the official upstream Apktool into /usr/local/bin, which takes precedence in PATH.

⚠️ Remove distro-installed Apktool (manual) do it manually: `sudo apt purge apktool`


### ▶️ Usage

* This script must be run with sudo, as it installs files into /usr/local/bin:

* `sudo python3 apktool.py`

### ✅ Verification

After installation:

* `apktool --version`
* `which apktool`

You should see /usr/local/bin/apktool.

