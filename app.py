import streamlit as st
import requests
import time

def research_topic(topic):
    url = "http://0.0.0.0:8000/research_topic"
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "topic": topic
    }
    response = requests.post(url=url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["results"]["raw"]
    else:
        return "Error"

def main():
    st.title("AI Researcher Agent")
    topic = st.text_input("Research Topic")
    
    if "button1" not in st.session_state:
        st.session_state.button1 = False

    if st.button("Research"):
        st.session_state.button1 = True

    if st.session_state.button1:
        start_time = time.time()
        with st.spinner("Researching..."):
            gif_path = "loading.gif"
            gif_placeholder = st.empty()
            gif_placeholder.image(gif_path)
            results = research_topic(topic)
            end_time = time.time()
            elapsed_time = end_time - start_time
            if results:
                gif_placeholder.empty()
                st.markdown("<h3 style='color:green;'>Research Completed</h3>", unsafe_allow_html=True)
                st.write("Research Report:")
                st.write(results)
                st.write(f"Elapsed time: {elapsed_time:.2f} seconds")
            else:
                st.error("Error occurred during research")

if __name__ == "__main__":
    main()