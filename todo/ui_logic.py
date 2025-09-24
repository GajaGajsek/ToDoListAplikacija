from datetime import date
from typing import Optional,Tuple
from task import Task


def pripravi_opravilo(opis: str, datum: str, prioriteta: str)->Tuple[str, Optional[date], int]:
    opis = opis.strip()
    if not opis:
        raise ValueError("Opis ne sme biti prazen.")
    d = None
    datum = datum.strip()
    if datum:
        try:
            d=date.fromisoformat(datum)
        except ValueError:
            raise ValueError("Datum mora biti v obliki YYYY-MM-DD.")
    if not prioriteta.strip():
        p = 3
    else:
        try:
            p = int(prioriteta.strip())
        except ValueError:
            raise ValueError("Prioriteta mora biti število.")
        if not 1<= p <= 5:
            raise ValueError("Prioriteta mora biti med 1 in 5.")
    return opis,d,p

def pripravi_spremembe(opis: str, datum: str, prioriteta: str) -> Tuple[Optional[str], Optional[date], Optional[int]]:
    """
    Validira vhodne podatke za POSODOBITEV opravila.
    None pomeni 'brez spremembe'.

    :param opis: nov opis (prazen niz pomeni brez spremembe)
    :param datum: niz v obliki YYYY-MM-DD ali prazen niz
    :param prioriteta: niz med 1 in 5 ali prazen niz (brez spremembe)
    :raises ValueError: če so podatki neveljavni
    """
    opis = opis.strip() if opis.strip() else None

    d = None
    if datum.strip():
        try:
            d = date.fromisoformat(datum.strip())
        except ValueError:
            raise ValueError("Datum mora biti v obliki YYYY-MM-DD.")

    p = None
    if prioriteta.strip():
        try:
            p = int(prioriteta)
        except ValueError:
            raise ValueError("Prioriteta mora biti število.")
        if not 1 <= p <= 5:
            raise ValueError("Prioriteta mora biti med 1 in 5.")

    return opis, d, p

def validacija_id(opravila:list[Task], vnos:str) ->int:
    """
    Preveri, ali je vnos veljaven ID izmed danih opravil.
    Vrne ID kot int ali sproži ValueError.
     """
    if not vnos.strip().isdigit():
        raise ValueError("Vnesi veljaven ID")
    id_izbranega = int(vnos)
    for o in opravila:
        if o.id == id_izbranega:
            return id_izbranega
    raise ValueError("Neveljaven ID opravila.")

def validacija_iskane_besede(kljucna_beseda:str)->str:
    """
    Očisti in validira iskalno besedo.
    Vrne ključno besedo v malih črkah ali sproži ValueError,
    če je niz prazen.
    """
    kljucna_beseda = kljucna_beseda.strip()
    if not kljucna_beseda:
        raise ValueError("Iskalna beseda ne sme biti prazna")
    return kljucna_beseda.lower()

def pripravi_pot(vnos: str, privzeta: str = "opravila.json") -> str:
    """
    Vrne očiščeno ime datoteke ali privzeto, če je vnos prazen.
    """
    vnos = vnos.strip()
    if not vnos:
        vnos = privzeta
    return vnos

def potrdi_vnos(vnos: str) -> bool:
    """
    Preveri, ali je uporabnik potrdil z 'd'.
    Vse ostalo pomeni preklic.
    """
    return vnos.strip().lower() == "d"
