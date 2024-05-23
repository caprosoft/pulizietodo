import datetime
import json
import locale
locale.setlocale(locale.LC_TIME, "it_IT.UTF-8") # imposto la lingua dei giorni e dei mesi in italiano


def data_pulizie():
    # controllo la data presente nel database.json
    with open('database.json', 'r', encoding='utf-8') as f:
        dati = json.load(f)
        anno = dati["data"][0]["anno"]
        mese = dati["data"][0]["mese"]
        giorno = dati["data"][0]["giorno"]
    # calcolo i giorni passati dalle ultime pulizie
    data_ultime_pulizie = datetime.datetime (anno, mese, giorno)
    data_attuale = datetime.datetime.now()
    diff_giorni = abs((data_attuale - data_ultime_pulizie).days)
    # stampo i giorni passati dalle ultime pulizie
    print(" >> L'ultima volta che avete fatto le pulizie era", data_ultime_pulizie.strftime("%A %d %B"), "(", diff_giorni, "giorni fa )")


def agg_data_pulizie():
    data_attuale = datetime.datetime.now()
    with open('database.json', 'r+', encoding='utf-8') as f:
        dati = json.load(f)       
        dati["data"][0]["anno"] = data_attuale.year             # modifico il file .json sovrascrivendo la data delle pulizie con quella attuale
        dati["data"][0]["mese"] = data_attuale.month
        dati["data"][0]["giorno"] = data_attuale.day
        f.seek(0)                                               # mi posiziono all' inizio del file ( 0 = inizio, 1 = corrente, 2 = fine )
        json.dump(dati, f, ensure_ascii=False, indent=4)        # inserisco i dati aggiornati


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


def stampa_turni(turni, dim, coinquilini):
    for i in range(dim):
        print(" - ", turni[i], "-->", coinquilini[i])


def main():
    # numero delle mansioni da dividere
    dim = 3

    # carico turni e coinquilini salvati nel json in corrispettive var
    with open('database.json', 'r', encoding='utf-8') as f:
        dati = json.load(f)       
        turni = dati["turni"]
        coinquilini = dati["coinquilini"]

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
            data_pulizie()

        elif inp=="2":
            # stampo i turni salvati
            print(" >> Turni ULTIME pulizie:")
            stampa_turni(turni, dim, coinquilini)

        elif inp=="3":
            # stampo i prossimi turni
            prossimi_turni(turni, dim)
            print(" >> Turni PROSSIME pulizie:") 
            stampa_turni(turni, dim, coinquilini)
            # riporto i turni al valore originale
            with open('database.json', 'r', encoding='utf-8') as f:
                dati = json.load(f)       
                turni = dati["turni"]
            
        elif inp=="4":
            conferma = input(" >> Stai per SOVRASCRIVERE la data delle ultime PULIZIE con quella attuale\n >> Sei sicuro di voler procedere? [Si/No]")
            if conferma.upper() in ["S", "SI"]:
                # aggiungo effettivamente i prossimi turni
                agg_prossimi_turni(turni, dim)
                # aggiungo data pulizie
                agg_data_pulizie()
                print(" >> Pulizie AGGIUNTE in data odierna con successo.")
            elif conferma.upper() in ["N", "NO"]:
                print(" >> Operazione ANNULLATA.")
            else:
                print(" >> Operazione ANNULLATA.")

        elif inp=="0":
            # esco dal programma
            conferma = input(" >> Sei sicuro di voler USCIRE? [Si/No]")
            if conferma.upper() in ["S", "SI"]:
                break
            elif conferma.upper() in ["N", "NO"]:
                print("\n")
            else:
                print("\n")

        else:
            print(" >> Opzione NON valida, inserire: 1, 2, 3, 4 o 0\n")
       

# eseguo il main
main()

