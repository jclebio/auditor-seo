# Documentação Técnica: Auditor SEO em Python

Este documento descreve a arquitetura, a evolução e o guia de manutenção do **Auditor SEO**, uma ferramenta modular desenvolvida em Python puro (com suporte a microframework web e SDK de Inteligência Artificial) executada no ambiente Fedora Linux.

---

## 1. Visão Geral da Arquitetura

O projeto foi construído seguindo uma abordagem incremental dividida em quatro etapas bem definidas, garantindo baixo acoplamento e separação de responsabilidades:

1. **Motor Técnico (Core):** Responsável por ler arquivos Markdown ou textos brutos em memória, extrair metadados (*Frontmatter*), limpar blocos de código e realizar a contagem e auditoria de elementos SEO.
2. **Camada de Apresentação (Interface Web):** Construída com **Flask** e estilizada com **Tailwind CSS**, permitindo o uso via navegador (colagem de texto ou upload de arquivos `.md`).
3. **Camada Cognitiva (Inteligência Artificial):** Integração com a API do **Google Gemini** (`google-genai`) para análise de intenção de busca, qualidade semântica e sugestões de melhoria.

---

## 2. Estrutura de Arquivos do Projeto

Na pasta raiz do seu projeto no Fedora, a árvore de arquivos final é organizada da seguinte forma:

```text
meu_projeto_seo/
│
├── auditor_seo.py          # Motor principal de auditoria (Etapas 1 e 2)
├── app.py                  # Servidor Flask e integração com a IA (Etapas 3 e 4)
├── documentacao_seo.md     # Este documento de referência técnica
└── templates/
    └── index.html          # Interface web responsiva em Tailwind CSS
```

---

## 3. Detalhamento das Etapas Desenvolvidas

### Etapa 1 — Script Funcional (Terminal)
* **Objetivo:** Ler arquivos Markdown no terminal e extrair métricas fundamentais.
* **Funcionalidades:** Contagem de palavras do corpo do texto, contagem de títulos H1 e H2, contagem de links em Markdown e ocorrências de uma palavra-chave específica (case-insensitive com limites de palavra `\b`).
* **Biblioteca Padrão:** `argparse`, `pathlib`, `re`, `sys`.

### Etapa 2 — Auditoria Técnica Ampliada
* **Objetivo:** Ampliar o escopo técnico para metadados de exibição na SERP e validação estrutural de mídia.
* **Funcionalidades:**
  * **Frontmatter:** Leitura de metadados delimitados por `---` no topo do arquivo (`seo_title` e `meta_description`), calculando seus comprimentos em caracteres.
  * **Isolamento de Código:** Funções de limpeza para ignorar blocos cercados por ``` ou ~~~ (evitando que comentários de código-fonte `#` sejam contados incorretamente como títulos H1).
  * **Auditoria de Imagens:** Identificação do padrão `![alt](url)` para separar imagens com texto alternativo (`alt`) preenchido daquelas sem `alt`.
  * **Validação de Links:** Separação de hiperlinks entre internos/relativos e externos (`http://`/`https://`), além de detecção de links quebrados ou com URLs vazias.

### Etapa 3 — Interface Web (Flask & Tailwind CSS)
* **Objetivo:** Disponibilizar um painel interativo local no navegador.
* **Funcionalidades:**
  * Rotas em **Flask** para recebimento de dados via método `POST` (suportando tanto texto colado em `textarea` quanto upload direto de arquivos `.md` via formulário `multipart/form-data`).
  * Estilização moderna e responsiva utilizando **Tailwind CSS via CDN**, estruturando cards limpos e alertas visuais baseados no status de SEO do artigo.

### Etapa 4 — Inteligência Artificial (Google Gemini API)
* **Objetivo:** Adicionar camada semântica e consultoria de redação automatizada.
* **Funcionalidades:**
  * Utilização do SDK oficial `google-genai` com o modelo `gemini-3.8-flash`.
  * Envio de contexto estruturado (palavra-chave, título SEO e corpo do texto) para o modelo avaliar a **Intenção de Busca**, a **Qualidade/Clareza** e sugerir **Melhorias Práticas**.
  * Tratamento robusto de exceções com foco em resiliência contra picos de tráfego na API (Erros HTTP 503 / `UNAVAILABLE`).

---

## 4. Como Executar o Projeto no Fedora Linux

### Pré-requisitos
Certifique-se de possuir o Python 3 instalado e configure o ambiente virtual/dependências necessárias:
```bash
pip install flask google-genai
```

### Configuração da Chave de IA
Defina sua chave de API do Gemini no terminal antes de iniciar o servidor web:
```bash
export GEMINI_API_KEY="sua-chave-de-api-aqui"
```

### Inicialização do Painel Web
Na pasta do projeto, execute o servidor Flask:
```bash
python3 app.py
```
Abra o navegador em: `http://127.0.0.1:5000`

---

## 5. Guia de Manutenção e Evolução Futura

Caso precise realizar manutenções ou expandir o código no futuro, siga estas diretrizes:

* **Modificações nas Regras de Análise:** Se precisar alterar a forma como os títulos H1/H2 ou os links são encontrados, edite exclusivamente o arquivo `auditor_seo.py`. As funções lá presentes são puras e retornam um dicionário padronizado (`dict`), o que facilita testes unitários com o módulo `unittest`.
* **Alterações Visuais:** Para modificar a aparência da interface sem mexer no backend, edite o arquivo `templates/index.html`. O layout utiliza classes utilitárias do Tailwind CSS.
* **Segurança de Chaves:** Nunca deixe a chave de API (`GEMINI_API_KEY`) hardcoded no código-fonte. Utilize sempre variáveis de ambiente no Fedora.