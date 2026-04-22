from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        pass

    def get_avg_umidita(self, mese):
        avg=MeteoDao().get_avg_umidita(mese) #dizionario
        return avg



