# Usa una imagen base con Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias de sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev curl

# Copia archivo de configuración de poetry
COPY pyproject.toml ./

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Configura e instala dependencias sin crear venvs
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copia el resto del código
COPY . .

# Expone el puerto por defecto de Uvicorn
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
