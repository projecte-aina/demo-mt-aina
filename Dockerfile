FROM python:3.8-slim

RUN apt-get update && apt-get install --no-install-recommends -y git git-lfs && \
     rm -rf /var/lib/{apt,dpkg,cache,log}

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /usr/src/app

RUN git lfs install
RUN git clone https://huggingface.co/projecte-aina/mt-aina-en-ca ./models/mt-aina-en-ca
RUN git clone https://huggingface.co/projecte-aina/mt-aina-ca-en ./models/mt-aina-ca-en
RUN git clone https://huggingface.co/projecte-aina/mt-aina-ca-es ./models/mt-aina-ca-es


COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir  --upgrade -r requirements.txt

COPY .streamlit /usr/src/app/.streamlit

COPY translate.py .

ENTRYPOINT ["streamlit", "run", "translate.py", "--server.port", "8083", "--browser.serverAddress", "0.0.0.0"]