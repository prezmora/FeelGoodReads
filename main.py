import streamlit as st
from auth import send_verification_code, verify_code, notify_unregistered_email, admin_login, create_admin, get_admins, delete_admin
from crud.moods import get_moods, add_mood, update_mood, delete_mood
from books import fetch_books_from_amazon

# Admin section to manage moods and admins
def admin_section():
    st.title("Admin Login")
    admin_username = st.text_input("Admin Username")
    admin_password = st.text_input("Admin Password", type="password")
    if st.button("Admin Login"):
        if admin_login(admin_username, admin_password):
            st.session_state['admin_logged_in'] = True
        else:
            st.error("Invalid admin credentials")

def admin_crud_interface():
    st.title("Admin - Manage Moods and Admins")
    
    # Manage Moods
    st.subheader("Manage Moods")
    mood_list = get_moods()
    moods = [mood['mood'] for mood in mood_list]
    
    st.write("### Current Moods")
    for mood in mood_list:
        st.write(f"{mood['id']}: {mood['mood']}")
    
    new_mood = st.text_input("Add a new mood")
    if st.button("Add Mood"):
        add_mood(new_mood)
        st.experimental_rerun()
    
    mood_id = st.text_input("Mood ID to update")
    updated_mood = st.text_input("New mood value")
    if st.button("Update Mood"):
        update_mood(mood_id, updated_mood)
        st.experimental_rerun()
    
    delete_mood_id = st.text_input("Mood ID to delete")
    if st.button("Delete Mood"):
        delete_mood(delete_mood_id)
        st.experimental_rerun()

    # Manage Admins
    st.subheader("Manage Admins")
    admin_list = get_admins()
    
    st.write("### Current Admins")
    for admin in admin_list:
        st.write(f"{admin['username']}")
    
    new_admin_username = st.text_input("New Admin Username")
    new_admin_password = st.text_input("New Admin Password", type="password")
    if st.button("Add Admin"):
        create_admin(new_admin_username, new_admin_password)
        st.experimental_rerun()
    
    delete_admin_username = st.text_input("Admin Username to delete")
    if st.button("Delete Admin"):
        delete_admin(delete_admin_username)
        st.experimental_rerun()

# Main user signup and login
def signup():
    st.title("Sign Up")
    email = st.text_input("Email")
    if st.button("Send Verification Code"):
        send_verification_code(email)
        st.session_state['email'] = email
        st.session_state['code_sent'] = True

def login():
    st.title("Login")
    email = st.text_input("Email")
    if st.button("Send Verification Code"):
        try:
            send_verification_code(email)
            st.session_state['email'] = email
            st.session_state['code_sent'] = True
        except:
            notify_unregistered_email(email)

if 'code_sent' in st.session_state and st.session_state['code_sent']:
    code = st.text_input("Enter Verification Code")
    if st.button("Verify"):
        if verify_code(st.session_state['email'], code):
            st.session_state['logged_in'] = True
        else:
            st.error("Invalid code")

if 'admin_logged_in' not in st.session_state or not st.session_state['admin_logged_in']:
    admin_section()
else:
    admin_crud_interface()

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
else:
    def main_app():
        st.title("Welcome")
        
        st.subheader("How are you feeling today?")
        mood_list = get_moods()
        moods = [mood['mood'] for mood in mood_list]
        selected_mood = st.selectbox("Select your mood", moods)
        if st.button("Show Books"):
            display_books(selected_mood)

    def display_books(mood):
        books = fetch_books_from_amazon(mood)
        for book in books:
            st.header(book['title'])
            st.subheader(book['author'])
            st.write(f"Category: {book['category']}")
            st.write(f"Rating: {book['rating']}")
            st.image(book['image_url'])

    main_app()
