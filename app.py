# -*- coding: utf-8 -*-
"""
Applicazione GUI: sistema ortogonale 12 numeri, 6 colonne da 10.
Progressione, saldo, estrazioni, tabella premi e probabilità.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import List, Optional

from premi import PREMI, premio
from probabilita import tutte_le_probabilità, probabilità_almeno_k_su_10
from logica import (
    colonne_ortogonali_default,
    numeri_colonna,
    vincita_sistema,
    aggiorna_indice_progressione,
    spesa_colpo,
)


class App10eLotto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema ortogonale 12 numeri su 10 - 10eLotto")
        self.geometry("1000x780")
        self.minsize(800, 600)

        self.numeri_12: List[int] = []
        self.estrazioni: List[List[int]] = []
        self.saldo = 0.0
        self.progressione: List[float] = [1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0]
        self.indice_progressione = 0
        self.tipo_gioco = tk.StringVar(value="10eLotto")
        self.colonne = colonne_ortogonali_default()

        self._crea_ui()

    def _crea_ui(self):
        # ----- Numeri giocati (12 numeri) -----
        f_numeri = ttk.LabelFrame(self, text="I tuoi 12 numeri (1-90)", padding=8)
        f_numeri.pack(fill=tk.X, padx=8, pady=4)
        self.entry_numeri = ttk.Entry(f_numeri, width=60)
        self.entry_numeri.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.entry_numeri.insert(0, "1 5 12 23 34 45 56 67 72 78 82 90")
        ttk.Button(f_numeri, text="Applica", command=self._applica_numeri).pack(side=tk.LEFT)

        # ----- Colonne (solo visualizzazione) -----
        f_col = ttk.LabelFrame(self, text="6 colonne da 10 numeri (sistema ortogonale)", padding=8)
        f_col.pack(fill=tk.X, padx=8, pady=4)
        self.label_colonne = ttk.Label(
            f_col,
            text="Inserisci i 12 numeri e clicca Applica per vedere le colonne.",
            wraplength=900,
        )
        self.label_colonne.pack(anchor=tk.W)

        # ----- Tipo gioco -----
        f_tipo = ttk.Frame(self)
        f_tipo.pack(fill=tk.X, padx=8, pady=4)
        ttk.Label(f_tipo, text="Tipo di gioco:").pack(side=tk.LEFT, padx=(0, 8))
        for nome in ["10eLotto", "Numero Oro", "Doppio Oro", "Extra"]:
            ttk.Radiobutton(f_tipo, text=nome, variable=self.tipo_gioco, value=nome).pack(
                side=tk.LEFT, padx=4
            )

        # ----- Progressione -----
        f_prog = ttk.LabelFrame(self, text="Progressione puntate (importo per colonna)", padding=8)
        f_prog.pack(fill=tk.X, padx=8, pady=4)
        self.entry_progressione = ttk.Entry(f_prog, width=70)
        self.entry_progressione.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.entry_progressione.insert(
            0, " ".join(str(x) for x in [1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0])
        )
        ttk.Button(f_prog, text="Applica progressione", command=self._applica_progressione).pack(
            side=tk.LEFT
        )
        self.label_step = ttk.Label(f_prog, text="Step attuale: 0 | Puntata per colonna: 1.00 €")
        self.label_step.pack(anchor=tk.W, pady=(6, 0))

        # ----- Estrazione -----
        f_est = ttk.LabelFrame(self, text="Numeri estratti (20 numeri, separati da spazio)", padding=8)
        f_est.pack(fill=tk.X, padx=8, pady=4)
        self.entry_estrazione = ttk.Entry(f_est, width=70)
        self.entry_estrazione.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ttk.Button(f_est, text="Registra estrazione e aggiorna saldo", command=self._registra_estrazione).pack(
            side=tk.LEFT
        )

        # ----- Saldo -----
        f_saldo = ttk.LabelFrame(self, text="Saldo (vincita - spesa)", padding=8)
        f_saldo.pack(fill=tk.X, padx=8, pady=4)
        row = ttk.Frame(f_saldo)
        row.pack(fill=tk.X)
        self.label_saldo = ttk.Label(row, text="Saldo: 0.00 €", font=("", 12, "bold"))
        self.label_saldo.pack(side=tk.LEFT)
        ttk.Label(row, text="  Saldo iniziale:").pack(side=tk.LEFT, padx=(20, 4))
        self.entry_saldo_iniziale = ttk.Entry(row, width=10)
        self.entry_saldo_iniziale.insert(0, "0")
        self.entry_saldo_iniziale.pack(side=tk.LEFT, padx=2)
        ttk.Button(row, text="Imposta", command=self._imposta_saldo_iniziale).pack(side=tk.LEFT, padx=4)

        # ----- Tabella premi + Probabilità -----
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Tab Premi
        f_premi = ttk.Frame(notebook, padding=8)
        notebook.add(f_premi, text="Tabella premi")
        self._crea_tabella_premi(f_premi)

        # Tab Probabilità
        f_prob = ttk.Frame(notebook, padding=8)
        notebook.add(f_prob, text="Probabilità di vincita")
        self._crea_tabella_probabilita(f_prob)

        self._applica_numeri()
        self._applica_progressione()

    def _imposta_saldo_iniziale(self):
        try:
            self.saldo = float(self.entry_saldo_iniziale.get().replace(",", "."))
            self.label_saldo.config(text=f"Saldo: {self.saldo:+.2f} €")
        except ValueError:
            messagebox.showwarning("Attenzione", "Inserisci un numero valido per il saldo.")

    def _crea_tabella_premi(self, parent):
        cols = ["Numeri vincenti", "10eLotto", "Numero Oro", "Doppio Oro", "Extra"]
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=12)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120)
        vsb = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        for k in range(10, -1, -1):
            tree.insert(
                "",
                tk.END,
                values=(
                    str(k),
                    self._fmt_premio(PREMI["10eLotto"].get(k, 0)),
                    self._fmt_premio(PREMI["Numero Oro"].get(k, 0)),
                    self._fmt_premio(PREMI["Doppio Oro"].get(k, 0)),
                    self._fmt_premio(PREMI["Extra"].get(k, 0)),
                ),
            )

    def _fmt_premio(self, x):
        if x == 0:
            return "-"
        if x >= 1_000_000:
            return f"€ {x/1_000_000:.1f} M"
        if x >= 1_000:
            return f"€ {x:,.0f}"
        return f"€ {x:,.0f}"

    def _crea_tabella_probabilita(self, parent):
        probs = tutte_le_probabilità()
        text = scrolledtext.ScrolledText(parent, height=14, width=70)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, "Probabilità di indovinare esattamente k numeri su 10 (estrazione 20 da 90):\n\n")
        for k in range(11):
            p = probs[k]
            pct = p * 100
            text.insert(tk.END, f"  k = {k:2}  →  P = {p:.6f}  ({pct:.4f}%)\n")
        text.insert(tk.END, "\nProbabilità di indovinare almeno k numeri:\n\n")
        for k in [6, 7, 8, 9, 10]:
            p = probabilità_almeno_k_su_10(k)
            text.insert(tk.END, f"  almeno {k}  →  P = {p:.6f}  ({p*100:.4f}%)\n")
        text.config(state=tk.DISABLED)

    def _parse_numeri(self, s: str, min_val=1, max_val=90) -> Optional[List[int]]:
        try:
            parts = s.strip().split()
            nums = []
            for p in parts:
                n = int(p)
                if n < min_val or n > max_val:
                    return None
                nums.append(n)
            return nums
        except ValueError:
            return None

    def _applica_numeri(self):
        s = self.entry_numeri.get()
        nums = self._parse_numeri(s)
        if nums is None or len(nums) != 12:
            messagebox.showwarning(
                "Attenzione",
                "Inserisci esattamente 12 numeri tra 1 e 90, separati da spazio.",
            )
            return
        self.numeri_12 = nums
        lines = []
        for i, col_indici in enumerate(self.colonne):
            numeri_col = numeri_colonna(col_indici, self.numeri_12)
            lines.append(f"Colonna {i+1}: {numeri_col}")
        self.label_colonne.config(text=" | ".join(lines))

    def _applica_progressione(self):
        s = self.entry_progressione.get()
        try:
            parts = s.strip().split()
            prog = [float(x) for x in parts if float(x) > 0]
            if not prog:
                raise ValueError("Progressione vuota")
            self.progressione = prog
            if self.indice_progressione >= len(self.progressione):
                self.indice_progressione = len(self.progressione) - 1
            self._aggiorna_label_step()
        except ValueError as e:
            messagebox.showwarning("Attenzione", "Progressione non valida. Usa numeri positivi separati da spazio.")

    def _aggiorna_label_step(self):
        if not self.progressione:
            self.label_step.config(text="Step: - | Puntata: -")
            return
        idx = min(self.indice_progressione, len(self.progressione) - 1)
        puntata = self.progressione[idx]
        tot = puntata * 6
        self.label_step.config(
            text=f"Step attuale: {idx + 1}/{len(self.progressione)} | Puntata per colonna: {puntata:.2f} € | Totale colpo: {tot:.2f} €"
        )

    def _registra_estrazione(self):
        s = self.entry_estrazione.get()
        estratti = self._parse_numeri(s, 1, 90)
        if estratti is None or len(estratti) != 20:
            messagebox.showwarning(
                "Attenzione",
                "Inserisci esattamente 20 numeri estratti (1-90), separati da spazio.",
            )
            return
        if len(self.numeri_12) != 12:
            messagebox.showwarning("Attenzione", "Prima inserisci e applica i 12 numeri.")
            return
        if not self.progressione:
            messagebox.showwarning("Attenzione", "Imposta la progressione.")
            return

        puntata = self.progressione[min(self.indice_progressione, len(self.progressione) - 1)]
        spesa = spesa_colpo(self.progressione, self.indice_progressione, 6)
        vincita = vincita_sistema(
            self.numeri_12,
            self.colonne,
            estratti,
            self.tipo_gioco.get(),
            puntata,
        )

        saldo_prima = self.saldo
        self.saldo += vincita - spesa
        self.indice_progressione = aggiorna_indice_progressione(
            self.indice_progressione,
            self.progressione,
            vincita,
            spesa,
            saldo_prima,
            riposiziona_se_vincita_minore=True,
        )
        self.estrazioni.append(estratti.copy())

        self.label_saldo.config(
            text=f"Saldo: {self.saldo:+.2f} €  (ultima vincita: {vincita:.2f} €, spesa: {spesa:.2f} €)"
        )
        self._aggiorna_label_step()
        self.entry_estrazione.delete(0, tk.END)
        messagebox.showinfo(
            "Estrazione registrata",
            f"Vincita: {vincita:.2f} €\nSpesa: {spesa:.2f} €\nSaldo: {self.saldo:+.2f} €\nNuovo step: {self.indice_progressione + 1}",
        )


def main():
    app = App10eLotto()
    app.mainloop()


if __name__ == "__main__":
    main()
