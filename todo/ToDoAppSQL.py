from __future__ import annotations
import json
from datetime import date
from task import Task
import  sqlite3
from typing import Optional
from repository import IToDoRepository
from napake import TaskNiMogoceNajti,TaskJeZeOpravljen,TaskNiMogoceDodati,NapakaPriBranjuDatoteke,NapakaPriShranjevanjuDatoteke

class ToDoAppSQL(IToDoRepository):
    """Razred za delo z opravili v SQLite bazi."""
    def _map_task(self, vrstica: sqlite3.Row)->Task:
        """Pretvori vrstico iz baze v objekt Task."""
        return Task(
            id=vrstica[0],
            opis=vrstica[1],
            status=bool(vrstica[2]),
            datum=date.fromisoformat(vrstica[3]) if vrstica[3] else None,
            prioriteta=vrstica[4]
        )

    def __init__(self,db_pot:str ="todo.db") ->None:
        """ Inicializacija aplikacije in samodejno ustvarjanje tabele, če še ne obstaja. """
        # Ustvari povezavo na bazo (če obstaja, jo odpre, sicer ustvari novo).
        self.db_pot = db_pot
        self.conn = self._povezi()
        self._ustvari_tabelo()

    def _povezi(self):
        """Vzpostavi povezavo z bazo."""
        conn = sqlite3.connect(self.db_pot)
        conn.row_factory = sqlite3.Row
        return conn

    def _ustvari_tabelo(self):
        """Ustvari tabelo, če še ne obstaja (CREATE TABLE IF NOT EXISTS)."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opis TEXT NOT NULL UNIQUE COLLATE NOCASE,
                status INTEGER NOT NULL DEFAULT 0,
                datum TEXT,
                prioriteta INTEGER NOT NULL CHECK(prioriteta BETWEEN 1 AND 5)
            )
        """)
        self.conn.commit()


    def close(self) -> None:
        """Zapre povezavo z bazo."""
        self.conn.close()

    def dodaj_opravilo(self,
                       opis:str,
                       status:bool=False,
                       datum: Optional[date]=None,
                       prioriteta:int=3 ) -> Task:
        """Doda opravilo v bazo. Vrže TaskNiMogoceDodati, če je opis prazen ali podvojen."""
        try:
            task = Task(opis, status, datum, prioriteta)

            kon = self.conn.execute(
                "INSERT INTO tasks (opis, status, datum, prioriteta) VALUES (?, ?, ?, ?)",
                (task.opis, int(task.status), task.datum.isoformat() if task.datum else None, task.prioriteta)
            )
            self.conn.commit()
            task.id = kon.lastrowid
            return task

        except sqlite3.IntegrityError:
            raise TaskNiMogoceDodati(TaskNiMogoceDodati.DUPLIKAT)
        except TaskNiMogoceDodati as e:
            raise e

    def izbrisi_opravilo(self,id:int) ->None:
        """Izbriše opravilo glede na ID. Vrže TaskNiMogoceNajti, če ne obstaja."""
        kon = self.conn.execute(
            "SELECT id FROM tasks WHERE id=?",(id,)
        )
        # podatke imamo v konstruktorju vendar jih nismo prenesli
        vrstica = kon.fetchone()
        if vrstica is None:
            raise TaskNiMogoceNajti(TaskNiMogoceNajti.NEVELJAVEN_ID)
        self.conn.execute(
            "DELETE FROM tasks WHERE id=?",(id,)
        )
        self.conn.commit()
    def oznaci_kot_dokoncano(self,id:int)->None:
        """Označi opravilo kot dokončano. Vrže izjemo, če je že dokončano."""
        kon = self.conn.execute(
            "SELECT id FROM tasks WHERE id=?",(id,)
        )
        vrstica = kon.fetchone()
        if vrstica is None:
            raise TaskNiMogoceNajti(TaskNiMogoceNajti.NEVELJAVEN_ID)
        kon = self.conn.execute(
            "SELECT status FROM tasks WHERE id=?",(id,)
        )
        vrstica = kon.fetchone()
        if vrstica[0] == 1:
            raise TaskJeZeOpravljen(TaskJeZeOpravljen.ZE_OPRAVLJEN)
        self.conn.execute(
            "UPDATE tasks SET status=1 WHERE id=?",(id,)
        )
        self.conn.commit()

    def uredi_opravilo(self,
                       id:int,
                       nopis:Optional[str]=None,
                       ndatum:Optional[date]=None,
                       nprioriteta:Optional[int]=None) ->Task:
        """Uredi opravilo (opis, datum, prioriteta)."""
        kon = self.conn.execute("SELECT * FROM tasks WHERE id=?",(id,))
        vrstica = kon.fetchone()
        if vrstica is None:
            raise TaskNiMogoceNajti(TaskNiMogoceNajti.NEVELJAVEN_ID)
        if ndatum is not None and not  isinstance(ndatum,date):
            raise TaskNiMogoceDodati(TaskNiMogoceDodati.NAPACEN_DATUM)
        if nprioriteta is not None:
            if not (1<= nprioriteta <=5):
                raise TaskNiMogoceDodati(TaskNiMogoceDodati.NAPACNA_PRIORITETA)
        if nopis is not None:
            try:
                self.conn.execute("UPDATE tasks SET opis=? WHERE id=?",(nopis,id,))
            except sqlite3.IntegrityError:
                raise TaskNiMogoceDodati(TaskNiMogoceDodati.DUPLIKAT)
        if ndatum is not None:
            self.conn.execute("UPDATE tasks SET datum=? WHERE id=?",(ndatum.isoformat(),id,))
        if nprioriteta is not None:
            self.conn.execute("UPDATE tasks SET prioriteta=? WHERE  id =?",(nprioriteta,id,))
        self.conn.commit()
        kon = self.conn.execute("SELECT * FROM tasks WHERE id=?",(id,))
        vrstica = kon.fetchone()
        return self._map_task(vrstica)

    def pridobi_vsa_opravila(self) ->list[Task]:
        """Vrne seznam vseh opravil iz baze kot objekte Task."""
        kon = self.conn.execute("SELECT * FROM tasks")
        return  [self._map_task(vrstica) for vrstica in kon.fetchall()]

    def save_to_file(self, pot: str = "opravila_sql.json") -> None:
        try:
            opravila = [t.to_dict() for t in self.pridobi_vsa_opravila()]
            with open(pot, "w", encoding="utf-8") as f:
                json.dump(opravila, f, ensure_ascii=False, indent=2)
        except Exception:
            raise NapakaPriShranjevanjuDatoteke(NapakaPriShranjevanjuDatoteke.PRIVZETO)

    def load_from_file(self, pot: str = "opravila_sql.json") -> None:
        try:
            with open(pot, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.conn.execute("DELETE FROM tasks")  # pobriši staro
            for d in data:
                self.conn.execute("INSERT INTO tasks (id, opis, status, datum, prioriteta) VALUES (?, ?, ?, ?, ?)",
                             (d["id"], d["opis"], int(d["status"]),
                              d["datum"] if d["datum"] else None,
                              d["prioriteta"]))
            self.conn.commit()
        except Exception:
            raise NapakaPriBranjuDatoteke(NapakaPriBranjuDatoteke.PRIVZETO)