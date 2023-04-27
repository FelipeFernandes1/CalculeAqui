import streamlit as st
import sys
from bs4 import BeautifulSoup as bs  # serve para fazer a reaspagem em si
import re  #serve para extrair o número float da string(expressão regular)
#Fazendo slicing para tirar todos indicadores que estão no script(gambiarra)
#Cada aba será um elemento da lista, totalizando 5
import cfscrape  #É uma alternativa à biblioteca Request


st.title(':green[*Calcule Aqui*]', help='Essa ferramenta tem como objetivo realizar uma análise preditiva sobre a reputação da empresa na plataforma Reclame Aqui.')

botaotipoanalise = st.selectbox('##### Para começarmos, escolha uma opção abaixo: ', options=('Abas do site Reclame Aqui', 'Período específico'), help='''A opção "abas do site" é indicada quando o objetivo é analisar a reputação da empresa no site do RA. 

A opção "período específico" é indicada para analisar períodos que não estão disponíveis no site. Os dados a serem inseridos podem ser obtidos em ferramentas como o Hugme.

Após escolher, preencha o questionário na parte esquerda da tela e clique em "Calcular".''')

st.divider()

try:
    if botaotipoanalise == 'Abas do site Reclame Aqui':
        with st.sidebar:
            empresa = st.text_input(label='#### Informe o nome da empresa', placeholder='olx', help='Pode ser que o nome exibido no site do RA seja divergente do nome que consta na URL, o nome a ser inserido precisa ser idêntico ao da URL. Não insira caracteres especiais, somente espaços quando houver.')
            if empresa == '':  # só para não deixar a variável em branco, pois estava exibindo erro
                empresa = 'olx'
            abaescolhida = st.selectbox(label='#### Escolha o período', options=('6 meses', '12 meses', 'Último ano', 'Penúltimo ano', 'Geral'))
            botao1 = st.button(label='Calcular')
        if abaescolhida == '6 meses':
            abaescolhida = 0
        elif abaescolhida == '12 meses':
            abaescolhida = 1
        elif abaescolhida == 'Último ano':
            abaescolhida = 2
        elif abaescolhida == 'Penúltimo ano':
            abaescolhida = 3
        elif abaescolhida == 'Geral':
            abaescolhida = 4

        #Validando o dado do imput usuário
        empresa = empresa.strip().lower()
        empresa = empresa.replace('     ', '-')
        empresa = empresa.replace('    ', '-')
        empresa = empresa.replace('   ', '-')
        empresa = empresa.replace('  ', '-')
        empresa = empresa.replace(' ', '-')

        #Obtendo o código HTML da página
        scraper = cfscrape.create_scraper()  # Obtendo o HTML da página
        response = scraper.get(f'https://www.reclameaqui.com.br/empresa/{empresa}/')
        content = response.content
        site = bs(content, 'html.parser')

        #Realizando o primeiro filtro
        indicadores = site.find('script', attrs={'id': '__NEXT_DATA__'})
        indicadores = str(indicadores)
        a = indicadores.find('panels')
        indicadores = indicadores[a:]
        indicadores = indicadores.split(']')
        indicadores = indicadores[0]
        indicadores.find('[')
        indicadores = indicadores[9:]
        indicadores = indicadores.split('},{')

        abaescolhida = indicadores[abaescolhida]

        # Extraindo os indocadores de acordo com a aba escolhida
        abaescolhida = str(abaescolhida).split(',')

        if 'finalScore' in abaescolhida[3]:  # só para conferir se o indicador não mudou de posição na lista
            AR = abaescolhida[3]
            if bool(re.search('\d', AR)):  # Verificando se possui número
                AR = re.search('\d+\.\d+', AR).group()  # extraindo o número com expressão regular
                AR = float(AR)
            else:
                AR = 0

        if 'totalComplains' in abaescolhida[5]:
            reclamacoes = abaescolhida[5]
            if bool(re.search('\d', reclamacoes)):
                reclamacoes = re.search('\d+', reclamacoes).group()
                reclamacoes = int(reclamacoes)
            else:
                reclamacoes = 0

        if 'totalAnswered' in abaescolhida[12]:
            respondidas = abaescolhida[12]
            if bool(re.search('\d', respondidas)):
                respondidas = re.search('\d+', respondidas).group()
                respondidas = int(respondidas)
            else:
                respondidas = 0

        if 'consumerScore' in abaescolhida[6]:
            MA = abaescolhida[6]
            if bool(re.search('\d', MA)):
                MA = re.search('\d+\.\d+', MA).group()
                MA = float(MA)
            else:
                MA = 0

        if 'solvedPercentual' in abaescolhida[10]:
            IS = abaescolhida[10]
            if bool(re.search('\d', IS)):
                IS = re.search('\d+\.\d+', IS).group()
                IS = float(IS)
            else:
                IS = 0

        if 'dealAgainPercentual' in abaescolhida[16]:
            IN = abaescolhida[16]
            if bool(re.search('\d', IN)):
                IN = re.search('\d+\.\d+', IN).group()
                IN = float(IN)
            else:
                IN = 0

        if 'totalEvaluated' in abaescolhida[17]:
            avaliacoes = abaescolhida[17]
            if bool(re.search('\d', avaliacoes)):
                avaliacoes = re.search('\d+', avaliacoes).group()
                avaliacoes = int(avaliacoes)
            else:
                avaliacoes = 0

    else:
        with st.sidebar:
            reclamacoes = st.number_input(label='#### Total de reclamações', format='%d', step=1, min_value=0)
            respondidas = st.number_input(label='#### Total de respostas', format='%d', step=1, min_value=0)
            MA = st.number_input(label='#### Média das notas', format="%.2f", min_value=0.0, max_value=10.00, step=0.01)
            IS = st.number_input(label='#### Índice de solução', format="%.1f", min_value=0.0, max_value=100.0, step=0.1)
            IN = st.number_input(label='#### Índice de novos negócios', format="%.1f", min_value=0.0, max_value=100.0, step=0.1)
            avaliacoes = st.number_input(label='#### Total de avaliações', format='%d', step=1, min_value=0)
            botao1 = st.button(label='#### Calcular')

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
            reputacao = ':green[**RA1000**]'
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

        if reputacao == ':green[**RA1000**]':
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
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Contudo, se você tomar mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo ÓTIMO.'''

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
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Para atingir a reputação REGULAR você precisa de mais {v1} avaliações positivas e mais {v2} novas respostas públicas. Por outro lado se você tomar mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo NÃO RECOMENDADA.'''

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
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Para atingir a reputação BOM você precisa de mais {v1} avaliações positivas e mais {v2} novas respostas públicas. Por outro lado se você tomar mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo RUIM.'''

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
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Para atingir a reputação ÓTIMO você precisa de mais {v1} avaliações positivas e mais {v2} novas respostas públicas. Por outro lado se você tomar mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo REGULAR.'''

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
                    nova_reputacao = ':green[**RA1000**]'
            while nova_reputacao != ':green[**RA1000**]':
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
                    nova_reputacao = ':green[**RA1000**]'
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
            resultado = f'''Sua reputação é {reputacao} e o AR é {AR}. Para atingir a reputação :green[**RA1000**] você precisa de mais {v1} avaliações positivas e mais {v2} novas respostas públicas. Por outro lado se você tomar mais {novas_avaliacoes_negativas} avaliações negativas, descerá para o selo BOM.'''
    st.markdown(f'''##### {resultado}''', help='O algoritimo considera como "avaliação positiva" aquela que obtém nota máxima nas três perguntas que compõem a avaliação. A "avaliação negativa" é proporcionalmente oposta, ou seja aquela que obtém nota mínima nas três perguntas que compõem a avaliação.')  #Printa o resultado no app
except:
    st.write(':red[Erro! Por favor, verifique os dados inseridos ou entre em contato com o suporte.]')


