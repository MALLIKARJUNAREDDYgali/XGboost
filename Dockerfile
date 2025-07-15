FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y build-essential

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ✅ Use Railway's required port
EXPOSE 8080

# ✅ Run Streamlit on port 8080
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
