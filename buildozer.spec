[app]

title = Teacher Result Manager
package.name = teacherresultmanager
package.domain = org.example

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0


[buildozer]

log_level = 2
warn_on_root = 1


[buildozer:android]

android.api = 35
android.minapi = 24
android.ndk = 28c
android.accept_sdk_license = True
