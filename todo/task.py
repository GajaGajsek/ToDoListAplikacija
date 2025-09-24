from __future__ import annotations

from datetime import date
from dataclasses import dataclass
from napake import TaskJeZeOpravljen,TaskNiMogoceDodati

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    # fallback, če colorama ni nameščen
    class Dummy:
        RESET_ALL = ""
        GREEN = ""
        RED = ""
        YELLOW = ""
    Fore = Style = Dummy()
    def init(*args, **kwargs):
        pass

@dataclass
class Task:
    """
      Razred, ki predstavlja posamezno nalogo v ToDo aplikaciji.
      """
    opis:str
    status: bool = False
    datum: date | None = None
    prioriteta: int = 3
    id: int | None = None # dodano pole za ID iz baze

    def __post_init__(self)->None:
        """
        Inicializacija po konstruktorju.
        Preveri, da je prioriteta med 1 in 5.
        """
        if not self.opis or not self.opis.strip():
            raise TaskNiMogoceDodati(TaskNiMogoceDodati.PRAZEN_OPIS)
        try:
            self.prioriteta = int(self.prioriteta)
        except (ValueError, TypeError):
            raise TaskNiMogoceDodati(TaskNiMogoceDodati.NAPACNA_PRIORITETA)
        if not (1 <= self.prioriteta <= 5):
            raise TaskNiMogoceDodati(TaskNiMogoceDodati.NAPACNA_PRIORITETA)

    def __str__(self)->str:
        """
        Vrne barvno tekstovno predstavitev naloge z ikono statusa in prioriteto.
        ✔️ – zaključeno,
        🔴 – rok pretekel,
        ❌ – še ni opravljeno.
        """
        #doloci znak in barvo
        if self.status:
            znak = "✔️"
            color = Fore.GREEN
        else:
            if self.datum and self.datum < date.today():
                znak = "🔴"
                color = Fore.RED
            else:
                znak = "❌"
                color = Fore.YELLOW

        besedilo = f"{color}{znak} (P{self.prioriteta}) {self.opis}{Style.RESET_ALL}"
        return besedilo
    def oznaci_kot_dokoncano(self)->None:
        """
        Označi nalogo kot dokončano.
        Vrže izjemo TaskJeZeOpravljen, če je že zaključena.
        """
        if not self.status:
            self.status = True
        else:
            raise TaskJeZeOpravljen(TaskJeZeOpravljen.ZE_OPRAVLJEN)

    def to_dict(self) ->dict:
        """
         Pretvori objekt Task v slovar, primeren za shranjevanje v bazo ali JSON.
         """
        return {
            "id": self.id,
            "opis": self.opis,
            "status": self.status,
            "datum" : self.datum.isoformat() if self.datum is not None else None,
            "prioriteta": self.prioriteta
        }

    @staticmethod
    def from_dict(data:dict)-> "Task":
        """
        Ustvari nov objekt Task iz slovarja (npr. podatki iz baze ali JSON).

        :param data: Slovar s ključi 'id', 'opis', 'status', 'datum', 'prioriteta'.
        :return: Objekt Task.
        """
        id = data.get("id")
        opis = data.get("opis","").strip()
        status = bool(data.get("status",False))
        datum = None
        datum_str = data.get("datum")
        if datum_str:
            try:
                datum = date.fromisoformat(datum_str)
            except(ValueError,TypeError):
                datum = None
        prioriteta_vr = data.get("prioriteta",3)
        try:
            prioriteta: int = int(prioriteta_vr)
        except (ValueError,TypeError):
            raise TaskNiMogoceDodati(TaskNiMogoceDodati.NAPACNA_PRIORITETA)
        return Task(opis,status,datum,prioriteta,id)

