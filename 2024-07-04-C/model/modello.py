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



#################################################
#################################################
sono all'opera

# ottenere i valori minimi e massimi delle durate
SELECT MIN(duration) AS min_duration, MAX(duration) AS max_duration
FROM sighting;

# ottenere tutti gli anni presenti nella colonna datetime
SELECT DISTINCT YEAR(datetime) AS year
FROM sighting
ORDER BY year DESC;

# trovare i nodi (Avvistamenti validi)
SELECT *
FROM sighting
WHERE YEAR(datetime) = @selected_year
  AND duration > @min_duration
  AND duration < @max_duration;

# trovare gli archi (Relazioni fra avvistamenti con la stessa forma)
SELECT s1.id AS source_id, s2.id AS target_id
FROM sighting s1
JOIN sighting s2 ON s1.shape = s2.shape
WHERE YEAR(s1.datetime) = @selected_year
  AND YEAR(s2.datetime) = @selected_year
  AND s1.duration > @min_duration
  AND s1.duration < @max_duration
  AND s2.duration > @min_duration
  AND s2.duration < @max_duration
  AND s1.id <> s2.id -- Evita la stessa riga
  AND (
    (s1.duration < s2.duration) OR
    (s1.duration = s2.duration AND s1.id < s2.id)
  );

# analisi delle durate nel grafo. Questa query conta il numero di nodi per ciascuna durata nel grafo e calcola la durata media.
SELECT duration, COUNT(*) AS node_count
FROM sighting
WHERE YEAR(datetime) = @selected_year
  AND duration > @min_duration
  AND duration < @max_duration
GROUP BY duration
ORDER BY duration;

SELECT AVG(duration) AS avg_duration
FROM sighting
WHERE YEAR(datetime) = @selected_year
  AND duration > @min_duration
  AND duration < @max_duration;


####################################
getAllEdges e buildGraph mi sembrano fatti bene, quindi l'output torna?


#####################################
# fammi sapere se può andar bene
 def analizza_grafo(self):
        # Conta il numero di nodi per ciascuna durata
        durata_counts = {}
        for node in self._grafo.nodes(data=True):
            duration = node[1]['duration']
            if duration not in durata_counts:
                durata_counts[duration] = 0
            durata_counts[duration] += 1

        # Stampa il numero di nodi per ciascuna durata
        print("Conteggio dei nodi per ciascuna durata:")
        for duration, count in sorted(durata_counts.items()):
            print(f"Durata: {duration} minuti - Nodi: {count}")

        # Calcola la durata media degli avvistamenti nel grafo
        if len(self._grafo.nodes) > 0:
            durata_media = sum(node[1]['duration'] for node in self._grafo.nodes(data=True)) / len(self._grafo.nodes)
            print(f"Durata media degli avvistamenti nel grafo: {durata_media:.2f} minuti")
        else:
            print("Non ci sono avvistamenti nel grafo.")

##########################################
# nuovo analizza grafo da mettere nel model:
def analizza_grafo(self):
        # Analizza il numero di nodi per ciascuna durata e la durata media
        durata_counts = {}
        for node in self._grafo.nodes(data=True):
            duration = node[1]['duration']
            if duration not in durata_counts:
                durata_counts[duration] = 0
            durata_counts[duration] += 1

        # Calcola la durata media degli avvistamenti
        durata_media = sum(node[1]['duration'] for node in self._grafo.nodes(data=True)) / len(self._grafo.nodes) if len(self._grafo.nodes) > 0 else 0

        # Restituisce i dati di analisi in un dizionario
        return {
            "durata_counts": durata_counts,
            "durata_media": durata_media
        }

# aggiungendo questo nell' handle_graph del controller ti vai ad accedere al dizionario creato nel model con l'analisi
    
        risultati_analisi = self._model.analizza_grafo()
        durata_counts = risultati_analisi["durata_counts"]
        durata_media = risultati_analisi["durata_media"]
