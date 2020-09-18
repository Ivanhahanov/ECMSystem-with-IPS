FROM python:3.8

RUN pip install fastapi uvicorn python-multipart elasticsearch>=7.8.0 aiohttp pdfminer.six

EXPOSE 80

COPY app /app

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "80"]