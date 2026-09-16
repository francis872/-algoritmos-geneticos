FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app

WORKDIR ${APP_HOME}

COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY . .

RUN mkdir -p outputs/feature_selection outputs/hyperparameters outputs/clustering && \
    chmod -R 755 outputs

RUN groupadd --system app && useradd --system --gid app --create-home --home-dir /home/app app && \
    chown -R app:app ${APP_HOME}

USER app

CMD ["python", "main.py"]
