[app]

# ============================================================
# TEACHER RESULT MANAGER PRO
# ============================================================

title = Teacher Result Manager Pro

package.name = teacherresultmanager
package.domain = org.teacherresultmanager

source.dir = .
source.main = main.py

# ------------------------------------------------------------
# Files to include
# ------------------------------------------------------------

source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json,txt,xml

# ------------------------------------------------------------
# Version
# ------------------------------------------------------------

version = 1.0.0

# ------------------------------------------------------------
# Python / Kivy requirements
# ------------------------------------------------------------

requirements = python3,kivy,kivymd,pyjnius,reportlab,pillow

# ------------------------------------------------------------
# Orientation
# ------------------------------------------------------------

orientation = portrait
fullscreen = 0

# ------------------------------------------------------------
# Android
# ------------------------------------------------------------

android.api = 35
android.minapi = 24
android.ndk = 28c

# IMPORTANT:
# First APK build uses ARM64 only.
# This greatly reduces native compilation time.
android.archs = arm64-v8a

# ------------------------------------------------------------
# Android permissions
# ------------------------------------------------------------

android.permissions = INTERNET

# ------------------------------------------------------------
# Android build options
# ------------------------------------------------------------

android.enable_androidx = True
android.allow_backup = True

# ------------------------------------------------------------
# APK output
# ------------------------------------------------------------

android.debug_artifact = apk
android.release_artifact = aab

# ------------------------------------------------------------
# Python-for-Android
# ------------------------------------------------------------

p4a.bootstrap = sdl2

# Do NOT force an old p4a branch.
# Buildozer will use the compatible p4a available
# in the build environment.
