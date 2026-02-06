# Opzione B – Build APK per Android

Per ottenere l’APK installabile sullo smartphone serve **WSL (Ubuntu)** su Windows o un PC **Linux**. Segui questi passaggi.

---

## 1. Aprire WSL (Windows)

1. Apri **PowerShell** o **Prompt dei comandi**.
2. Digita:
   ```bash
   wsl
   ```
   Se WSL non è installato, installa Ubuntu da Microsoft Store oppure:
   ```powershell
   wsl --install -d Ubuntu
   ```
   Poi riavvia e apri di nuovo `wsl`.

---

## 2. Andare nella cartella del progetto

La cartella del progetto in Windows è:
`C:\Users\mauro\Desktop\mauro\12numeri su 10`

In WSL diventa (percorso tipico):
```bash
cd "/mnt/c/Users/mauro/Desktop/mauro/12numeri su 10"
```
(usa le virgolette per lo spazio nel nome.)

Verifica di essere nella cartella giusta:
```bash
ls -la main_android.py buildozer.spec
```

---

## 3. Installare dipendenze (solo la prima volta)

In WSL esegui **nell’ordine**:

**3.1 Python 3 e pip** (se `pip3` non è installato e dà "not found"):
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

**3.2 Dipendenze per Buildozer e Android:**
```bash
sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

**3.3 Buildozer:**
```bash
pip3 install buildozer
```
Se ancora `pip3: not found`, prova:
```bash
python3 -m pip install buildozer
```

---

## 4. Lanciare la build dell’APK

Sempre nella stessa cartella in WSL:

```bash
./build_android.sh
```

Oppure direttamente:
```bash
buildozer android debug
```

- **Prima esecuzione**: Buildozer scarica SDK e NDK Android; può richiedere **20–40 minuti** e diversi GB di spazio.
- **Esecuzioni successive**: molto più veloci (solo ricompilazione).

---

## 5. Dove trovare l’APK

A build finita, l’APK è nella cartella `bin/`, ad esempio:

- `bin/numeri10elotto-1.0-arm64-v8a_debug.apk` (per la maggior parte degli smartphone recenti)
- `bin/numeri10elotto-1.0-armeabi-v7a_debug.apk` (per dispositivi più vecchi)

In Windows la stessa cartella è:
`C:\Users\mauro\Desktop\mauro\12numeri su 10\bin\`

---

## 6. Installare l’APK sullo smartphone

1. Copia il file `.apk` sul telefono (cavo USB, cloud, email, ecc.).
2. Sul telefono apri il file e avvia l’installazione.
3. Se richiesto, abilita **“Origini sconosciute”** (o “Installa app sconosciute”) per il browser o il file manager che stai usando.
4. Completa l’installazione e apri l’app **“12 numeri su 10”**.

---

## Risoluzione problemi

- **`execvpe(bash) failed: No such file or directory`** (quando usi `wsl -e bash -c "..."`)  
  Non usare `-e bash`. Prova da PowerShell nella cartella del progetto:
  ```powershell
  .\build_android.ps1
  ```
  Oppure apri WSL **senza** passare comandi: digita solo `wsl` e premi Invio. Poi nella shell WSL:
  ```bash
  cd "/mnt/c/Users/mauro/Desktop/mauro/12numeri su 10"
  buildozer android debug
  ```

- **`buildozer: command not found`**  
  Usa `pip3 install buildozer` e riprova, oppure: `python3 -m buildozer android debug`

- **Errori di permessi su `build_android.sh`**  
  ```bash
  chmod +x build_android.sh
  ./build_android.sh
  ```

- **Spazio insufficiente**  
  La prima build richiede diversi GB. Libera spazio su disco o usa un’unità con più spazio.

- **Errori Java/NDK**  
  Assicurati di aver installato `openjdk-17-jdk` e tutte le dipendenze del punto 3.
