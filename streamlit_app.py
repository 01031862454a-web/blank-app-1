import streamlit as st

# st.title("🎈 My new app")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )
import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="영어 공부 웹", layout="centered")
st.title("📚 영어 단어 공부")

# 단어 데이터
words = [
    {"word": "apple", "meaning": "사과"},
    {"word": "book", "meaning": "책"},
    {"word": "study", "meaning": "공부하다"},
    {"word": "friend", "meaning": "친구"},
    {"word": "computer", "meaning": "컴퓨터"}
]

# --- 상태 관리 (Streamlit은 매번 rerun되므로 session_state 필요)
if "mode" not in st.session_state:
    st.session_state.mode = "study"   # study / review
if "quiz_order" not in st.session_state:
    st.session_state.quiz_order = []
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0

# --- 단어 학습 모드
if st.session_state.mode == "study":
    st.subheader("단어 학습")

    for item in words:
        if st.button(item["word"]):
            st.info(f"{item['word']} → {item['meaning']}")

    if st.button("복습하기"):
        st.session_state.mode = "review"
        st.session_state.quiz_order = random.sample(range(len(words)), len(words))
        st.session_state.quiz_index = 0
        st.session_state.correct_count = 0
        st.rerun()

# --- 복습 모드
elif st.session_state.mode == "review":
    st.subheader("복습 퀴즈")

    idx = st.session_state.quiz_order[st.session_state.quiz_index]
    word, meaning = words[idx]["word"], words[idx]["meaning"]

    st.write(f"**{word}** 의 뜻은?")

    user_answer = st.text_input("정답 입력:", key=f"q{st.session_state.quiz_index}")
    submit = st.button("제출")

    if submit:
        if user_answer.strip() == meaning:
            st.success("정답! 🎉")
            st.session_state.correct_count += 1
        else:
            st.error(f"오답 😢 (정답: {meaning})")

        st.session_state.quiz_index += 1

        if st.session_state.quiz_index >= len(words):
            st.success(f"🎉 복습 완료! 정답 {st.session_state.correct_count} / {len(words)}")
            if st.button("다시하기"):
                st.session_state.mode = "review"
                st.session_state.quiz_order = random.sample(range(len(words)), len(words))
                st.session_state.quiz_index = 0
                st.session_state.correct_count = 0
                st.rerun()
            if st.button("그만하기"):
                st.session_state.mode = "study"
                st.rerun()
        else:
            st.rerun()

    if st.button("그만하기"):
        st.session_state.mode = "study"
        st.rerun()
