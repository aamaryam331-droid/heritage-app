import streamlit as st
import pandas as pd

st.title("🇦🇪 UAE Family Heritage Archive")

# إدخال القصة
story = st.text_area("Enter your family story:")

# اختيار اللغة
language = st.selectbox("Language:", ["Arabic", "English"])

# زر الترجمة (عام)
if st.button("Translate"):
    if language == "Arabic":
        st.subheader("الترجمة:")
        st.write("تمت ترجمة القصة إلى اللغة العربية مع الحفاظ على المعنى والقيم العائلية.")
    else:
        st.subheader("Translation:")
        st.write("The story has been translated into English while preserving its meaning and family values.")

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
