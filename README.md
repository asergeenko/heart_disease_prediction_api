# Heart Disease UCI prediction API
Heart Disease prediction model based on this (dataset)[https://archive.ics.uci.edu/ml/datasets/Heart+Diseaset] using the H2O AutoML (Generalized Linear Model)[https://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/glm.html]. 

## Endpoints
### /predict
Metod: POST

#### Request parameters
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

#### Response

**OK**

*{"target": 1}* or *{"target": 0}*

**Error**

*{"detail":[{"loc":["body","sex"],"msg":"value could not be parsed to a boolean","type":"type_error.bool"}]}*

**Sample requests**

$ curl -X 'POST' \
  'http://127.0.0.1/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 67,
  "sex": 1,
  "cp": 0,
  "trestbps": 160,
  "chol": 286,
  "fbs": 0,
  "restecg": 0,
  "thalach": 108,
  "exang": 1,
  "oldpeak": 1.5,
  "slope": 1,
  "ca": 3,
  "thal": 2
}'

$ curl -X 'POST' \
  'http://127.0.0.1/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 45,
  "sex": 1,
  "cp": 2,
  "trestbps": 135,
  "chol": 233,
  "fbs": 0,
  "restecg": 1,
  "thalach": 180,
  "exang": 1,
  "oldpeak": 0.4,
  "slope": 2,
  "ca": 0,
  "thal": 2
}'

## Installation
*docker build -t heart_disease_uci . && docker run -p 80:80 --rm heart_disease_uci*
