from __future__ import annotations

from datetime import date
from typing import Optional
from task import Task
from repository import IToDoRepository


class ToDoController:
    """
      Kontrolni razred, ki povezuje uporabniški vmesnik z jedrom aplikacije (ToDoApp).
      """
    def __init__(self,app:IToDoRepository)->None:
        """
        Inicializacija kontrolerja z izbrano aplikacijo (JSON ali SQL).
        """
        self.app = app

    def  dodaj_opravilo(self,
                        opis:str,
                        status:bool=False,
                        datum:Optional[date]=None,
                        prioriteta:int=3)->Task:
        """
        Doda novo opravilo v aplikacijo.
        """
        opis = opis.strip()
        return  self.app.dodaj_opravilo(opis,status,datum,prioriteta)

    def pridobi_opravila(self) ->list[Task]:
        """
               Vrne seznam vseh opravil.
               """
        return self.app.pridobi_vsa_opravila()

    def izbrisi_opravilo(self,stevilka:int)->None:
        """
        Izbriše opravilo glede na ID.
        """
        return self.app.izbrisi_opravilo(stevilka)

    def oznaci_opravilo_kot_dokoncano(self,stevilka:int)->None:
        """
        Označi izbrano opravilo kot dokončano.
        """
        self.app.oznaci_kot_dokoncano(stevilka)

    def razvrsti_po_prioriteti(self) ->list[Task]:
        """
        Vrne opravila razvrščena po prioriteti.
        """
        return self.app.razvrsti_po_prioriteti()

    def razvrsti_po_datumu(self) ->list[Task]:
        """
        Vrne opravila razvrščena po datumu roka.
        """
        return self.app.razvrsti_po_datumu()

    def iskanje_po_opisu(self,kljucna_beseda:str)->list[Task]:
        """
        Poišče opravila, ki vsebujejo iskano ključno besedo v opisu.
        """
        return self.app.iskanje_po_opisu(kljucna_beseda)

    def statistika(self)->dict[str,int]:
        """
        Vrne statistiko opravil (npr. število opravljenih/neopravljenih).
        """
        return self.app.statistika()

    def filtriraj_opravljena(self)->list[Task]:
        """
        Vrne seznam opravljenih opravil.
        """
        return self.app.filtriraj_opravljena()

    def filtriraj_neopravljena(self)->list[Task]:
        """
        Vrne seznam neopravljenih opravil.
        """
        return self.app.filtriraj_neopravljena()

    def filtriraj_zakasnjena(self)->list[Task]:
        """
        Vrne seznam zakasnjenih opravil (rok < danes).
        """
        return self.app.filtriraj_zakasnjena()

    def save_to_file(self, pot:str= "opravila.json")->None:
        """
        Shrani opravila v datoteko (JSON).
        """
        self.app.save_to_file(pot)

    def load_from_file(self,pot:str)->None:
        """
        Naloži opravila iz datoteke (JSON).
        """
        self.app.load_from_file(pot)

    def uredi_opravilo(self,
                       stevilka:int,
                       nopis:Optional[str]=None,
                       ndatum:Optional[date]=None,
                       nprioriteta:Optional[int]=None)->Task:
        """
        Uredi obstoječe opravilo.
        """
        return self.app.uredi_opravilo(stevilka,nopis,ndatum,nprioriteta)