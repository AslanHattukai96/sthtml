import streamlit as st
import pandas as pd
import numpy as np
import time

df = pd.read_csv('words.csv')

st.markdown("<h1 style='text-align: center; color: yellow;'>⋰Ẍ⋱</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: yellow;'>Learn Adyghabze</h1>", unsafe_allow_html=True)
st.markdown("""<div align="center">
            <h1>Welcome to our Adyghe Language Learning App! 🌍</h1>
            <p>This app is designed to help you learn Adyghe, also known as Circassian, by translating words from Adyghe to your chosen target language. Select your preferred target language from the sidebar on the left and start your language learning journey!</p>
            </div>""")
