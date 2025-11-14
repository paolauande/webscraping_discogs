from src.utils import (
    clean_artist_name,
    clean_album_name,
    clean_members,
    clean_track_name,
    clean_track_duration,
    clean_year,
    generate_id
)

# Testes para cada função de utils

# Testa se o nome do artista vem limpo
def test_clean_artist_name():
    assert clean_artist_name("Artista (1)") == "Artista"
    assert clean_artist_name("Artista Limpo") == "Artista Limpo"
    assert clean_artist_name(None) == "Desconhecido"

# Testa se apenas o titulo do álbum é extraído
def test_clean_album_name():
    # testa os dois separadores
    assert clean_album_name("Artista – Nome do Album") == "Nome do Album"
    assert clean_album_name("Artista - Nome do Album") == "Nome do Album"
    # testa se não quebra se não tiver separador
    assert clean_album_name("Nome do Album Sozinho") == "Nome do Album Sozinho"

# Testa se remove numeracao e redundancia das faixas
def test_clean_track_name():
    assert clean_track_name("1. Nome da Faixa") == "Nome da Faixa"
    # testa se ele também usa a lógica do clean_album_name
    assert clean_track_name("Artista - Nome da Faixa") == "Nome da Faixa"
    assert clean_track_name("1. Artista - Nome da Faixa") == "Nome da Faixa"

# Testa se o nome do artista é removido da lista de membros
def test_clean_members_remove_artista():
    membros = ["Membro A", "Membro B", "Artista Principal"]
    artista = "Artista Principal"
    esperado = ["Membro A", "Membro B"]
    
    # ordena as listas pra garantir que a comparação seja justa
    assert sorted(clean_members(membros, artista)) == sorted(esperado)

# Testa se a lista de membros vier vazia, retorna o artista
def test_clean_members_lista_vazia():
    membros = []
    artista = "Artista Sozinho"
    esperado = ["Artista Sozinho"]
    assert clean_members(membros, artista) == esperado

# Testa se a função remove duplicatas
def test_clean_members_remove_duplicados():
    membros = ["Membro A", "Membro A", "Membro B"]
    artista = "Artista Principal"
    esperado = ["Membro A", "Membro B"]
    assert sorted(clean_members(membros, artista)) == sorted(esperado)

# Testa a padronização de valores nulos
def test_clean_nulos_duration_e_year():
    # Teste da duração
    assert clean_track_duration("?") is None
    assert clean_track_duration("N/A") is None
    assert clean_track_duration("3:15") == "3:15"
    
    # Teste do ano
    assert clean_year("N/A") is None
    assert clean_year("1999") == "1999"


# Testa a criação do Id final
def test_generate_id():
    artista = "B.B. King"
    album = "Live & Well"
    
    # Esperado: minúsculo, sem espaços, sem caracteres especiais
    esperado = "bb_king_live_well"
    assert generate_id(artista, album) == esperado

    artista_vazio = ""
    assert generate_id(artista_vazio, album) == "id_desconhecido"