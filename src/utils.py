from datetime import datetime

fy = 2024


def row_contains_columns(row, columns):
    return all(col in row.values for col in columns)


def date_to_quarter(date):
    year = fy - 1
    if datetime(year, 4, 1) <= date <= datetime(year, 6, 15):
        return 'Q1'
    elif datetime(year, 6, 16) <= date <= datetime(year, 9, 15):
        return 'Q2'
    elif datetime(year, 9, 16) <= date <= datetime(year, 12, 15):
        return 'Q3'
    elif datetime(year, 12, 16) <= date <= datetime(year + 1, 3, 15):
        return 'Q4'
    elif datetime(year + 1, 3, 16) <= date <= datetime(year + 1, 3, 31):
        return 'Q5'
    else:
        return 'Q1'


def print_cg(slit, df, finy: int):
    fy = finy
    df['Sell Quarter'] = df['Sell date'].apply(date_to_quarter)
    df['Buy Quarter'] = df['Buy date'].apply(date_to_quarter)
    df['Date Diff'] = (df['Sell date'] - df['Buy date']).dt.days

    c1, c2 = slit.columns(2, gap="medium", vertical_alignment="top")
    st = df.query('`Date Diff` < 365 and `Date Diff` > 0 and `Category`.str.contains("Debt")')
    # not handling intraday, since they will be calculated under business or salary income.
    buy = st['Buy value'].sum().round(2)
    sell = st['Sell value'].sum().round(2)
    spl = sell - buy
    # STCG calculation:
    with c1:
        slit.subheader('Short term Capital Gain[STCG]')
        slit.write('For FY : ', fy)
        slit.write('Bought Value = ', buy, ' Sell Value = ', sell, ' STCG = ', spl.round(2))
        ss = st.groupby(['Sell Quarter'])[['Sell value', 'pnl']].sum()
        bs = st.groupby(['Buy Quarter'])[['Buy value']].sum()
        # print(a, '\n',b)
        stcol1, stcol2 = slit.columns(2, gap="small", vertical_alignment="top")
        with stcol1:
            slit.header('Bought')
            slit.dataframe(bs)

        with stcol2:
            slit.header('Sold')
            slit.dataframe(ss)

    lt = df[((df['Date Diff'] >= 365) &
             (df['Category'].str.contains('Equity') & (df['Category'].str.contains('Debt') == False)))]
    # lt = df[(df['Date Diff'] >= 365)]
    # not handling intraday, since they will be calculated under business or salary income.
    buy = lt['Buy value'].sum().round(2)
    sell = lt['Sell value'].sum().round(2)
    lpl = sell - buy
    # LTCG calculation:
    with c2:
        slit.subheader('Long term Capital Gain[LTCG]')
        slit.write('For FY : ', fy)
        slit.write('Bought Value = ', buy, ' Sell Value = ', sell, ' LTCG = ', lpl.round(2))
        ls = lt.groupby(['Sell Quarter'])[['Sell value', 'pnl']].sum()
        lb = lt.groupby(['Buy Quarter'])[['Buy value']].sum()
        # print(a, '\n',b)
        stcol1, stcol2 = slit.columns(2, gap="small", vertical_alignment="top")
        with stcol1:
            slit.header('Bought')
            slit.dataframe(lb)

        with stcol2:
            slit.header('Sold')
            slit.dataframe(ls)
            slit.toast('Your capital gain has been calculated!', icon='😍')
