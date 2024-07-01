import streamlit as st
from utils.email_verification import send_verification_code, verify_code

def login():
    st.title("Login")
    email = st.text_input("Email")
    if st.button("Send Verification Code"):
        send_verification_code(email)
        st.session_state['email'] = email
        st.session_state['code_sent'] = True

    if 'code_sent' in st.session_state and st.session_state['code_sent']:
        code = st.text_input("Enter Verification Code")
        if st.button("Verify"):
            if verify_code(st.session_state['email'], code):
                st.session_state['logged_in'] = True
            else:
                st.error("Invalid code")
