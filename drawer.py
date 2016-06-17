__author__ = 'tommaso'

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import os


def main():
    # For each file
    #   For each column
    #       do Heatmap
    #       do Contour

    for csv in [f for f in os.listdir('./') if f.endswith("csv")]:

        print("Reading " + csv)

        df = pd.read_csv(csv, header=0, decimal='.')

        csv = csv.split('.')[0]         # Keep only filename
        # data columns are lowercase
        for col in [c for c in df.columns.tolist() if c[0].islower()]:
                dataheat = [go.Heatmap(x=df['Colonna'],
                                       y=df['Riga'],
                                       z=df[col].tolist(),
                                       reversescale=True)]
                datacont = [go.Contour(x=df['Colonna'],
                                       y=df['Riga'],
                                       z=df[col].tolist(),
                                       reversescale=True)]

                title = csv + '-' + col
                py.image.save_as(go.Figure(data=dataheat, layout=go.Layout(title=title)),
                                 'images/' + title + '-heatmap.png')

                py.image.save_as(go.Figure(data=datacont, layout=go.Layout(title=title)),
                                 'images/' + title + '-contour.png')

                print("   Done!")

if __name__ == "__main__":
    main()
