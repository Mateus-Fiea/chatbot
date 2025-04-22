import streamlit as st
from fuzzywuzzy import fuzz, process
import json

st.set_page_config(page_title="Chat de Regras – Auditoria, Moskit e 360", layout="centered")
st.title("🤖 Chat Inteligente – Regras, Moskit e Solução 360")
st.write("Digite sua dúvida sobre modelos de gestão, Moskit ou 360:")

@st.cache_data(ttl=0)
def carregar_base():
    with open("base_conhecimento.json", "r", encoding="utf-8") as f:
        return json.load(f)

base_conhecimento = carregar_base()

pergunta = st.text_input("Sua dúvida:")

def encontrar_resposta(pergunta_usuario):
    todas_chaves = []
    mapa_respostas = {}
    palavras_chave = []

    for categoria, perguntas in base_conhecimento.items():
        for chave, resposta in perguntas.items():
            todas_chaves.append(chave)
            mapa_respostas[chave] = resposta

            # Coleta palavras-chave da chave para ajudar na sugestão
            palavras_chave.extend(chave.lower().split())

    # Verifica se há correspondência exata com a pergunta
    melhor, score = process.extractOne(pergunta_usuario.lower(), todas_chaves, scorer=fuzz.token_sort_ratio)

    if score >= 70:
        return mapa_respostas[melhor]
    else:
        # Sugestões de perguntas relacionadas com base nas palavras-chave
        sugestoes = [m for m, s in process.extract(pergunta_usuario.lower(), todas_chaves, limit=3) if s >= 50]
        if sugestoes:
            sugestao_txt = "\n".join([f"- {s}" for s in sugestoes])
            return f"🤔 Não encontrei resposta exata, mas talvez você quis dizer:\n\n{suggestao_txt}"

        # Se não houver correspondência exata ou sugestões, tenta sugerir palavras-chave
        palavras_usuario = pergunta_usuario.lower().split()
        palavras_encontradas = [p for p in palavras_usuario if p in palavras_chave]

        if palavras_encontradas:
            # Se encontrou palavras-chave relacionadas, sugere as perguntas
            sugestao_txt = "\n".join([f"- {s}" for s in palavras_encontradas])
            return f"🤔 Não encontrei resposta exata, mas com base nas palavras-chave, talvez você quis dizer:\n\n{suggestao_txt}"
        
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

