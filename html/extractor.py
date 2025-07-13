import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import time

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def extrair_html(url):
    """
    Extrai o código HTML de uma URL com suporte a encoding UTF-8
    
    Args:
        url (str): URL para extrair o HTML
        
    Returns:
        str: Conteúdo HTML da página
    """
    try:
        # Configuração do cabeçalho para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Faz a requisição HTTP
        print(f"Fazendo requisição para: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        
        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()
        
        # Define o encoding como UTF-8
        response.encoding = 'utf-8'
        
        # Obtém o conteúdo HTML
        html_content = response.text
        
        print(f"HTML extraído com sucesso! Tamanho: {len(html_content)} caracteres")
        
        return html_content
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def salvar_html(html_content, nome_arquivo=None):
    """
    Salva o conteúdo HTML em um arquivo
    
    Args:
        html_content (str): Conteúdo HTML para salvar
        nome_arquivo (str): Nome do arquivo (opcional)
    """
    if not nome_arquivo:
        # Gera um nome baseado na data/hora
        nome_arquivo = f"pagina_{int(time.time())}.html"
    
    caminho_arquivo = os.path.join(os.path.dirname(__file__), nome_arquivo)
    
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(html_content)
        print(f"HTML salvo em: {caminho_arquivo}")
        return caminho_arquivo
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return None

def main():
    """
    Função principal que executa a extração
    """
    # Obtém a URL do arquivo .env
    url = os.getenv('URL_ALVO')
    
    if not url:
        print("Erro: URL_ALVO não encontrada no arquivo .env")
        print("Por favor, configure a variável URL_ALVO no arquivo .env")
        return
    
    print("=== Extrator de HTML ===")
    print(f"URL configurada: {url}")
    print("-" * 30)
    
    # Extrai o HTML
    html_content = extrair_html(url)
    
    if html_content:
        # Salva o HTML em arquivo
        arquivo_salvo = salvar_html(html_content)
        
        if arquivo_salvo:
            print("\n✅ Extração concluída com sucesso!")
            print(f"📁 Arquivo salvo: {arquivo_salvo}")
        else:
            print("\n❌ Erro ao salvar o arquivo")
    else:
        print("\n❌ Falha na extração do HTML")

if __name__ == "__main__":
    main() 