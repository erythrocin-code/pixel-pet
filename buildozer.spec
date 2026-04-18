[app]

# (str) Title of your application
title = 像素宠物

# (str) Package name
package.name = pixel_pet

# (str) Package domain (needed for android/ios packaging)
package.domain = com.tamagotchi

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.1.0

# (str) Supported orientation (one of: landscape, sensorLandscape, portrait, allPortrait, sensorPortrait, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash of the application
#presplash.filename = %(source.dir)s/assets/presplash.png

# (string) Icon of the application
#icon.filename = %(source.dir)s/assets/icon.png

# (list) Permissions
#android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
# android.api = 33

# (int) Minimum API your APK will support.
# android.minapi = 21

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) p4a source directory (if local clone)
#p4a.source_dir = 

# (list) p4a recipes to use
#p4a.recipes = 

# (str) Git URL for python-for-android (use mirror if needed)
#p4a.url = https://github.com/kivy/python-for-android

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature
# android.allow_backup = True

# (str) The format used to name the compiled binaries
# product_name = %(app.name)s

# (str) The filename of the keystore
# android.keystore_filename = ~/.android/debug.keystore

# (str) The alias of the keystore
# android.keystore_alias = androiddebugkey

# (str) The password of the keystore
# android.keystore_password = android

# (p4a) --private property, not to be used directly in buildozer.spec
# In p4a, this is the --private property.
# If not set, then the value of source.dir will be used.

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app.example] for example:
#        This will be resolved to app.example = value1, value2, value3
#
#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with line of [profile:section]
#    Only one profile can be active at a time.
#    Example:
#        [app@debug]
#        source.dir = .
#
#        [app@release]
#        source.dir = src
