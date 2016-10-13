__author__ = 'melvin'
import os
import pandas as pd
from scipy import stats
import numpy
import plotly.plotly as py
import plotly.graph_objs as go

beaconIDs = "cQsW", "94gJ","Cvj5","cGTg", "At5a", "kpOU"
data = "9ottobre.csv"
outputFile = "result.csv"
defaultValue=-1000.0
py.sign_in('melvinm', '97fltrwjnm')



def main():
    rssis = dict()

    #leggo valori grezzi
    for csv in [f for f in os.listdir('./') if f.endswith("csv") and f == data]:
        df = pd.read_csv(csv, header=0, decimal='.')
        header = df.columns.values
        for row in df.itertuples():
            nomeCella=row[1]
            for i in range(2, len(row)):
                if row[i] != defaultValue : #statistiche solo su rssi
                    beaconID = (header[i-1][5:])
                    if (nomeCella,beaconID) in rssis:
                        rssis[nomeCella, beaconID].append(row[i])
                    else:
                        rssis[nomeCella,beaconID] = [ row[i] ]

    #print rssis

    # adding Row/Column coordinates for each cell
    df["riga"] = 0
    df["colonna"] = 0
    header = df.columns.values  # reload header
    indexRowColumn = len(header) - 1
    lastCell = ""
    lastRow = 1
    lastCol = 0
    for row in df.itertuples():  # itera per tuple il csv
        if row[indexRowColumn] == 0 and row[1] != lastCell:
            if lastCell != "":
                print str(lastCell) + "="  + str(lastRow) +  ","  + str(lastCol)
            lastCell = row[1]
            lastCol += 1
            if lastCol > 4:
                lastCol = 1
                lastRow += 1
        df.ix[row[0], "riga"] = lastRow  # row
        df.ix[row[0], "colonna"] = lastCol  # column
    print "8=" +  str(lastRow) + ","  + str(lastCol)    #patch lol
    # saving to file
    df.to_csv(outputFile, encoding='utf-8')

    # drawing
    for col in df.columns.tolist():
        if col != "cella" and col != "colonna" and col != "riga" :
            # heatmap for each sensor
            values = df[col].tolist()
            dataheat = [go.Heatmap(x=df['riga'],
                                   y=df['colonna'],
                                   z=values,
                                   reversescale=True,
                                   #outlinecolor="#2fab4a",
                                   #bordercolor="#2fab4a"
                                   colorscale=[[min(values), 'rgb(0,0,255)', [max(values), 'rgb(255,0,0)']] ]
                                   )]
            layout = go.Layout(title= col, width=800, height=640)
            fig = go.Figure(data=dataheat, layout=layout)
            py.image.save_as(fig, filename="2_ottobre/" + col + "heatmap.png")

            # contour
            # dataheat = [go.Contour(x=df['riga'],
            #                        y=df['colonna'],
            #                        z=df[col].tolist(),
            #                        reversescale=False)]
            # layout = go.Layout(title=method + "_" + col, width=800, height=640)
            # fig = go.Figure(data=dataheat, layout=layout)
            # py.image.save_as(fig, filename="new_images/" + method + "_" + col + "-contour.png")

    # py.plot(dataheat, filename='labelled-heatmap.png')   online!
    print("Done!")


if __name__ == "__main__":
    main()