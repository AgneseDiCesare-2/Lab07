import copy
from datetime import date

from model.situazione import Situazione


class Model:
    def __init__(self):
        self._soluzione={} #costo: soluzione
                            #float: lista di Soluzione

    def get_avg_umidita(self, mese):
        from database.meteo_dao import MeteoDao
        avg=MeteoDao().get_avg_umidita(mese) #dizionario
        return avg

    def leggi_umidita(self, citta, giorno) -> int: #restituisce il costo parziale
        from database.meteo_dao import MeteoDao
        umidita = MeteoDao().get_umidita_giorno(citta, giorno) #restituisce un valore numerico
        if umidita is None:
             return False
        return umidita

    def calcola_sequenza(self, mese):
        self._soluzione = {}
        self._ricorsione([], ["Milano", "Torino", "Genova"], mese, 0)
        if not self._soluzione:
            return None, []

        prima_chiave = min(self._soluzione.keys())
        primo_valore = self._soluzione[prima_chiave]
        return prima_chiave, primo_valore #restituisce costo_min : sequenza associata

    def controlla_tregiorni(self, parziale: list, i):
        l =len(parziale)
        if l == 0: #sto aggiungendo la prima città --> sempre bene
            return True

        elif parziale[-1].Localita == i:  # resto nella stessa città
            return True

        elif l<3:
            return False #non può ancora cambiare città

        else:  # cambio città: la precedente deve essere stata fatta per 3 giorni consecutivi
            ultimo = parziale[-1].Localita
            if parziale[-2].Localita == ultimo and parziale[-3].Localita == ultimo:
                return True

            return False

    @staticmethod
    def controlla_seigiorni(parziale:list, i:str):
        contatore=0
        for citta in parziale:
            if citta.Localita==i:
                contatore+=1
        if contatore>=6:
            return False
        return True

    def calcola_costo_giorno(self, parziale, nuova_citta, umidita):
        if len(parziale) == 0:
            return umidita

        ultima_citta = parziale[-1].Localita

        if ultima_citta == nuova_citta:
            return umidita

        return umidita + 100

    #parziale è la soluzione parziale, resto sono le città che non sono ancora state analizzate dal tecnico
    def _ricorsione(self, parziale, resto, mese, costo_parziale):
        if len(parziale) == 15: #tutte le città sono state analizzate
            self._soluzione[costo_parziale] = copy.deepcopy(parziale)
            return

        else:
            for i in resto: #i è la città
                #2. controllo
                ok_tre_giorni = self.controlla_tregiorni(parziale, i) #imposta self._x
                if ok_tre_giorni and self.controlla_seigiorni(parziale, i):
                    giorno = date(2013, mese, len(parziale)+1)

                    umidita = self.leggi_umidita(i, giorno)  # aggiorna self._umidita
                    nuova_soluzione=Situazione(i, giorno, umidita)
                    costo_giornaliero=self.calcola_costo_giorno(parziale, i, umidita)
                    # 1. aggiungo parziale
                    parziale.append(nuova_soluzione)

                    #costo_giornaliero = self.calcola_costo_giorno(self._umidita, self._x)
                    self._ricorsione(parziale, resto, mese, int(costo_parziale)+ int(costo_giornaliero))

                    parziale.pop()




