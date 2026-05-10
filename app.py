import streamlit as st
import pandas as pd
import requests
import os

st.title("🇦🇪 UAE Family Heritage AI Archivist")

# ----------------------------
# INPUTS
# ----------------------------
story = st.text_area("Enter Family Story (Arabic or English):")

language = st.selectbox("Select Language:", ["English", "Arabic"])

values = st.multiselect(
    "Select UAE Values",
    ["Respect", "Unity", "Responsibility", "Hard Work", "Compassion"]
)

# ----------------------------
# AI SIMULATION FUNCTION
# ----------------------------
def process_story(text):
    return "AI Processed Story: " + text

# ----------------------------
# TRANSLATION FUNCTION
# ----------------------------
def translate_text(text):
    text = text[:450]  # API limit fix
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|ar"
    response = requests.get(url)
    data = response.json()
    return data["responseData"]["translatedText"]

# ----------------------------
# FILE PATH (REAL STORAGE)
# ----------------------------
file_path = "heritage_data.csv"

# ----------------------------
# MAIN BUTTON
# ----------------------------
if st.button("Submit Story"):

    if story:

        # AI processing
        ai_story = process_story(story)

        # translation
        try:
            translated = translate_text(story)
        except:
            translated = "Translation failed"

        # show outputs
        st.write("### Original Story")
        st.write(story)

        st.write("### AI Processed Story")
        st.write(ai_story)

        st.write("### Translated Story")
        st.write(translated)

        # ----------------------------
        # SAVE TO CSV (FIXED PART)
        # ----------------------------
        new_data = pd.DataFrame([{
            "Story": story,
            "AI Story": ai_story,
            "Translation": translated,
            "Language": language,
            "Values": ", ".join(values)
        }])

        if os.path.exists(file_path):
            new_data.to_csv(file_path, mode="a", header=False, index=False)
        else:
            new_data.to_csv(file_path, index=False)

        st.success("Story saved successfully!")

    else:
        st.warning("Please enter a story")

# ----------------------------
# DISPLAY STORED DATA
# ----------------------------
st.write("## Stored Stories")

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.dataframe(df)
else:
    st.info("No stories saved yet.")

# ----------------------------
# DOWNLOAD BUTTON
# ----------------------------
if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    st.download_button(
        "Download CSV File",
        data=df.to_csv(index=False),
        file_name="heritage_data.csv",
        mime="text/csv"
    )
