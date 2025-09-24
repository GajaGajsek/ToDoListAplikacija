from todo.controller import ToDoController
from ToDoAppSQL import ToDoAppSQL
from todo.ui_logic import pripravi_opravilo
from task import Task

def test_integracije_controller_ui_logic_sql(tmp_path):
    #ustvari začasno SQL bazo
    db_pot = tmp_path / "integracija.db"
    app = ToDoAppSQL(str(db_pot))
    controller = ToDoController(app)

    #priptavi podatke kot bi jih vnesel uporabnik
    opis,datum,prioriteta =pripravi_opravilo("Opravi integracijski test","","5")

    #dodaj opravilo preko kontrolerja
    controller.dodaj_opravilo(opis,datum=datum,prioriteta=prioriteta)

    #preveri ali ga lahko pridobis
    opravilo = controller.pridobi_opravila()
    assert len(opravilo) == 1
    assert opravilo[0].opis == "Opravi integracijski test"
    assert opravilo[0].prioriteta == 5
    assert isinstance(opravilo[0],Task)