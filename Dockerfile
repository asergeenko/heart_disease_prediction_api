# We need Java for H2O AutoML
FROM openjdk:11
COPY --from=python:3.7 / /

RUN pip install pandas uvicorn fastapi h2o

EXPOSE 80

COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
