
import re
from pathlib import Path

def auditar_artigo(texto, palavra_chave):
    # Remove marcações Markdown para estimar o texto.
    texto_limpo = re.sub(r"```.*?```", " ", texto, flags=re.S)
    texto_limpo = re.sub(r"!\[.*?\]\(.*?\)", " ", texto_limpo)
    texto_limpo = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto_limpo)
    texto_limpo = re.sub(r"(?m)^#{1,6}\s+", "", texto_limpo)

    palavras = re.findall(r"\b[\wÀ-ÿ-]+\b", texto_limpo)
    titulos_h1 = re.findall(r"(?m)^#\s+.+$", texto)
    titulos_h2 = re.findall(r"(?m)^##\s+.+$", texto)
    links = re.findall(r"\[[^\]]+\]\([^)]+\)", texto)
    ocorrencias = len(
        re.findall(re.escape(palavra_chave), texto, flags=re.I)
    ) if palavra_chave.strip() else 0

    problemas = []

    if not titulos_h1:
        problemas.append("Não foi encontrado título H1 em Markdown.")
    elif len(titulos_h1) > 1:
        problemas.append("Há mais de um H1 em Markdown; revise a estrutura.")

    if not titulos_h2:
        problemas.append("Não foram encontrados subtítulos H2.")

    if len(palavras) < 300:
        problemas.append("Artigo curto para uma auditoria mais aprofundada.")

    if palavra_chave.strip() and ocorrencias == 0:
        problemas.append("Palavra-chave não encontrada.")

    print("\n=== AUDITORIA INICIAL DE SEO ===")
    print(f"Palavras estimadas: {len(palavras)}")
    print(f"Títulos H1 encontrados: {len(titulos_h1)}")
    print(f"Subtítulos H2 encontrados: {len(titulos_h2)}")
    print(f"Links em Markdown: {len(links)}")
    print(f"Ocorrências da palavra-chave: {ocorrencias}")

    print("\n=== PONTOS PARA REVISAR ===")
    if problemas:
        for problema in problemas:
            print(f"- {problema}")
    else:
        print("Nenhum dos problemas básicos configurados foi detectado.")

    print("\nAtenção: estas verificações não garantem bom posicionamento.")

def main():
    caminho = input("Caminho do artigo (.txt ou .md): ").strip()
    palavra_chave = input("Palavra-chave principal: ").strip()

    arquivo = Path(caminho).expanduser()

    if not arquivo.is_file():
        print("Arquivo não encontrado. Confira o caminho.")
        return

    texto = arquivo.read_text(encoding="utf-8")
    auditar_artigo(texto, palavra_chave)

if __name__ == "__main__":
    main()
