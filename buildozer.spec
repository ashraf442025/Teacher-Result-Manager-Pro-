[app]

# ============================================================
# TEACHER RESULT MANAGER PRO
# ============================================================

# (str) Title of your application
title = Teacher Result Manager Pro

# (str) Package name
package.name = teacherresultmanager

# (str) Package domain
package.domain = org.teacherresultmanager

# (str) Source code directory
source.dir = .

# (str) Main Python file
source.main = main.py

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json,txt,xml

# (list) Source files to exclude
# source.exclude_exts =

# (list) Directories to exclude
# source.exclude_dirs = tests, bin, .buildozer

# (str) Application version
version = 1.0.0

# (str) Application requirements
requirements = python3,kivy,kivymd,pyjnius,reportlab,pillow

# (str) Orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 0


# ============================================================
# ANDROID
# ============================================================

# Target Android API
android.api = 36

# Minimum Android API
android.minapi = 24

# Android NDK
android.ndk = 28c

# Android architectures
android.archs = arm64-v8a,armeabi-v7a

# Accept Android SDK license
android.accept_sdk_license = True

# Android application backup
android.allow_backup = True

# Debug APK
android.debug_artifact = apk

# Release artifact
android.release_artifact = aab


# ============================================================
# ANDROID PERMISSIONS
# ============================================================

android.permissions = INTERNET


# ============================================================
# ANDROIDX
# ============================================================

android.enable_androidx = True


# ============================================================
# PYTHON-FOR-ANDROID
# ============================================================

# Use Kivy's python-for-android
p4a.fork = kivy

# Current development branch
p4a.branch = develop

# SDL2 bootstrap for Kivy
p4a.bootstrap = sdl2


# ============================================================
# JAVA / GRADLE
# ============================================================

# Java 17 is used by GitHub Actions
# java version is controlled from build-apk.yml


# ============================================================
# PRESPLASH
# ============================================================

# presplash.filename = %(source.dir)s/data/presplash.png
# android.presplash_color = #FFFFFF


# ============================================================
# ICON
# ============================================================

# If you later add an icon:
# icon.filename = %(source.dir)s/icon.png


# ============================================================
# ANDROID LOGCAT
# ============================================================

# android.logcat_filters = *:S python:D


# ============================================================
# ANDROID IMMERSIVE MODE
# ============================================================

android.immersive_mode = False


# ============================================================
# ANDROID META DATA
# ============================================================

# android.meta_data =


# ============================================================
# ANDROID FEATURES
# ============================================================

# android.features =


# ============================================================
# GOOGLE PLAY / APP BUNDLE
# ============================================================

# Release builds can generate AAB.
# Debug builds generate APK.


# ============================================================
# PYTHON-FOR-ANDROID EXTRA ARGUMENTS
# ============================================================

# p4a.extra_args =


# ============================================================
# BUILD OPTIONS
# ============================================================

# android.copy_libs = 1

# android.no-byte-compile-python = False


# ============================================================
# OUTPUT
# ============================================================

# Debug APK will be generated in:
# bin/
