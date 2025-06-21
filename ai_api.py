from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
app = FastAPI()
iris = load_iris()
model = RandomForestClassifier()
model.fit(iris.data,iris.target)
class Features(BaseModel):
    data : list[float]
@app.get("/")
def root():
    return {"message ": "Pyautomate AI is running"}
@app.post("/predict")
def predict(features: Features):
    prediction = model.predict([features.data])
    return {"prediction": int(prediction[0])}