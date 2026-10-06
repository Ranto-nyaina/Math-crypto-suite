[app]
title = Math and Crypto Suite
package.name = mathcryptosuite
package.domain = org.edu

source.dir = .
source.include_extensions = py,kv,png,jpg,jpeg,json

version = 1.0.0

requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.0,kivymd==1.1.1,pillow

orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/assets/icon.jpeg         
presplash.filename = %(source.dir)s/assets/icon.jpeg     

android.permissions = 
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.archs = arm64-v8a

p4a.branch = master
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1