#!/usr/bin/env python3
"""
Auditor SEO em Python (Versão 2.1 - Etapa 2 Completa)
Analisa estrutura, metadados, distribuição de palavra-chave, imagens (alt) e links.
Utiliza apenas a biblioteca padrão do Python.
"""

import argparse
from pathlib import Path
import re
import sys


def extrair_metadados_e_corpo(texto_completo: str) -> tuple[dict, str]:
  """
    Separa o cabeçalho de metadados (Frontmatter entre '---') do corpo do artigo.
    """
  metadados = {"seo_title": "", "meta_description": ""}

  if texto_completo.startswith("---"):
    partes = texto_completo.split("---", 2)
    if len(partes) >= 3:
      bloco_meta = partes[1]
      corpo_artigo = partes[2].strip()

      for linha in bloco_meta.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or ":" not in linha:
          continue
        chave, _, valor = linha.partition(":")
        chave = chave.strip().lower()
        valor = valor.strip().strip("\"'")

        if chave in metadados:
          metadados[chave] = valor

      return metadados, corpo_artigo

  return metadados, texto_completo


def remover_blocos_codigo(texto: str) -> str:
  """
    Remove blocos de código cercados por ``` ou ~~~ antes de analisar títulos,
    links e imagens, evitando falsos positivos dentro de exemplos de código.
    """
  texto_limpo = re.sub(r"```.*?```", "", texto, flags=re.DOTALL)
  texto_limpo = re.sub(r"~~~.*?~~~", "", texto_limpo, flags=re.DOTALL)
  return texto_limpo


def contar_ocorrencias_termo(texto: str, termo: str) -> int:
  """Conta quantas vezes a palavra-chave aparece de forma exata (case-insensitive)."""
  if not termo or not texto:
    return 0
  padrao = rf"\b{re.escape(termo.strip())}\b"
  ocorrencias = re.findall(padrao, texto, flags=re.IGNORECASE)
  return len(ocorrencias)


def contem_termo(texto: str, termo: str) -> bool:
  """Retorna True se a palavra-chave estiver presente no texto."""
  return contar_ocorrencias_termo(texto, termo) > 0


def analisar_imagens(texto_sem_codigo: str) -> dict:
  """
    Encontra imagens no padrão ![alt](src) e verifica se o atributo alt foi preenchido.
    """
  # Captura grupo 1 (alt) e grupo 2 (src/url)
  padrao_img = r"!\[([^\]]*)\]\(([^)]*)\)"
  encontradas = re.findall(padrao_img, texto_sem_codigo)

  imagens_com_alt = []
  imagens_sem_alt = []

  for alt, src in encontradas:
    alt_limpo = alt.strip()
    src_limpo = src.strip()
    if alt_limpo:
      imagens_com_alt.append({"alt": alt_limpo, "src": src_limpo})
    else:
      imagens_sem_alt.append(src_limpo or "[URL vazia]")

  return {
      "total": len(encontradas),
      "com_alt": imagens_com_alt,
      "sem_alt": imagens_sem_alt,
  }


def analisar_links(texto_sem_codigo: str) -> dict:
  """
    Encontra links no padrão [ancora](url), ignorando imagens,
    e classifica entre internos, externos e links com problemas.
    """
  # (?<!!) garante que não há um '!' antes do colchete (ignora imagens)
  padrao_link = r"(?<!!)\[([^\]]*)\]\(([^)]*)\)"
  encontrados = re.findall(padrao_link, texto_sem_codigo)

  externos = []
  internos = []
  sem_ancora = []
  url_vazia = []

  for ancora, url in encontrados:
    ancora_limpa = ancora.strip()
    url_limpa = url.strip()

    if not url_limpa:
      url_vazia.append(ancora_limpa or "[Link totalmente vazio]")
      continue

    if not ancora_limpa:
      sem_ancora.append(url_limpa)

    # Classifica entre link externo (http/https) ou interno/relativo
    if url_limpa.lower().startswith(("http://", "https://")):
      externos.append({"ancora": ancora_limpa, "url": url_limpa})
    else:
      internos.append({"ancora": ancora_limpa, "url": url_limpa})

  return {
      "total": len(encontrados),
      "externos": externos,
      "internos": internos,
      "sem_ancora": sem_ancora,
      "url_vazia": url_vazia,
  }


def analisar_texto(
    conteudo_bruto: str,
    palavra_chave: str,
    nome_origem: str = "Texto Direto",
    titulo_cli: str = None,
    desc_cli: str = None,
) -> dict:
  """
    Motor principal de auditoria (pronto para ser usado pelo terminal ou pela Web na Etapa 3).
    """
  metadados, corpo = extrair_metadados_e_corpo(conteudo_bruto)

  seo_title = titulo_cli if titulo_cli is not None else metadados["seo_title"]
  meta_desc = (
      desc_cli if desc_cli is not None else metadados["meta_description"]
  )

  corpo_sem_codigo = remover_blocos_codigo(corpo)

  # Métricas de texto e títulos
  palavras = re.findall(r"\b\w+\b", corpo_sem_codigo)
  total_palavras = len(palavras)

  lista_h1 = re.findall(r"^#\s+(.+)$", corpo_sem_codigo, flags=re.MULTILINE)
  lista_h2 = re.findall(r"^##\s+(.+)$", corpo_sem_codigo, flags=re.MULTILINE)

  ocorrencias_kw_corpo = contar_ocorrencias_termo(
      corpo_sem_codigo, palavra_chave
  )

  # Auditoria de Links e Imagens
  dados_links = analisar_links(corpo_sem_codigo)
  dados_imagens = analisar_imagens(corpo_sem_codigo)

  # Verificações de Metadados e Posicionamento de Palavra-Chave
  seo_title_preenchido = bool(seo_title)
  meta_desc_preenchida = bool(meta_desc)

  kw_no_seo_title = contem_termo(seo_title, palavra_chave)
  kw_no_h1 = any(contem_termo(h1, palavra_chave) for h1 in lista_h1)
  h2_com_kw = [h2 for h2 in lista_h2 if contem_termo(h2, palavra_chave)]

  return {
      "arquivo": nome_origem,
      "palavra_chave": palavra_chave,
      "total_palavras": total_palavras,
      "lista_h1": lista_h1,
      "lista_h2": lista_h2,
      "ocorrencias_kw_corpo": ocorrencias_kw_corpo,
      "seo_title": seo_title,
      "seo_title_preenchido": seo_title_preenchido,
      "seo_title_chars": len(seo_title),
      "meta_desc": meta_desc,
      "meta_desc_preenchida": meta_desc_preenchida,
      "meta_desc_chars": len(meta_desc),
      "kw_no_seo_title": kw_no_seo_title,
      "kw_no_h1": kw_no_h1,
      "h2_com_kw": h2_com_kw,
      "links": dados_links,
      "imagens": dados_imagens,
  }


def analisar_artigo(
    caminho_arquivo: Path,
    palavra_chave: str,
    titulo_cli: str = None,
    desc_cli: str = None,
) -> dict:
  """Lê um arquivo Markdown do disco e repassa para analisar_texto."""
  conteudo_bruto = caminho_arquivo.read_text(encoding="utf-8")
  return analisar_texto(
      conteudo_bruto=conteudo_bruto,
      palavra_chave=palavra_chave,
      nome_origem=caminho_arquivo.name,
      titulo_cli=titulo_cli,
      desc_cli=desc_cli,
  )


def exibir_relatorio(dados: dict) -> None:
  """Imprime o relatório completo no terminal."""
  print("=" * 65)
  print(f" RELATÓRIO DE AUDITORIA SEO - {dados['arquivo']}")
  print("=" * 65)
  print(f"Palavra-chave analisada: '{dados['palavra_chave']}'\n")

  print("[1] METADADOS (SERP / Exibição nos Buscadores)")
  if dados["seo_title_preenchido"]:
    print(f"  • Título SEO: Preenchido ({dados['seo_title_chars']} caracteres)")
    print(f'    Texto: "{dados["seo_title"]}"')
  else:
    print("  • Título SEO: [Não preenchido]")

  if dados["meta_desc_preenchida"]:
    print(
        f"  • Meta Description: Preenchida ({dados['meta_desc_chars']}"
        " caracteres)"
    )
    print(f'    Texto: "{dados["meta_desc"]}"')
  else:
    print("  • Meta Description: [Não preenchida]")

  print(
      "  * Nota técnica: O tamanho em caracteres (ou largura em pixels) afeta"
      " se o"
  )
  print(
      "    texto será cortado visualmente na página de resultados (SERP), mas"
      " não"
  )
  print("    funciona como fator absoluto de ranqueamento.\n")

  print("[2] ESTRUTURA E CONTEÚDO")
  print(f"  • Contagem de palavras (corpo limpo): {dados['total_palavras']}")
  print(f"  • Quantidade de H1: {len(dados['lista_h1'])}")
  for i, h1 in enumerate(dados["lista_h1"], 1):
    print(f'      H1 #{i}: "{h1}"')
  print(f"  • Quantidade de H2: {len(dados['lista_h2'])}\n")

  print(f"[3] DISTRIBUIÇÃO DA PALAVRA-CHAVE ('{dados['palavra_chave']}')")
  print(f"  • Ocorrências no corpo do texto: {dados['ocorrencias_kw_corpo']}")
  status_title = (
      "Sim"
      if dados["kw_no_seo_title"]
      else "Não"
      if dados["seo_title_preenchido"]
      else "N/A (Título vazio)"
  )
  print(f"  • Presente no Título SEO? {status_title}")

  if dados["lista_h1"]:
    print(f"  • Presente no título H1? {'Sim' if dados['kw_no_h1'] else 'Não'}")
  else:
    print("  • Presente no título H1? N/A (Nenhum H1 encontrado)")

  if dados["lista_h2"]:
    qtd_h2_kw = len(dados["h2_com_kw"])
    total_h2 = len(dados["lista_h2"])
    print(
        f"  • Presente nos subtítulos H2? {'Sim' if qtd_h2_kw > 0 else 'Não'}"
        f" ({qtd_h2_kw} de {total_h2} H2s)"
    )
  else:
    print("  • Presente nos subtítulos H2? N/A (Nenhum H2 encontrado)")
  print()

  # Nova seção: Imagens
  imgs = dados["imagens"]
  print("[4] AUDITORIA DE IMAGENS (Acessibilidade e SEO Visual)")
  print(f"  • Total de imagens: {imgs['total']}")
  print(f"  • Com texto alternativo (alt): {len(imgs['com_alt'])}")
  print(f"  • Sem texto alternativo (alt vazio): {len(imgs['sem_alt'])}")
  if imgs["sem_alt"]:
    for src in imgs["sem_alt"]:
      print(f"      [!] Alerta: Imagem sem atributo alt -> ({src})")
  print()

  # Nova seção: Links
  lnks = dados["links"]
  print("[5] AUDITORIA DE LINKS (Internos e Externos)")
  print(f"  • Total de links: {lnks['total']}")
  print(f"  • Links internos / relativos: {len(lnks['internos'])}")
  print(f"  • Links externos (http/https): {len(lnks['externos'])}")
  if lnks["sem_ancora"]:
    for url in lnks["sem_ancora"]:
      print(f"      [!] Alerta: Link sem texto âncora -> ({url})")
  if lnks["url_vazia"]:
    for anc in lnks["url_vazia"]:
      print(f"      [!] Alerta: Link com URL vazia -> [{anc}]()")

  print("=" * 65)


def main():
  parser = argparse.ArgumentParser(
      description="Auditor SEO para artigos em Markdown (v2.1)"
  )
  parser.add_argument("arquivo", help="Caminho para o arquivo Markdown (.md)")
  parser.add_argument(
      "-k", "--keyword", required=True, help="Palavra-chave principal"
  )
  parser.add_argument(
      "--seo-title",
      help="Define/sobrescreve o Título SEO via linha de comando",
      default=None,
  )
  parser.add_argument(
      "--meta-desc",
      help="Define/sobrescreve a Meta Description via linha de comando",
      default=None,
  )

  args = parser.parse_args()
  caminho = Path(args.arquivo)

  if not caminho.is_file():
    print(
        f"Erro: O arquivo '{caminho}' não foi encontrado.", file=sys.stderr
    )
    sys.exit(1)

  resultados = analisar_artigo(
      caminho_arquivo=caminho,
      palavra_chave=args.keyword,
      titulo_cli=args.seo_title,
      desc_cli=args.meta_desc,
  )
  exibir_relatorio(resultados)


if __name__ == "__main__":
  main()