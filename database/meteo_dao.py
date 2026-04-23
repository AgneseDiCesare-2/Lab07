from database.DB_connect import DBConnect
from model.situazione import Situazione

class MeteoDao:

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_avg_umidita(mese):
        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT Localita, AVG(Umidita) as Media
                        FROM meteo.situazione
                        where month(`Data`)=%s
                        group by Localita"""
            cursor.execute(query, (mese, ) ) #il risultato è univoco
            #posso salvare il risultato in {Città: umidità}

            for row in cursor:
                result[row["Localita"]]= row["Media"]

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_umidita_giorno(citta, giorno):
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita")
            return None

        umidita = None
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT Umidita
                       FROM meteo.situazione
                       WHERE Localita = %s AND Data = %s"""
        cursor.execute(query, (citta, giorno))
        row = cursor.fetchone()
        if row is not None:
            umidita = row["Umidita"]

        cursor.close()
        cnx.close()
        return umidita


