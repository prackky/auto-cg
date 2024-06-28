import pandas as pd
from utils import row_contains_columns

def standardize_samco_mf(fp, fy: int):
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

    if rows_with_columns:
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


def standardize_samco_eq(fp, fy: int):
    sheetname = f"Equity+Bonds+SGB Trade Details"
    dataframe = pd.read_excel(fp, sheetname)
    fy = fy
    samco_eq_renames = {'Scrip Name': 'Name', 'Net Profit/Loss': 'pnl', 'Qty': 'Quantity', 'Buy Date': 'Buy date',
                        'Sell Date': 'Sell date', 'Buy Value': 'Buy value',
                        'Sell Value': 'Sell value', 'Type of instrument': 'Category'}
    samco_eq_drops = ['ISIN', 'Long term taxable income', 'Short term taxable income', 'Purchase Type', 'Avg Buy Price',
                      'Avg Sell Price', 'Cost Of Acquisition', 'Charges and Statutory Levies', 'STT']
    samco_header_req = ['ISIN', 'Scrip Name', 'Qty', 'Buy Date', 'Sell Date', 'Avg Buy Price', 'Buy Value',
                        'Avg Sell Price', 'Sell Value', 'Cost Of Acquisition',
                        'Charges and Statutory Levies', 'STT', 'Net Profit/Loss', 'Long term taxable income',
                        'Short term taxable income', 'Purchase Type', 'Type of instrument']

    contains_columns = dataframe.apply(lambda row: row_contains_columns(row, samco_header_req), axis=1)
    rows_with_columns = contains_columns[contains_columns].index.tolist()

    df = pd.DataFrame()
    if rows_with_columns:
        rows_with_columns.append(len(dataframe) - 1)
        print(rows_with_columns)
        for j in range(rows_with_columns[0] + 1, rows_with_columns[0 + 1] - 4):
            if dataframe.iloc[j][0] == 'Sub total':
                break
            # add row to the dataframe
            df = df._append(dataframe.iloc[j])

        df.columns = samco_header_req
        df = df.rename(columns=samco_eq_renames)
        df = df.dropna(axis=0, thresh=9)
        df = df.drop(samco_eq_drops, axis=1)
        df['Buy date'] = pd.to_datetime(df['Buy date'], format='%d/%m/%Y', errors='coerce')
        df['Sell date'] = pd.to_datetime(df['Sell date'], format='%d/%m/%Y', errors='coerce')

        df['Buy value'] = pd.to_numeric(df['Buy value'])
        df['Sell value'] = pd.to_numeric(df['Sell value'])
    else:
        raise ValueError("Not a SAMCO equity statement")

    return df