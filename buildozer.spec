# Receita do APK Android (Buildozer + python-for-android).
# Quem roda isto é o GitHub Actions (.github/workflows/apk.yml): não precisa instalar nada no PC.

[app]
title = Vale do Girassol
package.name = valedogirassol
package.domain = br.isabellaradael

source.dir = .
source.include_exts = py
source.exclude_dirs = build, web, android, bin, .buildozer, .github, .claude, __pycache__
source.exclude_patterns = save_fazenda.json

# o GitHub Actions troca para 1.0.<número do build> antes de gerar
version = 1.0

# a receita de pygame do python-for-android é a 2.1.0, que funciona com Python 3.10
requirements = python3==3.10.12,hostpython3==3.10.12,pygame

# o jogo é jogado deitado
orientation = landscape
fullscreen = 1

icon.filename = %(source.dir)s/web/icone.png
presplash.filename = %(source.dir)s/web/abertura.png
android.presplash_color = #3f2832

android.archs = arm64-v8a, armeabi-v7a
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.allow_backup = True
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
