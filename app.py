import os
from flask import Flask, render_template, request
from google import genai

# Importa o motor da Etapa 2
from auditor_seo import analisar_texto

app = Flask(__name__)


def analisar_com_ia(
    conteudo_texto: str, palavra_chave: str, seo_title: str
) -> str:
  """Usa o SDK oficial do Google GenAI com tratamento de erros de alta demanda."""
  api_key = os.environ.get("GEMINI_API_KEY")
  if not api_key:
    return (
        "Chave de API do Gemini não configurada."
        " Defina a variável GEMINI_API_KEY."
    )

  try:
    client = genai.Client(api_key=api_key)

    prompt = f"""
        Atue como um especialista sênior em SEO e Redação Web. 
        Analise o artigo em Markdown abaixo com base na palavra-chave principal e no título SEO fornecidos.

        Palavra-Chave Principal: "{palavra_chave}"
        Título SEO: "{seo_title}"

        Artigo:
        {conteudo_texto}

        Forneça uma avaliação objetiva dividida exatamente nestes três tópicos curtos:
        1. **Intenção de Busca:** O artigo atende satisfatoriamente ao que o usuário busca ao digitar essa palavra-chave?
        2. **Qualidade e Clareza:** O tom, a didática e o desenvolvimento do assunto estão adequados?
        3. **Sugestões Práticas de Melhoria:** 2 ou 3 recomendações rápidas para otimizar o conteúdo.
        """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )
    return response.text

  except Exception as e:
    # Trata especificamente erros 503 de alta demanda
    erro_str = str(e)
    if "503" in erro_str or "UNAVAILABLE" in erro_str:
      return (
          "⚠️ O modelo de Inteligência Artificial está temporariamente com alto"
          " volume de acessos (Erro 503). Por favor, clique em 'Executar"
          " Auditoria' novamente em alguns segundos."
      )
    return f"Erro ao consultar a Inteligência Artificial: {erro_str}"

@app.route("/", methods=["GET", "POST"])
def index():
  resultados = None
  analise_ia = None
  conteudo = ""
  keyword = ""

  if request.method == "POST":
    keyword = request.form.get("palavra_chave", "")

    arquivo_enviado = request.files.get("arquivo_md")
    if arquivo_enviado and arquivo_enviado.filename != "":
      conteudo = arquivo_enviado.read().decode("utf-8", errors="ignore")
      nome_origem = arquivo_enviado.filename
    else:
      conteudo = request.form.get("conteudo", "")
      nome_origem = "Texto Colado (Painel Web)"

    # 1. Executa a auditoria técnica (Etapa 2)
    resultados = analisar_texto(
        conteudo_bruto=conteudo, palavra_chave=keyword, nome_origem=nome_origem
    )

    # 2. Executa a análise inteligente com IA (Etapa 4)
    titulo_para_ia = (
        resultados["seo_title"] if resultados["seo_title_preenchido"] else "Sem título SEO"
    )
    analise_ia = analisar_com_ia(
        conteudo_texto=conteudo, palavra_chave=keyword, seo_title=titulo_para_ia
    )

  return render_template(
      "index.html",
      resultados=resultados,
      analise_ia=analise_ia,
      conteudo=conteudo,
      keyword=keyword,
  )


if __name__ == "__main__":
  app.run(debug=True, port=5000)