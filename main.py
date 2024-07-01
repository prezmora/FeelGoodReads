import streamlit as st
from login import login
from mood_selection import mood_selection
from book_listing import display_books

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'code_sent' not in st.session_state:
        st.session_state['code_sent'] = False

    if not st.session_state['logged_in']:
        login()
    else:
        mood = mood_selection()
        if mood:
            display_books(mood)

if __name__ == "__main__":
    main()
