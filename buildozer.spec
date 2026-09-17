[app]

title = Teacher Result Manager Pro
package.name = teacherresultmanager
package.domain = org.teacherresultmanager

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf

version = 1.0

requirements = python3,kivy,kivymd,reportlab,pillow

orientation = portrait

fullscreen = 0


[buildozer]

log_level = 2
warn_on_root = 1


[app:android]

android.api = 35
android.minapi = 23
android.ndk = 27c
android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.accept_sdk_license = True
