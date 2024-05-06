import streamlit as st
import pandas as pd
import numpy as np
import time

df = pd.read_csv('words.csv')

st.markdown("<h1 style='text-align: center; color: yellow;'>⋰Ẍ⋱</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: yellow;'>Leer Adyghabze</h1>", unsafe_allow_html=True)
st.title("")

target_language = 'Dutch'  # Set target language to Dutch

# Initialize or update previous language selection
if 'prev_language' not in st.session_state:
    st.session_state.prev_language = target_language

# Update target language in session state
st.session_state.target_language = target_language

# Check if language has changed
if st.session_state.prev_language != target_language:
    st.session_state.prev_language = target_language
    st.session_state.next_button_clicked = True

# Initialize session state variables if they don't exist
if 'words' not in st.session_state:
    st.session_state.words = df

# Filter DataFrame based on the selected target language
st.session_state.df = pd.DataFrame(st.session_state.words[['Circassian', target_language]])

# Initialize correct count if it doesn't exist
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0

# Initialize list of guessed words if it doesn't exist
if 'guessed_words' not in st.session_state:
    st.session_state.guessed_words = []

# Function to get a random word
def get_random_word():
    # Filter out words that have been guessed correctly
    available_words = st.session_state.df[~st.session_state.df['Circassian'].isin(st.session_state.guessed_words)]
    if available_words.empty:
        return None, None  # Return None if all words have been guessed correctly
    random_index = np.random.randint(len(available_words))
    return available_words.iloc[random_index]["Circassian"], available_words.iloc[random_index][target_language]

# Function to set a new word and translation
def set_new_word():
    st.session_state.circassian_word, st.session_state.correct_translation = get_random_word()

# Initialize or update random word and translation
if 'circassian_word' not in st.session_state or 'correct_translation' not in st.session_state or st.session_state.next_button_clicked:
    set_new_word()
    st.session_state.next_button_clicked = False

if st.session_state.circassian_word is not None:
    st.write(f"Vertaal het volgende woord van Circassian naar het Nederlands: **{st.session_state.circassian_word}**")

    user_translation = st.text_input(f"Jouw vertaling: ").strip()
    
    # Change button label according to the target language
    submit_button_label = "Controleren"  # Change button label to "Controleren"
    
    submit_button = st.button(submit_button_label)

    # Check if the user's translation is correct or incorrect, only when submit button is pressed
    if submit_button and user_translation:
        if user_translation.lower() == st.session_state.correct_translation.lower():
            st.success("Juiste vertaling!")
            st.session_state.correct_count += 1  # Increment correct count
            st.session_state.guessed_words.append(st.session_state.circassian_word)  # Add guessed word to list
            set_new_word()  # Set a new word and translation
            # Clear the text input field using JavaScript
            st.write(
                "<script>"
                "document.getElementById('text_input').value = ''"
                "</script>",
                unsafe_allow_html=True,
            )
            st.markdown("![Alt Text](https://media1.tenor.com/m/hiq7FodgfxcAAAAC/caucasian-caucasus.gif)")

            # Rerender the page
            time.sleep(3)  # Wait for 3 seconds
            st.experimental_rerun()
        else:
            st.error(f"Onjuiste vertaling. De juiste vertaling was: **{st.session_state.correct_translation}**")

    st.write(f"Totaal aantal juiste pogingen: {st.session_state.correct_count}")
else:
    st.write("🎈 Je bent klaar!")
    st.image("succes.jpeg")
