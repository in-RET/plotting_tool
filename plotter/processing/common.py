import pandas as pd


def buildLabel(text):
    replaceList = [["_HS", ""], ["_", " "],["WP", "Wärmepumpe"], ["GT", "Gasturbine"], ["oe", "ö"], ["ae", "ä"], ["ue", "ü"], ["HD", " Hochdruck"], ["ND", " Niederdruck"], ["DT", "Dampfturbine"]]

    for replacePair in replaceList:
        text = text.replace(replacePair[0], replacePair[1])

    return text


def readCsvData(filename):
    csv_data = pd.read_csv(filename, header=0, sep=",", index_col=0, decimal=".")
    dataframe = pd.DataFrame(csv_data)

    status_cols = []

    for column_head in dataframe.columns:
        #print(column_head)
        if str.find(column_head, "status") > 0:
            status_cols.append(column_head)

    print(status_cols)

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
        #print(column_head)
        tmp_float_list = []

        for rowValue in df[column_head]:
            tmp_float_list.append(float(rowValue))


        ret_data[column_head] = sum(tmp_float_list)

    return pd.Series(index=df.columns, data=ret_data)