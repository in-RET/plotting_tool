import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d

from plotter.processing.common import readCsvData, getDaylyAverageValues


def buildStackedPlot(ddir, pdir):
    filenames = os.listdir(ddir)

    for filename in filenames:
        csv_data = readCsvData(os.path.join(ddir, filename))
        data = pd.DataFrame(index=csv_data.index, data=csv_data)
        normed_data = getDaylyAverageValues(data)
        dauerlinie_data = data

        drop_columns = []

        for column in normed_data.columns:
            new_column_name = column.replace("(", "").replace(")", "").replace(", 'flow'", "").replace(", ", " > ").replace("'", "")

            if new_column_name.find(filename.replace(".csv", "")) == 0:
                normed_data[column] = gaussian_filter1d(-normed_data[column], sigma=2)
                drop_columns.append(new_column_name)
            else:
                normed_data[column] = gaussian_filter1d(normed_data[column], sigma=2)

            normed_data.rename(columns={column: new_column_name}, inplace=True)
            dauerlinie_data.rename(columns={column: new_column_name}, inplace=True)

        dauerlinie_data.drop(columns=drop_columns, inplace=True)

#######################################################################################################################
## Plot Area
#######################################################################################################################
        data2plot = normed_data

        fig = plt.figure()
        data2plot.plot(fig=fig,
                       kind='area',
                       stacked=True,
                       figsize=(19.1, 10.5),
                       grid=True,
                       xlabel="Datum",
                       ylabel="MW"
                       )

        plt.legend(loc='center left',
                   bbox_to_anchor=(1, 0.5),
                   ncol=1,
                   fontsize=7)
        plt.title(filename.replace(".csv", ""))
        plt.tight_layout()
        plt.xticks(rotation=30)
        plt.savefig(fname=os.path.join(pdir, filename.replace(".csv", "_stacked.png")),
                    dpi=None,
                    facecolor='w',
                    edgecolor='w',
                    orientation='portrait',
                    format=None,
                    transparent=False,
                    bbox_inches=None,
                    pad_inches=0.1,
                    metadata=None)

#######################################################################################################################
## Line Plot
#######################################################################################################################

        fig = plt.figure()
        data2plot.plot(fig=fig,
                       kind='line',
                       figsize=(19.1, 10.5),
                       grid=True,
                       xlabel="Datum",
                       ylabel="MW"
                       )

        plt.legend(loc='center left',
                   bbox_to_anchor=(1, 0.5),
                   ncol=1,
                   fontsize=7)
        plt.title(filename.replace(".csv", ""))
        plt.tight_layout()
        plt.xticks(rotation=30)
        plt.savefig(fname=os.path.join(pdir, filename.replace(".csv", "_line.png")),
                    dpi=None,
                    facecolor='w',
                    edgecolor='w',
                    orientation='portrait',
                    format=None,
                    transparent=False,
                    bbox_inches=None,
                    pad_inches=0.1,
                    metadata=None)

#######################################################################################################################
## Jahresdauerlinien
#######################################################################################################################

        fig, ax = plt.subplots(figsize=(19.1, 10.5))

        for column in dauerlinie_data:
            jahresdauerlinie = sorted(data[column], reverse=True)

            plt.plot(
                np.linspace(1,8760, 8760),
                jahresdauerlinie,
                label=column,
                drawstyle="steps-post"
            )
        plt.legend(loc='center left',
                   bbox_to_anchor=(1, 0.5),
                   ncol=1,
                   fontsize=7)
        plt.grid(True)
        plt.xlabel("kumulierte Zeit in h")
        plt.ylabel("MW")
        plt.title("Jahresdauerlinie:" + filename.replace(".csv", ""))
        plt.tight_layout()
        plt.xticks(rotation=30)

        plt.savefig(fname=os.path.join(pdir, filename.replace(".csv", "") + "_jahresdauerlinie.png"),
                    dpi=None,
                    facecolor='w',
                    edgecolor='w',
                    orientation='portrait',
                    format=None,
                    transparent=False,
                    bbox_inches=None,
                    pad_inches=0.1,
                    metadata=None)
        plt.close('all')

