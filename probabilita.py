# -*- coding: utf-8 -*-
"""
Probabilità di indovinare k numeri su 10 giocati con estrazione su 90 numeri.
Nel 10eLotto si estraggono 20 numeri da 90; per una colonna da 10 numeri
si contano quanti dei 10 sono tra i 20 estratti.
Modello: ipergeometrica C(10,k)*C(80,20-k)/C(90,20) per k numeri indovinati sui 10 giocati.
"""

from math import comb


def probabilità_k_su_10(k: int) -> float:
    """
    Probabilità di indovinare esattamente k numeri su 10 giocati
    quando vengono estratti 20 numeri da 90 (10eLotto).
    """
    if k < 0 or k > 10:
        return 0.0
    # C(10,k) * C(80, 20-k) / C(90, 20)
    return (comb(10, k) * comb(80, 20 - k)) / comb(90, 20)


def probabilità_almeno_k_su_10(k: int) -> float:
    """Probabilità di indovinare almeno k numeri su 10."""
    return sum(probabilità_k_su_10(i) for i in range(k, 11))


def tutte_le_probabilità() -> dict[int, float]:
    """Restituisce un dizionario k -> probabilità per k = 0..10."""
    return {k: probabilità_k_su_10(k) for k in range(11)}
