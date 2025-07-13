#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🍗 SCRAPER SADIA - Interface Principal
=====================================
Sistema completo para coleta e extração de dados nutricionais dos produtos Sadia

COMO USAR:
1. Execute: python main.py
2. Escolha a opção desejada no menu
3. Acompanhe o progresso em tempo real
4. Visualize os resultados na pasta dados/
"""

import os
import sys
import time
import glob
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================================
# 🎨 SISTEMA DE CORES ANSI PARA TERMINAL
# ============================================================================
class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    MAGENTA = '\033[95m'
    BRANCO = '\033[97m'

# ============================================================================
# 🛠️ FUNÇÕES UTILITÁRIAS
# ============================================================================
def limpar_terminal():
    """Limpa o terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    """Exibe o banner principal do programa"""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🍗 SCRAPER SADIA                          ║
║                                                              ║
║              Sistema de Coleta de Dados Nutricionais         ║
║                                                              ║
║  🔗 Coleta URLs de Produtos                                 ║
║  📊 Extração de Dados Nutricionais                          ║
║  📈 Análise e Relatórios                                    ║
╚══════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def mostrar_barra_progresso(texto: str, duracao: float = 2.0):
    """Exibe uma barra de progresso animada"""
    print(f"\n{Cores.AMARELO}⏳ {texto}...{Cores.RESET}")
    barra_tamanho = 40
    for i in range(barra_tamanho + 1):
        progresso = i / barra_tamanho
        barra = "█" * i + "░" * (barra_tamanho - i)
        porcentagem = int(progresso * 100)
        print(f"\r{Cores.VERDE}[{barra}] {porcentagem}%{Cores.RESET}", end="", flush=True)
        time.sleep(duracao / barra_tamanho)
    print()

def mostrar_menu():
    """Exibe o menu principal"""
    menu = f"""
{Cores.AZUL}{Cores.BOLD}═══════════════════ MENU PRINCIPAL ═══════════════════{Cores.RESET}

{Cores.VERDE}🚀 OPERAÇÕES PRINCIPAIS:{Cores.RESET}
  {Cores.AMARELO}1.{Cores.RESET} 🔗 {Cores.BRANCO}Coletar URLs{Cores.RESET} - Extrai URLs de produtos das categorias
  {Cores.AMARELO}2.{Cores.RESET} 📊 {Cores.BRANCO}Extrair Dados{Cores.RESET} - Coleta dados nutricionais dos produtos
  {Cores.AMARELO}3.{Cores.RESET} 🎯 {Cores.BRANCO}Coleta Completa{Cores.RESET} - URLs + Dados (automático)

{Cores.VERDE}📁 GERENCIAR DADOS:{Cores.RESET}
  {Cores.AMARELO}4.{Cores.RESET} 📋 {Cores.BRANCO}Ver Arquivos{Cores.RESET} - Lista arquivos gerados
  {Cores.AMARELO}5.{Cores.RESET} 🗑️  {Cores.BRANCO}Limpar Dados{Cores.RESET} - Remove arquivos antigos
  {Cores.AMARELO}6.{Cores.RESET} 📈 {Cores.BRANCO}Estatísticas{Cores.RESET} - Mostra resumo dos dados

{Cores.VERDE}⚙️  CONFIGURAÇÕES:{Cores.RESET}
  {Cores.AMARELO}7.{Cores.RESET} 🔧 {Cores.BRANCO}Verificar Ambiente{Cores.RESET} - Testa dependências
  {Cores.AMARELO}8.{Cores.RESET} 📖 {Cores.BRANCO}Sobre o Programa{Cores.RESET} - Informações e estatísticas
  {Cores.AMARELO}9.{Cores.RESET} ❌ {Cores.BRANCO}Sair{Cores.RESET} - Encerrar programa

{Cores.AZUL}══════════════════════════════════════════════════════{Cores.RESET}
"""
    print(menu)

def obter_escolha() -> str:
    """Obtém a escolha do usuário"""
    try:
        escolha = input(f"{Cores.MAGENTA}👉 Digite sua opção (1-9): {Cores.RESET}").strip()
        return escolha
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Programa interrompido pelo usuário{Cores.RESET}")
        sys.exit(0)

# ============================================================================
# 🎯 FUNÇÕES ESPECÍFICAS DO SCRAPER SADIA
# ============================================================================

def executar_coleta_urls():
    """Executa a coleta de URLs de produtos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🔗 COLETANDO URLs DE PRODUTOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.VERDE}✅ Configurações:{Cores.RESET}")
    print(f"   📊 Categorias: {Cores.AMARELO}12 categorias{Cores.RESET}")
    print(f"   🔗 Seletor: {Cores.AMARELO}btn-veja-mais{Cores.RESET}")
    print(f"   📁 Saída: {Cores.AMARELO}dados/urls_produtos.json{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            print(f"\n{Cores.VERDE}🚀 Iniciando coleta de URLs...{Cores.RESET}")
            
            # Mostra barra de progresso inicial
            mostrar_barra_progresso("Preparando coleta de URLs", 1.5)
            
            # Executa o coletor de URLs
            resultado = subprocess.run([
                sys.executable, 'config/url_collector.py'
            ], capture_output=True, text=True, encoding='utf-8')
            
            if resultado.returncode == 0:
                print(f"{Cores.VERDE}✅ Coleta de URLs concluída com sucesso!{Cores.RESET}")
                print(f"{Cores.CIANO}📊 Saída do processo:{Cores.RESET}")
                print(resultado.stdout)
            else:
                print(f"{Cores.VERMELHO}❌ Erro na coleta de URLs:{Cores.RESET}")
                print(resultado.stderr)
                
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def executar_extracao_dados():
    """Executa a extração de dados nutricionais"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📊 EXTRAINDO DADOS NUTRICIONAIS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    # Verifica se existe o arquivo de URLs
    if not os.path.exists('dados/urls_produtos.json'):
        print(f"{Cores.AMARELO}⚠️  Arquivo de URLs não encontrado!{Cores.RESET}")
        print(f"   • Execute primeiro a opção 'Coletar URLs'{Cores.RESET}")
        return
    
    print(f"\n{Cores.VERDE}✅ Configurações:{Cores.RESET}")
    print(f"   📊 Fonte: {Cores.AMARELO}dados/urls_produtos.json{Cores.RESET}")
    print(f"   📈 Saída: {Cores.AMARELO}dados/produtos_sadia.csv{Cores.RESET}")
    print(f"   ⏱️  Tempo estimado: {Cores.AMARELO}2-5 minutos{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            print(f"\n{Cores.VERDE}🚀 Iniciando extração de dados...{Cores.RESET}")
            
            # Mostra barra de progresso inicial
            mostrar_barra_progresso("Preparando extração de dados", 1.5)
            
            # Executa o scraper
            resultado = subprocess.run([
                sys.executable, 'config/scraper.py'
            ], capture_output=True, text=True, encoding='utf-8')
            
            if resultado.returncode == 0:
                print(f"{Cores.VERDE}✅ Extração de dados concluída com sucesso!{Cores.RESET}")
                print(f"{Cores.CIANO}📊 Saída do processo:{Cores.RESET}")
                print(resultado.stdout)
            else:
                print(f"{Cores.VERMELHO}❌ Erro na extração de dados:{Cores.RESET}")
                print(resultado.stderr)
                
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def executar_coleta_completa():
    """Executa a coleta completa (URLs + Dados)"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🎯 COLETA COMPLETA AUTOMÁTICA{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Esta operação pode demorar {Cores.VERMELHO}5-10 minutos{Cores.RESET}")
    print(f"   • Serão executadas duas etapas sequenciais")
    print(f"   • 1º: Coleta de URLs de todas as categorias")
    print(f"   • 2º: Extração de dados nutricionais")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            # Etapa 1: Coleta de URLs
            print(f"\n{Cores.VERDE}🔄 ETAPA 1: Coletando URLs...{Cores.RESET}")
            mostrar_barra_progresso("Preparando coleta de URLs", 1.0)
            resultado_urls = subprocess.run([
                sys.executable, 'config/url_collector.py'
            ], capture_output=True, text=True, encoding='utf-8')
            
            if resultado_urls.returncode != 0:
                print(f"{Cores.VERMELHO}❌ Erro na coleta de URLs:{Cores.RESET}")
                print(resultado_urls.stderr)
                return
            
            print(f"{Cores.VERDE}✅ URLs coletadas com sucesso!{Cores.RESET}")
            
            # Etapa 2: Extração de dados
            print(f"\n{Cores.VERDE}🔄 ETAPA 2: Extraindo dados nutricionais...{Cores.RESET}")
            mostrar_barra_progresso("Preparando extração de dados", 1.0)
            resultado_dados = subprocess.run([
                sys.executable, 'config/scraper.py'
            ], capture_output=True, text=True, encoding='utf-8')
            
            if resultado_dados.returncode == 0:
                print(f"{Cores.VERDE}✅ Coleta completa finalizada com sucesso!{Cores.RESET}")
                print(f"{Cores.CIANO}📊 Resultados:{Cores.RESET}")
                print(resultado_dados.stdout)
            else:
                print(f"{Cores.VERMELHO}❌ Erro na extração de dados:{Cores.RESET}")
                print(resultado_dados.stderr)
                
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def listar_arquivos_gerados():
    """Lista arquivos gerados pelo programa"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 ARQUIVOS GERADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    pasta_dados = "dados"
    extensoes = ["*.json", "*.csv"]
    
    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return
    
    arquivos = []
    for extensao in extensoes:
        arquivos.extend(glob.glob(f"{pasta_dados}/{extensao}"))
    
    if not arquivos:
        print(f"{Cores.AMARELO}📄 Nenhum arquivo encontrado em '{pasta_dados}'{Cores.RESET}")
        return
    
    print(f"\n{Cores.VERDE}📊 Total de arquivos: {len(arquivos)}{Cores.RESET}\n")
    
    for i, arquivo in enumerate(sorted(arquivos, reverse=True), 1):
        nome_arquivo = os.path.basename(arquivo)
        tamanho = os.path.getsize(arquivo)
        data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))
        
        # Calcula o tamanho em formato legível
        if tamanho < 1024:
            tamanho_str = f"{tamanho} B"
        elif tamanho < 1024 * 1024:
            tamanho_str = f"{tamanho / 1024:.1f} KB"
        else:
            tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"
        
        # Determina o tipo de arquivo
        if arquivo.endswith('.json'):
            tipo = "📋 URLs"
        elif arquivo.endswith('.csv'):
            tipo = "📊 Dados"
        else:
            tipo = "📄 Arquivo"
        
        print(f"{Cores.AMARELO}{i:2d}.{Cores.RESET} {Cores.BRANCO}{nome_arquivo}{Cores.RESET} {tipo}")
        print(f"     📅 {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"     📏 {tamanho_str}")
        print()

def limpar_dados_antigos():
    """Remove arquivos antigos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🗑️  LIMPAR DADOS ANTIGOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    pasta_dados = "dados"
    extensoes = ["*.json", "*.csv"]
    
    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return
    
    arquivos = []
    for extensao in extensoes:
        arquivos.extend(glob.glob(f"{pasta_dados}/{extensao}"))
    
    if not arquivos:
        print(f"{Cores.VERDE}✅ Nenhum arquivo para limpar{Cores.RESET}")
        return
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Serão removidos {Cores.VERMELHO}{len(arquivos)} arquivos{Cores.RESET}")
    print(f"   • Esta ação {Cores.VERMELHO}NÃO PODE ser desfeita{Cores.RESET}")
    
    for arquivo in arquivos:
        nome = os.path.basename(arquivo)
        print(f"   • {Cores.AMARELO}{nome}{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Tem certeza? Digite 'CONFIRMAR' para prosseguir: {Cores.RESET}")
    
    if confirmar == "CONFIRMAR":
        try:
            for arquivo in arquivos:
                os.remove(arquivo)
            print(f"\n{Cores.VERDE}✅ {len(arquivos)} arquivos removidos com sucesso!{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro ao remover arquivos: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def mostrar_estatisticas():
    """Mostra estatísticas dos dados coletados"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📈 ESTATÍSTICAS DOS DADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    # Verifica arquivo de URLs
    urls_file = "dados/urls_produtos.json"
    if os.path.exists(urls_file):
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                urls = json.load(f)
            print(f"{Cores.VERDE}🔗 URLs Coletadas:{Cores.RESET} {len(urls)} produtos")
        except:
            print(f"{Cores.VERMELHO}❌ Erro ao ler arquivo de URLs{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⚠️  Arquivo de URLs não encontrado{Cores.RESET}")
    
    # Verifica arquivo de dados
    dados_file = "dados/produtos_sadia.csv"
    if os.path.exists(dados_file):
        try:
            # Importa pandas apenas quando necessário
            try:
                import pandas as pd
                df = pd.read_csv(dados_file)
                print(f"{Cores.VERDE}📊 Dados Extraídos:{Cores.RESET} {len(df)} produtos")
                
                # Estatísticas por categoria
                if 'CATEGORIA' in df.columns:
                    categorias = df['CATEGORIA'].value_counts()
                    print(f"\n{Cores.VERDE}📂 Produtos por Categoria:{Cores.RESET}")
                    for categoria, quantidade in categorias.head(5).items():
                        print(f"   • {categoria}: {quantidade} produtos")
            except ImportError:
                print(f"{Cores.AMARELO}⚠️  Pandas não instalado - não é possível ler estatísticas do CSV{Cores.RESET}")
            
        except Exception as e:
            print(f"{Cores.VERMELHO}❌ Erro ao ler dados: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⚠️  Arquivo de dados não encontrado{Cores.RESET}")
    
    # Informações do sistema
    print(f"\n{Cores.VERDE}💾 Espaço em Disco:{Cores.RESET}")
    if os.path.exists('dados'):
        total_size = sum(os.path.getsize(f) for f in glob.glob('dados/*') if os.path.isfile(f))
        if total_size < 1024:
            size_str = f"{total_size} B"
        elif total_size < 1024 * 1024:
            size_str = f"{total_size / 1024:.1f} KB"
        else:
            size_str = f"{total_size / (1024 * 1024):.1f} MB"
        print(f"   • Pasta dados/: {size_str}")

def verificar_ambiente():
    """Verifica se o ambiente está configurado corretamente"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🔧 VERIFICANDO AMBIENTE{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    # Verifica Python
    print(f"\n{Cores.VERDE}🐍 Python:{Cores.RESET}")
    print(f"   • Versão: {sys.version.split()[0]}")
    
    # Verifica dependências
    print(f"\n{Cores.VERDE}📦 Dependências:{Cores.RESET}")
    dependencias = [
        'requests', 'beautifulsoup4', 'pandas', 'lxml', 'python-dotenv'
    ]
    
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - Não instalado")
    
    # Verifica arquivos do projeto
    print(f"\n{Cores.VERDE}📁 Arquivos do Projeto:{Cores.RESET}")
    arquivos_projeto = [
        'config/url_collector.py',
        'config/scraper.py',
        'requirements.txt'
    ]
    
    for arquivo in arquivos_projeto:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - Não encontrado")
    
    # Verifica pasta dados
    print(f"\n{Cores.VERDE}📂 Pasta de Dados:{Cores.RESET}")
    if os.path.exists('dados'):
        print(f"   ✅ Pasta 'dados' existe")
        arquivos = os.listdir('dados')
        if arquivos:
            print(f"   📄 Arquivos: {len(arquivos)} encontrados")
        else:
            print(f"   📄 Pasta vazia")
    else:
        print(f"   ❌ Pasta 'dados' não existe")

def mostrar_sobre():
    """Exibe informações sobre o programa"""
    sobre = f"""
{Cores.CIANO}{Cores.BOLD}📖 SOBRE O SCRAPER SADIA{Cores.RESET}
{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}

{Cores.VERDE}🎯 OBJETIVO:{Cores.RESET}
   Sistema completo para coleta e extração de dados nutricionais 
   dos produtos da Sadia, incluindo URLs e informações detalhadas.

{Cores.VERDE}📊 FUNCIONALIDADES:{Cores.RESET}
   • 🔗 Coleta automática de URLs de produtos
   • 📊 Extração de dados nutricionais completos
   • 📈 Geração de relatórios em CSV
   • 🎯 Interface interativa e intuitiva

{Cores.VERDE}🛠️  TECNOLOGIAS:{Cores.RESET}
   • Python 3.8+
   • Requests (requisições HTTP)
   • BeautifulSoup4 (parsing HTML)
   • Pandas (manipulação de dados)
   • LXML (parser XML/HTML)

{Cores.VERDE}📂 ARQUIVOS GERADOS:{Cores.RESET}
   • JSON: dados/urls_produtos.json
   • CSV: dados/produtos_sadia.csv
   • Formato: UTF-8 com BOM

{Cores.VERDE}⚡ CARACTERÍSTICAS:{Cores.RESET}
   • Interface CLI colorida e profissional
   • Tratamento de erros robusto
   • Filtros inteligentes de URLs
   • Formatação correta de valores numéricos
   • Suporte a múltiplas categorias

{Cores.VERDE}📝 DESENVOLVIDO POR:{Cores.RESET}
   • Sistema de Web Scraping
   • Versão: 1.0
   • Data: {datetime.now().strftime('%B %Y')}

{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}
"""
    print(sobre)

def pausar():
    """Pausa o programa aguardando input do usuário"""
    input(f"\n{Cores.CIANO}⏯️  Pressione Enter para continuar...{Cores.RESET}")

# ============================================================================
# 🚀 FUNÇÃO PRINCIPAL
# ============================================================================
def main():
    """Função principal do programa"""
    try:
        while True:
            limpar_terminal()
            mostrar_banner()
            mostrar_menu()
            
            escolha = obter_escolha()
            
            if escolha == "1":
                executar_coleta_urls()
                pausar()
                
            elif escolha == "2":
                executar_extracao_dados()
                pausar()
                
            elif escolha == "3":
                executar_coleta_completa()
                pausar()
                
            elif escolha == "4":
                listar_arquivos_gerados()
                pausar()
                
            elif escolha == "5":
                limpar_dados_antigos()
                pausar()
                
            elif escolha == "6":
                mostrar_estatisticas()
                pausar()
                
            elif escolha == "7":
                verificar_ambiente()
                pausar()
                
            elif escolha == "8":
                mostrar_sobre()
                pausar()
                
            elif escolha == "9":
                print(f"\n{Cores.VERDE}👋 Obrigado por usar o Scraper Sadia!{Cores.RESET}")
                print(f"{Cores.CIANO}🚀 Até a próxima!{Cores.RESET}\n")
                break
                
            else:
                print(f"\n{Cores.VERMELHO}❌ Opção inválida! Por favor, escolha entre 1-9{Cores.RESET}")
                time.sleep(2)
                
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}👋 Programa encerrado pelo usuário. Até logo!{Cores.RESET}\n")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro inesperado: {e}{Cores.RESET}")

if __name__ == "__main__":
    main() 