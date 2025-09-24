from __future__ import annotations

from datetime import date
from task import Task
import  json
import os
from typing import  Optional
from repository import IToDoRepository
from napake import TaskNiMogoceNajti,NapakaPriShranjevanjuDatoteke,TaskNiMogoceDodati,NapakaPriBranjuDatoteke


class ToDoApp(IToDoRepository):
    """Razred za upravljanje seznama opravil (dodajanje, brisanje, filtriranje, shranjevanje...)."""

    def __init__(self, seznam_opravil:Optional[list[Task]]=None) -> None:
        """Inicializira aplikacijo z opcijskim seznamom opravil."""
        self.seznam_opravil: list[Task]=seznam_opravil if seznam_opravil else []
        self.next_id = max((o.id for o in self.seznam_opravil if o.id),default=0)+1

    def pridobi_vsa_opravila(self) ->list[Task]:
        """Vrne seznam vseh opravil."""
        return self.seznam_opravil

    def dodaj_opravilo(self,
                       opis:str,
                       status:bool=False,
                       datum:Optional[date]=None ,
                       prioriteta:int=3,) ->Task:
        """
        Doda novo opravilo v seznam.
        Vrže izjemo TaskNiMogoceDodati, če je opis prazen ali če opravilo že obstaja.
        """
        task =Task(opis, status,datum,prioriteta,id=self.next_id)
        if any(o.opis.lower() == task.opis.lower() for o in self.seznam_opravil):
            raise TaskNiMogoceDodati(TaskNiMogoceDodati.DUPLIKAT)
        self.next_id +=1
        self.seznam_opravil.append(task)
        return task

    def __str__(self) -> str:
        """Vrne seznam opravil kot večvrstični niz."""
        return "\n".join(str(o) for o in self.seznam_opravil)

    def izbrisi_opravilo(self, id:int) -> None:
        """Izbriše opravilo po ID."""
        for i,o in enumerate(self.seznam_opravil):
            if id == o.id:
                del self.seznam_opravil[i]
                return
        raise TaskNiMogoceNajti(TaskNiMogoceNajti.NEVELJAVEN_ID)

    def oznaci_kot_dokoncano(self, id:int) -> None:
        """Označi opravilo kot dokončano po ID)."""
        for opravilo in self.seznam_opravil:
            if id == opravilo.id:
                opravilo.oznaci_kot_dokoncano()
                return
        raise TaskNiMogoceNajti(TaskNiMogoceNajti.NEVELJAVEN_ID)

    def save_to_file(self, pot:str) -> None:
        """
        Shrani seznam opravil v JSON datoteko.
         Vrže NapakaPriShranjevanjuDatoteke, če pride do napake pri pisanju.
        """
        podatki = [o.to_dict() for o in self.seznam_opravil]
        try:
            with open(pot,"w", encoding="utf-8") as f:
                json.dump(podatki,f,indent=4,ensure_ascii=False)
        except OSError:
            raise NapakaPriShranjevanjuDatoteke(NapakaPriShranjevanjuDatoteke.PRIVZETO)


    def load_from_file(self,pot:str) -> list[Task]:
        """
        Naloži seznam opravil iz JSON datoteke.
        Če datoteka ne obstaja, vrne prazen seznam.
        Vrže NapakaPriBranjuDatoteke, če JSON ni veljaven.
        """
        if not os.path.exists(pot):
            self.seznam_opravil = []
            return self.seznam_opravil
        try:
            with open(pot,"r",encoding="utf-8") as f:
                podatki = json.load(f)
            self.seznam_opravil = [Task.from_dict(d) for d in podatki]
        except(json.JSONDecodeError, OSError):
            raise NapakaPriBranjuDatoteke(NapakaPriBranjuDatoteke.PRIVZETO)
        return self.seznam_opravil

    def uredi_opravilo(self,
                       id:int,
                       nopis:Optional[str]=None,
                       ndatum:Optional[date]=None,
                       nprioriteta:Optional[int]=None) ->Task:
        """
        Uredi izbrano opravilo (opis, datum, prioriteta).
        Vrže izjemo TaskNiMogoceNajti, če ID ni veljaven.
        """

        for opravilo in self.seznam_opravil:
            if opravilo.id == id:
                if nopis is not None and nopis.strip():
                    opravilo.opis = nopis
                if ndatum is not None:
                    if not isinstance(ndatum,date):
                        raise TaskNiMogoceDodati(TaskNiMogoceDodati.NAPACEN_DATUM)
                    opravilo.datum=ndatum
                if nprioriteta is not None:
                    if not (1<=nprioriteta<=5):
                        raise TaskNiMogoceDodati(TaskNiMogoceDodati.NAPACNA_PRIORITETA)
                    opravilo.prioriteta = nprioriteta
                return opravilo
        raise TaskNiMogoceNajti(TaskNiMogoceNajti.NEVELJAVEN_ID)