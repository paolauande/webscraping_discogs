import json
import os

def save_to_jsonl(data_list, output_file):
    output_dir = os.path.dirname(output_file)

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Diretório '{output_dir}' criado")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data_list:
                json_string = json.dumps(item, ensure_ascii=False)
                f.write(json_string)
                f.write('\n')
    except IOError as e:
        print(f"Erro ao salvar o arquivo '{output_file}': {e}")
    except TypeError as e:
        print(f"Erro ao serializar dados para JSON: {e}")