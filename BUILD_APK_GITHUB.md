# Creare l’APK Android con GitHub Actions (senza WSL)

La build viene eseguita sui server di GitHub. Non serve configurare WSL, Python o Buildozer sul tuo PC.

---

## 1. Crea un repository su GitHub

1. Vai su [github.com](https://github.com) e accedi.
2. Clicca **“New repository”**.
3. Nome (es. `12numeri-su-10`), **Public**, non aggiungere README/license.
4. Clicca **“Create repository”**.

---

## 2. Carica il progetto con Git

Nella cartella del progetto (in PowerShell o Prompt dei comandi):

```powershell
cd "C:\Users\mauro\Desktop\mauro\12numeri su 10"
git init
git add .
git commit -m "App 12 numeri su 10 - Android"
git branch -M main
git remote add origin https://github.com/TUO-USERNAME/12numeri-su-10.git
git push -u origin main
```

Sostituisci **TUO-USERNAME** con il tuo nome utente GitHub e **12numeri-su-10** con il nome del repo se è diverso.

Se non hai Git su Windows: [git-scm.com/download/win](https://git-scm.com/download/win).  
Se GitHub chiede autenticazione: usa un **Personal Access Token** al posto della password (Settings → Developer settings → Personal access tokens).

---

## 3. Avvia la build su GitHub

1. Apri il repository su GitHub.
2. Vai alla tab **“Actions”**.
3. A sinistra clicca **“Build Android APK”**.
4. A destra clicca **“Run workflow”** → **“Run workflow”**.
5. Attendi che il job diventi verde (anche 30–60 minuti la prima volta: scarica SDK/NDK Android).

---

## 4. Scarica l’APK

1. Quando la build è finita, clicca sul run completato (es. “Build Android APK” con segno verde).
2. In fondo alla pagina, nella sezione **“Artifacts”**, clicca **“android-apk”**.
3. Si scaricherà uno zip con l’APK (es. `numeri10elotto-1.0-arm64-v8a_debug.apk`).
4. Estrai lo zip e installa l’APK sul telefono (consenti “Origini sconosciute” se richiesto).

---

## Riepilogo

| Passo | Dove | Cosa fare |
|-------|------|-----------|
| 1 | GitHub | Crea un nuovo repository (es. `12numeri-su-10`). |
| 2 | PC (PowerShell) | `git init`, `git add .`, `git commit`, `git remote add origin ...`, `git push`. |
| 3 | GitHub → Actions | Tab **Actions** → **Build Android APK** → **Run workflow**. |
| 4 | GitHub → Artifacts | Dopo la build, scarica **android-apk** e usa l’APK nello zip. |

Se modifichi il progetto, fai di nuovo `git add .`, `git commit -m "..."`, `git push` e, se vuoi rifare l’APK, rilanci **Run workflow** in Actions.
