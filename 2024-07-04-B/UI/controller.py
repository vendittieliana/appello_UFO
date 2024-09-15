import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listState = []

    def fillDD(self):
        self._listYear = self._model.getYears()
        for anno in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(anno))
        self._view.update_page()
    def fillDDState(self, anno):
        self._listShape = self._model.getStates(anno)
        for shape in self._listShape:
            self._view.ddstate.options.append(ft.dropdown.Option(shape))
        self._view.update_page()
    def read_anno(self, e):
        if e.control.value is None:
            self._anno = None
        else:
            self._anno = e.control.value
            self._view.ddstate.options.clear()
            self.fillDDState(self._anno)
    def read_state(self, e):
        if e.control.value is None:
            self._state = None
        else:
            self._state = e.control.value

    # Nodi: sighting filtrati per ANNO e STATE
    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        anno = self._view.ddyear.value
        state = self._view.ddstate.value
        if anno is None:
            self._view.create_alert("Anno non inserito")
            return
        if state is None:
            self._view.create_alert("Forma non inserita")
            return

        self._model.buildGraph(anno, state)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        components = self._model.get_connected_components()
        num_components = len(components)
        self._view.txt_result1.controls.append(ft.Text(
            f"Numero di componenti connesse: {num_components}"
        ))
        # identificare la componente connessa di dimensione
        # maggiore, e stamparne i nodi
        largest_component = max(components, key=len)
        largest_size = len(largest_component)
        self._view.txt_result1.controls.append(ft.Text(
            f"la componente maggiore contiene {largest_size} nodi"
        ))
        self._view.txt_result1.controls.append(ft.Text(f"Nodi della componente maggiore:"))
        for component in largest_component:
            self._view.txt_result1.controls.append(ft.Text(component))

        self._view.update_page()


    def handle_path(self, e):
        pass

