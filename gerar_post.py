from openai import OpenAI
from datetime import datetime
import os

# Autenticação com a chave da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_conteudo(dia_formatado):
    prompt = f"""
    Hoje é dia {dia_formatado}.
    Quais são as principais datas comemorativas no Brasil e no mundo?
    Quais pessoas famosas nasceram nesse dia? E quem faleceu?
    Conte também um ou dois eventos históricos marcantes.

    Formate com títulos e tópicos. Use emojis para separar as seções.
    """
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )
    return resposta.choices[0].message.content.strip()

def gerar_description_e_keywords(conteudo, dia_formatado):
    prompt = f"""
    A seguir está um conteúdo para um blog sobre o dia {dia_formatado}:

    {conteudo}

    Gere:
    1. Uma descrição curta e atrativa (máximo 160 caracteres) para SEO.
    2. Uma lista de 5 a 8 palavras-chave relevantes (keywords) separadas por vírgula.
    """
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=150
    )

    resultado = resposta.choices[0].message.content.strip()
    
    # Espera-se algo como:
    # Descrição: ...
    # Keywords: ...
    linhas = resultado.splitlines()
    descricao = ""
    keywords = ""

    for linha in linhas:
        if "Descrição" in linha:
