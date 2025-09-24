class TaskNiMogoceNajti(Exception):
    NEVELJAVEN_ID = "Neveljaven ID opravila."

    def __init__(self, msg: str = NEVELJAVEN_ID):
        super().__init__(msg)


class TaskJeZeOpravljen(Exception):
    ZE_OPRAVLJEN = "Opravilo je že opravljeno."

    def __init__(self, msg: str = ZE_OPRAVLJEN):
        super().__init__(msg)


class NapakaPriBranjuDatoteke(Exception):
    PRIVZETO = "Napaka pri branju datoteke."

    def __init__(self, msg: str = PRIVZETO):
        super().__init__(msg)


class NapakaPriShranjevanjuDatoteke(Exception):
    PRIVZETO = "Napaka pri shranjevanju datoteke."

    def __init__(self, msg: str = PRIVZETO):
        super().__init__(msg)

class TaskNiMogoceDodati(Exception):
    PRAZEN_OPIS = "Opis ne sme biti prazen."
    DUPLIKAT = "Opravilo s tem opisom že obstaja."
    NAPACNA_PRIORITETA = "Prioriteta mora biti med 1 in 5."
    NAPACEN_DATUM = "Datum mora biti objekt date."

    def __init__(self, msg: str):
        super().__init__(msg)
