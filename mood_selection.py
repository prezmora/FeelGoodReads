import streamlit as st

def mood_selection():
    st.title("Welcome")
    st.subheader("How are you feeling today?")
    mood = st.selectbox("Select your mood", ["Heartbroken", "Sad", "Happy", "In-love"])
    if st.button("Show Books"):
        return mood
    return None
