import streamlit as st
import re  #serve para extrair o número float da string(expressão regular)


st.markdown("<span style='color: green; font-style: italic; font-size: 50px; font-weight: bold;'>Calcule Aqui</span>", unsafe_allow_html=True)

try:    
    with st.sidebar:
            reclamacoes = st.number_input(label='Total de reclamações', format='%d', step=1, min_value=0)
            respondidas = st.number_input(label='Total de respostas', format='%d', step=1, min_value=0, help='Corresponde ao número de casos finalizados, ou seja, respondidos publicamente.')
            MA = st.number_input(label='Média das notas', format="%.2f", min_value=0.0, max_value=10.00, step=0.01)
            IS = st.number_input(label='Índice de solução', format="%.1f", min_value=0.0, max_value=100.0, step=0.1)
            IN = st.number_input(label='Índice de novos negócios', format="%.1f", min_value=0.0, max_value=100.0, step=0.1)
            avaliacoes = st.number_input(label='Total de avaliações', format='%d', step=1, min_value=0)
            botao1 = st.button(label='Calcular')

    resultado = ''

    if botao1:
        # CÁLCULANDO O ÍNDICE DE RESPOSTA
        IR = (respondidas / reclamacoes) * 100

        # FÓRMULA PRINCIPAL
        AR = ((IR * 2) + (MA * 10 * 3) + (IS * 3) + (IN * 2)) / 100
        AR = round(AR, 1)

        # CLASSIFICAÇÃO
        reputacao = ' '

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

        # PREVISÕES PARA TODAS CLASSIFICAÇÕES

        if reputacao == 'RA1000':
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            while nova_reputacao != 'ÓTIMO':
                novas_avaliacoes_negativas = novas_avaliacoes_negativas + 1
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3)
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3)
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                # Criei novas variáveis para que os critérios do RA100 sejam reavaliados a cada lopping
                MA2 = (MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                        avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA)))
                IS2 = (IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                        avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100
                IN2 = (IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                        avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100
                avaliacoes2 = novas_avaliacoes_negativas + avaliacoes
                if IR2 < 90 or MA2 < 7 or IS2 < 90 or IN2 < 70 or avaliacoes2 < 50:
                    nova_reputacao = 'ÓTIMO'
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Contudo, se você obter mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo ÓTIMO.'''

        elif reputacao == 'NÃO RECOMENDADA' and IR <= 50 and avaliacoes < 10:
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            while avaliacoes + novas_avaliacoes_positivas < 10:
                novas_avaliacoes_positivas = novas_avaliacoes_positivas + 1  # variável de controle
                IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
            while IR2 <= 50:
                novas_respostas_publicas = novas_respostas_publicas + 1  # variável de controle
                IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
            resultado = f'''Sua reputação é {reputacao} e você não possuí cálculo de AR. Essa classificação ocorre pois além do seu índice de resposta estar inferior ou igual a 50%, você também possui menos de 10 avaliações, o que impossibilita o cálculo da AR. Para regularizar sua classificação você precisa de mais {novas_respostas_publicas} novas respostas públicas e mais {novas_avaliacoes_positivas} novas avaliações. Seu cálculo resultará em AR {AR2} e a reputação será atualizada.'''

        elif reputacao == 'SEM ÍNDICE':
            novas_avaliacoes_positivas = 0
            while avaliacoes + novas_avaliacoes_positivas < 10:
                novas_avaliacoes_positivas = novas_avaliacoes_positivas + 1
            resultado = f'''Seu status é {reputacao}. Essa classificação ocorre pois para o cálculo é necessário no mínimo 10 avaliações. Para obter reputação é necessário mais {novas_avaliacoes_positivas} avaliações.'''

        elif reputacao == 'NÃO RECOMENDADA' and AR < 5:
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            while IR2 < 51:  # regra de no mínimo metade das reclamções respondidas
                novas_respostas_publicas = novas_respostas_publicas + 1  # variável de controle
                IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
            if AR2 >= 5:
                nova_reputacao = 'RUIM'
            if IR2 >= 51 and AR2 < 5:
                while IR2 < 90:
                    novas_respostas_publicas = novas_respostas_publicas + 1  # variável de controle
                    IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
                    AR2 = ((IR2 * 2) \
                           + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                           + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                           + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                    AR2 = round(AR2, 1)
                    if AR2 >= 5:
                        nova_reputacao = 'RUIM'
                        break
                while nova_reputacao != 'RUIM':
                    novas_avaliacoes_positivas = novas_avaliacoes_positivas + 1  # variável de controle
                    AR2 = ((IR2 * 2) \
                           + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                           + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                           + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                    AR2 = round(AR2, 1)
                    if AR2 >= 5:
                        nova_reputacao = 'RUIM'
            v1 = novas_avaliacoes_positivas
            v2 = novas_respostas_publicas
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Para atingir a reputação RUIM você precisa de mais {v1} avaliações positivas e mais {v2} novas respostas públicas.'''


        elif reputacao == 'NÃO RECOMENDADA':
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            while IR2 < 51:
                novas_respostas_publicas = novas_respostas_publicas + 1  # variável de controle
                IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
            resultado = f'''Sua reputação é {reputacao}, porém o AR é {AR}. Essa classificação ocorre pois você possui o índice de resposta igual ou inferior a 50%. Ao responder mais {novas_respostas_publicas} respostas públicas, sua nova AR será {AR2} e terá a classificação normalizada.'''


        elif reputacao == 'RUIM':
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            while IR2 < 90:
                novas_respostas_publicas = novas_respostas_publicas + 1  # variável de controle
                IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
                if AR2 >= 6:
                    nova_reputacao = 'REGULAR'
                    break
            while nova_reputacao != 'REGULAR':
                novas_avaliacoes_positivas = novas_avaliacoes_positivas + 1  # variável de controle
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
                if AR2 >= 6:
                    nova_reputacao = 'REGULAR'
            v1 = novas_avaliacoes_positivas
            v2 = novas_respostas_publicas
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            if reputacao == 'RUIM':
                while nova_reputacao != 'NÃO RECOMENDADA':
                    novas_avaliacoes_negativas = novas_avaliacoes_negativas + 1
                    AR2 = ((IR2 * 2) \
                           + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3)
                           + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3)
                           + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                    AR2 = round(AR2, 1)
                    if AR2 < 5:
                        nova_reputacao = 'NÃO RECOMENDADA'
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Para atingir a reputação REGULAR você precisa de mais {v1} avaliações positivas e mais {v2} novas respostas públicas. Por outro lado se você obter mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo NÃO RECOMENDADA.'''

        elif reputacao == 'REGULAR':
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            while IR2 < 90:
                novas_respostas_publicas = novas_respostas_publicas + 1  # variável de controle
                IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
                if AR2 >= 7:
                    nova_reputacao = 'BOM'
                    break
            while nova_reputacao != 'BOM':
                novas_avaliacoes_positivas = novas_avaliacoes_positivas + 1  # variável de controle
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
                if AR2 >= 7:
                    nova_reputacao = 'BOM'
            v1 = novas_avaliacoes_positivas
            v2 = novas_respostas_publicas
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            if reputacao == 'REGULAR':
                while nova_reputacao != 'RUIM':
                    novas_avaliacoes_negativas = novas_avaliacoes_negativas + 1
                    AR2 = ((IR2 * 2) \
                           + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3)
                           + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3)
                           + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                    AR2 = round(AR2, 1)
                    if AR2 < 6:
                        nova_reputacao = 'RUIM'
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Para atingir a reputação BOM você precisa de mais {v1} avaliações positivas e mais {v2} novas respostas públicas. Por outro lado se você obter mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo RUIM.'''

        elif reputacao == 'BOM':
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            while IR2 < 90:
                novas_respostas_publicas = novas_respostas_publicas + 1  # variável de controle
                IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
                if AR2 >= 8:
                    nova_reputacao = 'ÓTIMO'
                    break
            while nova_reputacao != 'ÓTIMO':
                novas_avaliacoes_positivas = novas_avaliacoes_positivas + 1  # variável de controle
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                AR2 = round(AR2, 1)
                if AR2 >= 8:
                    nova_reputacao = 'ÓTIMO'
            v1 = novas_avaliacoes_positivas
            v2 = novas_respostas_publicas
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            if reputacao == 'BOM':
                while nova_reputacao != 'REGULAR':
                    novas_avaliacoes_negativas = novas_avaliacoes_negativas + 1
                    AR2 = ((IR2 * 2) \
                           + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3)
                           + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3)
                           + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                    AR2 = round(AR2, 1)
                    if AR2 < 7:
                        nova_reputacao = 'REGULAR'
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Para atingir a reputação ÓTIMO você precisa de mais {v1} avaliações positivas e mais {v2} novas respostas públicas. Por outro lado se você obter mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo REGULAR.'''

        elif reputacao == 'ÓTIMO':
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            while IR2 < 90:
                novas_respostas_publicas = novas_respostas_publicas + 1  # variável de controle
                IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                if novas_avaliacoes_negativas + novas_avaliacoes_positivas + avaliacoes >= 50 \
                        and IR2 >= 90 \
                        and (MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                        avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) >= 7 \
                        and ((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                        avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) >= 90 \
                        and ((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                        avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) >= 70:
                    nova_reputacao = 'RA1000'
            while nova_reputacao != 'RA1000':
                novas_avaliacoes_positivas = novas_avaliacoes_positivas + 1  # variável de controle
                AR2 = ((IR2 * 2) \
                       + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3) \
                       + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3) \
                       + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                if novas_avaliacoes_negativas + novas_avaliacoes_positivas + avaliacoes >= 50 \
                        and IR2 >= 90 \
                        and (MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                        avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) >= 7 \
                        and ((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                        avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) >= 90 \
                        and ((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                        avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) >= 70:
                    nova_reputacao = 'RA1000'
            v1 = novas_avaliacoes_positivas
            v2 = novas_respostas_publicas
            novas_avaliacoes_positivas = 0
            novas_avaliacoes_negativas = 0
            novas_respostas_publicas = 0
            IR2 = ((respondidas + novas_respostas_publicas) / reclamacoes) * 100
            AR2 = 0
            nova_reputacao = ' '
            if reputacao == 'ÓTIMO':
                while nova_reputacao != 'BOM':
                    novas_avaliacoes_negativas = novas_avaliacoes_negativas + 1
                    AR2 = ((IR2 * 2) \
                           + ((MA + ((((MA * avaliacoes) + (novas_avaliacoes_positivas * 10)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - MA))) * 10 * 3)
                           + (((IS + ((((IS / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IS)) * 100) * 3)
                           + (((IN + ((((IN / 100) * avaliacoes) + (novas_avaliacoes_positivas)) / (
                                    avaliacoes + novas_avaliacoes_positivas + novas_avaliacoes_negativas) - IN)) * 100) * 2)) / 100
                    AR2 = round(AR2, 1)
                    if AR2 < 8:
                        nova_reputacao = 'BOM'
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Para atingir a reputação RA1000 você precisa de mais {v1} avaliações positivas e mais {v2} novas respostas públicas. Por outro lado se você obter mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo BOM.'''
    st.markdown(f'''##### {resultado}''')  #Printa o resultado no app
    st.markdown("""
    <p class='footer'>
        Desenvolvido por <a href='https://www.linkedin.com/in/luiz-felipe-fernandes-pires-325659105/' target='_blank'>Felipe Fernandes</a>
    </p>
    """, unsafe_allow_html=True)
except:
    st.write('''Erro! Por favor, verifique os dados inseridos ou entre em contato com o suporte.

contato: fernandes290692@gmail.com''')



