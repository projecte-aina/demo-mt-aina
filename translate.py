import streamlit as st
import sentencepiece as spm
import ctranslate2
import nltk
from nltk import sent_tokenize

nltk.download('punkt')

# Title for the page and nice icon
st.set_page_config(page_title="Projecte Aina: Model de Traducció Català-Castellà:",
                   header_title="Aina MT",
                   menu_items={
                       'Get Help': 'https://huggingface.co/projecte-aina',
                       'Report a bug': 'https://github.com/projecte-aina/demo-mt-aina/issues',
                       'About': None,
                   },
                   layout='wide')

models = {
    "Català-Castellà": ("models/mt-aina-ca-es/spm.model", "models/mt-aina-ca-es"),
    "Català-Anglès": ("models/mt-aina-ca-en/spm.model", "models/mt-aina-ca-en"),
    "Anglès-Català": ("models/mt-aina-en-ca/spm.model", "models/mt-aina-en-ca")
}


@st.cache(allow_output_mutation=True)
def load_models(lang_pair, device="cpu"):
    """Load CTranslate2 model and SentencePiece models

    Args:
        lang_pair (str): Language pair to load the models for
        device (str): "cpu" (default) or "cuda"
    Returns:
        CTranslate2 Translator and SentencePieceProcessor objects to load the models
    """
    sp_model = spm.SentencePieceProcessor(models[lang_pair][0])
    translator = ctranslate2.Translator(models[lang_pair][1])

    return translator, sp_model


def translate(source, translator, sp_model):
    """Use CTranslate model to translate a sentence

    Args:
        source (str): Source sentences to translate
        translator (object): Object of Translator, with the CTranslate2 model
        sp_model (object): Object of SentencePieceProcessor, with the SentencePiece source model
    Returns:
        Translation of the source text
    """

    source_sentences = sent_tokenize(source)
    source_tokenized = sp_model.encode(source_sentences, out_type=str)
    translations = translator.translate_batch(source_tokenized)
    translations = [translation[0]["tokens"] for translation in translations]
    translations_detokenized = sp_model.decode(translations)
    translation = " ".join(translations_detokenized)
    translation = translation.replace(' ⁇', ':')
    return translation


# st.set_page_config(page_title="AINA CA-ES", page_icon="🤖")
# Header
st.markdown("#### Traductor Automàtic")

st.markdown("""
<style>
.big-font {
    font-size:1.1rem !important;
}
</style>
""", unsafe_allow_html=True)

with st.expander("ℹ️ - Sobre Traductor Automàtic", expanded=False):
    st.markdown(
        '<p class=big-font>Versió online dels nostres traductors neuronals. Pots trobar més informació  i veure com fer-los servir localment en aquest <a href="https://huggingface.co/projecte-aina">enllaç</a>.</p>',
        unsafe_allow_html=True)

    st.write(f"[Descarrega el model Català-Castellà](https://huggingface.co/projecte-aina/mt-aina-ca-es)")
    st.write(f"[Descarrega el model Català-Anglès](https://huggingface.co/projecte-aina/mt-aina-ca-en)")
    st.write(f"[Descarrega el model Anglès-Català](https://huggingface.co/projecte-aina/mt-aina-en-ca)")

# Form to add your items
with st.form("my_form", clear_on_submit=True):
    # Dropdown menu to select a language pair
    lang_pair = st.selectbox("Selecciona l'idioma a traduir:",
                             ("Català-Castellà", "Català-Anglès", "Anglès-Català"))
    # st.write('You selected:', lang_pair)

    # Textarea to type the source text.
    user_input = st.text_area("Escriu el text que vols traduir", key='user_input', max_chars=5000)

    # Load models
    translator, sp_model = load_models(lang_pair, device="cpu")

    # Create a button
    submitted = st.form_submit_button("Traduir")
    # If the button pressed, print the translation
    # Here, we use "st.info", but you can try "st.write", "st.code", or "st.success".
    if submitted:
        if len(user_input) > 0 and user_input.strip() != "":
            with st.spinner(text="Traduint ..."):
                # Translate with CTranslate2 model
                translation = translate(user_input, translator, sp_model)
                st.write("Text d'entrada")
                st.warning(user_input)
                st.write("Traducció")
                st.info(translation)
        else:
            st.error('Si us plau, escriu el text que vols traduir', icon="⚠")
    # If the button pressed, print the translation
    # Here, we use "st.info", but you can try "st.write", "st.code", or "st.success".

# Optional Style
# Source: https://towardsdatascience.com/5-ways-to-customise-your-streamlit-ui-e914e458a17c
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# st.markdown(""" <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style> """, unsafe_allow_html=True)
