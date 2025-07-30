[app]
# Nome do seu app
title = Snake Chase

# Nome do pacote (sem espaços)
package.name = snakechase

# Domínio invertido (use algo único)
package.domain = org.zenofarms

# Versão do app
version = 1.0

# Onde está o seu código
source.dir = .

# Quais extensões incluir no build
source.include_exts = py,png,kv

# Corpo de requisitos: Python 3 e Kivy
requirements = python3,kivy

# Orientação da tela: landscape ou portrait
orientation = landscape

# Fullscreen?
fullscreen = 0

# Permissões Android que você precise
android.permissions = INTERNET

# API alvo e mínima
android.api = 31
android.minapi = 21

# Bootstrapping Kivy
# (SDL2 é padrão, mas reforçamos aqui)
p4a.bootstrap = sdl2

# ----------------------------------------------------
# Se quiser adicionar ícone do app, descomente e ajuste:
# icon.filename = assets/door.png

# [buildozer] seções abaixo normalmente não precisam mudar
[buildozer]
log_level = 2

