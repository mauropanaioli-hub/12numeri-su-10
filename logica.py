# -*- coding: utf-8 -*-
"""
Logica sistema ortogonale: 12 numeri, 6 colonne da 10.
Progressione, saldo, vincite.
"""

from typing import List, Optional
from premi import premio


def colonne_ortogonali_default() -> List[List[int]]:
    """
    Sistema ortogonale default: 12 numeri (indici 0..11), 6 colonne da 10.
    Ogni colonna esclude 2 numeri diversi.
    """
    return [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],       # mancano 10, 11
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 10],      # mancano 9, 11
        [0, 1, 2, 3, 4, 5, 6, 7, 9, 10],      # mancano 8, 11
        [0, 1, 2, 3, 4, 5, 6, 8, 9, 10],      # mancano 7, 11
        [0, 1, 2, 3, 4, 5, 7, 8, 9, 10],      # mancano 6, 11
        [0, 1, 2, 3, 4, 6, 7, 8, 9, 10],      # mancano 5, 11
    ]


def numeri_colonna(colonna_indici: List[int], numeri_12: List[int]) -> List[int]:
    """Dati i 12 numeri e gli indici di una colonna, restituisce i 10 numeri della colonna."""
    return [numeri_12[i] for i in colonna_indici if i < len(numeri_12)]


def conta_indovinati(numeri_giocati: List[int], estratti: List[int]) -> int:
    """Conta quanti dei numeri giocati sono presenti tra gli estratti."""
    set_estratti = set(estratti)
    return sum(1 for n in numeri_giocati if n in set_estratti)


def vincita_colonna(
    numeri_col: List[int],
    estratti: List[int],
    tipo_gioco: str,
    quota: float = 1.0,
) -> float:
    """
    Vincita per una colonna: conta indovinati, applica premio e quota (puntata).
    quota = moltiplicatore sul premio (es. puntata in euro come quota).
    """
    k = conta_indovinati(numeri_col, estratti)
    p = premio(tipo_gioco, k)
    return p * quota


def vincita_sistema(
    numeri_12: List[int],
    colonne: List[List[int]],
    estratti: List[int],
    tipo_gioco: str,
    puntata_per_colonna: float,
) -> float:
    """
    Vincita totale del sistema: somma vincite di ogni colonna.
    puntata_per_colonna = importo giocato per ogni colonna (stesso per tutte).
    """
    totale = 0.0
    for col_indici in colonne:
        numeri_col = numeri_colonna(col_indici, numeri_12)
        totale += vincita_colonna(numeri_col, estratti, tipo_gioco, puntata_per_colonna)
    return totale


def aggiorna_indice_progressione(
    indice_attuale: int,
    progressione: List[float],
    vincita: float,
    spesa: float,
    saldo_prima: float,
    riposiziona_se_vincita_minore: bool = True,
) -> int:
    """
    Calcola il nuovo indice della progressione dopo un colpo.
    - Se saldo (dopo il colpo) > 0: torna a 0 (riparti).
    - Se vincita >= spesa: scendi di 1 (max 0).
    - Se vincita minore (0 < vincita < spesa): riposiziona = scendi di 1 (max 0).
    - Se perdita (vincita < spesa e nessuna vincita): sali di 1 (aumenta puntata).
    """
    saldo_dopo = saldo_prima + vincita - spesa
    n = len(progressione)
    if n == 0:
        return 0

    if saldo_dopo > 0:
        return 0

    if vincita >= spesa:
        return max(0, indice_attuale - 1)

    if riposiziona_se_vincita_minore and vincita > 0:
        return max(0, indice_attuale - 1)
    return min(n - 1, indice_attuale + 1)


def spesa_colpo(progressione: List[float], indice: int, num_colonne: int = 6) -> float:
    """Spesa del colpo = progressione[indice] * num_colonne (una puntata per colonna)."""
    if not progressione or indice >= len(progressione):
        return 0.0
    return progressione[indice] * num_colonne
