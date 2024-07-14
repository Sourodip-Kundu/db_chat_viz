import streamlit as st
from helper import get_answer, get_code



# Page title and subtitle
st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> Chat-To-Visualization</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>Creating Visualisations using Natural Language with ChatGPT</h2>", unsafe_allow_html=True)

# # Sidebar for navigation or additional options
# st.sidebar.title("Navigation")
# st.sidebar.write("Select an option from the sidebar.")

# Textbox in the middle of the page
st.markdown("<div style='display: flex; justify-content: center;'><div style='width: 50%;'>", unsafe_allow_html=True)
user_input = st.text_area("Please provide your question", height=150)
submit_button = st.button("Submit")
st.markdown("</div></div>", unsafe_allow_html=True)

# Display user input (for testing purposes)
if user_input:
    st.write("You asked:", user_input)

    topic  = get_answer(user_input)

    st.write("Your Answer:", topic)
    
    with st.spinner("Processing for creating visualization..."):
        with st.container():
            st.markdown("<h3 style='text-align: center;'>Visualization</h3>", unsafe_allow_html=True)
            text = get_code(topic)
            
            exec(text)

