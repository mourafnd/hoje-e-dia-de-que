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
            descricao = linha.split(":", 1)[1].strip()
        elif "Keywords" in linha:
            keywords = linha.split(":", 1)[1].strip()

    return descricao, keywords

def salvar_post(conteudo, descricao, keywords, data_obj):
    titulo = f"Hoje é dia de quê? - {data_obj.strftime('%d de %B')}"
    slug = data_obj.strftime("%d-%m")
    pasta_posts = "content/posts"
    nome_arquivo = f"{pasta_posts}/hoje-e-dia-{slug}.md"

    # Garante que a pasta content/posts existe
    os.makedirs(pasta_posts, exist_ok=True)

    keywords_formatadas = [f'"{k.strip()}"' for k in keywords.split(",")]

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f'title: "{titulo}"\n')
        f.write(f"date: {data_obj.isoformat()}\n")
        f.write(f'slug: "hoje-e-dia-{slug}"\n')
        f.write(f'description: "{descricao}"\n')
        f.write(f'keywords: [{", ".join(keywords_formatadas)}]\n')
        f.write("---\n\n")
        f.write(conteudo)


def main():
    hoje = datetime.now()
    dia_formatado = hoje.strftime("%d de %B")

    conteudo = gerar_conteudo(dia_formatado)
    descricao, keywords = gerar_description_e_keywords(conteudo, dia_formatado)
    salvar_post(conteudo, descricao, keywords, hoje)

if __name__ == "__main__":
    main()
