import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('words.csv')
st.markdown("<h1 style='text-align: center; color: red;'>⋰Ẍ⋱</h1>", unsafe_allow_html=True)
st.title("French-English Translation App")


st.sidebar.subheader('Select Target Language')
target_language = st.sidebar.selectbox('Select language:', options=['English', 'Dutch'])

# Update target language in session state
st.session_state.target_language = target_language

# Initialize session state variables if they don't exist
if 'words' not in st.session_state:
    st.session_state.words = df

if 'df' not in st.session_state or st.session_state.df is None:
    st.session_state.df = pd.DataFrame(st.session_state.words)
else:
    # Update df based on the target language
    st.session_state.df = pd.DataFrame(st.session_state.words[['French', target_language]])

# Initialize correct count if it doesn't exist
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0

# Initialize list of guessed words if it doesn't exist
if 'guessed_words' not in st.session_state:
    st.session_state.guessed_words = []

# Function to get a random word
def get_random_word():
    # Filter out words that have been guessed correctly
    available_words = st.session_state.df[~st.session_state.df['French'].isin(st.session_state.guessed_words)]
    if available_words.empty:
        return None, None  # Return None if all words have been guessed correctly
    random_index = np.random.randint(len(available_words))
    return available_words.iloc[random_index]["French"], available_words.iloc[random_index][target_language]

# Function to set a new word and translation
def set_new_word():
    st.session_state.french_word, st.session_state.correct_translation = get_random_word()

# Initialize or update random word and translation
if 'french_word' not in st.session_state or 'correct_translation' not in st.session_state:
    set_new_word()

if st.session_state.french_word is not None:
    st.write(f"Translate the following word from French to {target_language}: **{st.session_state.french_word}**")

    user_translation = st.text_input(f"Your translation in {target_language}:").strip()
    submit_button = st.button("Submit Translation")

    # Check if the user's translation is correct or incorrect, only when submit button is pressed
    if submit_button and user_translation:
        if user_translation.lower() == st.session_state.correct_translation.lower():
            st.success("Correct translation!")
            st.markdown("![Alt Text](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzlzbWduN2htaWFieWJ5cGIxMjVpZzc5dTFxZmd0c28zeW8wOTEzcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/d3mlE7uhX8KFgEmY/giphy.gif)")
            st.session_state.correct_count += 1  # Increment correct count
            st.session_state.guessed_words.append(st.session_state.french_word)  # Add guessed word to list
            set_new_word()  # Set a new word and translation
            # Clear the text input field using JavaScript
            st.write(
                "<script>"
                "document.getElementById('text_input').value = ''"
                "</script>",
                unsafe_allow_html=True,
            )
        else:
            st.error(f"Incorrect translation. The correct translation was: **{st.session_state.correct_translation}**")
            st.markdown("![Alt Text]https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmtsdnQ4cGNicWVnbm9kYTJ3ano0aGNrZndqMHkxZjFqanNqMGxsaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/nR4L10XlJcSeQ/giphy.gif)")
    st.write(f"Total Correct Tries: {st.session_state.correct_count}")
else:
    st.write("🎈 You finished!")
    st.markdown("![Alt Text](https://media1.tenor.com/m/hiq7FodgfxcAAAAC/caucasian-caucasus.gif)")
