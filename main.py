import datetime
import json
import locale
locale.setlocale(locale.LC_TIME, "it_IT.UTF-8") # imposto la lingua dei giorni e dei mesi in italiano


def prossimi_turni(turni, dim):       # scorro a sx di una pos lungo l'array dei turni
    for i in range (dim-1):           # faccio tanti scambi quanti dim -1 (ex. dim=4, j=0; 0<3 )
        temp = turni[0]               # prendo il valore del primo el. e lo metto in una var. temp
        turni[0] = turni[dim-1-i]     # assegno al primo valore il valore dell'ultimo (che scorrera' a sx nei prossimi cicli)
        turni[dim-1-i] = temp         # assegno all'ultimo valore il valore della var. temp (che era il val. del primo el.)
    return turni                      # ritorno i prossimi turni


def agg_prossimi_turni(turni):
    prossimi_turni(turni)                                       #richiamo la funzione per il calcolo dei prossimi turni
    with open('database.json', 'r+', encoding='utf-8') as f:
        dati = json.load(f)                                     # carico i dati già presenti nel .json
        dati.append(turni)                                      # aggiungo alla fine (appendo) i turni aggiornati
        f.seek(0)                                               # mi posiziono all' inizio del file ( 0 = inizio, 1 = corrente, 2 = fine )
        json.dump(dati, f, ensure_ascii=False, indent=4)        # inserisco i dati aggiornati


def main():

    # numero delle mansioni da dividere
    dim = 3

    # carico nella var turni i turni salvati nel db
    with open('database.json', 'r', encoding='utf-8') as f:
        dati = json.load(f) 
        turni = dati
    
    # calcolo i giorni passati dalle ultime pulizie
    data_ultime_pulizie = datetime.datetime (2024, 5, 9)
    data_attuale = datetime.datetime.now()
    diff_giorni = abs((data_attuale - data_ultime_pulizie).days) 

    # stampo i giorni passati dalle ultime pulizie
    print("L'ultima volta che avete fatto le pulizie era", data_ultime_pulizie.strftime("%A %d %B"), "(", diff_giorni, "giorni fa )")

    # stampo i turni salvati
    print("Con i seguenti turni:", turni)
  
    # stampo i prossimi turni
    print("Prossimi turni:", prossimi_turni(turni, dim)) 


# eseguo il main
main()

