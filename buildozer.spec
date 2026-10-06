[app]
title = Math and Crypto Suite
package.name = mathcryptosuite
package.domain = org.edu

source.dir = .
source.include_extensions = py,kv,png,jpg,jpeg,json

version = 1.0.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow

orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/assets/icon.jpeg
presplash.filename = %(source.dir)s/assets/icon.jpeg

android.permissions =
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1