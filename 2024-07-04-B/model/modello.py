from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._listYear = []
        self._listState = []
        self._grafo = nx.Graph()  # Grafo NON orientato
        self._nodi = []
        self._archi = []
        self._idMap = {}

    def getYears(self):
        self._listYear = DAO.getAllYears()
        return self._listYear

    def getStates(self, anno):
        self._listState = DAO.getAllStates(anno)
        return self._listState

    # Nodi: sighting filtrati per ANNO e STATE
    # Arco: tra 2 sighting che hanno la stessa SHAPE e distance_HV per calcolare la distanza
    # un arco fra due avvistamenti esiste se e solo se tali avvistamenti hanno la
    # stessa Forma (colonna “shape” del db) e sono avvenuti ad una distanza inferiore a 100km.

    def buildGraph(self, anno, state):
        self._grafo.clear()
        self._nodi = DAO.get_all_sightings(anno, state)
        for s in self._nodi:
            self._idMap[s.id] = s
        self._grafo.add_nodes_from(self._nodi)

        self._archi = DAO.getAllEdges(anno, state)
        for e in self._archi:
            s1 = self._idMap[e[0]]  # s1 è l'avvistamento1
            s2 = self._idMap[e[3]]

            if s1.distance_HV(s2) < 100:
                self._grafo.add_edge(s1, s2)

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()
    def getNodes(self):
        return list(self._grafo.nodes())
    def getEdges(self):
        return list(self._grafo.edges())

    # Stampare il numero di componenti connesse
    def get_connected_components(self):
        components = list(nx.connected_components(self._grafo))
        return components
    def getConnectedComponents(self):
        return nx.number_connected_components(self._grafo)

