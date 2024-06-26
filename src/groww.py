import pandas as pd
from utils import row_contains_columns

def standardize_groww_mf(fp, fy: int):
    fy = fy
    headers = ['Scheme Name', 'Scheme Code', 'Category', 'Folio Number', 'Purchase Transaction Id', 'Purchase Date',
               'Matched Quantity', 'Purchase Price', 'Redeem Transaction Id',
               'Redeem Date', 'Grandfathered Nav', 'Redeem Price', 'Short Term-Capital Gain', 'Long Term-Capital Gain']
    groww_mf_renames = {'Scheme Name': 'Name', 'Matched Quantity': 'Quantity', 'Purchase Date': 'Buy date',
                        'Redeem Date': 'Sell date', 'Purchase Price': 'Buy price', 'Redeem Price': 'Sell price'}
    groww_mf_drops = ['Scheme Code', 'Folio Number', 'Purchase Transaction Id', 'Redeem Transaction Id',
                      'Grandfathered Nav', 'Short Term-Capital Gain', 'Long Term-Capital Gain', 'Buy price',
                      'Sell price']
    # Read the Excel file
    df = pd.read_excel(fp)
    categories = ['Equity', 'Debt (Specified - Other than Equity)', 'Debt (Unspecified - Other than Equity)']

    contains_columns = df.apply(lambda row: row_contains_columns(row, headers), axis=1)
    rows_with_columns = contains_columns[contains_columns].index.tolist()

    # print("\nRows that contain all required columns:")
    # print(rows_with_columns)

    if (rows_with_columns):
        df.columns = headers
        df = df.dropna(axis=0)
        df = df.rename(columns=groww_mf_renames)

        df = df[df.iloc[:, 2].isin(categories)]
        df['Buy date'] = pd.to_datetime(df['Buy date'], format='%Y-%m-%d', errors='coerce')
        df['Sell date'] = pd.to_datetime(df['Sell date'], format='%Y-%m-%d', errors='coerce')
        df['Buy value'] = pd.to_numeric(df['Quantity']) * pd.to_numeric(df['Buy price']).round(2)
        df['Sell value'] = pd.to_numeric(df['Quantity']) * pd.to_numeric(df['Sell price']).round(2)
        df['pnl'] = pd.to_numeric(df['Sell value'] - df['Buy value']).round(2)

        df = df.drop(groww_mf_drops, axis=1)
    else:
        raise ValueError("Not a groww mutual fund statement")
    return df


def standardize_groww_eq(fp, fy: int):
    fy = fy
    groww_eq_renames = {'Stock name': 'Name', 'Realised P&L': 'pnl'}
    groww_eq_drops = ['ISIN', 'Remark', 'Buy price', 'Sell price']
    headers = ['Stock name', 'ISIN', 'Quantity', 'Buy date', 'Buy price', 'Buy value', 'Sell date', 'Sell price',
               'Sell value', 'Realised P&L', 'Remark']
    # Read the Excel file
    df = pd.read_excel(fp)
    contains_columns = df.apply(lambda row: row_contains_columns(row, headers), axis=1)
    rows_with_columns = contains_columns[contains_columns].index.tolist()

    # print("\nRows that contain all required columns:")
    # print(rows_with_columns)

    if (rows_with_columns):
        df.columns = headers
        df = df.dropna(axis=0)
        df = df[~df['Stock name'].isin(df.columns)]

        df = df.drop(groww_eq_drops, axis=1)
        df = df.rename(columns=groww_eq_renames)
        df['Category'] = 'Equity'

        # df = df[df.iloc[:, 2].isin(categories)]
        df['Buy date'] = pd.to_datetime(df['Buy date'], format='%d-%m-%Y', errors='coerce')
        df['Sell date'] = pd.to_datetime(df['Sell date'], format='%d-%m-%Y', errors='coerce')

        df['Buy value'] = pd.to_numeric(df['Buy value'])
        df['Sell value'] = pd.to_numeric(df['Sell value'])

    else:
        raise ValueError("Not a groww equity statement")

    return df