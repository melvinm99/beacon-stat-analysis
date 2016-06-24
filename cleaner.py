__author__ = 'melvin'
import os
import pandas as pd
from scipy import stats
import numpy

dati = "dati_raw.csv"
fileDiSalvataggio = "result.csv"

def main( method, method_value, additional, additional_value ):
    distanze = dict()
    statistica = dict()

    #leggo valori grezzi
    for csv in [f for f in os.listdir('./') if f.endswith("csv") and f == dati]:
        df = pd.read_csv(csv, header=0, decimal='.')
        df = df.drop("1", 1);
        df = df.drop("Unnamed: 12", 1);
        df = df.drop("Unnamed: 13", 1)
        for row in df.itertuples():
            for i in range(2, len(row)):
                if i % 2 != 0 and row[i] != 0.0:
                    if not (i in distanze):
                        distanze[i]=[row[i]]
                    else:
                        distanze[i].append(row[i])
    #calcolo statistiche

    if method == "percentile":
        percentili = dict.fromkeys(distanze.keys())
        for key in distanze:
            percentili[key] = stats.scoreatpercentile(distanze[key], method_value)
        for row in df.itertuples():  # itera per tuple il csv
                for i in range(1, len(row)):  # itera su ogni tupla cercando gli 0, i= indice colonna
                    if i % 2 != 0 and row[i] == 0.0:
                        df.ix[row[0], i - 1] = percentili[i]
        print percentili
        statistica = percentili


    elif method == "truncated_mean":
        truncatedMeans = dict.fromkeys(distanze.keys())
        for key in distanze:
            truncatedMeans[key] = stats.trim_mean(distanze[key], method_value)
        for row in df.itertuples():  # itera per tuple il csv
            for i in range(1, len(row)):  # itera su ogni tupla cercando gli 0, i= indice colonna
                if i % 2 != 0 and row[i] == 0.0:
                    df.ix[row[0], i - 1] = truncatedMeans[i]
        print truncatedMeans
        statistica = truncatedMeans


    elif method == "simple_mean":
        simpleMeans = dict.fromkeys(distanze.keys())
        for key in distanze:
            simpleMeans[key] = numpy.mean(distanze)
        for row in df.itertuples():  # itera per tuple il csv
            for i in range(1, len(row)):  # itera su ogni tupla cercando gli 0, i= indice colonna
                if i % 2 != 0 and row[i] == 0.0:
                    df.ix[row[0], i - 1] = simpleMeans[i]
        print simpleMeans
        statistica = simpleMeans

    else:
        print "not supported yet!"
        return


                    # for index, riga in avs.iterrows():
                    #     if riga["Cella"] == row[1] and i>2: #salta colonna "cella" poiche letterale
                    #         if row[i] == 0.0 or row[i]==["nan"] or float(row[i]) - 50 > float(riga[i+1]) or float(row[i])+50 < float(riga[i]):
                    #         #print "cella:", row[1],"riga:", row[0],"colonna:",i,"valPre:" ,row[i], "valDop:", riga[i], row[i]
                    #             df.ix[row[0],i-1] = riga[i+1]
    if additional == "replace":
        count=0
        percentiliUP = dict.fromkeys(distanze.keys())
        for key in distanze:
            percentiliUP[key] = stats.scoreatpercentile(distanze[key], (100-additional_value/2) ) #percentile per ogni ID
        percentiliDOWN = dict.fromkeys(distanze.keys())
        for key in distanze:
            percentiliDOWN[key] = stats.scoreatpercentile(distanze[key], additional_value/2 ) #percentile per ogni ID
        print percentiliUP
        print percentiliDOWN
        for row in df.itertuples():  # itera per tuple il csv
            for i in range(2, len(row)):  # itera su ogni tupla cercando gli 0, i= indice colonna
                if i % 2 != 0 :
                    if row[i] < percentiliDOWN[i] or row[i] > percentiliUP[i]:
                        print row[i], percentiliDOWN[i], row[i], percentiliUP[i], additional_value
                        df.ix[row[0], i - 1] = statistica[i]
                        count += 1
    else:
        print "additional not supported yet, skipped"


    #print df
    if(additional_value != ""):
        print str(count) + " values replaced with " + method + " statistics"
    df.to_csv(fileDiSalvataggio, encoding='utf-8')


if __name__ == "__main__":
        main("truncated_mean", 0.2, "replace", 20)

#EXAMPLES
#percentile 80
#truncated_mean 0.2
#simple_mean
#--------ADDITIONAL---------#
#replace 20 -> rimpiazza  10% sopra e 10% sotto con la statistica (gia specificata)