from scraper import run_scraper
from data_handler import save_to_jsonl
from transform import process_file

GENRE = "Blues"
RAW_FILE = "data/blues_data_raw.jsonl"  
CLEAN_FILE = "data/blues_data_clean.jsonl"     

def main():
    # Extração
    raw_data = run_scraper(GENRE)
    
    if raw_data:
        # Salva o arquivo raw primeiro 
        save_to_jsonl(raw_data, RAW_FILE)
        print(f"\nDados brutos salvos em: {RAW_FILE}")
        
        # Transformação
        print("\n_____________FASE 2: TRANSFORMAÇÃO (Scraping)_____________")
        process_file(input_file=RAW_FILE, output_file=CLEAN_FILE)
        
        print(f"\n_____________PROCESSO CONCLUÍDO! Arquivo final: {CLEAN_FILE}________________")
    else:
        print("Nenhum dado coletado.")

if __name__ == "__main__":
    main()