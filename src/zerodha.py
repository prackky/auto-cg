import pandas as pd
from utils import row_contains_columns


def standardize_zerodha(fp, fy: int):
    sheetname = f"Tradewise Exits from {fy - 1}-04-01"
    dataframe = pd.read_excel(fp, sheetname)
    zerodha_mapping = {'Symbol': 'Name', 'Profit': 'pnl', 'Entry Date': 'Buy date', 'Exit Date': 'Sell date',
                       'Buy Value': 'Buy value', 'Sell Value': 'Sell value'}
    zerodha_cols_req = ['Symbol', 'Entry Date', 'Exit Date', 'Quantity', 'Buy Value', 'Sell Value', 'Profit']
    zerodha_cols_name = ['Symbol', 'ISIN', 'Entry Date', 'Exit Date', 'Quantity', 'Buy Value', 'Sell Value', 'Profit',
                         'Period of Holding', 'Category']
    df = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]

    contains_columns = dataframe.apply(lambda row: row_contains_columns(row, zerodha_cols_req), axis=1)
    rows_with_columns = contains_columns[contains_columns].index.tolist()

    # print("\nRows that contain all required columns:")
    # print(rows_with_columns)

    if (rows_with_columns):
        rows_with_columns.append(len(dataframe) - 1)
        # print(rows_with_columns)
        for i in range(3):
            print(rows_with_columns[i])
            category = str(dataframe.iloc[rows_with_columns[i] - 2][1])
            category = 'Equity' if 'Equity' in category else category
            for j in range(rows_with_columns[i] + 1, rows_with_columns[i + 1] - 4):
                # print(rows_with_columns[i], ' - ', rows_with_columns[i+1] - 4, ' and j = ', j)
                if ((str(dataframe.iloc[j][1]) != '') & (str(dataframe.iloc[j][1]) != 'Symbol')):
                    dataframe['Category'] = str(category)
                    # print(dataframe.iloc[j])
                    df[i] = df[i]._append(dataframe.iloc[j][1:])
                else:
                    break

    for i in range(3):
        df[i].drop(df[i].columns[9:len(df[i].columns) - 1], axis=1, inplace=True)
        df[i].columns = zerodha_cols_name
        df[i] = df[i].rename(columns=zerodha_mapping)
        df[i] = df[i].drop(['ISIN', 'Period of Holding'], axis=1)
        df[i]['Buy date'] = pd.to_datetime(df[i]['Buy date'], format='%Y-%m-%d', errors='coerce')
        df[i]['Sell date'] = pd.to_datetime(df[i]['Sell date'], format='%Y-%m-%d', errors='coerce')

        df[i]['Buy value'] = pd.to_numeric(df[i]['Buy value'])
        df[i]['Sell value'] = pd.to_numeric(df[i]['Sell value'])

    rdf = pd.concat(df)
    rdf = rdf.dropna(axis=0, thresh=4)

    return rdf
