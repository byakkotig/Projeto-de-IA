# 📋 Projeto de Análise e Classificação de Bulas de Medicamentos
**Grupo: Rafael de Souza Oliveira Cerqueira Tinôco, 10401436**

## 📌 Visão Geral

Este projeto utiliza processamento de linguagem natural (NLP) para analisar bulas de medicamentos em PDF, identificar efeitos adversos e classificá-los como **leves** ou **graves** usando o modelo BERT em português. A aplicação oferece uma interface web intuitiva via Streamlit para upload e análise dos arquivos.

## ✨ Funcionalidades Principais

- **Extrai texto** de bulas médicas em PDF (incluindo PDFs protegidos)
- **Identifica e classifica** efeitos adversos (leves/graves)
- **Organiza resultados** por seções da bula (Reações Adversas, Efeitos Colaterais, etc.)
- **Gera relatórios** com estatísticas e visualizações
- **Interface intuitiva** com filtros e opção de download

## 🛠️ Tecnologias Utilizadas

- **Python** (versão 3.8+ recomendada)
- **Streamlit** (interface web)
- **PyPDF2** (leitura de PDFs)
- **Transformers** (BERTimbau - BERT em português)
- **PyTorch** (framework de deep learning)
- **Pandas** (processamento de dados)

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- Pip instalado

## 📊 Métricas de Classificação

O modelo utiliza uma combinação de:
- **BERTimbau** (modelo de linguagem)
- **Regras baseadas** em terminologia médica
- **Dicionários especializados** com:
  - 150+ termos de sintomas
  - 15 sistemas do corpo humano
  - Sinônimos e variações linguísticas
 
## Vídeo
https://youtu.be/qdqzMuR_OmA
