from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._listYear = []
        self._listShape = []
        self._nodi = []
        self._archi = []
        self._idMap = {}
        self._grafo = nx.DiGraph()

    def getYears(self):
        self._listYear = DAO.getAllYears()
        return self._listYear

    def getShapes(self, anno):
        self._listShape = DAO.getAllShapes(anno)
        return self._listShape


    # creare un grafo ORIENTATO, NON PESATO, DIRETTO
    # VERTICI: avvistamenti filtrati per anno e shape
    # ARCHI: esiste se gli avvistamenti sono avvenuti nello stesso stato
    def buildGraph(self, anno, shape):
        self._grafo.clear()
        self._nodi = DAO.get_all_sightings(anno, shape)
        for s in self._nodi:
            self._idMap[s.id] = s
        self._grafo.add_nodes_from(self._nodi)

        self._archi = DAO.getAllEdges(anno, shape)
        for e in self._archi:
            if e[1]<e[3]:
                self._grafo.add_edge(self._idMap[e[0]], self._idMap[e[2]])
            elif e[1]>e[3]:
                self._grafo.add_edge(self._idMap[e[2]], self._idMap[e[0]])


    def getNumNodi(self):
        return self._grafo.number_of_nodes()
    def getNumArchi(self):
        return self._grafo.number_of_edges()
    def getNodes(self):
        return list(self._grafo.nodes())
    def getEdges(self):
        return list(self._grafo.edges())

    def getComponentiDebolmenteConnesse(self):
        componenti = list(nx.weakly_connected_components(self._grafo))
        return componenti
