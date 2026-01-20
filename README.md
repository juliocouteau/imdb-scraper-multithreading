🕷️ IMDB Movie Scraper (Multithreading)
Um web scraper de alta performance desenvolvido em Python para extração de dados cinematográficos do IMDB, utilizando multithreading para otimização de tempo.

💻 Sobre o Projeto
Extrair dados de grandes portais como o IMDB pode ser um processo demorado se feito de forma sequencial. Este projeto foi desenvolvido para solucionar esse problema, aplicando conceitos de programação paralela.

O script navega pelas páginas de filmes, extrai informações críticas e as organiza, tudo isso processando múltiplas requisições simultaneamente, o que reduz o tempo de execução em até 80% em comparação a um scraper tradicional.

⚙️ Funcionalidades
[x] Extração de Dados: Coleta título, ano de lançamento, nota (rating) e sinopse.

[x] Multithreading: Utiliza a biblioteca concurrent.futures para disparar múltiplas requisições em paralelo.

[x] Tratamento de Erros: Gestão de timeouts e requisições falhas para evitar a interrupção do processo.

[x] Exportação: Salva os dados estruturados em formato CSV para posterior análise de dados.

🛠 Tecnologias Utilizadas
Python 3.x

Requests: Para realizar as requisições HTTP.

BeautifulSoup4: Para o parsing e extração de dados do HTML.

Threading / Concurrent.futures: Para a lógica de multithreading.

Pandas: Para estruturação e exportação dos dados.

🔧 Como Executar
Pré-requisitos
Ter o Python instalado e as bibliotecas necessárias:

Bash
pip install requests beautifulsoup4 pandas
Passo a Passo
Clone o repositório

Bash
git clone https://github.com/juliocouteau/imdb-scraper-multithreading.git
Acesse a pasta

Bash
cd imdb-scraper-multithreading
Execute o script

Bash
python scraper.py
👤 Autor
Desenvolvido por Julio Couteau.
