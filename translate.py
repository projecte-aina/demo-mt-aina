import streamlit as st
import sentencepiece as spm
import ctranslate2
from nltk import sent_tokenize



# Title for the page and nice icon
st.set_page_config(page_title="Projecte Aina: Model de Traducció Català-Castellà:", 
                    header_title="Aina MT", 
                    menu_items={
                            'Get Help': 'https://huggingface.co/projecte-aina',
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
    translation = translation.replace(' ⁇', ':' )
    return translation

#st.set_page_config(page_title="AINA CA-ES", page_icon="🤖")
# Header
st.title("Traductor Automàtic")
st.markdown("""
<style>
.big-font {
    font-size:1.1rem !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class=big-font>Versió online dels nostres traductors neuronals. Pots trobar més informació  i veure com fer-los servir localment en aquest <a href="https://huggingface.co/projecte-aina">enllaç</a>.</p>', unsafe_allow_html=True)

# Form to add your items
with st.form("my_form", clear_on_submit=True):
    
    # Dropdown menu to select a language pair
    lang_pair = st.selectbox("Selecciona l'idioma a traduïr:",
                             ("Català-Castellà", "Català-Anglès",  "Anglès-Català"))
    # st.write('You selected:', lang_pair)


    # Textarea to type the source text.
    user_input = st.text_area("Escriu el text que vols traduïr", key='user_input', max_chars=5000)

    # Load models
    translator, sp_model = load_models(lang_pair, device="cpu")
    
    # Translate with CTranslate2 model
    translation = translate(user_input, translator, sp_model)

    # Create a button
    submitted = st.form_submit_button("Traduïr")
    # If the button pressed, print the translation
    # Here, we use "st.info", but you can try "st.write", "st.code", or "st.success".
    if submitted:
        st.write("Text d'entrada")
        st.warning(user_input)
        st.write("Traducció")
        st.info(translation)


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


st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)
