import streamlit as st
from PIL import Image
import load_data
import read_pandas
from read_pandas import read_my_csv
from read_pandas import pwr_plot  
from read_pandas import make_plot
from read_pandas import read_pd
from read_pandas import heartrate_plot
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



if __name__ == "__main__":
    main()


    