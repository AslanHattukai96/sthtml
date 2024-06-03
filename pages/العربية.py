import streamlit as st
import pandas as pd
import numpy as np
import time

st.markdown("""
<style>
body, html {
  direction: rtl;
  unicode-bidi: bidi-override;
  text-align: right;
}
p, div, input, label, h1, h2, h3, h4, h5, h6 {
  direction: rtl;
  unicode-bidi: bidi-override;
  text-align: right;
}
</style>
""", unsafe_allow_html=True)

# Set page title and header
st.markdown("<h1 style='text-align: center; color: yellow;'>تعلّم الأديغية</h1>", unsafe_allow_html=True)  # Replace Hebrew title with Arabic title for Adyghe learning
st.title("")

# Define the CSV files (Translate file names and categories to Arabic)
csv_files = {
  "حيوانات": "animals.csv",
  "كلمات": "words.csv",
  "أفعال أساسية": "basic verbs.csv",
  "أفعال تواصل": "communication verbs.csv",
  "أنشطة بدنية": "physical activities.csv"
}

# Add a selectbox to choose the CSV file
selected_file_key = st.selectbox("اختر ملف", list(csv_files.keys()))
selected_file_path = csv_files[selected_file_key]

# Store the selected file in session state
if 'selected_file' not in st.session_state or st.session_state.selected_file != selected_file_path:
  st.session_state.selected_file = selected_file_path
  st.session_state.words = pd.read_csv(st.session_state.selected_file)
  st.session_state.correct_count = 0
  st.session_state.guessed_words = []
  st.session_state.next_button_clicked = True

df = st.session_state.words

target_language = 'العربية'  # Set target language to Arabic

# Initialize or update previous language selection
if 'prev_language' not in st.session_state:
  st.session_state.prev_language = target_language

# Update target language in session state
st.session_state.target_language = target_language

# Check if language has changed
if st.session_state.prev_language != target_language:
  st.session_state.prev_language = target_language
  st.session_state.next_button_clicked = True

# Filter DataFrame based on the selected target language
st.session_state.df = pd.DataFrame(st.session_state.words[['Circassian', target_language]])

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
  st.markdown(f"ترجم الكلمة التالية من الأديغية إلى العربية: <span dir='rtl'>{st.session_state.circassian_word}</span>", unsafe_allow_html=True)  # Translate prompt to instruct user to translate from Adyghe to Arabic

  user_translation = st.text_input(f"ترجمتك إلى العربية:").strip()
  
  # Change button label according to the target language
  submit_button_label = "تحقق"  # Change button label to "تحقق" (verify/check in Arabic)

  submit_button = st.button(submit_button_label)

  # Check if the user's translation is correct or incorrect, only when submit button is pressed
  if submit_button and user_translation:
    if user_translation.lower() == st.session_state.correct_translation.lower():
      st.success("ترجمة صحيحة!")  # Change success message to Arabic (Correct translation!)
      st.session_state.correct_count += 1  # Increment correct count
      st.session_state.guessed_words.append(st.session_state.circassian_word)  # Add guessed word to list
      set_new_word()  # Set a new word and translation
      st.markdown("![Alt Text](https://media1.tenor.com/m/hiq7FodgfxcAAAAC/caucasian-caucasus.gif)")

      # Rerender the page
      time.sleep(3)  # Wait for 3 seconds
      st.experimental_rerun()
    else:
      st.error(f"ترجمة خاطئة. الإجابة الصحيحة هي: **{st.session_state.correct_translation}**")  # Change error message to Arabic (Incorrect translation. The correct answer is...)

  st.write(f"الإجمالي: محاولات صحيحة {st.session_state.correct_count}")  # Change total count message to Arabic (Total: Correct Attempts)
else:
  st.write(" لقد انتهيت!")  # Change completion message to Arabic (You've finished!)
  st.image("success.jpeg")