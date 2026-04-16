import streamlit as st
from PIL import Image
from solution import solution_master
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)


groq_client = Groq(api_key=os.getenv("GROQ_API_CHAT"))


if "debug_response" not in st.session_state:
    st.session_state.debug_response = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.title("Shaon AI Code Debugger App")
st.divider()


with st.sidebar:

    images = st.file_uploader(
        "Upload code error screenshots",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    pil_images = []

    if images:
        if len(images) > 2:
            st.error("Maximum 2 images allowed")
        else:
            cols = st.columns(len(images))
            for i in range(len(images)):
                img = Image.open(images[i])
                pil_images.append(img)
                with cols[i]:
                    st.image(images[i])

    selected_option = st.selectbox(
        "Choose mode",
        ("Hints", "Solution"),
        index=None
    )

    debug_btn = st.button("Debug Code")


if debug_btn:

    if not images:
        st.error("Please upload images")
    elif not selected_option:
        st.error("Please select Hints or Solution")
    else:
        with st.spinner("Gemini is analyzing your code..."):

            result = solution_master(pil_images, selected_option)
            st.session_state.debug_response = result

            st.success("Analysis complete!")


if st.session_state.debug_response:

    st.subheader("Gemini Debug Result")
    st.markdown(st.session_state.debug_response)


if st.session_state.debug_response:

    st.divider()
    st.subheader("Chat with AI (Groq)")

    user_query = st.text_input("Ask follow-up question")

    if st.button("Ask AI"):

        if user_query:

            with st.spinner("Groq is thinking..."):

                chat_prompt = f"""
You are a helpful programming assistant.

Context (from Gemini analysis):
{st.session_state.debug_response}

User question:
{user_query}

Answer clearly and simply.
"""

                response = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "user", "content": chat_prompt}
                    ]
                )

                answer = response.choices[0].message.content

                st.session_state.chat_history.append((user_query, answer))


if st.session_state.chat_history:

    st.subheader("Chat History")

    for q, a in st.session_state.chat_history[::-1]:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**AI:** {a}")
        st.divider()