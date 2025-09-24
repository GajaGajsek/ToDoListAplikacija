from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
from task import Task


class IToDoRepository(ABC):
    """Osnovni vmesnik za repozitorije opravil (JSON, SQL, ...).
    Vsebuje skupno logiko, ki temelji na pridobi_vsa_opravila().
    """
    @abstractmethod
    def dodaj_opravilo(self,opis:str,
                       status:bool=False,
                       datum:Optional[date]=None,
                       prioriteta:int=3)->Task:
        pass

    @abstractmethod
    def izbrisi_opravilo(self,id:int)->None:
        pass

    @abstractmethod
    def oznaci_kot_dokoncano(self,id:int)->None:
        pass

    @abstractmethod
    def pridobi_vsa_opravila(self)->list[Task]:
        pass

    @abstractmethod
    def save_to_file(self,pot:str)->None:
        pass

    @abstractmethod
    def load_from_file(self,pot:str)->list[Task]:
        pass


    @abstractmethod
    def uredi_opravilo(self,id:int,nopis:Optional[str]=None,
                       ndatum:Optional[date]=None,
                       nprioriteta:Optional[int]=None)->Task:
        pass

   # skupna logika (deluje enako za vse implementacije)
    def filtriraj_opravljena(self)->list[Task]:
        return [o for o in self.pridobi_vsa_opravila() if o.status]

    def filtriraj_neopravljena(self)->list[Task]:
        return [o for o in self.pridobi_vsa_opravila() if not o.status]

    def filtriraj_zakasnjena(self)->list[Task]:
        danes = date.today()
        return [o for o in self.pridobi_vsa_opravila() if o.datum is not None
                and o.datum<danes and not o.status]

    def razvrsti_po_prioriteti(self)->list[Task]:
        return sorted(self.pridobi_vsa_opravila(),key=lambda o:o.prioriteta)

    def razvrsti_po_datumu(self)->list[Task]:
        return sorted(
            self.pridobi_vsa_opravila(),
            key=lambda o: (o.datum is None, o.datum or date.max)
        )

    def iskanje_po_opisu(self,kljucna_beseda:str)->list[Task]:
        if not kljucna_beseda.strip():
            return []
        return [o for o in self.pridobi_vsa_opravila() if kljucna_beseda.lower() in o.opis.lower()]

    def statistika(self)->dict[str,int]:
        vsa = len(self.pridobi_vsa_opravila())
        opravlena = len(self.filtriraj_opravljena())
        nedokoncana = len(self.filtriraj_neopravljena())
        zamujene = len(self.filtriraj_zakasnjena())
        return {"st vseh": vsa, "st opravljenih": opravlena, "st nedokoncanih": nedokoncana,
                "st zamujenih": zamujene}
