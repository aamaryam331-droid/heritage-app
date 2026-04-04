import streamlit as st
import pandas as pd

st.title("🇦🇪 UAE Family Heritage Archive")

# إدخال القصة
story = st.text_area("Enter your family story:")

# اختيار اللغة
language = st.selectbox("Language:", ["Arabic", "English"])

# زر الترجمة (عام)
from googletrans import Translator

translator = Translator()

if st.button("Translate"):
    if story:
        if language == "Arabic":
            translated = translator.translate(story, dest='ar')
            st.subheader("الترجمة:")
            st.write(translated.text)
        else:
            translated = translator.translate(story, dest='en')
            st.subheader("Translation:")
            st.write(translated.text)

# زر الحفظ
if st.button("Save Story"):
    data = {
        "Story": [story],
        "Language": [language]
    }

    df = pd.DataFrame(data)

    try:
        old = pd.read_excel("stories.xlsx")
        df = pd.concat([old, df], ignore_index=True)
    except:
        pass

    df.to_excel("stories.xlsx", index=False)

    st.success("Story saved successfully! 🎉")
