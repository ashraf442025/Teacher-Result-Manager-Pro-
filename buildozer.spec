[app]

# ================================================================
# TEACHER RESULT MANAGER PRO
# Android / Pydroid 3 / GitHub Actions
# ================================================================

# (str) Title of your application
title = Teacher Result Manager Pro

# (str) Package name
package.name = teacherresultmanagerpro

# (str) Package domain
package.domain = org.teacherresultmanagerpro

# (str) Source code directory
source.dir = .

# (str) Main Python file
source.main = main.py

# (str) Application version
version = 1.0.0

# (str) Application requirements
requirements = python3,kivy,pyjnius,reportlab

# (str) Supported orientation
orientation = portrait

# (list) Source file extensions
source.include_exts = py,kv,png,jpg,jpeg,gif,ttf,otf,db,txt,pdf

# (list) Source include patterns
source.include_patterns = student_photos/*,fonts/*

# (str) Application icon
# Keep empty unless icon.png exists
# icon.filename = %(source.dir)s/icon.png

# (str) Presplash
# Keep disabled for maximum compatibility
# presplash.filename = %(source.dir)s/presplash.png


# ================================================================
# ANDROID
# ================================================================

# (str) Android API target
android.api = 35

# (str) Minimum Android API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (str) Android NDK API
android.ndk_api = 21

# (str) Android architectures
android.archs = arm64-v8a, armeabi-v7a

# (bool) Android accept SDK licenses
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.apptheme = @android:style/Theme.Material.Light.NoActionBar


# (str) Android permissions
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE


# ================================================================
# PYTHON FOR ANDROID
# ================================================================

# Use standard SDL2 bootstrap for Kivy
p4a.bootstrap = sdl2

# Do NOT force a GitHub fork/branch here.
# This avoids unnecessary external p4a source problems.

# p4a.fork =
# p4a.branch =


# ================================================================
# LOGCAT / DEBUG
# ================================================================

# (bool) Show Android logcat during debug
android.logcat_filters = *:S python:D


# ================================================================
# WINDOWS / DESKTOP
# ================================================================

# No special settings required.


# ================================================================
# BUILD SETTINGS
# ================================================================

# (str) Python-for-Android extra arguments
# Keep this empty.
# p4a.extra_args =


# ================================================================
# PRESPLASH
# ================================================================

# (int) Presplash background color
presplash.color = #FFFFFF


# ================================================================
# FILES / ASSETS
# ================================================================

# Additional files are already handled by source.include_exts
# and source.include_patterns.


# ================================================================
# ADVANCED
# ================================================================

# (str) Android additional arguments
# android.add_src =

# (str) Android additional libraries
# android.add_libs_armeabi_v7a =

# android.add_libs_arm64_v8a =

# (str) Android whitelist
# android.whitelist_src =

# (str) Android blacklist
# android.blacklist_src =

# (str) Python-for-Android whitelist
# p4a.whitelist_src =

# (str) Python-for-Android blacklist
# p4a.blacklist_src =


# ================================================================
# END
# ================================================================
