# Auditor SEO

Aplicação web desenvolvida em Python para auxiliar na auditoria
de artigos em Markdown, reunindo verificações técnicas de SEO e
uma análise textual com inteligência artificial usando o Gemini.

## Funcionalidades

- Recebimento de artigos por texto colado ou arquivo Markdown (.md).
- Auditoria técnica realizada pelo módulo `auditor_seo.py`.
- Análise de intenção de busca, qualidade e clareza com o Gemini.
- Interface web desenvolvida com Flask.
- Exibição dos resultados na página da aplicação.

## Tecnologias

- Python
- Flask
- Google Gen AI SDK
- Gemini
- HTML e Tailwind CSS

## Requisitos

- Python 3
- pip
- Uma chave de API do Gemini para utilizar a análise por IA.

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone URL_DO_SEU_REPOSITORIO
cd auditor-seo
```

Crie um ambiente virtual:
python3 -m venv .venv


Ative o ambiente virtual no Linux:
source .venv/bin/activate


Instale as dependências:
pip install -r requirements.txt


Configuração da API
Configure a variável de ambiente com sua chave do Gemini:
export GEMINI_API_KEY="SUA_CHAVE_AQUI"


Substitua SUA_CHAVE_AQUI pela sua chave real.
Não publique essa chave no GitHub.
A variável exportada dessa maneira permanece disponível somente
na sessão atual do terminal.
Executar a aplicação
Com o ambiente virtual ativado e a variável configurada, execute:
python app.py


Abra no navegador:
http://127.0.0.1:5000
Estrutura do projeto
auditor-seo/
├── app.py
├── auditor_seo.py
├── auditor.py
├── templates/
│   └── index.html
├── artigo_exemplo.md
├── artigo_teste.md
├── documentacao_tecnica_do_projeto.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md


Documentação
Consulte documentacao_tecnica_do_projeto.md para obter mais
detalhes sobre a implementação.
Situação do projeto
Projeto em desenvolvimento, criado para praticar Python,
desenvolvimento web e integração com inteligência artificial.
Segurança
Nunca publique chaves de API, senhas ou outros dados secretos.
O arquivo .gitignore exclui arquivos locais de configuração
que podem conter credenciais.
Licença
A licença ainda não foi definida.
