import streamlit as st
from groq import Groq
import pytesseract
from PIL import Image
import numpy as np

# Configuração da página
st.set_page_config(page_title="Corretor Groq", page_icon="⚡")

st.title("⚡ Corretor de Redação Ultra-Rápido")

# Configuração do Cliente Groq
# Nota: No Streamlit Cloud, oculte sua chave em "Secrets"
client = Groq(api_key="SUA_CHAVE_AQUI")

foto = st.camera_input("Tire foto da sua redação")

if foto:
    img = Image.open(foto)
    st.image(img, caption="Imagem carregada", width=300)
    
    with st.spinner("Lendo texto e avaliando..."):
        # 1. Extrair texto da imagem (OCR)
        # Certifique-se de ter o tesseract instalado no ambiente
        texto_extraido = pytesseract.image_to_string(img, lang='por')
        
        if len(texto_extraido.strip()) < 10:
            st.error("Não consegui ler o texto. Tente tirar uma foto mais nítida e de perto.")
        else:
            # 2. Mandar para o Groq analisar
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um professor corretor de redações. Avalie o texto e dê uma nota de 0 a 100%. Aponte erros e melhorias."
                    },
                    {
                        "role": "user",
                        "content": f"Analise esta redação:\n\n{texto_extraido}",
                    }
                ],
                model="llama3-8b-8192", # Modelo rápido do Groq
            )

            # 3. Exibir resultado
            resultado = chat_completion.choices[0].message.content
            st.success("Avaliação Concluída!")
            st.markdown("### 📝 Análise da IA")
            st.write(resultado)
