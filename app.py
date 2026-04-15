import streamlit as st
import pandas as pd
import requests

st.title("🇦🇪 UAE Family Heritage AI Archivist")

# ----------------------------
# SESSION STORAGE
# ----------------------------
if "data" not in st.session_state:
    st.session_state.data = []

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
# MAIN BUTTON
# ----------------------------
if st.button("Submit Story"):

    if story:

        ai_story = process_story(story)

        try:
            translated = translate_text(story)
        except:
            translated = "Translation failed"

        st.write("### Original Story")
        st.write(story)

        st.write("### AI Processed Story")
        st.write(ai_story)

        st.write("### Translated Story")
        st.write(translated)

        # SAVE DATA
        st.session_state.data.append({
            "Story": story,
            "AI Story": ai_story,
            "Translation": translated,
            "Language": language,
            "Values": ", ".join(values)
        })

        st.success("Story saved successfully!")

    else:
        st.warning("Please enter a story")

# ----------------------------
# DISPLAY DATA
# ----------------------------
st.write("## Stored Stories")
df = pd.DataFrame(st.session_state.data)
st.dataframe(df)

# ----------------------------
# DOWNLOAD FILE
# ----------------------------
st.download_button(
    "Download CSV File",
    data=df.to_csv(index=False),
    file_name="heritage_data.csv",
    mime="text/csv"
)
