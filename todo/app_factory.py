from __future__ import annotations

from typing import Literal
from  todoapp import ToDoApp
from ToDoAppSQL import ToDoAppSQL
from repository import IToDoRepository

class AppFactory:
    @staticmethod
    def ustvari_app(izbira:Literal["json","sql"]= "json",
                    db_pot:str = "todo.db")->IToDoRepository:
        """
        Ustvari in vrne instanco ToDo aplikacije glede na način shranjevanja.

        :param storage: "json" za datoteko/običajen seznam ali "sql" za SQLite.
        :param db_path: pot do SQLite baze (če je izbran "sql").
        """
        if izbira == "json":
            return ToDoApp()
        elif izbira == "sql":
            return ToDoAppSQL(db_pot)
        else:
            raise ValueError("Neznan način shranjevanja: izberi 'json' ali 'sql'")
