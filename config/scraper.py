#!/usr/bin/env python3
"""
Scraper para extrair dados nutricionais dos produtos da Sadia
Compatível com Python 3.13+
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import time
import re
from dotenv import load_dotenv
import json

# Carrega as variáveis de ambiente
load_dotenv()

class ScraperSadia:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.dados_produtos = []
        
    def extrair_html(self, url):
        """Extrai o HTML de uma URL"""
        try:
            print(f"🌐 Fazendo requisição para: {url}")
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            print(f"✅ HTML extraído com sucesso! Tamanho: {len(response.text)} caracteres")
            return response.text
            
        except Exception as e:
            print(f"❌ Erro ao extrair HTML: {e}")
            return None
    
    def extrair_nome_produto(self, soup):
        """Extrai o nome do produto"""
        try:
            # Procura pelo título do produto
            titulo = soup.find('h1', class_='title-product')
            if titulo:
                nome = titulo.get_text(strip=True)
                # Capitaliza a primeira letra e adiciona " - Sadia"
                nome = nome[0].upper() + nome[1:] + " - Sadia"
                return nome
            return "Nome não encontrado"
        except Exception as e:
            print(f"❌ Erro ao extrair nome: {e}")
            return "Erro ao extrair nome"
    
    def extrair_categoria(self, soup):
        """Extrai a categoria do produto"""
        try:
            # Procura por breadcrumbs ou informações de categoria
            breadcrumbs = soup.find('nav', class_='breadcrumb')
            if breadcrumbs:
                links = breadcrumbs.find_all('a')
                if len(links) > 1:
                    return links[1].get_text(strip=True)
            
            # Tenta encontrar na URL
            url = soup.find('meta', property='og:url')
            if url:
                url_content = url.get('content', '')
                if '/produtos/' in url_content:
                    partes = url_content.split('/produtos/')
                    if len(partes) > 1:
                        categoria = partes[1].split('/')[0]
                        return categoria.replace('-', ' ').title()
            
            return "Categoria não encontrada"
        except Exception as e:
            print(f"❌ Erro ao extrair categoria: {e}")
            return "Erro ao extrair categoria"
    
    def extrair_dados_nutricionais(self, soup):
        """Extrai os dados nutricionais da tabela"""
        dados = {
            'PORCAO (g)': 0.0,
            'CALORIAS (kcal)': 0.0,
            'CARBOIDRATOS (g)': 0.0,
            'PROTEINAS (g)': 0.0,
            'GORDURAS_TOTAIS (g)': 0.0,
            'GORDURAS_SATURADAS (g)': 0.0,
            'FIBRAS (g)': 0.0,
            'ACUCARES (g)': 0.0,
            'SODIO (mg)': 0.0
        }
        
        try:
            # Procura pela tabela nutricional
            tabela_nutricional = soup.find('div', class_='box-nutritional-table')
            if not tabela_nutricional:
                print("⚠️ Tabela nutricional não encontrada")
                return dados
            
            # Procura pela tabela dentro da div
            tabela = tabela_nutricional.find('table')
            if not tabela:
                print("⚠️ Tabela não encontrada dentro da div nutricional")
                return dados
            
            # Extrai as linhas da tabela
            linhas = tabela.find_all('tr')
            
            for linha in linhas:
                celulas = linha.find_all(['td', 'th'])
                if len(celulas) >= 2:
                    nutriente = celulas[0].get_text(strip=True).lower()
                    valor = celulas[1].get_text(strip=True)  # Sempre pega a segunda coluna
                    # Corrige o valor: remove pontos (milhar), troca vírgula por ponto (decimal)
                    valor_corrigido = valor.replace('.', '').replace(',', '.')
                    # Pega apenas o primeiro valor se houver divisores
                    valor_primeiro = valor_corrigido.split('=')[0].split('\\')[0].split('/')[0].strip()
                    try:
                        valor_final = float(valor_primeiro)
                    except ValueError:
                        valor_final = 0.0
                    
                    # Mapeia os nutrientes (busca apenas a palavra principal, ignorando parênteses)
                    if 'valor energético' in nutriente or 'calorias' in nutriente:
                        dados['CALORIAS (kcal)'] = valor_final
                    elif 'carboidratos' in nutriente:
                        dados['CARBOIDRATOS (g)'] = valor_final
                    elif 'proteínas' in nutriente or 'proteínas (g)' in nutriente:
                        dados['PROTEINAS (g)'] = valor_final
                    elif 'gorduras totais' in nutriente:
                        dados['GORDURAS_TOTAIS (g)'] = valor_final
                    elif 'gorduras saturadas' in nutriente:
                        dados['GORDURAS_SATURADAS (g)'] = valor_final
                    elif 'fibra alimentar' in nutriente or 'fibra' in nutriente:
                        dados['FIBRAS (g)'] = valor_final
                    elif 'açúcares' in nutriente or 'açúcares totais' in nutriente:
                        dados['ACUCARES (g)'] = valor_final
                    elif 'sódio' in nutriente:
                        dados['SODIO (mg)'] = valor_final
            
            # Define a porção como 100g (padrão)
            dados['PORCAO (g)'] = 100
            
            print("✅ Dados nutricionais extraídos com sucesso")
            return dados
            
        except Exception as e:
            print(f"❌ Erro ao extrair dados nutricionais: {e}")
            return dados
    
    def processar_produto(self, url):
        """Processa um produto individual"""
        print(f"\n🔄 Processando produto: {url}")
        
        # Extrai o HTML
        html = self.extrair_html(url)
        if not html:
            return None
        
        # Parse do HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extrai os dados
        nome = self.extrair_nome_produto(soup)
        categoria = self.extrair_categoria(soup)
        dados_nutricionais = self.extrair_dados_nutricionais(soup)
        
        # Monta o dicionário do produto
        produto = {
            'NOME_PRODUTO': nome,
            'URL': url,
            'CATEGORIA': categoria,
            **dados_nutricionais
        }
        
        print(f"✅ Produto processado: {nome}")
        return produto
    
    def salvar_csv(self, dados, nome_arquivo=None):
        """Salva os dados em um arquivo CSV"""
        if not nome_arquivo:
            nome_arquivo = "produtos_sadia.csv"
        
        # Cria o DataFrame
        df = pd.DataFrame(dados)
        
        # Define a ordem das colunas
        colunas = [
            'NOME_PRODUTO', 'URL', 'CATEGORIA', 'PORCAO (g)', 
            'CALORIAS (kcal)', 'CARBOIDRATOS (g)', 'PROTEINAS (g)', 
            'GORDURAS_TOTAIS (g)', 'GORDURAS_SATURADAS (g)', 
            'FIBRAS (g)', 'ACUCARES (g)', 'SODIO (mg)'
        ]
        
        # Reorganiza as colunas
        df = df[colunas]
        
        # Salva o arquivo
        caminho_arquivo = os.path.join('dados', nome_arquivo)
        os.makedirs('dados', exist_ok=True)
        
        df.to_csv(caminho_arquivo, index=False, encoding='utf-8-sig')
        print(f"💾 CSV salvo em: {caminho_arquivo}")
        return caminho_arquivo
    
    def processar_lista_urls(self, urls):
        """Processa uma lista de URLs"""
        print(f"🚀 Iniciando processamento de {len(urls)} produtos")
        
        for i, url in enumerate(urls, 1):
            print(f"\n📦 Produto {i}/{len(urls)}")
            
            produto = self.processar_produto(url)
            if produto:
                self.dados_produtos.append(produto)
            
            # Delay entre requisições para não sobrecarregar o servidor
            if i < len(urls):
                print("⏳ Aguardando 2 segundos...")
                time.sleep(2)
        
        print(f"\n✅ Processamento concluído! {len(self.dados_produtos)} produtos extraídos")
        
        # Salva os dados
        if self.dados_produtos:
            arquivo_salvo = self.salvar_csv(self.dados_produtos)
            print(f"📊 Dados salvos em: {arquivo_salvo}")
            return arquivo_salvo
        else:
            print("❌ Nenhum produto foi processado com sucesso")
            return None

def main():
    """Função principal"""
    print("🍗 Scraper Sadia - Extrator de Dados Nutricionais")
    print("=" * 50)
    
    # Cria o scraper
    scraper = ScraperSadia()
    
    # Tenta carregar URLs do JSON
    json_file = "dados/urls_produtos.json"
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                produtos_url = json.load(f)
            print(f"📋 Carregadas {len(produtos_url)} URLs do arquivo JSON")
        except Exception as e:
            print(f"❌ Erro ao carregar JSON: {e}")
            print("📋 Usando lista padrão de URLs")
            produtos_url = [
                'https://www.sadia.com.br/produtos/aves/linha-dia-a-dia/frango-inteiro-sem-miudos-4/',
                'https://www.sadia.com.br/produtos/nba/nba/empanadissimo-100-peito-de-frango-leve-picancia/',
                'https://www.sadia.com.br/produtos/frios/frios-dia-a-dia/presunto-cozido-fatiado-180g/',
                'https://www.sadia.com.br/produtos/frios/frios-dia-a-dia/mignoneto/',
                'https://www.sadia.com.br/produtos/lanches/batatas-fritas/batata-palito-pre-frita-105kg/',
                'https://www.sadia.com.br/produtos/lanches/batatas-fritas/batata-palito-pre-frita-2kg/',
                'https://www.sadia.com.br/produtos/linguicas/linguica-defumada/linguica-fininha-25kg/'
            ]
    else:
        print("📋 Arquivo JSON não encontrado, usando lista padrão")
        produtos_url = [
            'https://www.sadia.com.br/produtos/aves/linha-dia-a-dia/frango-inteiro-sem-miudos-4/',
            'https://www.sadia.com.br/produtos/nba/nba/empanadissimo-100-peito-de-frango-leve-picancia/',
            'https://www.sadia.com.br/produtos/frios/frios-dia-a-dia/presunto-cozido-fatiado-180g/',
            'https://www.sadia.com.br/produtos/frios/frios-dia-a-dia/mignoneto/',
            'https://www.sadia.com.br/produtos/lanches/batatas-fritas/batata-palito-pre-frita-105kg/',
            'https://www.sadia.com.br/produtos/lanches/batatas-fritas/batata-palito-pre-frita-2kg/',
            'https://www.sadia.com.br/produtos/linguicas/linguica-defumada/linguica-fininha-25kg/'
        ]
    
    # Processa os produtos
    arquivo_salvo = scraper.processar_lista_urls(produtos_url)
    
    if arquivo_salvo:
        print(f"\n🎉 Processamento concluído com sucesso!")
        print(f"📁 Arquivo salvo: {arquivo_salvo}")
    else:
        print("\n❌ Falha no processamento")

if __name__ == "__main__":
    main() 