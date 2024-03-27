import os

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns

from plotter.processing.common import (readCsvData,
                                       sumSingleColumnsFromData,
                                       reduceNodeName)


def buildSankeyDiagram(wdir, title, output=False):
    filenames = os.listdir(wdir)
    data = pd.DataFrame()

    for filename in filenames:
        csv_data = readCsvData(os.path.join(wdir, filename))
        csv_data = sumSingleColumnsFromData(csv_data)
        csv_df = pd.DataFrame(index=csv_data.index, data=csv_data)

        data = pd.concat([data, csv_df])

    dataframe = pd.DataFrame(columns=["input", "output", "value", "label", "color"])
    nodelist = []
    link_colors = {}
    node_colors = []

    palette = sns.color_palette("Spectral", 100).as_hex()

    i = 0
    for index in data.index:
        tmp_str = index.replace("(", "").replace(")", "").replace(" ", "").replace("'", "").split(",")

        if len(tmp_str) < 2:
            tmp_str.append("None")

        tmp_str[0] = reduceNodeName(tmp_str[0])
        tmp_str[1] = reduceNodeName(tmp_str[1])

        if not nodelist.__contains__(tmp_str[0]):
            color = str(palette[i])
            i += 1
            nodelist.append(tmp_str[0])
            link_colors[tmp_str[0]] = color
            node_colors.append(color)

        if not nodelist.__contains__(tmp_str[1]):
            color = str(palette[i])
            i += 1
            nodelist.append(tmp_str[1])
            link_colors[tmp_str[1]] = color
            node_colors.append(color)

        data2append = {
            'input': [nodelist.index(tmp_str[0])],
            'output': [nodelist.index(tmp_str[1])],
            'value': [data[0].loc[index]],
            'label': [tmp_str[0] + " -> " + tmp_str[1]],
            #'color': [link_colors[tmp_str[0]]]
        }

        concat_df = pd.DataFrame(data2append)
        dataframe = pd.concat([dataframe, concat_df], ignore_index=True)

    fig = go.Figure(
        data=[go.Sankey(
            valueformat=".0f",
            valuesuffix=" MWh",
            # Define nodes
            node=dict(
                pad=15,
                thickness=10,
                line=dict(width=0.5),
                label=nodelist,
                color=node_colors
            ),
            # Add links
            link=dict(
                source=dataframe['input'],
                target=dataframe['output'],
                value=dataframe['value'],
                label=dataframe['label'],
                #color=dataframe['color']
            )
        )]
    )

    fig.update_layout(
        title_text="<b>" + title + "</b><br>oemof-Simulation der Hochschule Nordhausen, Institut für Regenerative Energietechnik - in.RET",
        font_size=18
    )

    if output:
        fig.show()

    # return fig.to_image("png")
    return fig.to_html()