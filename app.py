import streamlit as st
import requests
st.title("RAG")
uploaded_file = st.file_uploader("Upload Your PDF", type = "pdf")
if uploaded_file:
    with open("Uploaded.pdf", "wb") as file:
        file.write(uploaded_file.getbuffer())
    st.success("PDF Uploaded Successfully!")
y = st.chat_input("Enter Your Prompt")
st.markdown(y)
if y:
    response = requests.post(
        "http://127.0.0.1:8000",
        json = {"x" : y}
    )
    if response.status_code == 200:
        r = response.json()
        st.write(r["answer"])
    else:
        st.write("Error")
