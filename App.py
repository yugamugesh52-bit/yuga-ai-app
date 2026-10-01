import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Yuga AI", page_icon="🤖")
st.title("🤖 யுகா (Yuga) - Personal Assistant")

# Sidebar-ல் API Key உள்ளிடுதல்
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")

        # Chat history
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
                    "உன் பெயர் யுகா (Yuga). நீ ஒரு அன்பான, புத்திசாலியான தமிழ் AI உதவியாளர். "
                    "முக்கிய விதி: பயனர் Tanglish (ஆங்கில எழுத்துக்களில் தமிழ்) அல்லது ஆங்கிலத்தில் பேசினாலும், "
                    "நீ எப்போதும் தமிழிலேயே (Tamil script) மிகத் தெளிவாகவும் இயல்பாகவும் பதிலளிக்க வேண்டும். "
                    "தேவைப்பட்டால் மட்டுமே எண்கள், ரயில் பெயர்கள், இடங்களின் பெயர்களை ஆங்கிலத்தில் குறிப்பிடலாம்.\n\n"
                    f"பயனர் கேள்வி: {prompt}"
                )

                # Rate Limit (429) பிழையைத் தவிர்க்க தானியங்கி Retry அமைப்பு
                reply_text = None
                for attempt in range(3):
                    try:
                        response = model.generate_content(prompt_full)
                        reply_text = response.text
                        break
                    except Exception as err:
                        if "429" in str(err) and attempt < 2:
                            time.sleep(12)  # Rate limit முடிவடையும் வரை சிறிது நேரம் காத்திருந்து மீண்டும் முயற்சிக்கும்
                        else:
                            raise err

                if reply_text:
                    st.markdown(reply_text)
                    st.session_state.messages.append({"role": "assistant", "content": reply_text})

    except Exception as e:
        if "429" in str(e):
            st.warning("அதிக முறை கேள்வி கேட்கப்பட்டுள்ளது. தயவுசெய்து 15 விநாடிகள் கழித்து மீண்டும் ஒருமுறை முயற்சிக்கவும்.")
        else:
            st.error(f"பிழை ஏற்பட்டது: {e}")
else:
    st.info("தொடங்குவதற்கு இடதுபுற மெனுவில் உங்கள் Gemini API Key-ஐ உள்ளிடவும்.")
