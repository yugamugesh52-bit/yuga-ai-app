import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Yuga AI", page_icon="🤖")
st.title("🤖 யுகா (Yuga) - Personal Assistant")

# Sidebar-ல் API Key வாங்குதல்
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")

        # Chat history maintain பண்ணுதல்
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
                prompt_full = (
                    "உன் பெயர் யுகா (Yuga). நீ ஒரு அதிபுத்திசாலி AI உதவியாளர். "
                    "பயனர் கேட்கும் கேள்விக்கு நேரடியாக, தெளிவாகவும் தமிழிலும் பதிலளி:\n\n"
                    f"{prompt}"
                )
                
                # நேரடி பதில் வரவழைத்தல்
                response = model.generate_content(prompt_full)
                reply_text = response.text
                
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
                
    except Exception as e:
        st.error(f"பிழை ஏற்பட்டது: {e}")
else:
    st.info("தொடங்குவதற்கு இடதுபுற மெனுவில் உங்கள் Gemini API Key-ஐ உள்ளிடவும்.")
