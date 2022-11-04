import pandas as pd


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