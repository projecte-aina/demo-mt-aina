# Demo MT Aina

Instrucciones para ejecutar en local la demo de traducción del proyecto Aina. Ahora utilizamos tres modelos:
    - Catalán - Castellano
    - Catalán - Inglés
    - Inglés - Catalán 


## Requisitos

La demo necesita las siguientes librerias:
    - ctranslate2>=2.1.0
    - nltk>=3.6.2
    - sentencepiece>=0.1.96
    - streamlit>=0.84.0
    - watchdog>=2.1.3 

```
pip3 install -r requirements.txt
```

## Modelos

Dentro del repositorio, los modelos están en la carpeta models. Cada uno tiene el mismo nombre que en [hugging face](ihttps://huggingface.co/projecte-aina). En cada carpeta hay que copiar tres ficheros:  
    - model.bin: Los pesos de la red que entrenamos.
    - shared_vocabulary.txt: El vocabulario que usa el modelo para representar los tokens.
    - spm.model: El modelo de SentencePiece que usamos para preprocesar los datos.

 Hay que copiar estos tres modelos:
    - projecte-aina/mt-aina-en-ca
    - projecte-aina/mt-aina-ca-es
    - projecte-aina/mt-aina-ca-es

Se pueden descargar de huggingface usando snapshot_download:

```
from huggingface_hub import snapshot_download
model_dir = snapshot_download(repo_id="projecte-aina/mt-aina-en-ca", revision="main")

```

# Ejecutar la demo

Una vez los modelos están en la carpeta models, se puede ejecutar con el comando:

```
streamlit run translate.py
```



