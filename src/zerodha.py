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
    df = pd.DataFrame()

    contains_columns = dataframe.apply(lambda row: row_contains_columns(row, zerodha_cols_req), axis=1)
    rows_with_columns = contains_columns[contains_columns].index.tolist()

    if rows_with_columns:
        rows_with_columns.append(len(dataframe) - 1)
        for i in range(3):
            category = str(dataframe.iloc[rows_with_columns[i] - 2][1])
            category = 'Equity' if 'Equity' in category else category
            for j in range(rows_with_columns[i] + 1, rows_with_columns[i + 1] - 4):
                if (str(dataframe.iloc[j][1]) != '') & (str(dataframe.iloc[j][1]) != 'Symbol'):
                    dataframe['Category'] = str(category)
                    df = df._append(dataframe.iloc[j][1:])
                else:
                    break

    df.drop(df.columns[9:len(df.columns) - 1], axis=1, inplace=True)
    df.columns = zerodha_cols_name
    df = df.rename(columns=zerodha_mapping)
    df = df.drop(['ISIN', 'Period of Holding'], axis=1)
    df['Buy date'] = pd.to_datetime(df['Buy date'], format='%Y-%m-%d', errors='coerce')
    df['Sell date'] = pd.to_datetime(df['Sell date'], format='%Y-%m-%d', errors='coerce')

    df['Buy value'] = pd.to_numeric(df['Buy value'])
    df['Sell value'] = pd.to_numeric(df['Sell value'])

    df = df.dropna(axis=0, thresh=4)

    return df
