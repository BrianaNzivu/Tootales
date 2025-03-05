import streamlit as st
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="D Tootales", layout="wide")

def load_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

html_path = os.path.join("html", "home.html")
html_content = load_file(html_path)

components.html(html_content, height=800, scrolling=True)
