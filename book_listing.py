import streamlit as st
from utils.fetch_books import fetch_books_from_amazon

def display_books(mood):
    books = fetch_books_from_amazon(mood)
    for category, book_list in books.items():
        st.header(category)
        for book in book_list:
            st.subheader(book['title'])
            st.write(f"Author: {book['author']}")
            st.write(f"Rating: {book['rating']}")
            st.image(book['image_url'])
