import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.filters import gaussian_filter1d

from plotter.processing.common import readCsvData, getDaylyAverageValues


def PlotStacked(ddir, pdir, output=False):
    filenames = os.listdir(ddir)

    for filename in filenames:
        if filename.__contains__("sequences") and not filename.__contains__("Strombus"):
            csv_data = readCsvData(os.path.join(ddir, filename))
            csv_df = pd.DataFrame(index=csv_data.index, data=csv_data)

            data = csv_df
            normed_data = getDaylyAverageValues(data)

            bus_names = ["Strom_HS_Eigenerzeugung", "WP_Abwaerme_Netz", "Strom_HS_Eigenverbrauch", "Strom_HS",
                         "FünfundneunzigGradbus", "Nachheizhilfebus", "Ausspeicherbus", "Fernwaerme", "Direktleitungsbus"]

            for column in normed_data.columns:
                new_column_name = column.replace("(", "").replace(")", "").replace(", 'flow'", "").replace(", ", "").replace("'", "")

                done = False

                for bus_name in bus_names:
                    if new_column_name.find(bus_name) == 0 and not done:
                        normed_data[column] = -normed_data[column]
                        normed_data[column] = gaussian_filter1d(normed_data[column], sigma=2)

                        done = True

                    new_column_name = new_column_name.replace(bus_name, "")

                normed_data.rename(columns={column: new_column_name}, inplace=True)

            data2plot = normed_data

            if plt is not None:
                fig = plt.figure()
                data2plot.plot(fig=fig,
                               kind='area',
                               stacked=True,
                               sort_columns=True,
                               figsize=(12, 8),
                               grid=True,
                               xlabel="Datum",
                               ylabel="MW"
                               )

        elif filename.__contains__("Strombus"):
            # mach was
            csv_data = readCsvData(os.path.join(ddir, filename))
            csv_df = pd.DataFrame(index=csv_data.index, data=csv_data)

            data = csv_df
            normed_data = getDaylyAverageValues(data)

            for column in normed_data.columns:
                new_column_name = column.replace("(", "").replace(")", "").replace(", 'flow'", "").replace(", ","")\
                    .replace("'", "").replace("Strom_HS", "")

                normed_data.rename(columns={column: new_column_name}, inplace=True)

                normed_data[new_column_name] = gaussian_filter1d(normed_data[new_column_name], sigma=2)

            data2plot = normed_data[["Import_Strom", "Ueberschuss_HS", "Trafo_Kosten_vnne"]]

            if plt is not None:
                fig = plt.figure()
                ax = data2plot.plot(fig=fig,
                                    kind='area',
                                    stacked=True,
                                    sort_columns=True,
                                    figsize=(12, 8),
                                    grid=True,
                                    xlabel="Datum",
                                    ylabel="MW"
                                    )

                data2plot = normed_data["Last_Strom"]
                data2plot.plot(ax=ax)

        if filename.__contains__("sequences"):
            if plt is not None:
                plt.legend(loc='center left',
                           bbox_to_anchor=(1, 0.5),
                           ncol=1,
                           fontsize=7)
                plt.title(filename.replace("_sequences.csv", ""))
                plt.tight_layout()
                plt.xticks(rotation=30)
                plt.savefig(fname=os.path.join(pdir, filename.replace("_sequences.csv", "_stacked.png")),
                            dpi=None,
                            facecolor='w',
                            edgecolor='w',
                            orientation='portrait',
                            format=None,
                            transparent=False,
                            bbox_inches=None,
                            pad_inches=0.1,
                            metadata=None)

                if output:
                    plt.show()
