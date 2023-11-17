import requests

# URL do endpoint
url = "http://0.0.0.0:8000/file_sand"  # Substitua pelo URL correto do seu servidor

# Caminho do arquivo Parquet que você deseja enviar
file_path = "/Users/joao/Downloads/06120092/TCRF_ARCHIVE_06120092_20230519154702.parquet"

# Crie um dicionário de arquivos para enviar o arquivo Parquet
files = {'file': open(file_path, 'rb')}

try:
    # Faça uma solicitação POST para o endpoint
    response = requests.post(url, files=files)
    
    # Verifique a resposta
    if response:
        print(f"{response.status_code} - {response.text}")
except Exception as e:
    print(f"Erro ao fazer a solicitação POST: {str(e)}")