import streamlit as st
import openai
import re

st.set_page_config(page_title="AI Doc Number Generator", layout="centered")

st.title("📄 AI Destekli Doküman Numarası Üretici")

# OpenAI API Key – Streamlit Secrets ile bağlan
openai.api_key = st.secrets["openai"]["api_key"]

user_input = st.text_input("Belge açıklamasını girin (örn: Foundation plan for turbine building):")

if st.button("Numara Üret"):
    if user_input.strip() == "":
        st.warning("Lütfen bir açıklama girin.")
    else:
        with st.spinner("Yapay zeka yorumluyor..."):
            prompt = f"""You are a document control assistant. Extract the following from this engineering document description: 
- Discipline code (T1)
- Document type (T2)
- Sub-document type (T3)

Return in format:
Discipline: <code>
Document Type: <code>
Sub Type: <code>

Input: {user_input}"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content

            discipline = re.search(r"Discipline:\s*(\w+)", content)
            doc_type = re.search(r"Document Type:\s*(\w+)", content)
            sub_type = re.search(r"Sub Type:\s*(\w+)", content)

            if discipline and doc_type and sub_type:
                doc_number = f"ROM-34-XXX-{discipline.group(1)}{doc_type.group(1)}{sub_type.group(1)}-CEI-001_A"
                st.success(f"✅ Üretilen Doküman Numarası: `{doc_number}`")
            else:
                st.error("Yorumlama başarısız. Lütfen farklı bir açıklama girin.")
