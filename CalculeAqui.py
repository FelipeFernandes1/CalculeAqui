import streamlit as st

# Título do App
st.markdown("<span style='color: green; font-style: italic; font-size: 50px; font-weight: bold;'>Calcule Aqui</span>", unsafe_allow_html=True)

# Barra Lateral para Input de Dados
with st.sidebar:
    st.header("Parâmetros de Entrada")
    reclamacoes = st.number_input(label='Total de reclamações', format='%d', step=1, min_value=0, value=0)
    respondidas = st.number_input(label='Total de respostas', format='%d', step=1, min_value=0, help='Corresponde ao número de casos finalizados, ou seja, respondidos publicamente.')
    MA = st.number_input(label='Média das notas', format="%.2f", min_value=0.0, max_value=10.00, step=0.01)
    IS = st.number_input(label='Índice de solução', format="%.1f", min_value=0.0, max_value=100.0, step=0.1)
    IN = st.number_input(label='Índice de novos negócios', format="%.1f", min_value=0.0, max_value=100.0, step=0.1)
    avaliacoes = st.number_input(label='Total de avaliações', format='%d', step=1, min_value=0)
    botao1 = st.button(label='Calcular')

# Processamento após o clique no botão
if botao1:
    if reclamacoes == 0:
        st.error("O 'Total de reclamações' deve ser maior que zero para realizar o cálculo.")
    else:
        # CÁLCULO DO ÍNDICE DE RESPOSTA (IR)
        IR = (respondidas / reclamacoes) * 100

        # FÓRMULA PRINCIPAL (AR)
        AR = ((IR * 2) + (MA * 10 * 3) + (IS * 3) + (IN * 2)) / 100
        AR = round(AR, 1)

        # DEFINIÇÃO DA REPUTAÇÃO INICIAL
        if IR >= 90 and MA >= 7 and IS >= 90 and IN >= 70 and avaliacoes >= 50:
            reputacao = 'RA1000'
        elif avaliacoes < 10 and IR > 50:
            reputacao = 'SEM ÍNDICE'
        elif AR < 5 or IR <= 50:
            reputacao = 'NÃO RECOMENDADA'
        elif avaliacoes < 10:
            reputacao = 'SEM ÍNDICE'
        elif AR <= 5.9:
            reputacao = 'RUIM'
        elif AR <= 6.9:
            reputacao = 'REGULAR'
        elif AR <= 7.9:
            reputacao = 'BOM'
        else:
            reputacao = 'ÓTIMO'

        # Variável para armazenar o texto final
        texto_resultado = ""

        # LÓGICA DE PREVISÃO (Simulações)
        if reputacao == 'RA1000':
            novas_avaliacoes_negativas = 0
            nova_reputacao = 'RA1000'
            while nova_reputacao == 'RA1000':
                novas_avaliacoes_negativas += 1
                total_av = avaliacoes + novas_avaliacoes_negativas
                MA2 = ((MA * avaliacoes) + (0)) / total_av # Simulando nota 0 nas novas
                IS2 = ((IS / 100 * avaliacoes) + 0) / total_av * 100
                IN2 = ((IN / 100 * avaliacoes) + 0) / total_av * 100
                if IR < 90 or MA2 < 7 or IS2 < 90 or IN2 < 70 or total_av < 50:
                    nova_reputacao = 'ÓTIMO'
            texto_resultado = f"Sua reputação é {reputacao} e o AR é {AR}. Contudo, se você receber mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo ÓTIMO."

        elif reputacao == 'SEM ÍNDICE':
            precisa = 10 - avaliacoes
            texto_resultado = f"Seu status é {reputacao}. Para obter uma reputação calculada, você precisa de mais {precisa} avaliações."

        elif reputacao == 'NÃO RECOMENDADA' and IR <= 50:
            respostas_necessarias = int((reclamacoes * 0.51) - respondidas)
            if respostas_necessarias < 0: respostas_necessarias = 1
            texto_resultado = f"Sua reputação é {reputacao} porque seu Índice de Resposta ({IR:.1f}%) está abaixo de 50%. Você precisa de pelo menos mais {max(1, respostas_necessarias)} respostas para normalizar."

        else:
            # Texto padrão para as demais categorias (RUIM, REGULAR, BOM, ÓTIMO)
            texto_resultado = f"Sua reputação atual é {reputacao} com AR de {AR}."

        # Exibição do Resultado
        st.markdown(f"### {texto_resultado}")

# Rodapé
st.markdown("---")
st.markdown("""
<style>
.footer {text-align: center; color: gray; font-size: 12px;}
</style>
<p class='footer'>Desenvolvido por Felipe Fernandes</p>
""", unsafe_allow_html=True)
