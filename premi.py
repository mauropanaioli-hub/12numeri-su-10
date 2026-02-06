# -*- coding: utf-8 -*-
"""
Tabella premi 10eLotto / Numero Oro / Doppio Oro / Extra.
Premi in euro per numero di numeri vincenti (0-10).
"""

PREMI = {
    "10eLotto": {
        10: 1_000_000,
        9: 20_000,
        8: 1_000,
        7: 150,
        6: 15,
        5: 5,
        4: 0,
        3: 0,
        2: 0,
        1: 0,
        0: 2,
    },
    "Numero Oro": {
        10: 2_500_000,
        9: 50_000,
        8: 2_500,
        7: 250,
        6: 25,
        5: 20,
        4: 5,
        3: 3,
        2: 3,
        1: 10,
        0: 0,
    },
    "Doppio Oro": {
        10: 5_000_000,
        9: 100_000,
        8: 5_000,
        7: 500,
        6: 70,
        5: 30,
        4: 20,
        3: 15,
        2: 10,
        1: 0,
        0: 0,
    },
    "Extra": {
        10: 2_000_000,
        9: 40_000,
        8: 2_000,
        7: 250,
        6: 35,
        5: 20,
        4: 6,
        3: 0,
        2: 0,
        1: 0,
        0: 1,
    },
}


def premio(tipo_gioco: str, numeri_vincenti: int) -> float:
    """Restituisce il premio in euro per il tipo di gioco e i numeri indovinati."""
    if tipo_gioco not in PREMI or numeri_vincenti not in range(11):
        return 0.0
    return float(PREMI[tipo_gioco].get(numeri_vincenti, 0))
