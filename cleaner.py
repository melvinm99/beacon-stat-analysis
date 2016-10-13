__author__ = 'melvin'
import os
import pandas as pd
from scipy import stats
import numpy
import plotly.plotly as py
import plotly.graph_objs as go

beaconIDs = "cQsW", "94gJ","Cvj5","cGTg", "At5a", "kpOU"
data = "data_raw.csv"
outputFile = "result.csv"
defaultValue=-1000.0
py.sign_in('melvinm', '97fltrwjnm')

def main( method, method_value, additional, additional_value , sideLen):
    distanze = dict()
    statistica = dict()

    #leggo valori grezzi
    for csv in [f for f in os.listdir('./') if f.endswith("csv") and f == data]:
        df = pd.read_csv(csv, header=0, decimal='.')
        header = df.columns.values
        for row in df.itertuples():
            nomeCella=row[1]
            for i in range(2, len(row)):
                if i % 2 != 0 and row[i] != defaultValue : #statistiche solo su distance
                    beaconID = (header[i-1][9:])
                    if (nomeCella,beaconID) in distanze:
                        distanze[nomeCella, beaconID].append(row[i])
                    else:
                        distanze[nomeCella,beaconID] = [ row[i] ]

    print distanze
    #calcolo statistiche

    if method == "percentile":
        percentili = dict.fromkeys(distanze.keys())
        for key in distanze:
            percentili[key] = stats.scoreatpercentile(distanze[key], method_value)
        for row in df.itertuples():  # itera per tuple il csv
                for i in range(1, len(row)):  # itera su ogni tupla cercando valori di default da rimpiazzare (es. -1000)
                    if i % 2 != 0 and row[i] == defaultValue and header[i-1][9:]!="kpOU":   #statistiche solo su distance
                        df.ix[row[0], i - 1] = percentili[row[1],(header[i-1][9:])]
        #print percentili
        statistica = percentili


    elif method == "truncated_mean":
        truncatedMeans = dict.fromkeys(distanze.keys())
        for key in distanze:
            truncatedMeans[key] = stats.trim_mean(distanze[key], method_value)
        for row in df.itertuples():  # itera per tuple il csv
            for i in range(2, len(row)):  # itera su ogni tupla cercando valori di default da rimpiazzare (es. -1000)
                if i % 2 != 0 and row[i] == defaultValue and header[i-1][9:]!="kpOU":
                    df.ix[row[0], i - 1] = truncatedMeans[row[1],(header[i-1][9:])]
        #print truncatedMeans
        statistica = truncatedMeans


    elif method == "simple_mean":
        simpleMeans = dict.fromkeys(distanze.keys())
        for key in distanze:
            simpleMeans[key] = numpy.mean(distanze)
        for row in df.itertuples():  # itera per tuple il csv
            for i in range(1, len(row)):   # itera su ogni tupla cercando valori di default da rimpiazzare (es. -1000)
                if i % 2 != 0 and row[i] == defaultValue:
                    df.ix[row[0], i - 1] = simpleMeans[i]
        #print simpleMeans
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
        for row in df.itertuples():  # itera per tuple il csv
            for i in range(2, len(row)):  # itera su ogni tupla cercando gli 0, i= indice colonna
                if i % 2 != 0 and header[i-1][9:]!="kpOU":
                    if row[i] < percentiliDOWN[row[1],(header[i-1][9:])] or row[i] > percentiliUP[row[1],(header[i-1][9:])] :
                        #print row[i], percentiliDOWN[i], row[i], percentiliUP[i], additional_value
                        df.ix[row[0], i - 1] = statistica[row[1],(header[i-1][9:])]
                        count += 1
    else:
        print "additional not supported yet, skipped"


    if(additional_value != ""):
        print str(count) + " values replaced with " + method + " statistics"


    #adding Row/Column coordinates for each cell
    df["riga"] = 0
    df["colonna"] = 0
    header = df.columns.values   #reload header
    indexRowColumn = len(header)-1
    lastCell=""
    lastRow = 1
    lastCol = 0
    for row in df.itertuples():  # itera per tuple il csv
        if  row[indexRowColumn] == 0 and row[1] != lastCell:
            lastCell = row[1]
            lastCol += 1
            if lastCol > sideLen:
                lastCol = 1
                lastRow += 1
        df.ix[row[0], "riga"] = lastRow  # row
        df.ix[row[0], "colonna"] = lastCol  # column

    # saving to file
    df.to_csv(outputFile, encoding='utf-8')

    #drawing
    for col in df.columns.tolist():
        if col != "cella" and col != "colonna" and col != "riga" and not "rssi" in col:

            # heatmap for each sensor
            dataheat = [go.Heatmap( x=df['riga'],
                                    y=df['colonna'],
                                    z=df[col].tolist(),
                                        reversescale=True)]
            layout = go.Layout(title=method + "_" + col, width=800, height=640)
            fig = go.Figure(data=dataheat, layout=layout)
            py.image.save_as(fig, filename = "new_images/" + method + str(method_value) + "-" + additional + str(additional_value) + "_" + col + "-heatmap.png")

            #contour
            # dataheat = [go.Contour(x=df['riga'],
            #                        y=df['colonna'],
            #                        z=df[col].tolist(),
            #                        reversescale=False)]
            # layout = go.Layout(title=method + "_" + col, width=800, height=640)
            # fig = go.Figure(data=dataheat, layout=layout)
            # py.image.save_as(fig, filename="new_images/" + method + "_" + col + "-contour.png")


    #py.plot(dataheat, filename='labelled-heatmap.png')   online!
    print("   Done!")


if __name__ == "__main__":
        main("truncated_mean", 0.3, "replace", 20, 3)

#EXAMPLES
#percentile 80
#truncated_mean 0.2
#simple_mean
#-ADDITIONAL- replace 20 -> rimpiazza  10% sopra e 10% sotto con la statistica (gia specificata)
#len of a side


#97fltrwjnm