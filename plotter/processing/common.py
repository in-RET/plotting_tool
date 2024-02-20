import pandas as pd


def buildLabel(text):
    replaceList = [["_HS", ""], ["_", " "],["WP", "Wärmepumpe"], ["GT", "Gasturbine"], ["oe", "ö"], ["ae", "ä"], ["ue", "ü"], ["HD", " Hochdruck"], ["ND", " Niederdruck"], ["DT", "Dampfturbine"]]

    for replacePair in replaceList:
        text = text.replace(replacePair[0], replacePair[1])

    return text


def readCsvData(filename):
    csv_data = pd.read_csv(filename, header=0, sep=";", index_col=0, decimal=",")
    dataframe = pd.DataFrame(csv_data)

    status_cols = []

    for column_head in dataframe.columns:
        if str.find(column_head, "status") > 0:
            status_cols.append(column_head)

    dataframe = dataframe.drop(columns=status_cols)

    return dataframe


def getDaylyAverageValues(df: pd.DataFrame) -> pd.DataFrame:
    n = 0
    m = 24

    avg_data = pd.DataFrame()

    while m < len(df.index.values):
        date = pd.to_datetime(df.index[n]).date()

        avg_data_row = pd.DataFrame.from_dict({date: df.iloc[n:m].sum() / 24}, orient="index")
        #avg_data_row = pd.DataFrame.from_dict({date: df.iloc[n:m].sum()}, orient="index")
        avg_data = pd.concat([avg_data, avg_data_row])

        m += 24
        n += 24

    return avg_data


def sumSingleColumnsFromData(df: pd.DataFrame) -> pd.Series:
    ret_data = {}
    for column_head in df.columns:
        ret_data[column_head] = df[column_head].sum()

    return pd.Series(index=df.columns, data=ret_data)


def reduceNodeName(node: str) -> str:
    reduceNodeName = node.replace("HWE_5_1_Nachheizung", "HWE_5_1").replace("HWE_5_1_Heißwasser", "HWE_5_1")
    reduceNodeName = reduceNodeName.replace("AHK_1_KB", "AHK_1").replace("AHK_1_FB", "AHK_1").replace("AHK_1_AB", "AHK_1")
    reduceNodeName = reduceNodeName.replace("AHK_2_KB", "AHK_2").replace("AHK_2_FB", "AHK_2").replace("AHK_2_AB", "AHK_2")
    reduceNodeName = reduceNodeName.replace("AHK_1_Biogas_KB", "AHK_1_Biogas").replace("AHK_1_Biogas_FB", "AHK_1_Biogas").replace("AHK_1_Biogas_AB", "AHK_1_Biogas")
    reduceNodeName = reduceNodeName.replace("AHK_2_Biogas_KB", "AHK_2_Biogas").replace("AHK_2_Biogas_FB", "AHK_2_Biogas").replace("AHK_2_Biogas_AB", "AHK_2_Biogas")
    reduceNodeName = reduceNodeName.replace("AHK_1_H2_KB", "AHK_1_H2").replace("AHK_1_H2_FB", "AHK_1_H2").replace("AHK_1_H2_AB", "AHK_1_H2")
    reduceNodeName = reduceNodeName.replace("AHK_2_H2_KB", "AHK_2_H2").replace("AHK_2_H2_FB", "AHK_2_H2").replace("AHK_2_H2_AB", "AHK_2_H2")
    reduceNodeName = reduceNodeName.replace("AHK_3_AB", "AHK_3")
    reduceNodeName = reduceNodeName.replace("DT-Tandem HD-Teil", "DT-Tandem").replace("DT-Tandem ND-Teil", "DT-Tandem")

    if reduceNodeName.startswith("WP_") and reduceNodeName not in ["WP_Luftwaerme_direkt", "WP_PVT "]:
        reduceNodeName = "Wärmepumpen"

    return reduceNodeName