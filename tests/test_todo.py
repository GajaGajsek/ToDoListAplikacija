from task import Task
from todo import ToDoApp
import pytest
from napake import TaskNiMogoceNajti,TaskNiMogoceDodati,TaskJeZeOpravljen,NapakaPriBranjuDatoteke

from datetime import date, timedelta
def test_task_creation_and_str():
    task = Task("Naredi domačo nalogo", prioriteta=2)
    assert task.opis == "Naredi domačo nalogo"
    assert task.prioriteta == 2
    assert "Naredi domačo nalogo" in str(task)
    assert "(P2)" in str(task)

def test_task_neveljavna_prioriteta():
    # povedati moramo da gre za izjemo
    with pytest.raises(TaskNiMogoceDodati, match= TaskNiMogoceDodati.NAPACNA_PRIORITETA):
        Task("Naredi domačo nalogo", prioriteta=10)

def test_urejanje_opravila_vrne_task():
    app =ToDoApp()
    app.dodaj_opravilo("Opravi domačo nalogo")
    urejeno = app.uredi_opravilo(1,nopis="Pojdi v trgovino")
    assert  urejeno.opis == "Pojdi v trgovino"
    urejeno = app.uredi_opravilo(1,nprioriteta=5)
    assert urejeno.prioriteta == 5
    from datetime import date
    ndatum = date(2025,9,12)
    urejeno= app.uredi_opravilo(1,ndatum=ndatum)
    assert  urejeno.datum == ndatum

def test_uredi_opravilo_ni_spremembe():
    app = ToDoApp()
    from datetime import date
    ndatum = date(2025, 9, 12)
    app.dodaj_opravilo(opis="Opravi domačo nalogo", datum=ndatum, prioriteta=5 )
    app.uredi_opravilo(1)
    assert app.seznam_opravil[0].opis == "Opravi domačo nalogo"
    assert app.seznam_opravil[0].datum == ndatum
    assert app.seznam_opravil[0].prioriteta == 5

def test_uredi_opravilo_napacen_id():
    app = ToDoApp()
    app.dodaj_opravilo("Opravi domačo nalogo")
    with pytest.raises(TaskNiMogoceNajti,match=TaskNiMogoceNajti.NEVELJAVEN_ID):
        app.uredi_opravilo(2)

def test_uredi_opravilo_neuspešna_prioriteta():
    app =ToDoApp()
    app.dodaj_opravilo("Opravi domačo nalogo")
    with pytest.raises(TaskNiMogoceDodati,match=TaskNiMogoceDodati.NAPACNA_PRIORITETA):
        app.uredi_opravilo(1,nprioriteta=10)


def test_task_dokoncano():
    task = Task("Naredi domačo nalogo")
    assert task.status == False
    task.oznaci_kot_dokoncano()
    assert task.status == True

def test_isto_opravilo_dvakrat_dokoncano():
    task =Task("Naredi domačo nalogo")
    task.oznaci_kot_dokoncano()  #prvič uspe
    with pytest.raises(TaskJeZeOpravljen, match=TaskJeZeOpravljen.ZE_OPRAVLJEN):
        task.oznaci_kot_dokoncano() # drugič izjema

def test_dodajanje_in_brisanje_opravila():
    app = ToDoApp()
    assert len(app.seznam_opravil) == 0
    app.dodaj_opravilo("Naredi domačo nalogo")
    assert len(app.seznam_opravil) == 1
    app.izbrisi_opravilo(1)
    assert len(app.seznam_opravil) == 0

def test_brisanje_ni_mogoce():
    app = ToDoApp()
    app.dodaj_opravilo("Naredi domačo nalogo")
    with pytest.raises(TaskNiMogoceNajti,match=TaskNiMogoceNajti.NEVELJAVEN_ID):
        app.izbrisi_opravilo(2)

def test_filtriraj_zakasnjena():
    app = ToDoApp()
    yesterday = date.today() - timedelta(days=1)
    app.dodaj_opravilo("Naredi domačo nalogo",datum=yesterday)
    zamujena = app.filtriraj_zakasnjena()
    assert len(zamujena) == 1
    assert zamujena[0].opis == "Naredi domačo nalogo"

def test_statistiko():
    app = ToDoApp()
    app.dodaj_opravilo("Naredi domačo nalogo")
    app.oznaci_kot_dokoncano(1)
    app.dodaj_opravilo("Pospravi stanovanje")
    statistika = app.statistika()
    assert statistika["st vseh"] == len(app.seznam_opravil)
    assert statistika["st nedokoncanih"] == len(app.filtriraj_neopravljena())
    assert statistika["st opravljenih"] == len(app.filtriraj_opravljena())

def test_iskanje_po_opisu():
    app = ToDoApp()
    app.dodaj_opravilo("Naredi domačo nalogo")
    app.dodaj_opravilo("Pospravi sobo")
    iskanje = app.iskanje_po_opisu("Naredi")
    iskanje1 = app.iskanje_po_opisu("SOBO")
    iskanje2 = app.iskanje_po_opisu("Nakup")
    assert  len(iskanje) == 1
    assert iskanje[0] == app.seznam_opravil[0]
    assert  len(iskanje1) == 1
    assert  iskanje1[0] == app.seznam_opravil[1]
    assert  len(iskanje2) == 0

def test_razvrsti_po_prioriteti():
    app = ToDoApp()
    app.dodaj_opravilo("Pojdi v trgovino")
    app.dodaj_opravilo("Naredi domačo nalogo",prioriteta=5)
    app.dodaj_opravilo("Pospravi sobo", prioriteta=2)
    razvrsti = app.razvrsti_po_prioriteti()
    prioritete = [t.prioriteta for t in razvrsti]
    assert prioritete == sorted(prioritete)

def test_shrani():
    app = ToDoApp()
    app.dodaj_opravilo("Naredi domačo nalogo")
    app.dodaj_opravilo("Pospravi sobo")
    app.save_to_file("test.json")
    import  os
    assert  os.path.exists("test.json")
    assert  os.path.getsize("test.json") > 0

def test_nalozi():
    app = ToDoApp()
    app.dodaj_opravilo("Naredi domačo nalogo")
    app.dodaj_opravilo("Pospravi sobo")
    pot = "test.json"
    app.save_to_file(pot)
    seznam = app.load_from_file(pot)
    assert  len(seznam) == 2
    assert  seznam[0].opis == "Naredi domačo nalogo"
    assert  seznam[1].opis == "Pospravi sobo"

def test_razvrsti_datum():
    from datetime import date,timedelta
    app = ToDoApp()
    app.dodaj_opravilo("Naredi domačo nalogo",datum=date.today())
    app.dodaj_opravilo("Pospravi sobo", datum= date.today() - timedelta(days=1))
    app.dodaj_opravilo("Pojdi v trgovino", datum=date.today()+ timedelta(days=1))
    razvrščeno = app.razvrsti_po_datumu()
    datumi = [t.datum for t in razvrščeno]
    assert len(razvrščeno) == len(app.seznam_opravil)
    assert sorted(datumi) == datumi

def test_dokoncana():
    app = ToDoApp()
    app.dodaj_opravilo("Naredi domačo nalogo")
    app.dodaj_opravilo("Pospravi sobo")
    app.oznaci_kot_dokoncano(1)
    dokoncano = app.filtriraj_opravljena()
    assert  len(dokoncano) == 1
    assert dokoncano[0].opis =="Naredi domačo nalogo"

def test_nedokoncana():
    app = ToDoApp()
    app.dodaj_opravilo("Naredi domačo nalogo")
    app.dodaj_opravilo("Pospravi sobo")
    app.oznaci_kot_dokoncano(2)
    nedokoncano = app.filtriraj_neopravljena()
    assert  len(nedokoncano) == 1
    assert nedokoncano[0].opis =="Naredi domačo nalogo"

def test_dodajanje_prazen_opis():
    app = ToDoApp()
    with pytest.raises(TaskNiMogoceDodati,match=TaskNiMogoceDodati.PRAZEN_OPIS):
        app.dodaj_opravilo("")

def test_dodajanje_duplikat():
    app =ToDoApp()
    app.dodaj_opravilo("Naredi domačo nalogo")
    with pytest.raises(TaskNiMogoceDodati,match=TaskNiMogoceDodati.DUPLIKAT):
        app.dodaj_opravilo("Naredi domačo nalogo")

def test_oznaci_neobstojec():
    app = ToDoApp()
    with pytest.raises(TaskNiMogoceNajti, match=TaskNiMogoceNajti.NEVELJAVEN_ID):
        app.oznaci_kot_dokoncano(1)


def test_napaka_pri_branju(tmp_path):
    pot = tmp_path / "pokvarjen.json"
    pot.write_text("{neveljavno}")
    app = ToDoApp()
    with pytest.raises(NapakaPriBranjuDatoteke,match=NapakaPriBranjuDatoteke.PRIVZETO):
        app.load_from_file(str(pot))

def test_nalaganje_prazne_datoteke(tmp_path):
    prazna_pot = tmp_path / "prazna.json"
    prazna_pot.write_text("")
    app = ToDoApp()
    with pytest.raises(NapakaPriBranjuDatoteke,match=NapakaPriBranjuDatoteke.PRIVZETO):
        app.load_from_file(str(prazna_pot))

def test_zamujeno_opravilo_izpis():
    from datetime import date,timedelta
    vceraj = date.today() - timedelta(days=1)
    task = Task("Pospravi sobo",datum=vceraj)
    izpis = str(task)
    assert "🔴" in izpis
    from colorama import Fore
    assert Fore.RED in izpis