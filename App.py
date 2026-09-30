
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Yuga AI", page_icon="🤖")
st.title("🤖 யுகா (Yuga) - Personal Assistant")

# Sidebar la API Key vanga
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    system_instruction = (
        "உன் பெயர் யுகா (Yuga). நீ ஒரு அதிபுத்திசாலி மற்றும் நம்பகமான தனிப்பட்ட AI உதவியாளர். "
        "பயனர் கேட்கும் கேள்விகளுக்குத் தெளிவாகவும் சுருக்கமாகவும் தமிழ் மற்றும் ஆங்கிலத்தில் பதிலளிக்க வேண்டும். "
        "எப்போதும் மரியாதையுடனும் உதவியாகவும் உரையாட வேண்டும்."
    )
    
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)

    # Chat history maintain panna
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box
    if prompt := st.chat_input("யுகாவிடம் கேளுங்கள்..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("தொடங்குவதற்கு இடதுபுற மெனுவில் உங்கள் Gemini API Key-ஐ உள்ளிடவும்.")
