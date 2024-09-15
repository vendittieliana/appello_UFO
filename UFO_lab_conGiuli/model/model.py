import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._listYear = []
        self._listShape = []
        self._grafo = nx.Graph()   # Grafo NON orientato
        self._nodi = []
        self._archi = []
        self._idMap = {}

    def getYears(self):
      self._listYear = DAO.getAllYears()
      return self._listYear

    def getShapes(self, anno):
        self._listShape = DAO.getAllShapes(anno)
        return self._listShape

    # Nodi: Stati
    # Archi: . Un arco collega due stati solo se sono confinanti, come indicato
    # nella tabella “neighbor”.
    def buildGraph(self, anno, shape):
        self._grafo.clear()
        self._nodi = DAO.getAllStates()
        for stato in self._nodi:
            self._idMap[stato.id] = stato
        self._grafo.add_nodes_from(self._nodi)

        self._archi = DAO.getAllweightedEdges(anno,shape)
        for archi in self._archi:
            stato1 = self._idMap[archi[0]]
            stato2 = self._idMap[archi[1]]
            peso = archi[2]
            self._grafo.add_edge(stato1, stato2, weight=peso)

    def getPesiArchiAdiacenti(self, nodo):
        vicini = self._grafo.neighbors(nodo)
        pesoTot = 0
        for v in vicini:
            pesoTot += self._grafo[nodo][v]['weight']
        return pesoTot


    def getNumNodi(self):
        return self._grafo.number_of_nodes()
    def getNumArchi(self):
        return self._grafo.number_of_edges()
    def getNodes(self):
        return list(self._grafo.nodes())
    def getEdges(self):
        return list(self._grafo.edges())
