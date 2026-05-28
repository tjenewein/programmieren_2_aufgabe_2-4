import streamlit as st
from read_pandas import read_my_csv
from read_pandas import pwr_plot  
from read_pandas import make_plot
from read_pandas import read_pd
from read_pandas import heartrate_plot
from read_pandas import pwr_hr_plot


# Wo startet sie Zeitreihe
# Wo endet sich
# Was ist die Maximale und Minimale Spannung
# Grafik



tab1, tab2 = st.tabs(["EKG-Data", "Power-Data"])

with tab1:

    st.header("EKG-Data")
    st.write("# My Plot")
    df = read_my_csv()
    fig1 = make_plot(df)
    st.plotly_chart(fig1)

with tab2:
    st.header("Power-Data")

    slide = st.slider("Maximale Herzfrequenz", min_value=100, max_value=230, step=1)
    
    df1 = read_pd()

   
    fig3 = pwr_hr_plot(slide,df1)
    st.plotly_chart(fig3)

    max_power = df1["PowerOriginal"].max()
    mean = df1["PowerOriginal"].mean()
    st.write(f"Maximale Leistung: {max_power}")
    st.write(f"Durchschnittliche Leistung: {mean}")

    max_heart_rate = df1["HeartRate"].max()
    st.write(f"Maximale Herzfrequenz: {max_heart_rate}")

    st.write(f"Maximale Herzfrequenz (Slider): {slide}")
