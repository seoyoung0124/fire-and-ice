import streamlit as st

# Set page configuration with a dark theme background feel
st.set_page_config(page_title="페이지 만들기 테스트", page_icon="🧪", layout="centered")

# Custom CSS to ensure a dark background styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .test-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-top: 20vh;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the text on the page
st.markdown(
    '<div class="test-title">페이지 만들기 테스트</div>', unsafe_allow_html=True
)
