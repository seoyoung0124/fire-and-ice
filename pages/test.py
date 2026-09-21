import streamlit as st

# 페이지 설정
st.set_page_config(page_title="페이지 만들기 테스트", page_icon="🧪", layout="centered")

# 검은색 배경 및 줄어든 폰트 크기 스타일 적용
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .test-title {
        font-size: 1.8rem; /* 폰트 크기를 기존 3rem에서 1.8rem으로 줄임 */
        font-weight: bold;
        text-align: center;
        margin-top: 20vh;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 텍스트 출력
st.markdown(
    '<div class="test-title">페이지 만들기 테스트</div>', unsafe_allow_html=True
)
