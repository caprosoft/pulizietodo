import datetime
import json
import locale
locale.setlocale(locale.LC_TIME, "it_IT.UTF-8") # imposto la lingua dei giorni e dei mesi in italiano


def data_pulizie(anno, mese, giorno):
    # calcolo i giorni passati dalle ultime pulizie
    data_ultime_pulizie = datetime.datetime (anno, mese, giorno)
    data_attuale = datetime.datetime.now()
    diff_giorni = abs((data_attuale - data_ultime_pulizie).days) 

    # stampo i giorni passati dalle ultime pulizie
    print(" >> L'ultima volta che avete fatto le pulizie era", data_ultime_pulizie.strftime("%A %d %B"), "(", diff_giorni, "giorni fa )")


def prossimi_turni(turni, dim):       # scorro a sx di una pos lungo l'array dei turni
    for i in range (dim-1):           # faccio tanti scambi quanti dim -1 (ex. dim=4, j=0; 0<3 )
        temp = turni[0]               # prendo il valore del primo el. e lo metto in una var. temp
        turni[0] = turni[dim-1-i]     # assegno al primo valore il valore dell'ultimo (che scorrera' a sx nei prossimi cicli)
        turni[dim-1-i] = temp         # assegno all'ultimo valore il valore della var. temp (che era il val. del primo el.)
    return turni                      # ritorno i prossimi turni


def agg_prossimi_turni(turni, dim):
    prossimi_turni(turni, dim)                                  # richiamo la funzione per il calcolo dei prossimi turni
    with open('database.json', 'r+', encoding='utf-8') as f:
        dati = json.load(f)                                     # carico i dati già presenti nel .json
        dati["turni"] = turni                                   # modifico il file .json sovrascrivendo i turni prec. con quelli successivi
        f.seek(0)                                               # mi posiziono all' inizio del file ( 0 = inizio, 1 = corrente, 2 = fine )
        json.dump(dati, f, ensure_ascii=False, indent=4)        # inserisco i dati aggiornati


def stampa_turni(dim, turni, coinquilini):
    for i in range(dim):
        print(" - ", turni[i], "-->", coinquilini[i])


def main():
    # numero delle mansioni da dividere
    dim = 3

    # carico i valori salvati nel json in corrispettive var
    with open('database.json', 'r', encoding='utf-8') as f:
        dati = json.load(f)       
        
        turni = dati["turni"]
        coinquilini = dati["coinquilini"]
        
        anno = dati["data"][0]["anno"]
        mese = dati["data"][0]["mese"]
        giorno = dati["data"][0]["giorno"]


    # menù scelta funzioni del programma
    inp=""
    print("*** Benvenuto in PULIZIE TO-DO ! ***")
    print(
    """    
    1. Visualizza DATA ultime pulizie
    2. Visualizza turni ULTIME pulizie
    3. Visualizza turni PROSSIME pulizie
    4. AGGIUNGI pulizie in data odierna
    0. ESCI dal programma"""
    )
    while 1:
        
        inp = input("\n >> Inserire numero opzione desiderata: ")

        if inp=="1":
            data_pulizie(anno, mese, giorno)

        elif inp=="2":
            # stampo i turni salvati
            print(" >> Turni ULTIME pulizie:")
            stampa_turni(dim, turni, coinquilini)

        elif inp=="3":
            # stampo i prossimi turni
            prossimi_turni(turni, dim)
            print(" >> Turni PROSSIME pulizie:") 
            stampa_turni(dim, turni, coinquilini)
            # riporto i turni al valore originale
            with open('database.json', 'r', encoding='utf-8') as f:
                dati = json.load(f)       
                turni = dati["turni"]
            
        elif inp=="4":
            # aggiungo effettivamente i prossimi turni
            agg_prossimi_turni(turni, dim)
            # aggiungo data pulizie
            # TO-DO! implementare agg_data !!!
            print(" >> Aggiornate ultime pulizie a data odierna")
            

        elif inp=="0":
            # esco dal programma
            break

        else:
            print("Opzione non valida")
       

# eseguo il main
main()

