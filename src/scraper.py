import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import re

BASE_URL = "https://www.discogs.com"
driver = None

def _get_driver():
    global driver
    if driver is None:
        print("Inicializando Chrome...")
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options, use_subprocess=True)
    return driver

def _get_page_content(url):
    try:
        current_driver = _get_driver()
        print(f"Acessando: {url}")
        current_driver.get(url)
        time.sleep(2) # Delay leve para carregar
        return BeautifulSoup(current_driver.page_source, 'html.parser')
    except Exception as e:
        print(f"Erro em {url}: {e}")
        return None

def _parse_album_page(album_url):
    soup = _get_page_content(album_url)
    if not soup: return None
    
    try:
        # Extração bruta
        
        # Titulo (álbum)
        title_tag = soup.select_one('h1[class*="title"]') or soup.select_one('h1')
        raw_title = title_tag.text.strip() if title_tag else "Desconhecido"

        # Gravadora
        label_tag = soup.select_one('a[href*="/label/"]')
        label = label_tag.text.strip() if label_tag else "Independente"

        # Ano lançamento álbum
        year_tag = soup.select_one('a[href*="/year/"]')
        year = year_tag.text.strip() if year_tag else "N/A"
        
        if year == "N/A":
            header_text = soup.text[:1000]
            year_match = re.search(r'\b(19|20)\d{2}\b', header_text)
            if year_match: year = year_match.group(0)

        styles = [a.text.strip() for a in soup.select('a[href*="/style/"]')]

        # Faixas do álbum
        tracks_data = []
        track_rows = soup.select('[class*="tracklist"] tr')
        if not track_rows:
            track_rows = soup.select('[class*="tracklist"] div[class*="row"]')

        for i, row in enumerate(track_rows):
            text = row.text.strip()
            if not text: continue
            
            duration_match = re.search(r'\d{1,2}:\d{2}', text)
            duration = duration_match.group(0) if duration_match else "?"
            track_name_raw = text.replace(duration, "").strip()

            tracks_data.append({
                "track_number": str(i + 1),
                "track_name": track_name_raw, 
                "track_duration": duration
            })

        return {
            "album_name": raw_title,
            "album_launch_year": year,
            "album_label": label,
            "album_styles": styles,
            "album_tracks": tracks_data
        }
    except Exception as e:
        print(f"Erro parse álbum: {e}")
        return None

def _parse_artist_page(artist_url):
    soup = _get_page_content(artist_url)
    if not soup: return {}, []

    try:
        # Nome do artista
        h1 = soup.select_one('h1')
        artist_name_raw = h1.text.strip() if h1 else "Desconhecido"
        # Limpeza leve apenas para comparação interna no scraper
        artist_name_clean = re.sub(r'\s+\(\d+\)$', '', artist_name_raw)

        # Membros
        members = []
        # Procura a tabela específica de perfil
        table_rows = soup.select('.table_c5ftk tr')
        if table_rows:
            for tr in table_rows:
                th = tr.select_one('th')
                # Verifica se o cabeçalho da linha tem "Membros"
                if th and re.search(r'Membros|Members', th.text, re.IGNORECASE):
                    print("   -> Seção 'Membros' localizada via TABELA.")
                    # Pega os links dentro das células de dados (td)
                    links = tr.select('td a')
                    for link in links:
                        name = link.text.strip()
                        href = link.get('href', '')
                        if name and "/artist/" in href and "img" not in str(link):
                            if name.lower() != artist_name_clean.lower():
                                members.append(name)
                    break 

        # Sites
        sites = []
        # Tenta achar Sites na tabela também
        if table_rows:
            for tr in table_rows:
                th = tr.select_one('th')
                if th and re.search(r'Sites|Sítios', th.text, re.IGNORECASE):
                    links = tr.select('td a')
                    for link in links:
                        sites.append(link.get('href', ''))
                    break
        

        artist_data = {
            "artist_name": artist_name_raw, 
            "artist_members": members, 
            "artist_sites": sites      
        }

        # Álbuns
        album_links = []
        # Tenta pegar masters (versao principal do álbum)
        potential_albums = soup.select('a[href^="/master/"]')
        
        # Se não tiver masters, pega releases 
        if not potential_albums:
            potential_albums = soup.select('a[href^="/release/"]')

        # Busca direta pelo padrao do link (CSS Selector),
        # sem precisar navegar por divs aninhadas.
        for link in potential_albums:
            if len(album_links) >= 20: break
            
            href = link['href']
            if not href.startswith('http'): href = BASE_URL + href
            
            # Evita duplicados
            if href not in album_links: 
                album_links.append(href)

        return artist_data, album_links

    except Exception as e:
        print(f"Erro no artista: {e}")
        return {}, []

def run_scraper(genre_name="Blues"):
    start_url = f"{BASE_URL}/genre/{genre_name}"
    print(f"____________ FASE 1: EXTRAÇÃO (Scraping) _________________")
    soup = _get_page_content(start_url)
    if not soup: return []

    all_data = []
    processed_artists = 0
    seen_urls = set()

    artist_links = soup.select('a[href^="/artist/"]')

    for link in artist_links:
        if processed_artists >= 10: break
        
        url = link['href']
        if not url.startswith('http'): url = BASE_URL + url
        if url in seen_urls or "Various" in url: continue
        if not re.search(r'/artist/\d+', url): continue
        
        seen_urls.add(url)
        print(f"Artista {processed_artists + 1}: {url}")
        
        artist_data, album_urls = _parse_artist_page(url)
        if not artist_data: continue

        processed_artists += 1
        
        count = 0
        for alb_url in album_urls:
            if count >= 10: break
            alb_data = _parse_album_page(alb_url)
            if alb_data:
                record = {
                    "id": "temp_id",
                    "genre": genre_name,
                    **artist_data,
                    **alb_data
                }
                all_data.append(record)
                count += 1
                print(f" -----> Álbum coletado: {alb_data['album_name']}")

    if driver: driver.quit()
    return all_data