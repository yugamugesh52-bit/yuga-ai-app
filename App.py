import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Yuga AI", page_icon="🤖")
st.title("🤖 யுகா (Yuga) - Personal Assistant")

# Sidebar-ல் API Key வாங்குதல்
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # உங்கள் API Key-ல் செயல்படும் மாடலைத் தானாகக் கண்டறிதல்
        supported_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        if not supported_models:
            st.error("உங்கள் API Key-ல் GenerateContent மாடல்கள் எதுவும் கிடைக்கவில்லை.")
        else:
            # flash அல்லது pro மாடலைத் தேர்ந்தெடுத்தல்
            selected_model = None
            for m in supported_models:
                if "flash" in m:
                    selected_model = m
                    break
            if not selected_model:
                selected_model = supported_models[0]

            model = genai.GenerativeModel(selected_model)

            # Chat history maintain பண்ண
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
                        "பயனர் கேட்கும் பின்வரும் கேள்விக்குத் தெளிவாகவும் மரியாதையுடனும் பதிலளி:\n\n"
                        f"{prompt}"
                    )
                    response = model.generate_content(prompt_with_identity)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"பிழை ஏற்பட்டது: {e}")
else:
    st.info("தொடங்குவதற்கு இடதுபுற மெனுவில் உங்கள் Gemini API Key-ஐ உள்ளிடவும்.")
