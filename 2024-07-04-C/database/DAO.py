from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


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
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

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
    def get_all_sightings(anno, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    where year(s.`datetime`) = %s
                    and s.shape = %s"""
            cursor.execute(query, (anno, shape,))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    # Arco: tra 2 sighting che sono avvenuti nello stesso STATO
    #
    # Peso: differenza delle due longitudini
    @staticmethod
    def getAllEdges(anno, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id as id1, s1.Longitude as long1, s2.id as id2, s2.Longitude as long2
                        from sighting s1, sighting s2 
                        where year (s1.`datetime`)  = %s
                        and year (s2.`datetime`)  = %s
                        and s1.shape = %s
                        and s2.shape = %s
                        and s2.state = s1.state
                        and s1.id <> s2.id"""
            cursor.execute(query, (anno, anno, shape, shape, ))

            for row in cursor:
                result.append((row["id1"], row["long1"], row["id2"], row["long2"]))
            cursor.close()
            cnx.close()
        return result
