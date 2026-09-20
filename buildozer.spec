[app]

# ============================================================
# TEACHER RESULT MANAGER PRO
# ============================================================

title = Teacher Result Manager Pro

package.name = teacherresultmanager
package.domain = org.teacherresultmanager

source.dir = .
source.main = main.py

source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json,txt,xml

version = 1.0.0

# ============================================================
# APPLICATION REQUIREMENTS
# ============================================================

requirements = python3,kivy,kivymd,pyjnius,reportlab,pillow

# ============================================================
# DISPLAY
# ============================================================

orientation = portrait
fullscreen = 0

# ============================================================
# ANDROID
# ============================================================

android.api = 35
android.minapi = 24
android.ndk = 28c

# ARM64 only for the first stable build
android.archs = arm64-v8a

# ============================================================
# ANDROID PERMISSIONS
# ============================================================

android.permissions = INTERNET

# ============================================================
# ANDROID OPTIONS
# ============================================================

android.enable_androidx = True
android.allow_backup = True

# Automatically accept Android SDK licenses
android.accept_sdk_license = True

# ============================================================
# OUTPUT
# ============================================================

android.debug_artifact = apk
android.release_artifact = aab

# ============================================================
# PYTHON-FOR-ANDROID
# ============================================================

p4a.bootstrap = sdl2
