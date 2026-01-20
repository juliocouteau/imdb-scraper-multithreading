import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup

# Configurações globais
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
MAX_THREADS = 10

def extract_movie_details(movie_link):
    """Extrai detalhes de um filme individual."""
    time.sleep(random.uniform(0.1, 0.3)) # Evita bloqueios por excesso de requisições
    try:
        response = requests.get(movie_link, headers=headers, timeout=10)
        movie_soup = BeautifulSoup(response.content, 'html.parser')

        # Seletores baseados em data-testid (mais estáveis no IMDb atual)
        title = movie_soup.find('h1').get_text() if movie_soup.find('h1') else "N/A"
        
        # Tenta encontrar a data de lançamento
        date_tag = movie_soup.find('a', href=lambda href: href and 'releaseinfo' in href)
        date = date_tag.get_text().strip() if date_tag else "N/A"

        # Tenta encontrar a nota (Rating)
        rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
        rating = rating_tag.find('span').get_text() if rating_tag else "N/A"

        # Tenta encontrar a sinopse (Plot)
        plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
        plot = plot_tag.get_text().strip() if plot_tag else "N/A"

        print(f"Extraído: {title}")
        return [title, date, rating, plot]

    except Exception as e:
        print(f"Erro ao acessar {movie_link}: {e}")
        return None

def main():
    start_time = time.time()
    print("Iniciando Scraping do IMDb...")

    # 1. Pegar a lista de filmes populares
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/'
    response = requests.get(popular_movies_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar os links (Ajustado para o layout atual do IMDb)
    movie_links = []
    for a in soup.find_all('a', class_='ipc-title-link-wrapper', limit=50): # Limitado a 50 para testar
        movie_links.append('https://www.imdb.com' + a['href'].split('?')[0])

    # 2. Multithreading para extrair detalhes
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # O map envia os links para a função e retorna os resultados na ordem
        future_to_movie = {executor.submit(extract_movie_details, link): link for link in movie_links}
        for future in concurrent.futures.as_completed(future_to_movie):
            data = future.result()
            if data:
                results.append(data)

    # 3. Salvar no CSV (Escrita única e segura)
    with open('movies_imdb.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Título', 'Data de Lançamento', 'Avaliação', 'Sinopse']) # Cabeçalho
        writer.writerows(results)

    end_time = time.time()
    print(f"\nConcluído! {len(results)} filmes salvos em 'movies_imdb.csv'.")
    print(f'Tempo total: {end_time - start_time:.2f} segundos')

if __name__ == '__main__':
    main()