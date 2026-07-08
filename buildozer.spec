[app]

# نام اپلیکیشن که روی گوشی نمایش داده می‌شود
title = RIS Simulator

# نام پکیج (باید یکتا و بدون فاصله باشد)
package.name = rissimulator
package.domain = org.example

# مسیر سورس (پوشه‌ای که main.py در آن است)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

# وابستگی‌ها؛ کیوی از طریق pip روی دستگاه بیلد نصب می‌شود
requirements = python3,kivy

# جهت صفحه: portrait, landscape یا all
orientation = portrait

# آیکون و اسپلش (اختیاری - اگر فایل دارید اینجا مسیرش را بگذارید)
#icon.filename = %(source.dir)s/icon.png
#presplash.filename = %(source.dir)s/presplash.png

fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1

[app:android]

# حداقل و هدف API اندروید
android.minapi = 21
android.api = 33
android.ndk = 25b

# پذیرش خودکار مجوزهای Android SDK (بدون این، بیلد خودکار متوقف می‌شود)
android.accept_sdk_license = True

# دسترسی‌های لازم (این اپ به دوربین/اینترنت نیازی ندارد)
android.permissions =

# معماری‌های خروجی (armeabi-v7a برای اکثر گوشی‌ها، arm64-v8a برای گوشی‌های جدید)
android.archs = arm64-v8a, armeabi-v7a
