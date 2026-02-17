[app]
title = Calculadora Matemática Pro
package.name = calculadoramath
package.domain = org.calculadoramath
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 0.1
requirements = python3,kivy==2.1.0
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
api = 30
minapi = 21
ndk = 23b
sdk = 30
build_tools = 30.0.3
android.accept_sdk_license = True
android.gradle_dependencies = 
android.permissions = INTERNET
android.private_storage = True
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r23b
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk

[requirements]
# No dependencies here, they're in the requirements section above
