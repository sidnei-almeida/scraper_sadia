#!/usr/bin/env python3
"""
URL Collector para produtos da Sadia
Coleta URLs de produtos de todas as categorias e salva em JSON
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
import os

class URLCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.urls_produtos = set()  # Usa set para evitar duplicatas
        
        # Categorias da Sadia
        self.categorias = {
            'NBA': 'https://www.sadia.com.br/produtos/nba',
            'AVES': 'https://www.sadia.com.br/produtos/aves',
            'FRIOS': 'https://www.sadia.com.br/produtos/frios',
            'LANCHES': 'https://www.sadia.com.br/produtos/lanches',
            'SUINOS': 'https://www.sadia.com.br/produtos/suinos',
            'LINGUICA': 'https://www.sadia.com.br/produtos/linguicas',
            'PRATOS': 'https://www.sadia.com.br/produtos/pratos-prontos',
            'PESCADOS': 'https://www.sadia.com.br/produtos/pescados',
            'SALSICHAS': 'https://www.sadia.com.br/produtos/salsichas',
            'SOBREMESAS': 'https://www.sadia.com.br/produtos/sobremesas',
            'VEGETAIS': 'https://www.sadia.com.br/produtos/vegetais',
            'COMEMORATIVOS': 'https://www.sadia.com.br/produtos/comemorativos'
        }
        
        # URLs para excluir (não são produtos)
        self.urls_excluir = {
            'https://www.sadia.com.br/produtos/',
            'https://www.sadia.com.br/produtos/nba',
            'https://www.sadia.com.br/produtos/aves',
            'https://www.sadia.com.br/produtos/frios',
            'https://www.sadia.com.br/produtos/lanches',
            'https://www.sadia.com.br/produtos/suinos',
            'https://www.sadia.com.br/produtos/linguicas',
            'https://www.sadia.com.br/produtos/pratos-prontos',
            'https://www.sadia.com.br/produtos/pescados',
            'https://www.sadia.com.br/produtos/salsichas',
            'https://www.sadia.com.br/produtos/sobremesas',
            'https://www.sadia.com.br/produtos/vegetais',
            'https://www.sadia.com.br/produtos/comemorativos'
        }
    
    def extrair_html(self, url):
        """Extrai o HTML de uma URL"""
        try:
            print(f"🌐 Acessando: {url}")
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            print(f"✅ HTML extraído: {len(response.text)} caracteres")
            return response.text
            
        except Exception as e:
            print(f"❌ Erro ao acessar {url}: {e}")
            return None
    
    def extrair_urls_da_pagina(self, html, url_base):
        """Extrai URLs de produtos usando o seletor específico"""
        urls_encontradas = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procura especificamente pelos links de produtos com a classe btn-veja-mais
            links_produtos = soup.find_all('a', class_='btn-default tiny-btn btn-veja-mais')
            
            for link in links_produtos:
                href = link.get('href')
                if href:
                    # Adiciona o domínio base se necessário
                    if href.startswith('produtos/'):
                        url_absoluta = f"https://www.sadia.com.br/{href}"
                    else:
                        # Converte para URL absoluta
                        url_absoluta = urljoin(url_base, href)
                    
                    # Filtra apenas URLs da Sadia
                    if 'sadia.com.br' in url_absoluta:
                        urls_encontradas.add(url_absoluta)
            
            print(f"🔗 Encontradas {len(urls_encontradas)} URLs de produtos em {url_base}")
            return urls_encontradas
            
        except Exception as e:
            print(f"❌ Erro ao extrair URLs: {e}")
            return set()
    
    def filtrar_urls_produtos(self, urls):
        """Filtra apenas URLs de produtos válidas"""
        urls_produtos = set()
        
        for url in urls:
            # Remove URLs que não são produtos
            if url in self.urls_excluir:
                continue
            
            # Verifica se é uma URL de produto válida
            if '/produtos/' in url and not url.endswith('/'):
                # Verifica se tem pelo menos 2 níveis após /produtos/
                partes = url.split('/produtos/')
                if len(partes) > 1:
                    caminho = partes[1]
                    if caminho.count('/') >= 1:  # Pelo menos categoria/produto
                        urls_produtos.add(url)
        
        print(f"✅ Filtradas {len(urls_produtos)} URLs de produtos válidas")
        return urls_produtos
    
    def processar_categoria(self, nome_categoria, url_categoria):
        """Processa uma categoria específica"""
        print(f"\n📂 Processando categoria: {nome_categoria}")
        print(f"🔗 URL: {url_categoria}")
        
        # Extrai HTML da categoria
        html = self.extrair_html(url_categoria)
        if not html:
            return set()
        
        # Extrai URLs da página
        urls_pagina = self.extract_urls_from_page(html, url_categoria)
        
        # Filtra URLs de produtos
        urls_produtos = self.filtrar_urls_produtos(urls_pagina)
        
        return urls_produtos
    
    def extract_urls_from_page(self, html, url_base):
        """Extrai URLs de produtos usando o seletor específico (método auxiliar)"""
        urls_encontradas = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procura especificamente pelos links de produtos com a classe btn-veja-mais
            links_produtos = soup.find_all('a', class_='btn-default tiny-btn btn-veja-mais')
            
            for link in links_produtos:
                href = link.get('href')
                if href:
                    # Adiciona o domínio base se necessário
                    if href.startswith('produtos/'):
                        url_absoluta = f"https://www.sadia.com.br/{href}"
                    else:
                        # Converte para URL absoluta
                        url_absoluta = urljoin(url_base, href)
                    
                    # Filtra apenas URLs da Sadia
                    if 'sadia.com.br' in url_absoluta:
                        urls_encontradas.add(url_absoluta)
            
            return urls_encontradas
            
        except Exception as e:
            print(f"❌ Erro ao extrair URLs: {e}")
            return set()
    
    def processar_todas_categorias(self):
        """Processa todas as categorias"""
        print("🚀 Iniciando coleta de URLs de produtos")
        print("=" * 50)
        
        for nome_categoria, url_categoria in self.categorias.items():
            urls_produtos = self.processar_categoria(nome_categoria, url_categoria)
            self.urls_produtos.update(urls_produtos)
            
            # Delay entre categorias
            if nome_categoria != list(self.categorias.keys())[-1]:
                print("⏳ Aguardando 3 segundos...")
                time.sleep(3)
        
        print(f"\n✅ Coleta concluída!")
        print(f"📊 Total de URLs de produtos encontradas: {len(self.urls_produtos)}")
    
    def salvar_json(self, nome_arquivo="urls_produtos.json"):
        """Salva as URLs em arquivo JSON"""
        # Converte set para list para JSON
        urls_lista = list(self.urls_produtos)
        
        # Cria pasta dados se não existir
        os.makedirs('dados', exist_ok=True)
        
        # Salva o JSON
        caminho_arquivo = os.path.join('dados', nome_arquivo)
        
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(urls_lista, f, indent=2, ensure_ascii=False)
        
        print(f"💾 URLs salvas em: {caminho_arquivo}")
        return caminho_arquivo
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas da coleta"""
        print(f"\n📈 Estatísticas da Coleta:")
        print(f"   • Total de URLs de produtos: {len(self.urls_produtos)}")
        
        # Agrupa por categoria
        categorias_encontradas = {}
        for url in self.urls_produtos:
            if '/produtos/' in url:
                partes = url.split('/produtos/')
                if len(partes) > 1:
                    categoria = partes[1].split('/')[0]
                    if categoria not in categorias_encontradas:
                        categorias_encontradas[categoria] = 0
                    categorias_encontradas[categoria] += 1
        
        print(f"   • Categorias encontradas:")
        for categoria, quantidade in categorias_encontradas.items():
            print(f"     - {categoria}: {quantidade} produtos")

def main():
    """Função principal"""
    print("🔗 URL Collector - Sadia")
    print("=" * 30)
    
    # Cria o coletor
    coletor = URLCollector()
    
    # Processa todas as categorias
    coletor.processar_todas_categorias()
    
    # Mostra estatísticas
    coletor.mostrar_estatisticas()
    
    # Salva o JSON
    arquivo_salvo = coletor.salvar_json()
    
    print(f"\n🎉 Coleta concluída com sucesso!")
    print(f"📁 Arquivo salvo: {arquivo_salvo}")

if __name__ == "__main__":
    main() 