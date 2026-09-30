import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Yuga AI", page_icon="🤖")
st.title("🤖 யுகா (Yuga) - Personal Assistant")

# Sidebar la API Key vanga
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # நிலையான gemini-pro மாடல்
        model = genai.GenerativeModel("gemini-pro")

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
                prompt_with_identity = (
                    "உன் பெயர் யுகா (Yuga). நீ ஒரு அதிபுத்திசாலி AI உதவியாளர். "
                    "பயனர் கேட்கும் பின்வரும் கேள்விக்குத் தெளிவாகவும் அழகாகவும் பதிலளி:\n\n"
                    f"{prompt}"
                )
                response = model.generate_content(prompt_with_identity)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"பிழை ஏற்பட்டது: {e}")
else:
    st.info("தொடங்குவதற்கு இடதுபுற மெனுவில் உங்கள் Gemini API Key-ஐ உள்ளிடவும்.")
