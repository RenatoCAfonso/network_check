import streamlit as st
import pandas as pd

# Função para realizar o de-para e gerar o output
def realizar_de_para(malha_antiga, malha_atual):
    try:
        # Carregar os DataFrames
        df_antigo = pd.read_excel(malha_antiga, dtype=str)
        df_atual = pd.read_excel(malha_atual, dtype=str)

        # Adicionar uma coluna 'Malha' para indicar a origem da diferença
        df_antigo['_Malha'] = 'Antiga'
        df_atual['_Malha'] = 'Atual'

        # Checar se as informações agrupadas são iguais
        grupo_antigo = df_antigo.groupby(['ORIGEM', 'DESTINO_FINAL', 'PROXIMO_STEP']).size().reset_index(name='count_antigo')
        grupo_atual = df_atual.groupby(['ORIGEM', 'DESTINO_FINAL', 'PROXIMO_STEP']).size().reset_index(name='count_atual')

        # Realizar o merge para encontrar diferenças
        diff = pd.merge(grupo_antigo, grupo_atual, on=['ORIGEM', 'DESTINO_FINAL', 'PROXIMO_STEP'], how='outer', indicator=True)

        # Adicionar a coluna 'Malha' ao DataFrame resultante
        diff['_Malha'] = diff['_merge'].map({'left_only': 'Antiga', 'right_only': 'Atual', 'both': 'Ambas'})
        
        diff_filtrado = diff.query('_Malha != "Ambas"')

        return diff_filtrado[['ORIGEM', 'DESTINO_FINAL', 'PROXIMO_STEP', '_Malha']]

    except Exception as e:
        return f"Não foi possível checar as informações - verifique o formato do arquivo.\nErro: {str(e)}"


# Interface do aplicativo
st.title("Aplicativo De-Para de Malhas")

# Upload dos arquivos
malha_antiga = st.file_uploader("Carregar Malha Antiga (Excel com colunas ORIGEM, DESTINO_FINAL e PROXIMO_STEP - em caixa alta)", type=["xlsx", "xls"])
malha_atual = st.file_uploader("Carregar Malha Atual (Excel com colunas ORIGEM, DESTINO_FINAL e PROXIMO_STEP - em caixa alta)", type=["xlsx", "xls"])

# Botão para realizar o de-para
if st.button("Realizar De-Para"):
    # Verificar se os dois arquivos foram carregados
    if malha_antiga is not None and malha_atual is not None:
        # Executar a função de-para
        resultado_de_para = realizar_de_para(malha_antiga, malha_atual)

        # Mostrar o resultado na interface
        st.write("Resultado do De-Para:")
        st.write(resultado_de_para)

    else:
        st.warning("Por favor, carregue os arquivos para realizar o De-Para.")



