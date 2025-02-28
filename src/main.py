import streamlit as slit
import pandas as pd
from groww import *
from utils import print_cg
from zerodha import *
from samco import *

slit.set_page_config(page_title="Capital Gains", layout="wide")
slit.header('Capital Gains Auto Calculator')

# FY and File upload displayed in 2 columns
c1, c2 = slit.columns(2, gap="medium", vertical_alignment="top")
with c1:
    number = slit.number_input("Financial Year:", 2024, 2025)

# initiate financial year for taxation
fy = number

# initiate empty dataframe to collect all files data
df = pd.DataFrame()


# process_file method only returns dataframe only if it matches any of the broker pattern, else fails
@slit.cache_data
def process_file(file):
    for func in [standardize_groww_mf, standardize_groww_eq, standardize_zerodha, standardize_samco_eq]:
        try:
            return func(file, fy)
        except Exception as e:
            print(e)
    slit.write("filename: ", file.name, " is not supported right now.")
    return pd.DataFrame()


with c2:
    uploaded_files = slit.file_uploader("Choose a Excel file", accept_multiple_files=True, label_visibility='collapsed')

slit.caption("""Disclosure:
1. Calculations are for educational purpose only, please get in touch with a professional CA for tax filing.
2. Uploaded files are parsed and processed on the fly, we do not store them anywhere.
3. Debt Mutual funds redemption will be considered here as STCG.
4. Currently, we support Capital Gains excel from **Zerodha, Groww and Samco** only, more powers will be added soon.
""")

for uploaded_file in uploaded_files:
    temdf = process_file(uploaded_file)
    df = pd.concat([df, temdf])

if not df.empty:
    print_cg(slit, df, fy)

slit.markdown(r"""
    <style>.stDeployButton {visibility: hidden;}</style>
    """, unsafe_allow_html=True
              )

footer_html = """<style>.footer {position: fixed;left: 0;bottom: 0;width: 100%;text-align: center;}</style>
<div class='footer' style='text-align: center;'>
  <p>Developed with ❤️ by <a href='https://www.linkedin.com/in/prakhar092/' target=”_blank”>Prakhar</></p>
</div>"""
slit.markdown(footer_html, unsafe_allow_html=True)
