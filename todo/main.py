from todo.controller import ToDoController
import ui
from collections.abc import Callable
from typing import Any
from todo.app_factory import AppFactory

"""
main.py je zagonska točka aplikacije ToDo.
Definira meni in preslika uporabniške izbire v funkcije iz modula ui.py.
"""

ACTION: dict[int, tuple[Callable[[ToDoController], Any], str]]= {
    1: (ui.main_dodaj_opravilo, "Dodaj opravilo"),
    2: (ui.main_prikazi_opravilo, "Prikaži opravila"),
    3: (ui.main_izbrisi_opravilo, "Izbriši opravilo"),
    4: (ui.main_oznaci_opravilo_kot_koncano, "Označi opravilo kot dokončano"),
    5: (ui.main_razvrscanje_po_prioriteti, "Razvrščanje po prioriteti"),
    6: (ui.main_razvrscanje_po_datumu, "Razvrščanje po datumu"),
    7: (ui.main_iskanje_po_podnizu, "Iskanje po opisu podnizu"),
    8: (ui.main_statistika, "Statistika"),
    9: (ui.main_izhod, "Izhod"),
    10: (ui.main_shrani, "Shrani"),
    11: (ui.main_nalozi, "Naloži"),
    12: (ui.main_opravljena, "Prikaži samo opravljena opravila"),
    13: (ui.main_neopravljena, "Prikaži samo neopravljena opravila"),
    14: (ui.main_zakasnjena, "Prikaži samo zakasnjena opravila"),
    15: (ui.main_uredi_opravilo, "Uredi izbrano opravilo")
}

def preberi_stevilo(spodnja:int, zgornja:int, sporocilo:str) -> int:
    while True:
        try:
            vnos = int(input(sporocilo).strip())
            if spodnja <= vnos <= zgornja:
                return vnos
            print(f"Napaka: vnesi število med {spodnja} in {zgornja}.")
        except ValueError:
            print("Napaka: vnesi celo število.")

def main() ->None:
    """
     Zažene glavni meni aplikacije ToDo in obdeluje uporabniške izbire.
     """
    print("Izberi način shranjevanja podatkov:")
    print("1. JSON/datoteka")
    print("2. SQLite baza")

    app = None
    while app is None:
        try:
            izbira = int(input("Vnos (1/2): ").strip())
            if izbira == 2:
                app = AppFactory.ustvari_app("sql", "todo.db")
            elif izbira == 1:
                app = AppFactory.ustvari_app("json")
            else:
                print("Napaka: vnesi 1 ali 2")
        except ValueError:
            print("Napaka: vnos mora biti številka 1 ali 2.")

    controller = ToDoController(app)

    while True:
        print("\n--- TO-DO MENI ---")
        for i,(funkcija,opis) in ACTION.items():
            print(f"{i}. {opis}")

        izbira = preberi_stevilo(1, 15, "Izberi možnost (1-15): ")
        action = ACTION.get(izbira)
        if action:
            funkcija, opis = action
            print(f"\n>>> {opis}")
            funkcija(controller)
            if izbira == 9:
                print("\nProgram zaključen. Hvala za uporabo!")
                break
        else:
            print("Napačna izbira, poskusi znova.")

if __name__ == "__main__":
    main()