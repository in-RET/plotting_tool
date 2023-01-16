import os
import random

import pandas as pd
import plotly.graph_objects as go

from PIL import ImageColor


def buildLabel(text):
    replaceList = [["_HS", ""], ["_", " "],["WP", "Wärmepumpe"], ["GT", "Gasturbine"], ["oe", "ö"], ["ae", "ä"], ["ue", "ü"], ["HD", " Hochdruck"], ["ND", " Niederdruck"], ["DT", "Dampfturbine"]]

    for replacePair in replaceList:
        text = text.replace(replacePair[0], replacePair[1])

    return text


def readCsvData(filename):
    csv_data = pd.read_csv(filename, header=0, sep=",", index_col=0, decimal=",")
    return pd.DataFrame(csv_data)


def getDaylyAverageValues(df: pd.DataFrame) -> pd.DataFrame:
    n = 0
    m = 24

    avg_data = pd.DataFrame()

    while m < len(df.index.values):
        date = pd.to_datetime(df.index[n]).date()

        avg_data_row = pd.DataFrame.from_dict({date: df.iloc[n:m].sum() / 24}, orient="index")
        avg_data = pd.concat([avg_data, avg_data_row])

        m += 24
        n += 24

    return avg_data


def sumSingleColumnsFromData(dataframe) -> pd.Series:
    ret_data = {}
    for column_head in dataframe.columns:
        tmp_float_list = []

        for rowValue in dataframe[column_head]:
            tmp_float_list.append(rowValue)

        ret_data[column_head] = sum(tmp_float_list)

    return pd.Series(index=dataframe.columns, data=ret_data)


def optimizeNodelistCandidate(nodelist):
    if nodelist.__contains__("AHK_"):
        nodelist = nodelist[0:5]

    if nodelist.__contains__("ST_"):
        nodelist = nodelist[0:2]

    return nodelist


def buildDataFrame(singleData, nodes, df, kompakt):
    for index in singleData.index:
        tmp_str = index

        tmp_str = tmp_str.replace("(", "").replace(")", "").replace(" ", "").replace("'", "")
        tmp_str = tmp_str.split(",")

        if kompakt:
            tmp_str[0] = optimizeNodelistCandidate(tmp_str[0])
            tmp_str[1] = optimizeNodelistCandidate(tmp_str[1])

        tmp_str[0] = buildLabel(tmp_str[0])
        tmp_str[1] = buildLabel(tmp_str[1])

        if not nodes.__contains__(tmp_str[0]):
            nodes.append(tmp_str[0])

        if not nodes.__contains__(tmp_str[1]):
            nodes.append(tmp_str[1])

        data2append = {
            'input': [nodes.index(tmp_str[0])],
            'output': [nodes.index(tmp_str[1])],
            'value': [singleData[0].loc[index]],
            'label': [tmp_str[0] + " -> " + tmp_str[1]]
        }

        concat_df = pd.DataFrame(data2append)
        df = pd.concat([df, concat_df], ignore_index=True)

    return df, nodes


def buildSankeyDiagram(wdir, title, kompakt=True):
    filenames = os.listdir(wdir)

    data = pd.DataFrame()

    for filename in filenames:
        if filename.__contains__("sequences"):
            #print(filename)

            csv_data = readCsvData(os.path.join(wdir, filename))
            csv_data = sumSingleColumnsFromData(csv_data)
            csv_df = pd.DataFrame(index=csv_data.index, data=csv_data)

            data = pd.concat([data, csv_df])

    dataframe = pd.DataFrame(columns=["input", "output", "value", "label"])
    nodelist = []

    dataframe, nodelist = buildDataFrame(data, nodelist, dataframe, kompakt)

    fig = go.Figure(
        data=[go.Sankey(
            valueformat=".0f",
            valuesuffix=" MW",
            # Define nodes
            node=dict(
                pad=15,
                thickness=10,
                line=dict(width=0.5),
                label=nodelist
            ),
            # Add links
            link=dict(
                source=dataframe['input'],
                target=dataframe['output'],
                value=dataframe['value'],
                label=dataframe['label']
            )
        )]
    )

    fig.update_layout(
        title_text="<b>" + title + "</b><br>oemof-Simulation der Hochschule Nordhausen, Institut für Regenerative Energietechnik - in.RET",
        font_size=18
    )

    fig.show()
    return fig.to_html()

wpath = os.path.join(os.getcwd(), "auswertung")
spath = os.path.join(os.getcwd(), "plots")

datafolders = []

for (root, dirs, files) in os.walk(wpath, topdown=True):
    if len(dirs) == 0 and len(files) > 0:
        datafolders.append(root)

print(datafolders)

for ddir in datafolders:
    pdir = os.path.join(spath, os.path.relpath(ddir, wpath))

    print(ddir)
    print(pdir)

    if not os.path.exists(pdir):
        os.makedirs(pdir)

    picture = buildSankeyDiagram(ddir, "Energieflussdiagramm SWE")

    file = open(os.path.join(pdir, "energieflussdiagramm_" + os.path.basename(ddir) + ".html"), 'wt', encoding="utf-8")
    file.write(picture)
    file.close()


