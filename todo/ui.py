from __future__ import annotations

from napake import TaskJeZeOpravljen,TaskNiMogoceNajti,NapakaPriShranjevanjuDatoteke
from todo.controller import ToDoController
from typing import Optional
from task import Task
from ui_logic import pripravi_opravilo,pripravi_spremembe,validacija_id,validacija_iskane_besede,potrdi_vnos,pripravi_pot


def izberi_opravilo(controller:ToDoController) -> Optional[int]:
    """
    Prikaže seznam opravil in vrne ID izbranega opravila.
    Če uporabnik vnese napačno vrednost, vrne None.
    """
    opravila = controller.pridobi_opravila()
    if not opravila:
        print("Seznam opravil je prazen.")
        return None

    # prikažemo vsa opravila s številčenjem
    for o in opravila:
        print(f"{o.id}. {o}")

    # uporabnik vnese številko opravila
    vnos = input("Vnesi ID opravila, ki ga želiš izbrati: ").strip()
    try:
        return validacija_id(opravila,vnos)
    except ValueError as e:
        print(e)
        return None

def prikazi_seznam(seznam: list[Task], prazno_sporocilo:str) ->None:
    """
    Prikaže seznam opravil s njihovimi ID ali sporočilo, če je seznam prazen.
    """
    if not seznam:
        print(prazno_sporocilo)
        return
    for opravilo in seznam:
        print(f"{opravilo.id}. {opravilo}")


def main_dodaj_opravilo(controller:ToDoController)->None:
    """Doda novo opravilo."""
    opis = input("Vpiši opis opravila: ")
    datum = input("Vpiši rok (YYYY-MM-DD) ali pusti prazno: ")
    prioriteta = input("Prioriteta 1-5 (pusti prazno za 3): ")
    try:
        opis,datum,prioriteta = pripravi_opravilo(opis,datum,prioriteta)
    except ValueError as e:
        print(e)
        return
    opravilo = controller.dodaj_opravilo(opis,False,datum,prioriteta)
    print(f"Opravilo dodano: {opravilo}")

def main_prikazi_opravilo(controller:ToDoController)->None:
    """Prikaže vsa opravila v seznamu."""
    opravila = controller.pridobi_opravila()
    prikazi_seznam(opravila,"Seznam opravil je prazen.")

def main_izbrisi_opravilo(controller:ToDoController)->None:
    """Izbriše izbrano opravilo iz seznama po ID-ju."""
    id = izberi_opravilo(controller)
    if id is None:
        return
    opravilo = next((o for o in controller.pridobi_opravila() if o.id == id),None)
    if opravilo is None:
        print("Neveljaven ID opravila.")
        return
    print(f"Izbrano opravilo: {opravilo}")
    potrdi = input("Si prepričan, a želiš izbrisati? (d/n): ")
    if potrdi_vnos(potrdi):
        try:
            controller.izbrisi_opravilo(id)
            print("Opravilo izbrisano.")
        except TaskNiMogoceNajti as e:
            print(e)
    else:
        print("Brisanje preklicano.")

def main_oznaci_opravilo_kot_koncano(controller:ToDoController)->None:
    """Označi izbrano opravilo kot dokončano."""
    id = izberi_opravilo(controller)
    if id is None:
        return
    opravilo = next((o for o in controller.pridobi_opravila() if o.id==id),None)
    if opravilo is None:
        print("Neveljaven ID opravila.")
        return
    print(f"Izbrano opravilo: {opravilo}")
    potrdi = input("Si prepričan, da želiš označiti kot dokončano? (d/n): ")
    if potrdi_vnos(potrdi):
        try:
            controller.oznaci_opravilo_kot_dokoncano(id)
            print("Opravilo označeno kot dokončano.")
        except (TaskNiMogoceNajti,TaskJeZeOpravljen) as e:
            print(e)
    else:
        print("Označevanje preklicano.")


def main_razvrscanje_po_prioriteti(controller:ToDoController)->None:
    """Prikaže opravila razvrščena po prioriteti (1 = najvišja)."""
    opravila = controller.razvrsti_po_prioriteti()
    prikazi_seznam(opravila, "Seznam opravil je prazen.")

def main_razvrscanje_po_datumu(controller:ToDoController)->None:
    """Prikaže opravila razvrščena po datumu (najprej najbližji rok)."""
    opravila = controller.razvrsti_po_datumu()
    prikazi_seznam(opravila, "Seznam opravil je prazen.")

def main_iskanje_po_podnizu(controller:ToDoController)->None:
    """Poišče opravila glede na del opisa (neobčutljivo na velikost črk)."""
    kljucna_beseda = input("Vnesi besedo, ki jo naj opravila vsebujejo: ")
    kljucna_beseda = validacija_iskane_besede(kljucna_beseda)
    opravila = controller.iskanje_po_opisu(kljucna_beseda)
    prikazi_seznam(opravila,"Seznam opravil je prazen.")

def main_statistika(controller:ToDoController)->None:
    """Prikaže statistiko: vsa, opravljena, nedokončana, zamujena."""
    s = controller.statistika()
    print(
        f"Vseh: {s['st vseh']}\n"
        f"Opravljenih: {s['st opravljenih']}\n"
        f"Nedokončanih: {s['st nedokoncanih']}\n"
        f"Zamujenih: {s['st zamujenih']}"
    )


def main_opravljena(controller:ToDoController)->None:
    """Prikaže samo opravljena opravila."""
    opravljena = controller.filtriraj_opravljena()
    prikazi_seznam(opravljena, "Seznam opravil je prazen.")

def main_neopravljena(controller:ToDoController)->None:
    """Prikaže samo neopravljena opravila."""
    neopravljena = controller.filtriraj_neopravljena()
    prikazi_seznam(neopravljena, "Seznam opravil je prazen.")

def main_zakasnjena(controller:ToDoController)->None:
    """Prikaže zamujena opravila (rok pretekel, status še False)."""
    zakasnjena = controller.filtriraj_zakasnjena()
    prikazi_seznam(zakasnjena, "Seznam opravil je prazen.")

def main_izhod(controller:ToDoController)->None:
    """Konča program."""
    print("Izhod iz aplikacije.")

def main_shrani(controller:ToDoController)->None:
    """Shrani seznam opravil v JSON datoteko (privzeto opravila.json).
    Ni podprto pri SQL repozitoriju."""
    pot = pripravi_pot(input("Ime datoteke (npr. opravila.json): "))
    try:
        controller.save_to_file(pot)
        print(f"Shranjeno v {pot}.")
    except NapakaPriShranjevanjuDatoteke as e:
        print(e)

def main_nalozi(controller:ToDoController)->None:
    """Naloži seznam opravil iz JSON datoteke (privzeto opravila.json).
    Ni podprto pri SQL repozitoriju."""

    pot = pripravi_pot(input("Ime datoteke (npr. opravila.json): "))
    controller.load_from_file(pot)
    seznam = controller.pridobi_opravila()
    if not seznam:
        print("Datoteka ne obstaja ali pa je seznam prazen.")
    else:
        print(f"Naloženo iz {pot}.")

def main_uredi_opravilo(controller:ToDoController)->None:
    """Uredi obstoječe opravilo (opis, datum, prioriteta)."""
    id = izberi_opravilo(controller)
    if id is None:
        return
    opravilo =next((o for o in controller.pridobi_opravila() if o.id==id),None)
    if opravilo is None:
        print("Neveljaven ID opravila.")
        return
    print(f"Želim spremeniti naslednje opravilo: {opravilo}")
    nopis = input("Dodaj novi opis opravila in stisni enter če želiš"
                  "obdržati opis opravila: ").strip() or None
    ndatum = input("Dodaj novi datum opravila in stisni enter če želiš"
                   "obdržati datum opravila")
    nprioriteta = input("Dodaj novo prioriteto opravila in stisni enter če želiš"
                   "obdržati prioriteto opravila")
    try:
        nopis,ndatum,nprioriteta = pripravi_spremembe(nopis,ndatum,nprioriteta)
    except ValueError as e:
        print(e)
        return
    opravilo =controller.uredi_opravilo(id,nopis,ndatum,nprioriteta)
    print(f"Opravilo posodobljeno: {opravilo}")



