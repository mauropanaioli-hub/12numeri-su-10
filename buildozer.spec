[app]

# Nome applicazione
title = 12 numeri su 10

# Pacchetto (nome univoco, no spazi)
package.name = numeri10elotto

# Dominio per il pacchetto
package.domain = org.numeri10

# Script di avvio (senza .py)
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0

# Requisiti Python
requirements = python3,kivy

# Orientamento (portrait per smartphone)
orientation = portrait

# Permessi Android (nessuno particolare richiesto)
android.permissions = 

# Entry point: script che avvia l'app
android.entrypoint = main_android

# API minime Android
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31

# Architetture (arm64 per la maggior parte dei dispositivi)
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# Livello di log
log_level = 2

# Directory di build
warn_on_root = 1
