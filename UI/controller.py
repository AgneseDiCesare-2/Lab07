import flet as ft

from UI.view import View
from model.model import Model
from model.situazione import Situazione

class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        avg=self._model.get_avg_umidita(self._mese)
        for chiave in avg.keys():
            self._view.lst_result.controls.append(ft.Text(f"{chiave}: {avg[chiave]}"))
        self._view.update_page()
        return

    def leggi_umidita(self, e):
        pass

    def handle_sequenza(self, e):
        lista_citta=self._model.calcola_sequenza(self._mese)
        for citta in lista_citta:
            self._view.lst_result.controls.append(ft.Text(citta))
            self._view.update_page()
        return

    def read_mese(self, e):
        self._mese = int(e.control.value)

