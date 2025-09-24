import tkinter as tk
from tkinter import messagebox
from controller import ToDoController
from app_factory import AppFactory
from ui_logic import pripravi_opravilo,pripravi_spremembe
from napake import TaskNiMogoceDodati,TaskNiMogoceNajti
class GUI:
    def __init__(self,okno, controller:ToDoController):
        self.controller = controller
        self.okno = okno
        self.okno.title("ToDo Aplikacija")

        # seznam opravil
        self.opravila = tk.Listbox(okno,width=60,height=15)
        self.opravila.pack(pady=10)

        #vnosno polje za opis
        tk.Label(okno, text="Opis opravila:").pack()
        self.opis_vnos = tk.Entry(okno,width=40)
        self.opis_vnos.pack(pady=5)
        # vnosno polje za datum
        tk.Label(okno, text="Rok (YYYY-MM-DD):").pack()
        self.datum_vnos = tk.Entry(okno,width=20)
        self.datum_vnos.pack(pady=2)
        #vnosno polje za prioriteto
        tk.Label(okno, text="Prioriteta (1–5):").pack()
        self.prioriteta_vnos = tk.Entry(okno,width=5)
        self.prioriteta_vnos.insert(0,"3")
        self.prioriteta_vnos.pack(pady=2)
        # vnosno polje kljucna_beseda
        tk.Label(text="Ključna beseda za iskanje po opisu").pack()
        self.kljucna_beseda_vnos = tk.Entry(okno,width=30)
        self.kljucna_beseda_vnos.pack(pady=2)

        #menu datoteka
        menubar = tk.Menu(okno)
        datoteka = tk.Menu(menubar,tearoff=0)
        datoteka.add_command(label="💾 Shrani",command=self.shrani)
        datoteka.add_command(label="📂 Naloži", command=self.nalozi)
        datoteka.add_command(label="Izhod",command=okno.quit)
        menubar.add_cascade(label="Datoteka", menu=datoteka)

        #menu pogled
        pogled = tk.Menu(menubar,tearoff=0)
        pogled.add_command(label="Razvrsti opravila po datumu",command=self.razvrsti_po_datumu)
        pogled.add_command(label="Razvrsti opravila po prioriteti", command=self.razvrsti_po_prioriteti)
        menubar.add_cascade(label="Pogled",menu=pogled)

        #menu filtriraj
        filtriraj = tk.Menu(menubar,tearoff=0)
        filtriraj.add_command(label="Prikazi opravila, ki ustrezajo kljucni besedi ", command=self.filtriraj_po_opisu)
        filtriraj.add_command(label="Prikazi opravila, ki so že opravljena", command=self.filtriraj_opravljena)
        filtriraj.add_command(label="Prikazi opravila, ki še niso dokoncana", command=self.filtriraj_neopravljena)
        filtriraj.add_command(label="Prikazi zamujena opravila", command=self.filtriraj_zakasnjena)
        menubar.add_cascade(label="Filtriraj",menu=filtriraj)

        okno.config(menu=menubar)

        #gumbi
        tk.Button(okno,text="Dodaj opravilo",command=self.dodaj_opravilo).pack(pady=2)
        tk.Button(okno,text="Brisanje opravila",command=self.izbrisi_opravilo).pack(pady=2)
        tk.Button(okno,text="Označi kot dokončano",command=self.oznaci_kot_dokoncano).pack(pady=2)
        tk.Button(okno,text="Uredi opravilo",command=self.uredi_opravilo).pack(pady=2)

        self.status_label = tk.Label(okno, text="", anchor="w")
        self.status_label.pack(fill="x", side="bottom")

        self.osvezi()

    def osvezi(self):
        self.opravila.delete(0,tk.END)
        for o in self.controller.pridobi_opravila():
            status = "✅" if o.status else "❌"
            self.opravila.insert(tk.END, f"[{o.id}] {status} {o.opis}")


        podatki = self.controller.statistika()
        self.status_label.config(
            text=f"Skupaj: {podatki['st vseh']} | "
                 f"Dokončanih: {podatki['st opravljenih']} | "
                 f"Nedokončanih: {podatki['st nedokoncanih']}"
        )


    def dodaj_opravilo(self):
        opis = self.opis_vnos.get().strip()
        datum =self.datum_vnos.get().strip()
        prioriteta = self.prioriteta_vnos.get().strip()
        try:
            opis,d,p = pripravi_opravilo(opis,datum,prioriteta)
            self.controller.dodaj_opravilo(opis,False,d,p)
            self.osvezi()
            self.opis_vnos.delete(0,tk.END)
            self.datum_vnos.delete(0,tk.END)
            self.prioriteta_vnos.delete(0,tk.END)
            self.prioriteta_vnos.insert(0, "3")
        except ValueError as e:
            messagebox.showerror("Napaka",str(e))

    def izbrisi_opravilo(self):
        izbrano = self.opravila.curselection()
        if not izbrano:
            messagebox.showerror("Napaka","Najprej izberi opravilo.")
            return
        vrstica = self.opravila.get(izbrano[0])
        opravilo_id = int(vrstica.split("]")[0][1:])
        self.controller.izbrisi_opravilo(opravilo_id)
        self.osvezi()

    def oznaci_kot_dokoncano(self):
        izbrano = self.opravila.curselection()
        if not izbrano:
            messagebox.showerror("Napaka","Najprej izberi opravilo.")
            return
        vrstica = self.opravila.get(izbrano[0])
        opravilo_id = int(vrstica.split("]")[0][1:])
        self.controller.oznaci_opravilo_kot_dokoncano(opravilo_id)
        self.osvezi()

    def uredi_opravilo(self):
        izbrano = self.opravila.curselection()
        if not izbrano:
            messagebox.showerror("Napaka", "Naprej izberi opravilo.")
            return
        vrstica = self.opravila.get(izbrano[0])
        opravilo_id = int(vrstica.split("]")[0][1:])

        opis = self.opis_vnos.get()
        datum = self.datum_vnos.get()
        prioriteta = self.prioriteta_vnos.get()

        try:
            nopis,ndatum,nprioriteta = pripravi_spremembe(opis,datum,prioriteta)
            self.controller.uredi_opravilo(opravilo_id,nopis, ndatum, nprioriteta)
            self.osvezi()
        except TaskNiMogoceDodati as e:
            messagebox.showerror("Napaka pri podatkih", str(e))
        except TaskNiMogoceNajti as e:
            messagebox.showerror("Napaka pri ID_ju", str(e))
        except Exception as e:
            messagebox.showerror("Nepričakovana napaka", str(e))
    def razvrsti_po_datumu(self):
        self.opravila.delete(0,tk.END)
        opravila = self.controller.razvrsti_po_datumu()
        for o in opravila:
            status = "✅" if o.status else "❌"
            self.opravila.insert(tk.END, f"[{o.id}] {status} {o.opis} (rok: {o.datum}, prioriteta: {o.prioriteta})")

    def razvrsti_po_prioriteti(self):
        self.opravila.delete(0,tk.END)
        opravila = self.controller.razvrsti_po_prioriteti()
        for o in opravila:
            status = "✅" if o.status else "❌"
            self.opravila.insert(tk.END, f"[{o.id}] {status} {o.opis} (rok: {o.datum}) (prioriteta: {o.prioriteta}) ")

    def filtriraj_po_opisu(self):
        kljucna_beseda = self.kljucna_beseda_vnos.get().strip().lower()
        opravila = self.controller.iskanje_po_opisu(kljucna_beseda)
        if not opravila:
            messagebox.showinfo("Rezultat iskanja",f"Ni najdenih opravil za: '{kljucna_beseda}'")
            return
        rezultat = "\n".join(
            f"[{o.id}] {'✅' if o.status else '❌'} {o.opis}" for o in opravila
        )
        messagebox.showinfo("Rezultat iskanja", rezultat)


    def filtriraj_opravljena(self):
        opravila = self.controller.filtriraj_opravljena()
        if not opravila:
            messagebox.showinfo("Rezultat iskanja", f"Ni najdenih opravil za status opravljeno")
            return
        rezultat = "\n".join(
            f"[{o.id}] {'✅' if o.status else '❌'} {o.opis}" for o in opravila
        )
        messagebox.showinfo("Rezultat iskanja", rezultat)

    def filtriraj_neopravljena(self):
        opravila = self.controller.filtriraj_neopravljena()
        if not opravila:
            messagebox.showinfo("Rezultat iskanja", f"Ni najdenih opravil za status nedokončano'")
            return
        rezultat = "\n".join(
            f"[{o.id}] {'✅' if o.status else '❌'} {o.opis}" for o in opravila
        )
        messagebox.showinfo("Rezultat iskanja", rezultat)

    def filtriraj_zakasnjena(self):
        opravila = self.controller.filtriraj_zakasnjena()
        if not opravila:
            messagebox.showinfo("Rezultat iskanja", f"Ni najdenih opravil, ki bi imela potekel datum in bila neopravljena")
            return
        rezultat = "\n".join(
            f"[{o.id}] {'✅' if o.status else '❌'} {o.opis}" for o in opravila
        )
        messagebox.showinfo("Rezultat iskanja", rezultat)

    def shrani(self):
        from tkinter import filedialog
        pot = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON datoteke", "*.json"), ("Vse datoteke", "*.*")]
        )
        if not pot:
            return  # uporabnik je preklical
        self.controller.save_to_file(pot)
        messagebox.showinfo("Shranjevanje", f"Opravila so bila shranjena v datoteko:\n{pot}")

    def nalozi(self):
        try:
            from tkinter import filedialog
            pot = filedialog.askopenfilename(
                filetypes=[("JSON datoteke", "*.json"), ("Vse datoteke", "*.*")]
            )
            if not pot:
                return  # uporabnik je preklical
            self.controller.load_from_file(pot)
            messagebox.showinfo("Nalaganje", f"Opravila so bila naložena iz datoteke:\n{pot}")
        except Exception as e:
            messagebox.showerror("Napaka", f"Nalaganje ni uspelo:\n{e}")


if __name__ == "__main__":

    app = AppFactory.ustvari_app("json")
    controller = ToDoController(app)

    okno = tk.Tk()
    gui = GUI(okno, controller)
    okno.mainloop()


