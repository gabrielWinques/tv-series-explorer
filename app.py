import streamlit as st
from dotenv import load_dotenv

from view.config.dependencies import criar_dependencias

load_dotenv()

st.set_page_config(page_title="TV Series Explorer", page_icon="📺", layout="wide")


@st.cache_resource
def obter_dependencias():
    return criar_dependencias()


def renderizar_serie(serie, deps, prefixo):
    with st.container(border=True):
        col_imagem, col_info = st.columns([1, 3])

        with col_imagem:
            if serie.imagem_url:
                st.image(serie.imagem_url)

        with col_info:
            st.subheader(serie.nome)
            st.caption(" · ".join(serie.generos or []) or "Sem gêneros")
            if serie.avaliacao is not None:
                st.write(f"⭐ {serie.avaliacao}")
            st.write(serie.sinopse or "Sem sinopse disponível.")

            col_fav, col_insight = st.columns(2)

            if col_fav.button("Favoritar", key=f"{prefixo}_fav_{serie.id}"):
                try:
                    deps.favoritar_serie.executar(serie)
                    st.toast("Série favoritada!")
                except Exception:
                    st.error("Não foi possível favoritar agora.")

            if col_insight.button("Gerar insight", key=f"{prefixo}_ins_{serie.id}"):
                with st.spinner("Gerando insight..."):
                    st.session_state["insights"][serie.id] = deps.gerar_insight.executar(serie)

            insight = st.session_state["insights"].get(serie.id)
            if insight:
                st.info(insight)


st.session_state.setdefault("resultados", [])
st.session_state.setdefault("insights", {})

deps = obter_dependencias()

st.title("📺 TV Series Explorer")
aba_busca, aba_favoritos = st.tabs(["Buscar", "Favoritos"])

with aba_busca:
    nome = st.text_input("Nome da série")

    if st.button("Buscar"):
        try:
            st.session_state["resultados"] = deps.buscar_serie.executar(nome)
        except ValueError as erro:
            st.warning(str(erro))
        except Exception:
            st.error("Não foi possível buscar séries agora. Tente novamente.")

    for serie in st.session_state["resultados"]:
        renderizar_serie(serie, deps, prefixo="busca")

with aba_favoritos:
    try:
        favoritas = deps.listar_favoritas.executar()
    except Exception:
        st.error("Não foi possível carregar os favoritos.")
        favoritas = []

    if not favoritas:
        st.info("Você ainda não favoritou nenhuma série.")

    for serie in favoritas:
        renderizar_serie(serie, deps, prefixo="fav")