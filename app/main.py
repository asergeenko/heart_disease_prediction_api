from fastapi import FastAPI, Request, status,Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from fastapi.responses import HTMLResponse

import h2o
import pandas as pd
import os

cwd = os.getcwd()

h2o.init()
model = h2o.load_model("/app/GLM_1_AutoML_20210903_182621")
#from enum import IntEnum

app = FastAPI()

class Item(BaseModel):
    age: int
    sex: bool
    cp: int
    trestbps: int
    chol: int
    fbs: bool
    restecg: int
    thalach: int
    exang: bool
    oldpeak: float
    slope: int
    ca: int
    thal: int

    @validator('cp')
    def check_cp(cls, v):
        if v < 0 or v > 3:
            raise ValueError('must be in [0-3]')
        return v

    @validator('restecg')
    def check_restecg(cls, v):
        if v < 0 or v > 2:
            raise ValueError('must be in [0-2]')
        return v


    @validator('ca')
    def check_ca(cls, v):
        if v < 0 or v > 3:
            raise ValueError('must be in [0-3]')
        return v

    @validator('thal')
    def check_thal(cls, v):
        if v < 1 or v > 3:
            raise ValueError('must be in [1-3]')
        return v

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

@app.get("/predict")
def predict(data: Item=Depends()):
    """
    Predict the heart disease from follwing inputs:

    - **age**: age [int],
    - **sex**: sex [0,1],
    - **cp**: chest pain type [0-3],
    - **trestbps**: resting blood pressure [int],
    - **chol**: serum cholestoral in mg/dl [int],
    - **fbs**: fasting blood sugar > 120 mg/dl [0,1],
    - **restecg**: resting electrocardiographic results [0-2],
    - **thalach**: maximum heart rate achieved [int],
    - **exang**: exercise induced angina [0,1],
    - **oldpeak**: = ST depression induced by exercise relative to rest [float],
    - **slope**: the slope of the peak exercise ST segment[int],
    - **ca**: number of major vessels (0-3) colored by flourosopy [0-3],
    - **thal**: thal [1-3]
    """
    df = h2o.H2OFrame(pd.DataFrame({key:[value] for key,value in dict(data).items()}))
    for col in df.col_names:
        if col in ['sex','cp','fbs','restecg','exang','slope','ca','thal']:
            df[col] = df[col].asfactor() 
    prediction = model.predict(df)[0,0]
    return {'target': int(prediction)}

@app.get("/")
async def root():
    html_content = '''
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>Heart Disease UCI prediction</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>
<div class="container">
<h2>Heart Disease UCI prediction</h2>
<p>Heart Disease prediction model based on this <a href="https://archive.ics.uci.edu/ml/datasets/Heart+Disease">dataset</a> using the H2O AutoML <a href="https://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/glm.html">Generalized Linear Model</a>.</p>

<ul>
<li><a href="/docs#/default/predict_predict_get">Documentation</a></li>
<li><a href="https://github.com/asergeenko/heart_disease_prediction_api">Git repo</a></li>
</ul>
<h3>Sample requests:</h3>
<pre><code>
curl -X 'GET' &#92;
  'http://127.0.0.1/predict?age=67&sex=true&cp=0&trestbps=160&chol=286&fbs=false&restecg=0&thalach=108&exang=true&oldpeak=1.5&slope=1&ca=3&thal=2' &#92;
  -H 'accept: application/json'
</code></pre>
<pre><code>
curl -X 'GET' &#92;
  'http://127.0.0.1/predict?age=45&sex=true&cp=2&trestbps=135&chol=233&fbs=false&restecg=1&thalach=180&exang=true&oldpeak=0.4&slope=2&ca=0&thal=2' &#92;
  -H 'accept: application/json'
</code></pre>
</div>
</body>
</html>	
'''
    return HTMLResponse(content=html_content, status_code=200)
