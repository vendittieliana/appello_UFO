import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []
        self._listNodi = []

    def fillDD(self):
        self._listYear = self._model.getYears()
        for anno in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(anno))
        self._view.update_page()
    def fillDDShape(self, anno):
        self._listShape = self._model.getShapes(anno)
        for shape in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()
    def read_anno(self, e):
        if e.control.value is None:
            self._anno = None
        else:
            self._anno = e.control.value
            self._view.ddshape.options.clear()
            self.fillDDShape(self._anno)

    def read_shape(self, e):
        if e.control.value is None:
            self._shape = None
        else:
            self._shape = e.control.value

    # e CREA GRAFO, creare un grafo semplice, pesato e non orientato
    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        anno = self._view.ddyear.value
        shape = self._view.ddshape.value
        if anno is None:
            self._view.create_alert("Anno non inserito")
            return
        if shape is None:
            self._view.create_alert("Forma non inserita")
            return

        self._model.buildGraph(anno, shape)
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._listNodi = self._model.getNodes()
        for nodo in self._listNodi:
            self._view.txt_result.controls.append(ft.Text(
                f"Nodo {nodo.id} somma pesi su archi: {self._model.getPesiArchiAdiacenti(nodo)}"))

        self._view.update_page()

    def handle_path(self, e):
        pass