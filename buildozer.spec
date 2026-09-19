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

requirements = python3,kivy,kivymd,pyjnius,reportlab,pillow

orientation = portrait

fullscreen = 0


# ============================================================
# ANDROID
# ============================================================

android.api = 36

android.minapi = 24

android.ndk = 28c

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

android.allow_backup = True

android.debug_artifact = apk

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

p4a.fork = kivy

p4a.branch = develop

p4a.bootstrap = sdl2


# ============================================================
# ANDROID DISPLAY
# ============================================================

android.immersive_mode = False


# ============================================================
# OPTIONAL
# ============================================================

# icon.filename = %(source.dir)s/icon.png

# presplash.filename = %(source.dir)s/presplash.png
# android.presplash_color = #FFFFFF

