[app]

# ---------------------------------
# Основные параметры приложения
# ---------------------------------

# Название (отображаемое в лаунчере)
title = Клевер_4

# Уникальное имя пакета (без пробелов)
package.name = clever_4

# Уникальный домен (обычно в обратном порядке)
package.domain = com.clever_4

# Основная точка входа вашего приложения
source.main = main.py

# Директория с исходниками (обычно корневая папка проекта)
source.dir = .

# Расширения файлов, которые нужно включать в сборку
# (чтобы рядом с .py попадали .png, .jpg, .ttf и т.д.)
source.include_exts = py,png,jpg,ttf,mp3,mp4,db,sqlite3,json,txt

# Паттерны (шаблоны) для включения файлов в APK
source.include_patterns = data/*, files/*, user_progress.db, *.py, *.kv

# Картинка-иконка приложения и presplash
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/splash.png

# Короткое текстовое описание
description = Приложение для развитие когнитивных функций

# Версия приложения (формат X.Y.Z)
version = 1.0.0

# Автор(ы)
author = Vladislav Lerdon Team

# ---------------------------------
# Python / Kivy / зависимости
# ---------------------------------

# Основные зависимости, которые будут установлены внутри APK.
# Указываем без пробелов, разделяя запятой:
requirements = python3==3.11.0, kivy==2.2.1, kivymd==1.2.0, pyjnius, cython, ffpyplayer, ffmpeg, sdl2, sdl2_image, sdl2_mixer, sdl2_ttf

# Ядро Python-for-Android:
p4a.python_version = 3.11.0

# ---------------------------------
# Параметры Android
# ---------------------------------

# Версии SDK/NDK/API (Android)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# Сборка через конкретный SDK и Build Tools (опционально, Buildozer сам его подтянет)
android.sdk = 33
android.build_tools = 33.0.0

# Архитектуры, которые должна поддерживать сборка.
# Если не указать какую-либо, библиотеки туда не попадут.
android.archs = arm64-v8a, armeabi-v7a

# Если нужно собирать «bundle» (AAB) вместо «apk», переключите в True
android.bundle = False

# Полностью прозрачное приложение (полноэкранное)
fullscreen = 1

# Перечисляем разрешения, которые запрашиваем у пользователя
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Уровень логов (0–verbosity: debug, 1: info, 2: warning, 3: error)
log_level = 0

# ---------------------------------
# Release-подпись
# ---------------------------------

# Включаем режим «release»
android.release = True

# Если вы хотите явно задать, что артефакт — только .apk (не AAB), указываем:
android.release_artifact = apk

# ---------------------------------
# Прочие параметры сборки
# ---------------------------------

# Если собрать «не очищая» предыдущие артефакты, ускоряется отладка
buildozer.build_logfile = buildozer.log

# Пакетировать дополнительные ресурсы (например, папки внутри assets)
android.add_assets = files

# Ориентация экрана (portrait или landscape)
orientation = portrait
