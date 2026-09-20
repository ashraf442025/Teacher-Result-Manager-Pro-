[app]

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

android.api = 35
android.minapi = 24
android.ndk = 28c

android.archs = arm64-v8a

android.permissions = INTERNET

android.enable_androidx = True
android.allow_backup = True

android.debug_artifact = apk
android.release_artifact = aab

p4a.bootstrap = sdl2
