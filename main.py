from operator import contains

import streamlit as st
from PIL import Image
import load_data
import read_pandas
from read_pandas import read_my_csv
from read_pandas import pwr_plot  
from read_pandas import make_plot
from read_pandas import read_pd
from read_pandas import heartrate
from read_pandas import pwr_hr_plot



def main():

    # Initialize session state BEFORE using it
    if 'picture_path' not in st.session_state:
        st.session_state.picture_path = 'data/pictures/none.jpg'

    col1, col2 = st.columns(2)

    with col1:
        st.write("# EKG APP")
        st.write("## Versuchsperson auswählen")
        person_names = load_data.person_list()

        st.session_state.current_user = st.selectbox(
            'Versuchsperson', options=person_names, key="sbVersuchsperson"
        )

        st.write("Der Name der ist: ", st.session_state.current_user)
        st.write("Der Pfad ist: ", st.session_state.picture_path)

    with col2:
        if st.session_state.current_user in person_names:
            person = load_data.find_person_data_by_name(st.session_state.current_user)
            if person:
                st.session_state.picture_path = person["picture_path"]

        image = Image.open(st.session_state.picture_path)
        st.image(image, caption=st.session_state.current_user)

    tab1, tab2 = st.tabs(["EKG-Data", "Power-Data"])

    with tab1:

        st.header("EKG-Data")
        st.write("# My Plot")
        df = read_pandas.read_my_csv()
        fig1 = read_pandas.make_plot(df)
        st.plotly_chart(fig1)

    with tab2:
        st.header("Power-Data")
    
        df1 = read_pandas.read_pd()

        #Power Plot:
        fig = read_pandas.pwr_plot(df1)
        st.plotly_chart(fig, use_container_width=True)

        max_power = df1["PowerOriginal"].max()
        mean = df1["PowerOriginal"].mean()
        st.write(f"Maximale Leistung: {max_power}")
        st.write(f"Durchschnittliche Leistung: {mean}")

        #Heartrate Plot:
        fig2 = read_pandas.heartrate(df1)
        st.plotly_chart(fig2, use_container_width=True)
   
   


        fig3 = read_pandas.pwr_hr_plot(df1)
        st.plotly_chart(fig3, use_container_width=True)





if __name__ == "__main__":
    main()


    