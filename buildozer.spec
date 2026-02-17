[app]
title = Calculadora Matemática Pro
package.name = calculadoramath
package.domain = org.calculadoramath
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.3.0
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
api = 31
minapi = 21
ndk = 25b
sdk = 30
android.accept_sdk_license = True
android.gradle_dependencies = 
android.permissions = INTERNET
android.private_storage = True
android.add_assets =
android.add_res =
android.add_jar =
android.add_src =
