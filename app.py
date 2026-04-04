import streamlit as st
import pandas as pd
from googletrans import Translator

# إنشاء المترجم
translator = Translator()

st.title("🇦🇪 UAE Family Heritage Archive")

# إدخال القصة
story = st.text_area("Enter your family story:")

# اختيار اللغة
language = st.selectbox("Language:", ["Arabic", "English"])

# زر الترجمة
if st.button("Translate"):
    if story:
        try:
            if language == "Arabic":
                translated = translator.translate(story, dest='ar')
                st.subheader("الترجمة:")
                st.write(translated.text)
            else:
                translated = translator.translate(story, dest='en')
                st.subheader("Translation:")
                st.write(translated.text)
        except:
            st.error("Translation failed. Please try again.")
    else:
        st.warning("Please enter a story first.")

# زر الحفظ
if st.button("Save Story"):
    if story:
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
    else:
        st.warning("Please enter a story before saving.")
