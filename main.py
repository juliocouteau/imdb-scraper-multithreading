import requests
import time
import csv
import random
import os
import concurrent.futures
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
MAX_THREADS = 10  
OUTPUT_DIR = 'resultados'
FILE_NAME = 'movies_imdb.csv'

def extract_movie_details(movie_link):
    """Função executada por cada thread para extrair dados de um filme específico."""
   
    time.sleep(random.uniform(0.1, 0.3))
    
    try:
        response = requests.get(movie_link, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            return None
            
        movie_soup = BeautifulSoup(response.content, 'html.parser')

        
        title_tag = movie_soup.find('h1')
        title = title_tag.get_text().strip() if title_tag else "N/A"

        date_tag = movie_soup.find('a', href=lambda href: href and 'releaseinfo' in href)
        date = date_tag.get_text().strip() if date_tag else "N/A"

        rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
        rating = rating_tag.find('span').get_text() if rating_tag else "N/A"

        plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
        plot = plot_tag.get_text().strip() if plot_tag else "N/A"

        print(f"Sucesso: {title}")
        return [title, date, rating, plot]

    except Exception as e:
        print(f"Erro ao processar link {movie_link}: {e}")
        return None

def main():
    start_time = time.time()
    
   
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Pasta '{OUTPUT_DIR}' criada.")

    print("--- Iniciando Scraping do IMDb ---")

   
    popular_url = 'https://www.imdb.com/chart/moviemeter/'
    try:
        response = requests.get(popular_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        
        movie_links = []
        for a in soup.find_all('a', class_='ipc-title-link-wrapper', limit=50):
            link = 'https://www.imdb.com' + a['href'].split('?')[0]
            movie_links.append(link)
            
    except Exception as e:
        print(f"Erro ao obter lista principal: {e}")
        return

  
    all_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
       
        future_to_movie = {executor.submit(extract_movie_details, link): link for link in movie_links}
        
        for future in concurrent.futures.as_completed(future_to_movie):
            result = future.result()
            if result:
                all_results.append(result)

    
    path_final = os.path.join(OUTPUT_DIR, FILE_NAME)
    with open(path_final, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Título', 'Data', 'Avaliação', 'Sinopse']) 
        writer.writerows(all_results)

    end_time = time.time()
    print("\n" + "="*30)
    print(f"CONCLUÍDO!")
    print(f"Total de filmes salvos: {len(all_results)}")
    print(f"Arquivo: {path_final}")
    print(f"Tempo total gasto: {end_time - start_time:.2f} segundos")
    print("="*30)

if __name__ == '__main__':
    main()