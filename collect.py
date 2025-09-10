import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

def coletar_noticias():
    response = requests.get(URL)
    data = response.json()
    articles = data.get("articles", [])
    df = pd.DataFrame(articles, columns=["title", "description", "publishedAt", "source"])

    #Limpando os dados com pandas

    df = df.dropna()
    df["publishedAt"] = pd.to_datetime(df["publishedAt"])

    return df


if __name__ == "__main__":
    df = coletar_noticias()
    df.to_csv("data/noticias.csv", index=False)
    print("Notícias Coletadas e salvas em data/noticias.csv")