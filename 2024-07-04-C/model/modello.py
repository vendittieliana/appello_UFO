from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self._listYear = []
        self._listShape = []
        self._grafo = nx.DiGraph()   # Grafo orientato
        self._nodi = []
        self._archi = []
        self._idMap = {}

        ###############
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

    def getYears(self):
      self._listYear = DAO.getAllYears()
      return self._listYear

    def getShapes(self, anno):
        self._listShape = DAO.getAllShapes(anno)
        return self._listShape

    # Nodi: sighting filtrati per ANNO e SHAPE
    #
    # Arco: tra 2 sighting che sono avvenuti nello stesso STATO
    #
    # Peso: differenza delle due longitudini
    def buildGraph(self, anno, shape):
        self._grafo.clear()
        self._nodi = DAO.get_all_sightings(anno, shape)
        for s in self._nodi:
            self._idMap[s.id] = s
        self._grafo.add_nodes_from(self._nodi)

        self._archi = DAO.getAllEdges(anno, shape)
        for e in self._archi:
            if e[1] < e[3]:
                peso = e[3]-e[1]
                self._grafo.add_edge(self._idMap[e[0]], self._idMap[e[2]], weight=peso)
            elif e[1] > e[3]:
                peso = e[1] - e[3]
                self._grafo.add_edge(self._idMap[e[2]], self._idMap[e[0]], weight=peso)

    # Stampare i 5 archi di peso maggiore, ordinati in ordine decrescente di peso (vedere esempi di soluzione). Per
    # ognuno di questi 5 archi stampare l’id del nodo di origine, l’id del nodo di destinazione, ed il peso.
    def getArchiPesoMaggiore(self):
        listaArchi = []
        listaBest5 = []
        for uscente, entrante in self._grafo.edges():
            pesoArco = self._grafo[uscente][entrante]["weight"]
            listaArchi.append((uscente, entrante, pesoArco))
        listaArchi.sort(key=lambda x: x[2], reverse=True)
        conta = 0
        for a in range(0, len(listaArchi)):
            if (conta <= 4):
                listaBest5.append(listaArchi[a])
                conta += 1
        return listaBest5


    def getNumNodi(self):
        return self._grafo.number_of_nodes()
    def getNumArchi(self):
        return self._grafo.number_of_edges()
    def getNodes(self):
        return list(self._grafo.nodes())
    def getEdges(self):
        return list(self._grafo.edges())


    ##################################################
    # RICORSIONE #
    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1,13), 0)

        for nodo in self._nodi:
            self._occorrenze_mese[nodo.datetime.month] += 1
            successivi_durata_crescente = self._calcola_successivi(nodo)
            self._calcola_cammino_ricorsivo([nodo], successivi_durata_crescente)
            self._occorrenze_mese[nodo.datetime.month] -= 1
        return self._cammino_ottimo, self._score_ottimo

    def _calcola_successivi(self, nodo: Sighting) -> list[Sighting]:
        pass

    def _calcola_cammino_ricorsivo(self, parziale: list[Sighting], successivi: list[Sighting]):
        pass
