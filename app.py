import streamlit as st
import pandas as pd
import requests
import os

st.title("🇦🇪 UAE Family Heritage AI Archivist")

# ----------------------------
# FILE SETUP
# ----------------------------
FILE_NAME = "heritage_data.csv"

# Create file if it doesn't exist
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "Story",
        "AI Story",
        "Translation",
        "Language",
        "Values"
    ])
    df.to_csv(FILE_NAME, index=False, encoding="utf-8-sig")

# ----------------------------
# INPUTS
# ----------------------------
story = st.text_area("Enter Family Story")

language = st.selectbox(
    "Select Language",
    ["Arabic", "English"]
)

values = st.multiselect(
    "Select UAE Values",
    ["Respect", "Unity", "Responsibility", "Hard Work", "Compassion"]
)

# ----------------------------
# AI PROCESSING
# ----------------------------
def process_story(text):
    return "AI Processed Story: " + text

# ----------------------------
# TRANSLATION
# ----------------------------
def translate_text(text, language):

    text = text[:450]

    # Arabic → English
    if language == "Arabic":
        langpair = "ar|en"

    # English → Arabic
    else:
        langpair = "en|ar"

    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={langpair}"

    response = requests.get(url)
    data = response.json()

    return data["responseData"]["translatedText"]

# ----------------------------
# BUTTON
# ----------------------------
if st.button("Submit Story"):

    if story:

        ai_story = process_story(story)

        try:
            translated = translate_text(story, language)
        except:
            translated = "Translation failed"

        st.write("### Original Story")
        st.write(story)

        st.write("### AI Processed Story")
        st.write(ai_story)

        st.write("### Translated Story")
        st.write(translated)

        # ----------------------------
        # SAVE DATA
        # ----------------------------
        new_data = pd.DataFrame([{
            "Story": story,
            "AI Story": ai_story,
            "Translation": translated,
            "Language": language,
            "Values": ", ".join(values)
        }])

        old_data = pd.read_csv(FILE_NAME, encoding="utf-8-sig")

        updated_data = pd.concat([old_data, new_data], ignore_index=True)

        updated_data.to_csv(
            FILE_NAME,
            index=False,
            encoding="utf-8-sig"
        )

        st.success("Story saved successfully!")

    else:
        st.warning("Please enter a story")

# ----------------------------
# DISPLAY DATA
# ----------------------------
df = pd.read_csv(FILE_NAME, encoding="utf-8-sig")

st.write("## Stored Stories")
st.dataframe(df)

# ----------------------------
# DOWNLOAD BUTTON
# ----------------------------
csv = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

st.download_button(
    "Download CSV File",
    data=csv,
    file_name="heritage_data.csv",
    mime="text/csv"
)
