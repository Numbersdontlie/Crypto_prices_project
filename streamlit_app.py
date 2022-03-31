import streamlit as st
import s3fs 
import os 
import pandas as pd 
import matplotlib.pyplot as plt 
import glob 
import altair as alt

#config the page 
st.set_page_config(page_icon="📈", page_title="Crypto Visualization")

st.markdown(
    """# **Crypto Visualization**
    A simple cryptocurrency price visualizator pulling data from a S3 bucket
    """
)

st.header("**Selected Crypto**")

#create connection object
fs = s3fs.S3FileSystem(anon=False) 
fs.glob('crypto-price-project/')
csv_files = fs.glob('crypto-price-project' + "/*.csv")


#retrieve file contents into a dataframe 
@st.experimental_memo
def get_data():
    df_list = (pd.read_csv(file) for file in csv_files)
    return pd.concat(df_list, ignore_index=True)

df = get_data()

#user selects crypto
@st.cache
def get_select_box_data():
    return pd.Dataframe({
        "first column": ["select stock", "ADA", "BNB", "BTC", "DOT", "ETH", "LUNA", "SOL", "USDC", "USDT", "XRP",]
    })

df_new = get_select_box_data()
col3 = st.columns(1)
with col3:
    option = st.selectbox("select a crypto to visualize", df_new["first column"])
filter_df = df_new[df_new["first column"] == option]

#crypto = df['name']
#cryptos_choice = st.sidebar.selectbox("Select the crypto of your interest:" crypto)

#create the graphs 
def get_chart(df):
    hover = alt.selection_single(
        fields=["time"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(df, title="Evolution of crypto prices")
        .markline()
        .encode(
            x="date",
            y="price",
            color="symbol",
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65) #draw point on the line

    tooltips = (
        alt.Chart(df)
        .mark_rule()
        .encode(
            x="time",
            y="close",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("time", title="Date"),
                alt.Tooltip("close", title="Price ($ USD)"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

chart = get_chart(df)

st.altair_chart(chart.interactive(), use_container_width=True)