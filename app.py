import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Corretor de Redação IA", page_icon="📝")

st.title("📝 Corretor de Redação Inteligente")
st.subheader("Tire uma foto e receba sua nota em segundos")

# Configurar a API Key (No Streamlit Cloud, use Secrets)
os_api_key = st.sidebar.text_input("Cole sua Google API Key aqui", type="password")

if os_api_key:
    genai.configure(api_key=os_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Opção de tirar foto ou carregar arquivo
    foto = st.camera_input("Capture a foto da sua redação")
    
    if foto:
        img = Image.open(foto)
        st.image(img, caption="Redação capturada", use_container_width=True)
        
        if st.button("Avaliar Redação"):
            with st.spinner("Analisando caligrafia e conteúdo..."):
                # O Prompt mágico
                prompt = """
                Analise esta imagem de uma redação manuscrita. 
                1. Transcreva o texto (se possível).
                2. Dê uma nota de 0 a 100% baseada em critérios de gramática, estrutura e coesão.
                3. Aponte exatamente onde o aluno deve melhorar.
                4. Seja motivador, mas honesto.
                Retorne a nota em destaque.
                """
                
                # Envia a imagem diretamente para a IA
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.markdown("### 📊 Resultado da Avaliação")
                st.write(response.text)
else:
    st.warning("Por favor, insira sua API Key do Google Gemini na barra lateral para começar.")
