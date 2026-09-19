FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    sqlalchemy \
    python-dotenv \
    passlib \
    bcrypt==4.0.1 \
    python-jose \
    python-multipart\
    email-validator

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

