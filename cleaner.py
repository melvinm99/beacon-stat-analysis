__author__ = 'melvin'
import os
import pandas as pd

medie = "medie.csv"
dati = "dati_raw.csv"
fileDiSalvataggio = "ciaone.csv"
offset = 50 #(valore inteso per la distance)

def main():
    #legge medie
    for csv in [f for f in os.listdir('./') if f==medie]:
        avs = pd.read_csv(csv, header=0, decimal='.')


    for csv in [f for f in os.listdir('./') if f.endswith("csv") and f==dati]:
        df = pd.read_csv(csv, header=0, decimal='.')
        df = df.drop("1",1) ; df = df.drop("Unnamed: 12",1); df = df.drop("Unnamed: 13",1)
        for row in df.itertuples():     #itera per tuple il csv
            for i in range(1,len(row)):   #itera su ogni tupla cercando gli 0, i= indice colonna
                    for index, riga in avs.iterrows():
                        if riga["Cella"] == row[1] and i>2: #salta colonna "cella" poiche letterale
                            if row[i] == 0.0 or row[i]==["nan"] or float(row[i]) - 50 > float(riga[i+1]) or float(row[i])+50 < float(riga[i]):
                            #print "cella:", row[1],"riga:", row[0],"colonna:",i,"valPre:" ,row[i], "valDop:", riga[i], row[i]
                                df.ix[row[0],i-1] = riga[i+1]


    print df
    df.to_csv(fileDiSalvataggio, encoding='utf-8')


if __name__ == "__main__":
        main()
