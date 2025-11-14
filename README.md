# Discogs Web Scraper

Este projeto faz o webscrapping dos dados do site [Discogs](https://www.discogs.com/pt_BR/), focado no gênero **Blues**.

O bot coleta informações detalhadas de **10 artistas** e até **10 álbuns por artista**, incluindo faixas, gravadora, ano, duração, consolidando os dados em um arquivo estruturado. 

## Stack utilizada
* **Linguagem:** `Python 3.12+`
* **Automação de Navegador:** `undetected-chromedriver`
* **Parsing de HTML:** `BeautifulSoup4`
* **Testes:** `pytest`
* **Formato de Saída:** `JSONL`

## Estrutura do projeto
```
webscraping_discogs/
├── data/                     # Armazena os dados 'raw' (bruto) e 'clean' (tratado)
├── src/                      
│   ├── data_handler.py       # Gerencia I/O
│   ├── main.py               # Orquestrador
│   ├── scraper.py            # Camada de Extração
│   ├── transform.py          # Camada de Transformação
│   └── utils.py              # Funções auxiliares
├── tests/                    
│   └── test_utils.py         # Testes unitários 
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação
```

## Pré-requisitos
* **Python 3.12 ou +**
* **Google Chrome**

## Instalação
**1. Clone este repositório:**
```
git clone https://github.com/paolauande/webscraping_discogs.git
cd webscraping_discogs
```
**2. Crie e ative um ambiente virtual:**
* *Windows*:
```
# Cria a pasta venv
python -m venv venv

# Ativa o ambiente
venv\Scripts\activate
```
* *Linux/Mac*:
```
python3 -m venv venv
source venv/bin/activate
```
**3. Instale as dependências:**
```
pip install -r requirements.txt
```

## Como executar
**1. Confirme se o ambiente virtual está ativo.** 

**2. Execute o comando:**
```
python src/main.py
```

**Atenção durante a execução:** \
Ao rodar o script, uma janela do Google Chrome será aberta automaticamente.

* Não feche esta janela: A automação está utilizando-a para navegar.

* Fechamento automático: A janela será encerrada sozinha assim que o processo for finalizado.

**Saída de dados** \
Após a execução, os arquivos serão gerados no formato JSONL e salvos no diretório ``data/``.
* Arquivo bruto: ``data/blues_data_raw.jsonl``
* Arquivo tratado: ``data/blues_data_clean.jsonl``
* Estrutura: Os dados do arquivo final estão agrupados por Álbum (incluindo o nome do artista para facilitar consultas).
* ID único: Foi gerada uma chave composta no formato Artista_Album.

## Como testar
Há um teste unitário que foca na validação das funções auxiliares (`src/utils.py`), garantindo que a lógica de limpeza de texto e formatação de dados esteja funcionando corretamente antes de ser aplicada em larga escala.

Há um teste de integração que simula o fluxo completo de transformação de dados. O teste cria um arquivo temporário com dados brutos (raw), executa a função de processamento e verifica se o arquivo final (clean) foi gerado com a estrutura esperada.

Para executar o teste basta rodar:
```
pytest
```
