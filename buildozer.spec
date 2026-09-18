[app]

# (str) Title of your application
title = Teacher Result Manager Pro

# (str) Package name
package.name = teacherresultmanagerpro

# (str) Package domain
package.domain = org.teacherresultmanager

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json,txt,db

# (list) Source exclude patterns
source.exclude_exts = pyc,pyo

# (list) List of inclusions using pattern matching
# source.include_patterns = assets/*,images/*

# (str) Application version
version = 1.0.0


# ----------------------------------------------------------------
# REQUIREMENTS
# ----------------------------------------------------------------

# (list) Python modules required by the application
requirements = python3,kivy,pyjnius,reportlab


# ----------------------------------------------------------------
# ORIENTATION
# ----------------------------------------------------------------

# (str) Supported orientation (one of landscape, sensorLandscape,
# portrait or sensorPortrait)
orientation = portrait


# ----------------------------------------------------------------
# ICON
# ----------------------------------------------------------------

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png


# ----------------------------------------------------------------
# ANDROID
# ----------------------------------------------------------------

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.apptheme = @android:style/Theme.Material.Light.NoActionBar

# (str) Android API to use
android.api = 35

# (str) Minimum API required
android.minapi = 23

# (str) Android NDK version
android.ndk = 27c

# (str) Android architecture
android.archs = arm64-v8a,armeabi-v7a

# (bool) Android accept SDK license
android.accept_sdk_license = True

# (str) Android permissions
android.permissions = INTERNET

# (str) Android application activity orientation
android.orientation = portrait

# (bool) Enable Android backup
android.allow_backup = True


# ----------------------------------------------------------------
# ANDROID META-DATA
# ----------------------------------------------------------------

# (str) Android app label
android.add_src =


# ----------------------------------------------------------------
# JAVA / GRADLE
# ----------------------------------------------------------------

# (str) Gradle version
# Leave blank so Buildozer/p4a selects the compatible version

# android.gradle_dependencies =

# (str) Android private storage
android.private_storage = True


# ----------------------------------------------------------------
# LOGGING
# ----------------------------------------------------------------

# (str) Log level
log_level = 2

# (bool) Warn on unsupported requirements
warn_on_root = 1


# ----------------------------------------------------------------
# BUILD OPTIONS
# ----------------------------------------------------------------

# (str) Build mode
# debug or release
android.debug = 1

# (str) Android build tools version
# Leave empty for automatic selection
# android.build_tools_version =


# ----------------------------------------------------------------
# P4A OPTIONS
# ----------------------------------------------------------------

# (str) Python-for-Android extra arguments
# p4a.extra_args =


# ----------------------------------------------------------------
# PRESPLASH
# ----------------------------------------------------------------

# (int) Presplash background color
# presplash.color = #FFFFFF


# ----------------------------------------------------------------
# WINDOWS / DESKTOP
# ----------------------------------------------------------------

# No special desktop settings required.


# ----------------------------------------------------------------
# ADVANCED
# ----------------------------------------------------------------

# (bool) Android fullscreen immersive mode
android.immersive_mode = False

# (str) Android backup rules
# android.backup_rules =

# (str) Android manifest additions
# android.add_manifest_xml =


# ----------------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------------

# APK will normally be generated inside:
# bin/


# ----------------------------------------------------------------
# USER DATA
# ----------------------------------------------------------------

# The application will use its Android private storage for:
# teacher_result_manager.db
# student_photos/
# PDF files/
