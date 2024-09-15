from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year (`datetime`) as anno
                                    from sighting s
                                    order by anno desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShapes(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape
                                    from sighting s
                                    where s.shape <> ""
                                    and year (s.`datetime`)  = %s
                                    order by s.shape asc"""
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row["shape"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllStates():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query,)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllweightedEdges(anno, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select n.state1 as stato1, n.state2 as stato2, count(*) as peso
                    from neighbor n, sighting s 
                    where (n.state1 = s.state or n.state2 = s.state)
                    and year(s.`datetime`) = %s
                    and s.shape = %s
                    group by n.state1, n.state2 """
            cursor.execute(query,(anno, shape,))

            for row in cursor:
                result.append((row["stato1"], row["stato2"], row["peso"]))

            cursor.close()
            cnx.close()
        return result
