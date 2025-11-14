import re

# Funções de limpeza de texto

def clean_text(text):
    if not text: return None
    return re.sub(r'\s+', ' ', text).strip()

def clean_artist_name(name):
    if not name: return "Desconhecido"
    return re.sub(r'\s+\(\d+\)$', '', name)

def clean_album_name(raw_title):
    if not raw_title: return "Desconhecido"
    separators = [" – ", " - "]
    for sep in separators:
        if sep in raw_title:
            return raw_title.split(sep)[-1].strip()
    return raw_title

def clean_track_name(name):
    if not name: return "Unknown"
    name = re.sub(r'^\d+\.\s*', '', name)
    name = clean_album_name(name)
    return name

def clean_members(members_list, artist_name_clean):
    cleaned = []
    
    for m in members_list:
        m = clean_text(m)
        if not m: continue
        
        # Não adiciona se for o próprio artista
        if m.lower() == artist_name_clean.lower(): continue

        cleaned.append(m)
    
    # Remove duplicados 
    cleaned = list(set(cleaned))

    # Se a lista vier vazia, o "membro" será o próprio artista.
    if not cleaned:
        return [artist_name_clean]
    
    return cleaned

# N/A pra nulo
def clean_track_duration(duration):
    if duration == "?" or duration == "N/A":
        return None
    return duration

# N/A pra nulo
def clean_year(year):
    if year == "N/A":
        return None
    return year

def generate_id(artist, album):
    if not artist or not album:
        return "id_desconhecido"
        
    # Concatenacao, troca espaco por _ e deixa minusculo
    new_id = f"{artist}_{album}".replace(" ", "_").lower()
    
    # Remove caracteres especiais, exceto underline
    new_id = re.sub(r'[^a-z0-9_]', '', new_id)

    # Se ocorrer multiplos '_' substitui por apenas um
    new_id = re.sub(r'_+', '_', new_id)
    return new_id