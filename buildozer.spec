[app]

# ================================================================
# TEACHER RESULT MANAGER PRO
# ================================================================

title = Teacher Result Manager Pro

package.name = teacherresultmanagerpro

package.domain = org.teacherresultmanagerpro

source.dir = .

source.main = main.py

version = 1.0.0

# ================================================================
# PYTHON REQUIREMENTS
# ================================================================

requirements = python3,kivy,kivymd,pyjnius,reportlab,pillow

# ================================================================
# SOURCE FILES
# ================================================================

source.include_exts = py,kv,png,jpg,jpeg,gif,ttf,otf,atlas,json,txt,xml

source.include_patterns = student_photos/*,fonts/*

source.exclude_exts = pyc,pyo

source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__


# ================================================================
# DISPLAY
# ================================================================

orientation = portrait

fullscreen = 0


# ================================================================
# ICON
# ================================================================

# If you have icon.png in the root folder, remove the # below.
#
# icon.filename = %(source.dir)s/icon.png


# ================================================================
# PRESPLASH
# ================================================================

# Disabled intentionally for maximum compatibility.
#
# presplash.filename = %(source.dir)s/presplash.png


# ================================================================
# ANDROID
# ================================================================

android.api = 35

android.minapi = 21

android.ndk = 25b

android.ndk_api = 21

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

android.entrypoint = org.kivy.android.PythonActivity

android.apptheme = @android:style/Theme.Material.Light.NoActionBar

android.allow_backup = True

android.permissions = INTERNET


# ================================================================
# PYTHON-FOR-ANDROID
# ================================================================

p4a.bootstrap = sdl2

# IMPORTANT:
# Use the stable/master p4a branch with Python 3.12.
#
p4a.branch = master


# ================================================================
# ANDROID DEBUG
# ================================================================

android.debug_artifact = apk


# ================================================================
# ANDROID RELEASE
# ================================================================

android.release_artifact = aab


# ================================================================
# LOGCAT
# ================================================================

android.logcat_filters = *:S python:D


# ================================================================
# EXTRA P4A ARGUMENTS
# ================================================================

# Keep empty.
#
# p4a.extra_args =


# ================================================================
# BACKUP
# ================================================================

# Keep Android backup enabled.
android.allow_backup = True


# ================================================================
# END
# ================================================================
