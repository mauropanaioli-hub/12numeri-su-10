# Sistema ortogonale 12 numeri su 10 - 10eLotto

Applicazione per gestire un sistema ortogonale di **12 numeri totali** e **6 colonne da 10 numeri**, con progressione di gioco e saldo vincita/perdita.

## Funzionalità

- **12 numeri**: inserisci i tuoi 12 numeri (1–90). Le 6 colonne sono generate automaticamente con uno schema ortogonale (ogni colonna contiene 10 dei 12 numeri, con 2 numeri esclusi per colonna in modo diverso).
- **Tipo di gioco**: 10eLotto, Numero Oro, Doppio Oro, Extra (tabella premi integrata).
- **Progressione**: definisci la lista di puntate (importo per colonna). L’app aggiorna lo step in base a vincita/perdita:
  - **Saldo positivo** → riparti dal primo step.
  - **Vincita ≥ spesa** → scendi di uno step.
  - **Vincita minore** (0 < vincita < spesa) → riposizionamento: scendi di uno step.
  - **Perdita** (vincita = 0) → sali di uno step (puntata successiva).
- **Estrazioni**: inserisci i 20 numeri estratti; l’app calcola vincite per colonna, aggiorna saldo e step della progressione.
- **Tabella premi** e **probabilità** (k numeri su 10, estrazione 20 da 90) in due tab nella GUI.

## Requisiti

- Python 3.8+ (libreria `tkinter` inclusa in Python).

## Avvio

```bash
python app.py
```

## Struttura file

- `app.py` – GUI principale (numeri, colonne, tipo gioco, progressione, estrazione, saldo, tab premi/probabilità).
- `logica.py` – Sistema ortogonale, conteggio indovinati, vincite, aggiornamento indice progressione.
- `premi.py` – Tabella premi per 10eLotto, Numero Oro, Doppio Oro, Extra.
- `probabilita.py` – Probabilità ipergeometriche (k su 10 con 20 estratti da 90).

## Versione Android (smartphone)

L’app è disponibile anche per **Android** (stessa logica, interfaccia ottimizzata per touch).

### Test su PC (opzionale)

Per provare l’interfaccia Android su computer (con Python e Kivy):

```bash
pip install kivy
python main_android.py
```

### Build APK per Android (Opzione B)

Per generare l’APK installabile sullo smartphone serve **Buildozer** su **WSL (Ubuntu)** o **Linux**. Istruzioni complete passo-passo:

- **Vedi [OPZIONE_B_ANDROID.md](OPZIONE_B_ANDROID.md)** per tutti i comandi (WSL, dipendenze, build, dove trovare l’APK, installazione sul telefono).

In sintesi: apri WSL, vai nella cartella del progetto, installa dipendenze e Buildozer (una tantum), poi esegui `./build_android.sh` oppure `buildozer android debug`. L’APK sarà in `bin/`.

### File Android

- `main_android.py` – App Kivy (schermata principale, tabella premi, probabilità).
- `buildozer.spec` – Configurazione per Buildozer (titolo, pacchetto, requisiti, entry point `main_android`).

I moduli `premi.py`, `logica.py` e `probabilita.py` sono condivisi con la versione desktop.

## Note

I premi sono quelli della tabella ufficiale (Premi). Le probabilità sono calcolate con il modello: 20 numeri estratti da 90, 10 numeri giocati per colonna.
