import boto3
import json
import pandas as pd
import time
import botocore

# Cliente Bedrock
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

def analisar_sentimento(texto: str):
    """Chama o modelo Claude no Bedrock para classificar sentimento"""
    body = json.dumps({
        "prompt": f"\n\nHuman: Classifique o sentimento da frase abaixo como 'positivo', 'negativo' ou 'neutro'.\n\nFrase: {texto}\n\nAssistant:",
        "max_tokens_to_sample": 50,
        "temperature": 0.0,
        "stop_sequences": ["\n\nHuman:"]
    })

    response = client.invoke_model(
        modelId="anthropic.claude-v2",
        body=body
    )

    result = json.loads(response["body"].read())
    return result["completion"].strip()

def analisar_noticias(csv_path="data/noticias.csv"):
    df = pd.read_csv(csv_path)

    resultados = []
    for index, row in df.iterrows():
        title = row["title"]
        description = row.get("description", "")

        # Retry automático
        for i in range(3):
            try:
                sentimento_title = analisar_sentimento(title)
                sentimento_desc = analisar_sentimento(description) if description else "N/A"
                resultados.append({
                    "title": title,
                    "description": description,
                    "sentimento_title": sentimento_title,
                    "sentimento_description": sentimento_desc
                })
                print(f"✅ Processado: {title}")
                time.sleep(1.5)  # pausa para evitar throttling
                break
            except botocore.exceptions.ClientError as e:
                print(f"⚠ Erro no título '{title}', tentativa {i+1}/3. Retentando em 2s...")
                time.sleep(2)
            except Exception as e:
                print(f"⚠ Erro inesperado: {e}")
                resultados.append({
                    "title": title,
                    "description": description,
                    "sentimento_title": "Erro",
                    "sentimento_description": "Erro"
                })
                break

    resultados_df = pd.DataFrame(resultados)
    resultados_df.to_csv("data/noticias_com_sentimento.csv", index=False)
    print("🎯 Análise concluída → data/noticias_com_sentimento.csv")

if __name__ == "__main__":
    analisar_noticias()
