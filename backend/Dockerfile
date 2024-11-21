FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
# Nutze Gunicorn als Produktionsserver nein ich benutze waitress als produktionsserver
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]