__author__ = 'tommaso'

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import pandas as pd
import numpy as np
from plotly.tools import FigureFactory as FF
import glob
import os



plotly.tools.set_credentials_file(username='totomz', api_key='uk5clj1ogp')

def testCsv():

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
                                 title + '-heatmap.png')

                py.image.save_as(go.Figure(data=datacont, layout=go.Layout(title=title)),
                                 title + '-contour.png')

                print("   Done!")

def main():
    testCsv()

if __name__ == "__main__":
    main()
