import streamlit as st
import pandas as pd
import requests

st.title("🇦🇪 UAE Family Heritage Archive")

# إدخال القصة
story = st.text_area("Enter your family story:")

# اختيار اللغة
language = st.selectbox("Language:", ["Arabic", "English"])

# دالة الترجمة
def translate_text(text, target_lang):
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_lang}"
    response = requests.get(url)
    data = response.json()
    return data['responseData']['translatedText']

# زر الترجمة
if st.button("Translate"):
    if story:
        try:
            if language == "Arabic":
                translated = translate_text(story, "ar")
                st.subheader("الترجمة:")
                st.write(translated)
            else:
                translated = translate_text(story, "en")
                st.subheader("Translation:")
                st.write(translated)
        except:
            st.error("Translation failed.")
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
