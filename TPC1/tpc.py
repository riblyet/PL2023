def ler_arquivo(arquivo):

    with open(arquivo) as f:

        # Ignora o cabeçalho do arquivo
        next(f)

        # Cria uma lista com os dados do arquivo
        dados = []
        
        for linha in f:
            # Separa os campos da linha pelo caractere ","
            campos = linha.strip().split(",")
            # Converte os dados do arquivo para os tipos corretos
            idade = int(campos[0])
            sexo = campos[1]
            tensao = int(campos[2])
            colesterol = int(campos[3])
            batimento = int(campos[4])
            tem_doenca = bool(int(campos[5]))
            # Adiciona os dados em um dicionário
            registo = {'idade': idade, 'sexo': sexo, 'tensao': tensao, 'colesterol': colesterol, 'batimento': batimento, 'temDoença': tem_doenca}
            dados.append(registo)
    # Retorna a lista com os dados do arquivo
    return dados



def distribuicao_doenca_por_sexo(modelo):
    # Conta o número total de registros de cada sexo
    contagem_por_sexo = {'M': 0, 'F': 0}
    # Conta o número de registros de cada sexo que têm a doença
    contagem_com_doenca_por_sexo = {'M': 0, 'F': 0}

    for registo in modelo:
        sexo = registo['sexo']
        tem_doenca = registo['temDoença']
        contagem_por_sexo[sexo] += 1
        if tem_doenca:
            contagem_com_doenca_por_sexo[sexo] += 1

    proporcao_doenca_por_sexo = {
        'X': contagem_com_doenca_por_sexo['M'],
        'M': contagem_por_sexo['M'],
        'Y': contagem_com_doenca_por_sexo['F'],
        'F': contagem_por_sexo['F']
    }

    return proporcao_doenca_por_sexo



def distribuicao_doenca_por_idade(dados):
    # criar um dicionário vazio para armazenar as contagens
    contagens = {}
    
    # iterar sobre os dados
    for d in dados:
        # arredondar a idade para baixo para o múltiplo de 5 mais próximo
        idade_grupo = (d['idade'] // 5) * 5
        
        # obter a contagem atual para este grupo etário
        contagem_atual = contagens.get(idade_grupo, {'total': 0, 'doentes': 0})
        
        # incrementar o total e o número de doentes para este grupo etário
        contagem_atual['total'] += 1
        contagem_atual['doentes'] += d['temDoença']
        
        # atualizar o dicionário de contagens
        contagens[idade_grupo] = contagem_atual
    
    # ordena a lista por ordem crescente de idades
    contagens_ordenadas = dict(sorted(contagens.items()))

    # retornar o dicionário de contagens
    return contagens_ordenadas



def distribuicao_doenca_por_colesterol(dados):
    # encontrar o menor e o maior valor de colesterol nos dados
    menor_colesterol = float('inf')
    maior_colesterol = float('-inf')
    
    for d in dados:
        if d['colesterol'] < menor_colesterol:
            menor_colesterol = d['colesterol']
        if d['colesterol'] > maior_colesterol:
            maior_colesterol = d['colesterol']
    
    # criar os níveis de colesterol a partir do menor e do maior valor
    limites_inferiores = list(range(menor_colesterol // 10 * 10, maior_colesterol // 10 * 10 + 1, 10))
    limites_superiores = list(range(menor_colesterol // 10 * 10 + 10, maior_colesterol // 10 * 10 + 11, 10))
    
    # criar um dicionário vazio para armazenar as contagens
    contagens = {}
    
    # iterar sobre os dados
    for d in dados:

        # ignorar os dados com colesterol igual a zero
        if d['colesterol'] == 0:
            continue

        # encontrar o nível de colesterol correspondente ao dado
        nivel_colesterol = None
        for i in range(len(limites_inferiores)):
            if limites_inferiores[i] <= d['colesterol'] < limites_superiores[i]:
                nivel_colesterol = f'{limites_inferiores[i]}-{limites_superiores[i]-1}'
                break
        
        # se o nível de colesterol não foi encontrado, ignorar o dado
        if nivel_colesterol is None:
            continue
        
        # obter a contagem atual para este nível de colesterol
        contagem_atual = contagens.get(nivel_colesterol, {'total': 0, 'doentes': 0})
        
        # incrementar o total e o número de doentes para este nível de colesterol
        contagem_atual['total'] += 1
        contagem_atual['doentes'] += d['temDoença']
        
        # atualizar o dicionário de contagens
        contagens[nivel_colesterol] = contagem_atual
    
    # retornar o dicionário de contagens ordenado por níveis de colesterol
    contagens_ordenadas = dict(sorted(contagens.items() , key=lambda x: int(x[0].split('-')[0])))
    return contagens_ordenadas
  


def tabela_distribuicao(distribuicao, tipo_distribuicao):
    print('-' * 35)
    if tipo_distribuicao == "idade":
    # imprimir cabeçalho da tabela
        print('|{:^10} | {:^8} | {:^8} |'.format('Intervalo', 'Total', 'Doentes'))

    # iterar sobre os níveis da idade da distribuição
        for especificacao, contagem in distribuicao.items():
        # obter o total e o número de doentes para este nível de idade
            total = contagem['total']
            doentes = contagem['doentes']

        # imprimir a linha correspondente na tabela
            print('-' * 35)
            print('|{:5}-{:<4} | {:^8} | {:^8} |'.format(especificacao,especificacao+4, total, doentes))
    elif tipo_distribuicao == "colesterol":
    # imprimir cabeçalho da tabela
        print('|{:^10} | {:^8} | {:^8} |'.format('Intervalo', 'Total', 'Doentes'))
    
    # iterar sobre os níveis de colesterol da distribuição
        for especificacao, contagem in distribuicao.items():
        # obter o total e o número de doentes para este nível de colesterol
            total = contagem['total']
            doentes = contagem['doentes']
        
        # imprimir a linha correspondente na tabela
            print('-' * 35)
            print('|{:^10} | {:^8} | {:^8} |'.format(especificacao, total, doentes))

    elif tipo_distribuicao == "sexo":
    # imprimir cabeçalho da tabela
        print('|{:^10} | {:^8} | {:^8} |'.format('Sexo', 'Total', 'Doentes'))
        print('-' * 35)
        print("|{:^10} | {:^8} | {:^8} |".format('M', distribuicao['M'], distribuicao['X']))
        print('-' * 35)
        print("|{:^10} | {:^8} | {:^8} |".format('F', distribuicao['F'], distribuicao['Y']))
    
    print('-' * 35)
    print('\n') 



def main():

    arquivo = "myheart.csv"
    modelo = ler_arquivo(arquivo) 
    
    # Calcula a distribuição da doença por sexo
    distribuicao_Sexo = distribuicao_doenca_por_sexo(modelo)

    # Calcula a distribuição da doença por faixa etaria
    contagens_por_grupo_etario = distribuicao_doenca_por_idade(modelo)

    # Calcula a distribuição da doença por faixa de colesterol
    contagens_por_colesterol = distribuicao_doenca_por_colesterol(modelo)

    #imprime a distribuição da doença por sexo
    print("\n")
    
    tabela_distribuicao(contagens_por_colesterol, "colesterol")
    tabela_distribuicao(contagens_por_grupo_etario, "idade")
    tabela_distribuicao(distribuicao_Sexo, "sexo")


if __name__ == '__main__':
    main()
