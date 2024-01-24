import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d

from plotter.processing.common import readCsvData, getDaylyAverageValues, reduceNodeName


def buildStackedPlot(ddir, pdir):
    filenames = os.listdir(ddir)

    os.makedirs(os.path.join(pdir, "Jahresganglinien"), exist_ok=True)
    os.makedirs(os.path.join(pdir, "Area Plots"), exist_ok=True)
    os.makedirs(os.path.join(pdir, "Stacked Plots"), exist_ok=True)

    for filename in filenames:
        print(filename)

        dataCSV = readCsvData(os.path.join(ddir, filename))
        data = pd.DataFrame(index=dataCSV.index, data=dataCSV)
        dataSimplified = pd.DataFrame()
        dataSimplifiedNodes = ["AHK_1", "AHK_1_Biogas", "AHK_1_H2", "AHK_2", "AHK_2_Biogas", "AHK_2_H2", "AHK_3", "HWE_5_1", "Wärmepumpen"]

        drop_columns = []

        # rename columns
        for column in data.columns:
            cleanedColumnName = column.replace("(", "").replace(")", "").replace(", 'flow'", "").replace("'", "")

            # Ist der Bus Eingang oder Ausgang?
            if cleanedColumnName.find(filename.replace(".csv", "")) == 0:
                # Wenn er Ausgang ist, wird der Wert negiert
                data[column] = gaussian_filter1d(-data[column], sigma=2)
            else:
                data[column] = gaussian_filter1d(data[column], sigma=2)

            data.rename(columns={column: cleanedColumnName}, inplace=True)

        # simplify data
        for column in data.columns:
            cleanedColumnName = column.replace("(", "").replace(")", "").replace(", 'flow'", "").replace("'", "")

            inputNode, outputNode = cleanedColumnName.split(", ")

            reducedInputNode = reduceNodeName(inputNode)
            reducedOutputNode = reduceNodeName(outputNode)

            # Erstmal alle Tabellen suchen und Addieren --> in neuen DF
            if reducedInputNode in dataSimplifiedNodes:
                reducedColumn = (reducedInputNode, outputNode)
            elif reducedOutputNode in dataSimplifiedNodes:
                reducedColumn = (inputNode, reducedOutputNode)
            else:
                reducedColumn = (inputNode, outputNode)

            if reducedColumn in dataSimplified.columns:
                dataSimplified[reducedColumn] += data[column]
            else:
                dataSimplified[reducedColumn] = data[column]

#######################################################################################################################
## Plot Area
#######################################################################################################################
        data2plot = getDaylyAverageValues(dataSimplified)

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
        plt.savefig(fname=os.path.join(pdir, "Area Plots", filename.replace(".csv", "_stacked.png")),
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
        plt.savefig(fname=os.path.join(pdir, "Stacked Plots", filename.replace(".csv", "_line.png")),
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

        for column in dataSimplified:
            plt.plot(
                np.linspace(1, 8760, 8760),
                sorted(dataSimplified[column].abs(), reverse=True),
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
        plt.title("Jahresdauerlinie: " + filename.replace(".csv", ""))
        plt.tight_layout()
        plt.xticks(rotation=30)

        plt.savefig(fname=os.path.join(pdir, "Jahresganglinien", filename.replace(".csv", "") + "_jahresdauerlinie.png"),
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

