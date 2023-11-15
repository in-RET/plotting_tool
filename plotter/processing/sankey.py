import os
import random

import pandas as pd
import plotly.graph_objects as go
from PIL import ImageColor

from plotter.processing.common import (buildLabel, readCsvData,
                                       sumSingleColumnsFromData)


def buildDataFrame(singleData, nodes, df):
    for index in singleData.index:
        tmp_str = index

        tmp_str = tmp_str.replace("(", "").replace(")", "").replace(" ", "").replace("'", "")
        tmp_str = tmp_str.split(",")

        if len(tmp_str) < 2:
            tmp_str.append("None")

        if not nodes.__contains__(tmp_str[0]):
            nodes.append(tmp_str[0])

        if not nodes.__contains__(tmp_str[1]):
            nodes.append(tmp_str[1])

        data2append = {
            'input': [nodes.index(tmp_str[0])],
            'output': [nodes.index(tmp_str[1])],
            'value': [singleData[0].loc[index]],
            'label': [tmp_str[0] + " -> " + tmp_str[1]],
            'color': [tmp_str[0]]
        }

        concat_df = pd.DataFrame(data2append)
        df = pd.concat([df, concat_df], ignore_index=True)

    return df, nodes


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

    dataframe, nodelist = buildDataFrame(data, nodelist, dataframe)

    fig = go.Figure(
        data=[go.Sankey(
            valueformat=".0f",
            valuesuffix=" MW",
            # Define nodes
            node=dict(
                pad=15,
                thickness=10,
                line=dict(width=0.5),
                label=nodelist,
                #color=nodeColors
            ),
            # Add links
            link=dict(
                source=dataframe['input'],
                target=dataframe['output'],
                value=dataframe['value'],
                label=dataframe['label'],
                # color=dataframe['color']
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