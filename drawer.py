__author__ = 'tommaso'

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import pandas as pd
import numpy as np
from plotly.tools import FigureFactory as FF

plotly.tools.set_credentials_file(username='totomz', api_key='uk5clj1ogp')

def testCsv():
    # Import data from csv

    # For each dataset (file)
    df = pd.read_csv('medie.csv', header=0, decimal='.')

    # For each file
    #   For each column
    #       do Heatmap
    #       do Contour
    col = [c for c in df.columns.tolist() if c[0].islower() ]

    # PEr ogni file
        # Per ogni colonna
            # Faccio heatmap e contour che si chiamano file - colonna


    print(df)
    print("**********************")
    print(df.values)
    print("---")
    print(df.size)
    print("**********************")

#    data = [go.Heatmap(x=df['Colonna'],
#                       y=df['Riga'],
#                       z=df['distance_kpOU'].tolist(),
#                       reversescale=True)]
    data = [go.Contour(x=df['Colonna'],
                       y=df['Riga'],
                       z=df['distance_kpOU'].tolist(),
                       reversescale=True)]

    layout = go.Layout(title='distance_kpOU')

    fig = go.Figure(data=data,layout=layout)


    # Save the figure as a png image:
    py.image.save_as(fig, 'mssy_plot.png')

    print("Immagine salvata")


def createHeatmap(file, column):
    data = [
        go.Heatmap(
            z=[[1, 20, 30],
               [20, 1, 60],
               [30, 60, 1]]
        )
    ]
    plot(data, filename='basic-heatmap')

def main():
    testCsv()

if __name__ == "__main__":
    main()
