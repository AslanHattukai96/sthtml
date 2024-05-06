import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('words.csv')

st.markdown("<h1 style='text-align: center; color: yellow;'>⋰Ẍ⋱</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: yellow;'>Learn Adyghabze</h1>", unsafe_allow_html=True)
st.title("")
st.sidebar.subheader('Select Target Language')
target_language = st.sidebar.selectbox('Select language:', options=['English', 'Dutch'])

# Initialize or update previous language selection
if 'prev_language' not in st.session_state:
    st.session_state.prev_language = target_language

# Update target language in session state
st.session_state.target_language = target_language

# Check if language has changed and simulate a click on "Next Word" button
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
    st.write(f"Translate the following word from Circassian to {target_language}: **{st.session_state.circassian_word}**")

    user_translation = st.text_input(f"Your translation in {target_language}:").strip()
    
    # Change button labels according to the target language
    next_button_label = f"Next Word in {target_language}" if target_language == 'Dutch' else "Next Word"
    submit_button_label = f"Submit Translation in {target_language}" if target_language == 'Dutch' else "Submit Translation"
    
    submit_button = st.button(submit_button_label)
    next_button = st.button(next_button_label)  # Update button label

    # Check if the user clicks Next Word button
    if next_button:
        st.session_state.next_button_clicked = True

    # Check if the user's translation is correct or incorrect, only when submit button is pressed
    if submit_button and user_translation:
        if user_translation.lower() == st.session_state.correct_translation.lower():
            st.success("Correct translation!")
            st.session_state.correct_count += 1  # Increment correct count
            st.session_state.guessed_words.append(st.session_state.circassian_word)  # Add guessed word to list
            # Clear the text input field using JavaScript
            st.write(
                "<script>"
                "document.getElementById('text_input').value = ''"
                "</script>",
                unsafe_allow_html=True,
            )
        else:
            st.error(f"Incorrect translation. The correct translation was: **{st.session_state.correct_translation}**")

    st.write(f"Total Correct Tries: {st.session_state.correct_count}")
else:
    st.write("🎈 You finished!")
