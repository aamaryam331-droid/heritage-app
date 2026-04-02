import streamlit as st
import pandas as pd

st.title("UAE Family Heritage 🇦🇪")

story = st.text_area("Enter your family story:")
language = st.selectbox("Language:", ["Arabic", "English"])

if st.button("Save"):
    data = {"Story": [story], "Language": [language]}
    df = pd.DataFrame(data)
    
    try:
        old = pd.read_excel("stories.xlsx")
        df = pd.concat([old, df], ignore_index=True)
    except:
        pass
    
    df.to_excel("stories.xlsx", index=False)
    
    st.success("Saved!")
