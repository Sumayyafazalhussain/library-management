import streamlit as st
import json
import time
import pandas as pd

# Load library from file
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save library to file
def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_library()

# Streamlit UI Customization
st.set_page_config(page_title="Library Manager", page_icon="📚", layout="wide")

# Custom CSS for Light Theme & Row Layout
st.markdown(
    """
    <style>
        /* Sidebar - Light and Clean Look */
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, rgba(255, 255, 255, 0.9), rgba(240, 240, 240, 0.9));
            color: black;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.1);
        }

        .stSidebar .stRadio button, .stSidebar .stTextInput input, .stSidebar .stSelectbox select {
            background-color: #f7f7f7;
            border: 1px solid #ddd;
            color: black;
        }

        /* Main Title and Section Titles */
        h1, h2 {
            color: #1E88E5;
            font-family: 'Arial', sans-serif;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
        }

        /* Buttons - Light and Sleek */
        .stButton button {
            background: linear-gradient(to right, #42A5F5, #1E88E5);
            color: white;
            font-weight: bold;
            border-radius: 15px;
            padding: 12px 24px;
            border: none;
            transition: all 0.4s ease-in-out;
        }
        .stButton button:hover {
            background: linear-gradient(to right, #1E88E5, #0D47A1);
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        /* Book Cards with Light Colors */
        .book-card {
            background: #ffffff;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            transition: 0.3s ease-in-out;
            text-align: center;
            border: 1px solid #ddd;
            margin: 10px;
        }
        .book-card:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
            border-color: #42A5F5;
        }

        /* Enhanced Table for Stats */
        .stMetric {
            background-color: #42A5F5;
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            padding: 20px;
            margin-top: 20px;
        }

        /* General Styles */
        .book-card-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-start;
        }
        .book-card-container .book-card {
            width: 30%;
            margin: 1%;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
menu = st.sidebar.radio(
    "Select an Option",
    ["📖 Add a Book", "❌ Remove a Book", "🔍 Search a Book", "📚 Library Collection", "📊 Library Dashboard", "💾 Save & Exit"]
)

# Main Title
st.title("📚 Library Management System")
st.write("📖 **A Modern & Elegant Digital Library by SUMAYYA FAZAL HUSSAIN**")

# 📖 Add a New Book
if menu == "📖 Add a Book":
    st.header("➕ Add a New Book")
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("📖 Enter Book Title")
        author = st.text_input("✍️ Enter Author Name")

    with col2:
        year = st.number_input("📅 Publication Year", min_value=1000, max_value=2100, step=1)
        genre = st.selectbox("📂 Select Genre", ["Fiction", "Mystery", "Drama", "Romance", "Sci-Fi", "Fantasy", "Horror", "History", "Travel", "Philosophy"])

    read_status = st.checkbox("✅ Mark as Read")

    if st.button("➕ Add Book", use_container_width=True):
        library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
        save_library()
        st.success("✅ Book added successfully!", icon="✅")
        time.sleep(1)
        st.rerun()

# ❌ Remove a Book
elif menu == "❌ Remove a Book":
    st.header("🗑️ Remove a Book")
    book_titles = [book["title"] for book in library]

    if book_titles:
        book_to_remove = st.selectbox("Select a Book to Remove", book_titles)

        if st.button("❌ Remove", use_container_width=True):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library()
            st.warning("⚠️ Book removed!", icon="⚠️")
            time.sleep(1)
            st.rerun()
    else:
        st.warning("⚠️ No books available to remove.")

# 🔍 Search a Book
elif menu == "🔍 Search a Book":
    st.header("🔍 Search & Filter Your Books")
    search_query = st.text_input("🔍 Enter Book Title or Author").strip().lower()

    filtered_books = [book for book in library if search_query in book["title"].lower() or search_query in book["author"].lower()]

    if filtered_books:
        st.markdown('<div class="book-card-container">', unsafe_allow_html=True)
        for book in filtered_books:
            st.markdown(f"""
                <div class="book-card">
                    📖 **{book['title']}**  
                    ✍️ _by {book['author']}_  
                    📂 Genre: {book['genre']}  
                    📅 Year: {book['year']}  
                    ✅ Read: {"Yes" if book["read"] else "No"}  
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ No books found.")

# 📚 Library Collection
elif menu == "📚 Library Collection":
    st.header("📚 Your Library Collection")

    if library:
        st.markdown('<div class="book-card-container">', unsafe_allow_html=True)
        for book in library:
            st.markdown(f"""
                <div class="book-card">
                    📖 **{book['title']}**  
                    ✍️ _by {book['author']}_  
                    📂 Genre: {book['genre']}  
                    📅 Year: {book['year']}  
                    ✅ Read: {"Yes" if book["read"] else "No"}  
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ No books found in the library.")

# 📊 Library Dashboard
elif menu == "📊 Library Dashboard":
    st.header("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    unread_books = total_books - read_books
    genre_counts = pd.Series([book["genre"] for book in library]).value_counts()

    st.metric(label="📚 Total Books", value=total_books)
    st.metric(label="✅ Read Books", value=read_books)
    st.metric(label="📖 Unread Books", value=unread_books)

    st.bar_chart(genre_counts)

# 💾 Save & Exit
elif menu == "💾 Save & Exit":
    save_library()
    st.success("💾 Library saved successfully!", icon="💾")
    st.warning("🚪 You can now safely close the app!", icon="🚪")
