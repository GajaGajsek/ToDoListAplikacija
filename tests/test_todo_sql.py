import pytest
from ToDoAppSQL import ToDoAppSQL
from napake import TaskNiMogoceDodati,TaskNiMogoceNajti
from task import Task


#vsakič dobim svezo različico datoteke .db
@pytest.fixture
def app(tmp_path):
    db_pot = tmp_path / "test.db"
    app = ToDoAppSQL(str(db_pot))
    return app

def test_dodajopravilosql(app):
    app.dodaj_opravilo("Pospravi sobo", prioriteta=3)
    opravila = app.pridobi_vsa_opravila()
    assert len(opravila) == 1
    assert opravila[0].opis == "Pospravi sobo"
    assert opravila[0].prioriteta == 3
    assert isinstance(opravila[0],Task)

def test_dodaj_opravilo_vrne_task(app):
    task = app.dodaj_opravilo("Pospravi sobo", prioriteta=3)
    assert task.opis == "Pospravi sobo"
    assert task.prioriteta == 3

def test_brisanje_opravila_sql(app):
    app.dodaj_opravilo("Pospravi sobo",prioriteta=4)
    app.dodaj_opravilo("Opravi domačo nalogo",prioriteta=5)
    opravila = app.pridobi_vsa_opravila()
    id = [o.id for o in opravila if o.opis == "Opravi domačo nalogo"][0]
    app.izbrisi_opravilo(id)
    opravila = app.pridobi_vsa_opravila()
    assert len(opravila) == 1
    assert opravila[0].opis == "Pospravi sobo"
    assert opravila[0].prioriteta == 4

def test_oznacikotdokoncanosql(app):
    app.dodaj_opravilo("Pospravi sobo",prioriteta=4)
    opravila = app.pridobi_vsa_opravila()
    id = [o.id for o in opravila if o.opis == "Pospravi sobo"][0]
    app.oznaci_kot_dokoncano(id)
    opravila = app.pridobi_vsa_opravila()
    assert len(opravila) == 1
    assert opravila[0].opis == "Pospravi sobo"
    assert opravila[0].status is True

def test_iskanjepoopisusql(app):
    app.dodaj_opravilo("Pospravi sobo",prioriteta=4)
    app.dodaj_opravilo("Opravi domačo nalogo",prioriteta=5)
    opravila =app.iskanje_po_opisu("Pospravi")
    assert len(opravila) == 1
    assert opravila[0].opis == "Pospravi sobo"

def test_filtriranje_po_statusu(app):
    app.dodaj_opravilo("Pospravi sobo")
    app.dodaj_opravilo("Opravi domačo nalogo")
    opravila = app.pridobi_vsa_opravila()
    id = [o.id for o in opravila if o.opis == "Pospravi sobo"][0]
    app.oznaci_kot_dokoncano(id)
    dokoncana = app.filtriraj_opravljena()
    nedokoncana = app.filtriraj_neopravljena()
    assert len(dokoncana) == 1
    assert dokoncana[0].opis == "Pospravi sobo"
    assert dokoncana[0].status is True
    assert len(nedokoncana) == 1
    assert nedokoncana[0].opis == "Opravi domačo nalogo"
    assert nedokoncana[0].status is False

def test_statistikasql(app):
    from datetime import date,timedelta
    vceraj = date.today() - timedelta(days=1)
    app.dodaj_opravilo("Pospravi kuhinjo", datum=vceraj)
    app.dodaj_opravilo("Pospravi sobo")
    app.dodaj_opravilo("Opravi domačo nalogo")
    opravila = app.pridobi_vsa_opravila()
    id = [o.id for o in opravila if o.opis == "Pospravi sobo"][0]
    app.oznaci_kot_dokoncano(id)
    statistika = app.statistika()
    assert  statistika["st vseh"] == len(app.pridobi_vsa_opravila())
    assert  statistika["st opravljenih"] == len(app.filtriraj_opravljena())
    assert statistika["st nedokoncanih"] == len((app.filtriraj_neopravljena()))
    assert statistika["st zamujenih"] == len(app.filtriraj_zakasnjena())
    assert statistika["st zamujenih"] > 0

def test_dodajanje_duplikatsql(app):
    app.dodaj_opravilo("Pospravi sobo")
    with pytest.raises(TaskNiMogoceDodati, match= TaskNiMogoceDodati.DUPLIKAT):
        app.dodaj_opravilo("Pospravi sobo")

def test_urejanje_opravila(app):
    app.dodaj_opravilo("Pospravi sobo",prioriteta=3)
    opravila = app.pridobi_vsa_opravila()
    id = [o.id for o in opravila if o.opis =="Pospravi sobo"][0]
    app.uredi_opravilo(id=id,nopis="Pospravi kuhinjo",nprioriteta=5)
    opravila = app.pridobi_vsa_opravila()
    assert  len(opravila)==1
    assert opravila[0].opis == "Pospravi kuhinjo"
    assert opravila[0].prioriteta == 5

def test_shranjevanje_in_nalaganje_sql(app,tmp_path):
    app.dodaj_opravilo("Opravi domačo nalogo",prioriteta=2)
    app.dodaj_opravilo("Pospravi sobo",prioriteta=4)
    # preveri ali sta v bazi
    opravila = app.pridobi_vsa_opravila()
    assert len(opravila) == 2
    # ustvari novo instanco na isti bazi
    app2 = ToDoAppSQL(str(tmp_path/"test.db"))
    opravila2 = app2.pridobi_vsa_opravila()
    assert len(opravila2) == 2
    assert opravila2[0].opis == "Opravi domačo nalogo"
    assert opravila2[0].prioriteta == 2
    assert opravila2[1].opis == "Pospravi sobo"
    assert opravila2[1].prioriteta == 4

def test_uredi_opravilo(app):
    from datetime import date
    opravilo = app.dodaj_opravilo("Opravi domačo nalogo",prioriteta=5)
    task = app.uredi_opravilo(opravilo.id,nopis="Pospravi kuhinjo")
    assert task.opis == "Pospravi kuhinjo"
    task= app.uredi_opravilo(opravilo.id,nprioriteta=2)
    assert task.prioriteta == 2
    nov_datum = date(2025,9,25)
    task = app.uredi_opravilo(opravilo.id,ndatum=nov_datum)
    assert task.datum == nov_datum

def test_brisanje_neobstoječca_id_opravila(app):
    opravilo = app.dodaj_opravilo("Pospravi sobo")
    novi_id = opravilo.id + 1
    with pytest.raises(TaskNiMogoceNajti, match=TaskNiMogoceNajti.NEVELJAVEN_ID):
        app.izbrisi_opravilo(novi_id)

def test_urejanje_napacen_datum(app):
    opravilo = app.dodaj_opravilo("Pospravi sobo")
    nov_datum= "napacen"
    with pytest.raises(TaskNiMogoceDodati,match=TaskNiMogoceDodati.NAPACEN_DATUM):
        app.uredi_opravilo(opravilo.id,ndatum=nov_datum)

def test_statistika_prazen_seznam(app):
    assert len(app.pridobi_vsa_opravila()) == 0
    statistika = app.statistika()
    assert  statistika["st vseh"] == 0
    assert  statistika["st opravljenih"] == 0
    assert statistika["st nedokoncanih"] == 0
    assert statistika["st zamujenih"] == 0

def test_urejanje_napacna_prioriteta(app):
    opravilo = app.dodaj_opravilo("Pospravi sobo",prioriteta=4)
    nova_prioriteta = 10
    with pytest.raises(TaskNiMogoceDodati,match=TaskNiMogoceDodati.NAPACNA_PRIORITETA):
        app.uredi_opravilo(opravilo.id,nprioriteta=nova_prioriteta)