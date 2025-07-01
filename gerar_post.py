from openai import OpenAI
from datetime import datetime
import os

# Usa a nova forma de autenticação
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
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    return resposta.choices[0].message.content.strip()

def salvar_post(conteudo, data_obj):
    titulo = f"Hoje é dia de quê? - {data_obj.strftime('%d de %B')}"
    slug = data_obj.strftime("%d-%m")
    nome_arquivo = f"content/posts/hoje-e-dia-{slug}.md"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"---\n")
        f.write(f'title: "{titulo}"\n')
        f.write(f"date: {data_obj.isoformat()}\n")
        f.write(f'slug: "hoje-e-dia-{slug}"\n')
        f.write(f"---\n\n")
        f.write(conteudo)

def main():
    hoje = datetime.now()
    dia_formatado = hoje.strftime("%d de %B")
    conteudo = gerar_conteudo(dia_formatado)
    salvar_post(conteudo, hoje)

if __name__ == "__main__":
    main()
