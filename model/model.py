import copy
from datetime import date


class Model:
    def __init__(self):
        self._soluzione={} #costo: soluzione
                            #float: list()
        self._x=None #valore booleano che dice se nel costo devo considerare 100 oppure no
        self._umidita=0

    def get_avg_umidita(self, mese):
        from database.meteo_dao import MeteoDao
        avg=MeteoDao().get_avg_umidita(mese) #dizionario
        return avg

    def leggi_umidita(self, citta, giorno):
        from database.meteo_dao import MeteoDao
        situazioni=MeteoDao().leggi_umidita(citta) #lista di Situazioni
        trovato=False
        for situazione in situazioni:
            if situazione.Data==giorno:
                self._umidita=situazione.Umidita
                trovato=True
                break

        if not trovato:
            print("errore, valore non trovato!")

    def calcola_sequenza(self, mese):
        self._ricorsione([], ["Milano", "Torino", "Genova"], mese)
        if not self._soluzione:
            return None, []
        prima_chiave = max(self._soluzione.keys())
        primo_valore = self._soluzione[prima_chiave]
        return prima_chiave, primo_valore

    def controlla_tregiorni(self, parziale: list, i: str):
        l=len(parziale)
        if l<=3:
            self._x=1
            return True

        elif parziale[-1]==i: #non sto cambiando città
            self._x=0 #non considero 100$
            return True
        #sto cambiando città --> devo controllare che quella di prima compaia tra volte di seguito
        else:
            ultimo = parziale[-1]
            if parziale[-2]==ultimo and parziale[-3]==i:
                self._x = 1  # considero i 100$
                return True
            return False

    @staticmethod
    def controlla_seigiorni(parziale:list, i:str):
        contatore=0
        for citta in parziale:
            if citta==i:
                contatore+=1
        if contatore>=6:
            return False
        return True

    def calcola_costo_giorno(self, umidita: float, x):
        #come x gli passo self._x : 0,1
        return umidita + 100*x

    #parziale è la soluzione parziale, resto sono le città che non sono ancora state analizzate dal tecnico
    def _ricorsione(self, parziale, resto, mese):
        costo_soluzione=0
        if (len(parziale) == 15): #tutte le città sono state analizzate
            self._soluzione[costo_soluzione]=parziale #dizionario
            return

        else:
            for i in (resto):
                if self.controlla_tregiorni(parziale, i) and self.controlla_seigiorni(parziale, i):
                    #imposta self._x
                    parziale.append(i)
                    giorno = date(2013, mese, len(parziale))
                    self.leggi_umidita(i, giorno)
                    costo_soluzione+=self.calcola_costo_giorno(self._umidita, self._x)
                    self._ricorsione(parziale, resto, mese)

                    parziale.pop()




