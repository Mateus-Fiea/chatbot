import streamlit as st
from fuzzywuzzy import fuzz, process
import json

st.set_page_config(page_title="Chat de Regras – Auditoria, Moskit e 360", layout="centered")
st.title("🤖 Chat Inteligente – Regras, Moskit e Solução 360")
st.write("Digite sua dúvida sobre modelos de gestão, Moskit ou 360:")

@st.cache_data
def carregar_base():
    with open("base_conhecimento.json", "r", encoding="utf-8") as f:
        return json.load(f)

base_conhecimento = carregar_base()

pergunta = st.text_input("Sua dúvida:")

def encontrar_resposta(pergunta_usuario):
    todas_chaves = []
    mapa_respostas = {}

    for categoria, perguntas in base_conhecimento.items():
        for chave, resposta in perguntas.items():
            todas_chaves.append(chave)
            mapa_respostas[chave] = resposta

    melhor, score = process.extractOne(pergunta_usuario.lower(), todas_chaves, scorer=fuzz.partial_ratio)

    if score >= 70:
        return mapa_respostas[melhor]
    else:
        sugestões = [m for m, s in process.extract(pergunta_usuario.lower(), todas_chaves, limit=3) if s >= 50]
        if sugestões:
            sugestao_txt = "\n".join([f"- {s}" for s in sugestões])
            return f"🤔 Não encontrei resposta exata, mas talvez você quis dizer:\n\n{suggestao_txt}"
        return None

if pergunta:
    resposta = encontrar_resposta(pergunta)
    if resposta:
        st.success(resposta)
    else:
        st.error("❌ Ainda não sei responder essa pergunta. Fale com o Mateus.")

if "historico" not in st.session_state:
    st.session_state.historico = []

if pergunta:
    st.session_state.historico.append(pergunta)

if st.session_state.historico:
    with st.expander("📜 Ver histórico"):
        for h in reversed(st.session_state.historico[-5:]):
            st.markdown(f"• {h}")
