import os

import pandas as pd
import plotly.graph_objects as go

from plotter.processing.common import readCsvData, sumSingleColumnsFromData
from plotter.processing.sankey import buildDataFrame

def buildRadarPlot(wdir, title, kompakt=True, output=True):
    filenames = os.listdir(wdir)

    data = pd.DataFrame()

    for filename in filenames:
        if filename.__contains__("sequences"):
            csv_data = readCsvData(os.path.join(wdir, filename))
            csv_data = sumSingleColumnsFromData(csv_data)
            csv_df = pd.DataFrame(index=csv_data.index, data=csv_data)

            data = pd.concat([data, csv_df])

    dataframe = pd.DataFrame(columns=["input", "output", "value", "label", "color"])
    nodelist = []

    dataframe, nodelist = buildDataFrame(data, nodelist, dataframe, kompakt)

    link=dict(
            source=dataframe['input'],
            target=dataframe['output'],
            value=dataframe['value'],
            label=dataframe['label'],
        )

    import_list = []
    import_nodelist = []
    export_list = []
    export_nodelist = []

    position = 0
    for label in link["label"]:
        # wenn das Label bus nach dem > enthält .. ist es ein Import
        if label.find("bus") > label.find(">"):
            import_list.append(link["value"][position])
            import_nodelist.append(link["label"][position])
        # wenn nicht dann ein Export
        elif label.find("bus") < label.find(">"):
            export_list.append(link["value"][position])
            export_nodelist.append(link["label"][position])
        # sonst fehler
        else: print("Fehler!", position)
        position += 1

    print(import_list)
    print(import_nodelist)

    print(export_list)
    print(export_nodelist)

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r = import_list,
            theta = import_nodelist,
            fill = "toself",
            name="Inputs"            
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r = export_list,
            theta = export_nodelist,
            fill = "toself",
            name="Exports"            
        )
    )


    fig.update_layout(
        title_text="<b>" + title + "</b><br>oemof-Simulation der Hochschule Nordhausen, Institut für Regenerative Energietechnik - in.RET",
        font_size=18
    )

    if output:
        fig.show()

    # return fig.to_image("png")
    return fig.to_html()