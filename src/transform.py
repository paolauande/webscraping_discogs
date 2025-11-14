import json
import os
from src.utils import (
    clean_artist_name,
    clean_album_name,
    clean_members,
    clean_track_name,
    clean_track_duration,
    clean_year,
    generate_id
)

def process_file(input_file="data/blues_data_raw.jsonl", output_file="data/blues_data_clean.jsonl"):
    
    if not os.path.exists(input_file):
        print(f"Arquivo não encontrado: {input_file}")
        return

    print(f"Iniciando transformação...")
    
    processed_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        
        for line in fin:
            try:
                raw = json.loads(line)
                
                # Fase de limpeza
                
                artist_clean = clean_artist_name(raw.get('artist_name'))
                album_clean = clean_album_name(raw.get('album_name'))
                members_clean = clean_members(raw.get('artist_members', []), artist_clean)
                sites_clean = raw.get('artist_sites', []) 
                
                # Faixas
                tracks_clean = []
                for t in raw.get('album_tracks', []):
                    tracks_clean.append({
                        "track_number": t.get("track_number"),
                        "track_name": clean_track_name(t.get('track_name')),
                        "track_duration": clean_track_duration(t.get("track_duration"))
                    })

                # Geração do Id
                new_id = generate_id(artist_clean, album_clean)

                # Criando o JSON final
                clean_record = {
                    "id": new_id,
                    "genre": raw.get('genre'),
                    "artist_name": artist_clean,
                    "artist_members": members_clean,
                    "artist_sites": sites_clean,
                    "album_name": album_clean,
                    "album_launch_year": clean_year(raw.get('album_launch_year')),
                    "album_label": raw.get('album_label'),
                    "album_styles": raw.get('album_styles'),
                    "album_tracks": tracks_clean
                }
                
                # Escreve o JSON limpo no arquivo de saída
                fout.write(json.dumps(clean_record, ensure_ascii=False) + '\n')
                processed_count += 1
                
            except json.JSONDecodeError:
                print("Erro ao ler uma linha (JSON mal formado), pulando...")
                continue
            except Exception as e:
                print(f"Erro inesperado no processamento: {e}")
                continue

    print(f"Sucesso! {processed_count} registros transformados.")

if __name__ == "__main__":
    process_file()