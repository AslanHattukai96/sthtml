import streamlit as st
import pandas as pd
import numpy as np
import time

# Set page title and header
st.markdown("<h1 style='text-align: center; color: yellow;'>⋰Ẍ⋱</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: yellow;'>Learn Adyghabze</h1>", unsafe_allow_html=True)
st.title("")

# CSV dosyalarını tanımla
csv_files = {
    "Hayvanlar": "animals.csv",
    "Kelimeler": "words.csv",
    "Temel Fiiller": "basic verbs.csv",
    "İletişim Fiilleri": "communication verbs.csv",
    "Fiziksel Aktiviteler": "physical activities.csv"
}

# CSV dosyası seçmek için bir selectbox ekle
selected_file_key = st.selectbox("Bir dosyası seçin", list(csv_files.keys()))
selected_file_path = csv_files[selected_file_key]

# Seçilen dosyayı session state'de sakla
if 'selected_file' not in st.session_state or st.session_state.selected_file != selected_file_path:
    st.session_state.selected_file = selected_file_path
    st.session_state.words = pd.read_csv(st.session_state.selected_file)
    st.session_state.correct_count = 0
    st.session_state.guessed_words = []
    st.session_state.next_button_clicked = True

df = st.session_state.words

target_language = 'Türkçe'  # Hedef dili Türkçe olarak ayarla

# Önceki dil seçimini başlat veya güncelle
if 'prev_language' not in st.session_state:
    st.session_state.prev_language = target_language

# Session state'de hedef dili güncelle
st.session_state.target_language = target_language

# Dilin değişip değişmediğini kontrol et
if st.session_state.prev_language != target_language:
    st.session_state.prev_language = target_language
    st.session_state.next_button_clicked = True

# Seçilen hedef dile göre DataFrame'i filtrele
st.session_state.df = pd.DataFrame(st.session_state.words[['Circassian', target_language]])

# Rastgele bir kelime almak için fonksiyon
def get_random_word():
    # Doğru tahmin edilen kelimeleri filtrele
    available_words = st.session_state.df[~st.session_state.df['Circassian'].isin(st.session_state.guessed_words)]
    if available_words.empty:
        return None, None  # Tüm kelimeler doğru tahmin edilirse None döndür
    random_index = np.random.randint(len(available_words))
    return available_words.iloc[random_index]["Circassian"], available_words.iloc[random_index][target_language]

# Yeni bir kelime ve çeviri ayarlamak için fonksiyon
def set_new_word():
    st.session_state.circassian_word, st.session_state.correct_translation = get_random_word()

# Rastgele kelime ve çeviriyi başlat veya güncelle
if 'circassian_word' not in st.session_state or 'correct_translation' not in st.session_state or st.session_state.next_button_clicked:
    set_new_word()
    st.session_state.next_button_clicked = False

if st.session_state.circassian_word is not None:
    st.write(f"Çerkesçeden Türkçeye aşağıdaki kelimeyi çevirin: **{st.session_state.circassian_word}**")

    user_translation = st.text_input(f"Türkçe çeviriniz:").strip()
    
    # Hedef dile göre buton etiketini değiştir
    submit_button_label = "Kontrol Et"  # Buton etiketini "Kontrol Et" olarak değiştir
    
    submit_button = st.button(submit_button_label)

    # Kullanıcının çevirisi doğru mu yanlış mı kontrol et, sadece submit butonu tıklandığında
    if submit_button and user_translation:
        if user_translation.lower() == st.session_state.correct_translation.lower():
            st.success("Doğru çeviri!")
            st.session_state.correct_count += 1  # Doğru sayısını arttır
            st.session_state.guessed_words.append(st.session_state.circassian_word)  # Tahmin edilen kelimeyi listeye ekle
            set_new_word()  # Yeni bir kelime ve çeviri ayarla
            st.markdown("![Alt Text](https://media1.tenor.com/m/hiq7FodgfxcAAAAC/caucasian-caucasus.gif)")

            # Sayfayı yeniden render et
            time.sleep(3)  # 3 saniye bekle
            st.experimental_rerun()
        else:
            st.error(f"Yanlış çeviri. Doğru çeviri: **{st.session_state.correct_translation}**")

    st.write(f"Toplam Doğru Deneme Sayısı: {st.session_state.correct_count}")
else:
    st.write("🎈 Tamamlandı!")
    st.image("success.jpeg")
