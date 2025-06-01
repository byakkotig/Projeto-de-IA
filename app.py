import os
import streamlit as st
import pandas as pd
from preparacao_dados import extrair_texto, normalizar_termos, separar_secoes, TERMOS_MEDICOS, CATEGORIAS
from modelo import carregar_modelo, classificar_frase

# Configurações
PASTA_EXEMPLOS = 'exemplos'

def processar_bula(texto, tokenizer, model, pdf_path):
    """Processa o texto da bula e classifica os sintomas"""
    if not texto:
        return pd.DataFrame()
    
    secoes_relevantes = separar_secoes(texto)
    resultados = []
    
    for secao, conteudo in secoes_relevantes.items():
        if not conteudo:
            continue
            
        frases = [f.strip() for f in conteudo.split('.') if f.strip()]
        
        for frase in frases:
            frase_lower = frase.lower()
            
            # Verificar se há termos médicos na frase
            termos_encontrados = [
                termo for termo in TERMOS_MEDICOS["sintomas"] 
                if termo in frase_lower
            ]
            
            if termos_encontrados:
                try:
                    # Classificação com BERT
                    classificacao = classificar_frase(frase, tokenizer, model)
                    
                    # Refinamento com palavras-chave
                    if any(palavra in frase_lower for palavra in CATEGORIAS['grave']):
                        classificacao = 'grave'
                    elif any(palavra in frase_lower for palavra in CATEGORIAS['leve']):
                        classificacao = 'leve'
                    
                    # Identificar sistemas afetados
                    sistemas_afetados = [
                        s for s in TERMOS_MEDICOS["sistemas"] 
                        if s in frase_lower
                    ]
                    
                    resultados.append({
                        'Arquivo': os.path.basename(pdf_path),
                        'Seção': secao,
                        'Termos Encontrados': ', '.join(termos_encontrados),
                        'Texto': frase,
                        'Classificação': classificacao,
                        'Sistema Afetado': ', '.join(sistemas_afetados)
                    })
                except Exception:
                    continue
    
    return pd.DataFrame(resultados)

def main():
    """Função principal da aplicação Streamlit"""
    st.set_page_config(page_title="Classificador de Bulas", layout="wide")
    st.title("📋 Classificador Avançado de Bulas de Medicamentos")
    
    # Verificar pasta de exemplos
    if not os.path.exists(PASTA_EXEMPLOS):
        st.error(f"Pasta '{PASTA_EXEMPLOS}' não encontrada!")
        return
    
    # Carregar modelo
    tokenizer, model = carregar_modelo()
    
    # Listar arquivos PDF
    pdf_files = [f for f in os.listdir(PASTA_EXEMPLOS) if f.lower().endswith('.pdf')]
    if not pdf_files:
        st.warning(f"Nenhum arquivo PDF encontrado na pasta '{PASTA_EXEMPLOS}'")
        return
    
    # Interface
    st.sidebar.header("Configurações")
    arquivo_selecionado = st.sidebar.selectbox("Selecione um arquivo PDF", pdf_files)
    
    if arquivo_selecionado:
        pdf_path = os.path.join(PASTA_EXEMPLOS, arquivo_selecionado)
        
        with st.spinner(f'Processando {arquivo_selecionado}...'):
            texto = extrair_texto(pdf_path)
            
            if texto is None:
                st.error(f"Erro ao processar o arquivo: {arquivo_selecionado}")
                st.stop()
                
            df_resultados = processar_bula(texto, tokenizer, model, pdf_path)
        
        # Exibir resultados
        if not df_resultados.empty:
            st.subheader("📊 Estatísticas")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total de Sintomas", len(df_resultados))
            col2.metric("Sintomas Leves", len(df_resultados[df_resultados['Classificação'] == 'leve']))
            col3.metric("Sintomas Graves", len(df_resultados[df_resultados['Classificação'] == 'grave']))
            col4.metric("Sistemas Afetados", df_resultados['Sistema Afetado'].nunique())
            
            st.subheader("🔍 Resultados Detalhados")
            
            # Filtros avançados
            st.sidebar.subheader("Filtros Avançados")
            filtro_classificacao = st.sidebar.multiselect(
                "Classificação",
                options=['leve', 'grave'],
                default=['leve', 'grave']
            )
            
            sistemas_disponiveis = df_resultados['Sistema Afetado'].unique()
            filtro_sistema = st.sidebar.multiselect(
                "Sistema Afetado",
                options=sistemas_disponiveis,
                default=sistemas_disponiveis
            )
            
            secoes_disponiveis = df_resultados['Seção'].unique()
            filtro_secao = st.sidebar.multiselect(
                "Seção da Bula",
                options=secoes_disponiveis,
                default=secoes_disponiveis
            )
            
            df_filtrado = df_resultados[
                (df_resultados['Classificação'].isin(filtro_classificacao)) &
                (df_resultados['Sistema Afetado'].isin(filtro_sistema)) &
                (df_resultados['Seção'].isin(filtro_secao))
            ]
            
            st.dataframe(df_filtrado)
            
            # Visualizações adicionais
            st.subheader("📈 Análise Visual")
            tab1, tab2 = st.tabs(["Distribuição por Classificação", "Sistemas Afetados"])
            
            with tab1:
                st.bar_chart(df_resultados['Classificação'].value_counts())
            
            with tab2:
                st.bar_chart(df_resultados['Sistema Afetado'].value_counts())
            
            # Download
            csv = df_resultados.to_csv(index=False, sep=';').encode('utf-8')
            st.download_button(
                "⬇️ Baixar Resultados (CSV)",
                data=csv,
                file_name=f"resultados_{arquivo_selecionado.replace('.pdf', '.csv')}",
                mime="text/csv"
            )
        else:
            st.warning("Nenhum sintoma relevante encontrado neste arquivo.")
    
    # Rodapé
    st.sidebar.markdown("---")
    st.sidebar.subheader("Sobre")
    st.sidebar.info("""
    **Classificador de Bulas v2.0**\n
    - Analisa termos médicos complexos
    - Classifica por gravidade e sistema
    - Suporte a PDFs protegidos
    """)

if __name__ == "__main__":
    main()