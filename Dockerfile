FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 5000

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

RUN groupadd -r admin && useradd -r -g admin admin
RUN chown -R admin:admin /app/

RUN apt-get update \
    && apt-get install -y g++ gcc+ curl libpq-dev unixodbc unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=10s --timeout=5s \
    CMD curl -f http://localhost:5000/media/health || exit 1

SHELL ["/bin/bash"]
USER admin

CMD ["/bin/bash", "/app/entrypoint.sh"]