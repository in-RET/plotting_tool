import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage import gaussian_filter1d

from plotter.processing.common import readCsvData, getDaylyAverageValues


def buildStackedPlot(ddir, pdir):
    filenames = os.listdir(ddir)

    for filename in filenames:
        csv_data = readCsvData(os.path.join(ddir, filename))
        data = pd.DataFrame(index=csv_data.index, data=csv_data)
        normed_data = getDaylyAverageValues(data)

        for column in normed_data.columns:
            new_column_name = column.replace("(", "").replace(")", "").replace(", 'flow'", "").replace(", ", " > ").replace("'", "")

            if new_column_name.find(filename.replace(".csv", "")) == 0:
                normed_data[column] = gaussian_filter1d(-normed_data[column], sigma=2)
            else:
                normed_data[column] = gaussian_filter1d(normed_data[column], sigma=2)

            normed_data.rename(columns={column: new_column_name}, inplace=True)

        data2plot = normed_data

        fig = plt.figure()
        data2plot.plot(fig=fig,
                       kind='area',
                       stacked=True,
                       figsize=(12, 8),
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


        fig = plt.figure()
        data2plot.plot(fig=fig,
                       kind='line',
                       figsize=(12, 8),
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

        fig = plt.figure()
        #print(data2plot)
        #data2plot = data2plot.sort_values(by=1, ascending=False)

        data2plot.plot(fig=fig,
                       kind='line',
                       figsize=(12, 8),
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
        plt.savefig(fname=os.path.join(pdir, filename.replace(".csv", "_gangline.png")),
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

