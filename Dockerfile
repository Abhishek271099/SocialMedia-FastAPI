FROM python:3.11

WORKDIR /user/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app", "--port", "8000"]

