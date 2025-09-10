from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Analisador de Notícias com IA"}

@app.get("/news")
def get_news():
    df = pd.read_csv("data/noticias_com_sentimento.csv")
    
    return df[["title", "description", "sentimento_title", "sentimento_description"]].head(5).to_dict(orient="records")