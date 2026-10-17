import os
from google import genai
from google.genai import types


def analisar_com_ia(
    conteudo_texto: str, palavra_chave: str, seo_title: str
) -> str:
  """Envia o artigo e os dados de SEO para o Gemini analisar qualidade e intenção de busca."""
  # Inicializa o cliente usando a variável de ambiente GEMINI_API_KEY
  client = genai.Client()

  prompt = f"""
    Atue como um especialista sênior em SEO e Redação Web. 
    Analise o artigo em Markdown abaixo com base na palavra-chave principal e no título SEO fornecidos.

    Palavra-Chave Principal: "{palavra_chave}"
    Título SEO: "{seo_title}"

    Artigo:
    {conteudo_texto}

    Por favor, forneça uma avaliação objetiva dividida em três tópicos curtos:
    1. **Intenção de Busca:** O artigo atende satisfatoriamente ao que o usuário busca ao digitar essa palavra-chave?
    2. **Qualidade e Clareza:** O tom, a didática e o desenvolvimento do assunto estão adequados?
    3. **Sugestões Práticas de Melhoria:** 2 ou 3 recomendações rápidas para otimizar o conteúdo.
    """

  try:
    # Utiliza o modelo gemini-2.5-flash ideal para tarefas rápidas de texto
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text
  except Exception as e:
    return f"Erro ao consultar a Inteligência Artificial: {str(e)}"