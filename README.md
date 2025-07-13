# 🍗 Scraper Sadia

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/sidnei-almeida/scraper_sadia/)

> **Sistema completo para coleta e extração de dados nutricionais dos produtos Sadia**

Um scraper inteligente em Python que automatiza a coleta de informações nutricionais dos produtos da Sadia, organizando os dados de forma estruturada para análises, catálogos ou integrações com sistemas externos.

## ✨ Características

- 🔗 **Coleta Automática de URLs**: Navega pelas categorias do site da Sadia
- 📊 **Extração de Dados Nutricionais**: Captura tabelas nutricionais completas
- 🎯 **Interface Interativa**: Menu CLI com cores e barras de progresso
- 📈 **Relatórios e Estatísticas**: Análise detalhada dos dados coletados
- 🛡️ **Tratamento de Erros**: Sistema robusto com tratamento de exceções
- 📁 **Organização Estruturada**: Dados salvos em formatos JSON e CSV

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/sidnei-almeida/scraper_sadia.git
   cd scraper_sadia
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Como Usar

### Interface Principal

Execute o programa principal:

```bash
python main.py
```

O sistema apresenta um menu interativo com as seguintes opções:

```
═══════════════════ MENU PRINCIPAL ═══════════════════

🚀 OPERAÇÕES PRINCIPAIS:
  1. 🔗 Coletar URLs - Extrai URLs de produtos das categorias
  2. 📊 Extrair Dados - Coleta dados nutricionais dos produtos
  3. 🎯 Coleta Completa - URLs + Dados (automático)

📁 GERENCIAR DADOS:
  4. 📋 Ver Arquivos - Lista arquivos gerados
  5. 🗑️  Limpar Dados - Remove arquivos antigos
  6. 📈 Estatísticas - Mostra resumo dos dados

⚙️  CONFIGURAÇÕES:
  7. 🔧 Verificar Ambiente - Testa dependências
  8. 📖 Sobre o Programa - Informações e estatísticas
  9. ❌ Sair - Encerrar programa
```

### Fluxo de Trabalho

1. **Coletar URLs** (Opção 1)
   - Navega pelas categorias do site da Sadia
   - Coleta URLs dos produtos usando seletor específico
   - Salva em `dados/urls_produtos.json`

2. **Extrair Dados** (Opção 2)
   - Lê as URLs coletadas
   - Extrai dados nutricionais de cada produto
   - Salva em `dados/produtos_sadia.csv`

3. **Coleta Completa** (Opção 3)
   - Executa automaticamente as duas etapas
   - Ideal para uso inicial

### Uso Direto dos Scripts

#### Coletor de URLs
```bash
python config/url_collector.py
```

#### Scraper de Dados
```bash
python config/scraper.py
```

## 📁 Estrutura do Projeto

```
scraper_sadia/
├── 📁 config/                 # Scripts principais
│   ├── url_collector.py      # Coletor de URLs
│   └── scraper.py            # Extrator de dados
├── 📁 dados/                 # Arquivos gerados
│   ├── urls_produtos.json    # URLs coletadas
│   └── produtos_sadia.csv    # Dados nutricionais
├── 📁 html/                  # Arquivos HTML de teste
├── 📁 venv/                  # Ambiente virtual
├── main.py                   # Interface principal
├── requirements.txt          # Dependências
├── template_main.py          # Template do menu
└── README.md                # Este arquivo
```

## 📊 Dados Coletados

O sistema extrai as seguintes informações dos produtos:

- **Nome do Produto**: Título completo do produto
- **Categoria**: Categoria do produto (ex: Frangos, Embutidos)
- **Tabela Nutricional**: Valores por 100g/100ml
  - Valor energético (kcal)
  - Carboidratos (g)
  - Proteínas (g)
  - Gorduras totais (g)
  - Gorduras saturadas (g)
  - Gorduras trans (g)
  - Fibra alimentar (g)
  - Sódio (mg)

### Formato de Saída

#### JSON (URLs)
```json
{
  "categoria": "Frangos",
  "urls": [
    "https://sadia.com.br/produto/1",
    "https://sadia.com.br/produto/2"
  ]
}
```

#### CSV (Dados Nutricionais)
```csv
nome,categoria,valor_energetico,carboidratos,proteinas,gorduras_totais,gorduras_saturadas,gorduras_trans,fibra,sodio
Peito de Frango,Frangos,165,0,31,3.5,1.2,0,0,70
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Requests**: Requisições HTTP
- **BeautifulSoup4**: Parsing HTML
- **Pandas**: Manipulação de dados
- **LXML**: Parser XML/HTML
- **Urllib3**: Cliente HTTP

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do Scraper
DELAY_REQUESTS=1.0
MAX_RETRIES=3
TIMEOUT=30

# Configurações de Saída
OUTPUT_DIR=dados
CSV_FILENAME=produtos_sadia.csv
JSON_FILENAME=urls_produtos.json
```

### Personalização

Você pode modificar os seguintes parâmetros:

- **Delay entre requisições**: Evita sobrecarga do servidor
- **Seletores CSS**: Para adaptar a mudanças no site
- **Categorias**: Adicionar/remover categorias de produtos
- **Campos extraídos**: Modificar dados nutricionais coletados

## 📈 Estatísticas e Relatórios

O sistema oferece funcionalidades de análise:

- **Contagem de produtos por categoria**
- **Estatísticas nutricionais**
- **Verificação de dados completos**
- **Relatórios de qualidade**

## 🐛 Solução de Problemas

### Erros Comuns

1. **Erro de conexão**
   ```
   Solução: Verifique sua conexão com a internet
   ```

2. **Arquivo de URLs não encontrado**
   ```
   Solução: Execute primeiro a coleta de URLs
   ```

3. **Dependências não instaladas**
   ```bash
   pip install -r requirements.txt
   ```

### Logs e Debug

O sistema gera logs detalhados para facilitar o debug:

- **Progresso em tempo real**
- **Contadores de sucesso/erro**
- **Mensagens de status**

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Sidnei Almeida**

- GitHub: [@sidnei-almeida](https://github.com/sidnei-almeida)
- Projeto: [scraper_sadia](https://github.com/sidnei-almeida/scraper_sadia/)

## 🙏 Agradecimentos

- **Sadia**: Pela disponibilização dos dados nutricionais
- **Comunidade Python**: Pelas bibliotecas utilizadas
- **Contribuidores**: Por sugestões e melhorias

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões:

1. Abra uma [Issue](https://github.com/sidnei-almeida/scraper_sadia/issues)
2. Descreva o problema detalhadamente
3. Inclua logs e screenshots se necessário

---

⭐ **Se este projeto foi útil, considere dar uma estrela no repositório!**
