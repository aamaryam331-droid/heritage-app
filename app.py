import streamlit as st
import pandas as pd
import requests

st.title("🇦🇪 UAE Family Heritage Archive")

# Session storage (IMPORTANT FIX)
if "data" not in st.session_state:
    st.session_state.data = []

# Input
story = st.text_area("Enter your family story:")
language = st.selectbox("Language:", ["Arabic", "English"])

# Translation function
def translate_text(text, target_lang):
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_lang}"
    response = requests.get(url)
    data = response.json()
    return data['responseData']['translatedText']

# Translate button
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

# Save button (FIXED)
if st.button("Save Story"):
    if story:
        st.session_state.data.append({
            "Story": story,
            "Language": language
        })
        st.success("Story saved successfully! 🎉 (temporary storage)")
    else:
        st.warning("Please enter a story before saving.")

# Show data table
df = pd.DataFrame(st.session_state.data)
st.dataframe(df)

# Download button (IMPORTANT FOR MARKS)
st.download_button(
    "Download Archive (Excel CSV)",
    data=df.to_csv(index=False),
    file_name="stories.csv",
    mime="text/csv"
)
