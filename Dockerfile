FROM python:3
WORKDIR /yaml-converter-api
COPY ./src/requirements.txt /yaml-converter-api/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src/ /yaml-converter-api
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
