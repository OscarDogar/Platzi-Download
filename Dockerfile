FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg fontconfig && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Fontconfig writable cache fix
ENV HOME=/tmp
ENV XDG_CACHE_HOME=/tmp/.cache
RUN mkdir -p /tmp/.cache/fontconfig && chmod -R 777 /tmp/.cache

COPY . /app

RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "src/main.py"]