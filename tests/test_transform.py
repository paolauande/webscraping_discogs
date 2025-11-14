import json
import os
import pytest
from src.transform import process_file 

# Esse teste cria um arquivo sujo, faz o processamento e le o arquivo limpo
def test_transformacao_com_arquivos(tmp_path):

    # Criacao de caminho de arquivos temporarios
    arquivo_entrada = tmp_path / "teste_raw.jsonl"
    arquivo_saida = tmp_path / "teste_clean.jsonl"

    # Simulacao da estrutura que o codigo espera (dados brutos)
    dado_bruto = {
        "artist_name": "B.B. King (2)",      
        "album_name": "Live & Well",         
        "album_launch_year": "1969",          
        "album_tracks": [                     
            {"track_name": "1. So Excited", "track_duration": "3:15"}, 
            {"track_name": "2. The Thrill Is Gone", "track_duration": "?"} 
        ],
        "genre": "Blues"
    }

    # Escrevemos esse dado no arquivo de entrada
    with open(arquivo_entrada, "w", encoding="utf-8") as f:
        f.write(json.dumps(dado_bruto) + "\n")

    # Chama a função original
    process_file(str(arquivo_entrada), str(arquivo_saida))

    # Lê o arquivo que foi gerado
    assert os.path.exists(arquivo_saida)

    with open(arquivo_saida, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()
        resultado = json.loads(conteudo)
    
    # Verifica Id
    assert resultado["id"] == "bb_king_live_well"
    
    # Verifica os outros campos
    assert resultado["artist_name"] == "B.B. King"
    assert resultado["album_name"] == "Live & Well"
    assert resultado["album_launch_year"] == "1969"
    
    # Verifica se limpou a lista de faixas
    assert len(resultado["album_tracks"]) == 2
    assert resultado["album_tracks"][0]["track_name"] == "So Excited"
    
    # Verifica tratamento de nulos na duração
    assert resultado["album_tracks"][1]["track_duration"] is None

    # Verifica as chaves esperadas
    chaves_esperadas = {
        "id", "genre", "artist_name", "artist_members", "artist_sites", 
        "album_name", "album_launch_year", "album_label", "album_styles", "album_tracks"
    }
    assert chaves_esperadas.issubset(resultado.keys())