import re
import datetime
from collections import Counter
import json

def frequencia_processos_por_ano_regex(arquivo):
    # Abrir arquivo e ler linhas
    with open(arquivo, 'r') as f:
        lines = f.readlines()

    # Dicionário para armazenar frequências de processos por ano
    freq_por_ano = {}

    # Expressão regular para extrair a data do processo
    data_regex = re.compile(r'\d{4}-\d{2}-\d{2}')

    # Iterar sobre as linhas e analisar as datas dos processos
    for line in lines:
        # Extrair a data do processo usando expressão regular
        match = data_regex.search(line)
        if match:
            data_str = match.group()
            data = datetime.datetime.strptime(data_str, '%Y-%m-%d')
            # Extrair o ano da data
            ano = data.year
            # Adicionar o ano ao dicionário e incrementar a frequência
            if ano in freq_por_ano:
                freq_por_ano[ano] += 1
            else:
                freq_por_ano[ano] = 1

    # Retornar o dicionário de frequências por ano
    return {ano: freq for ano, freq in sorted(freq_por_ano.items())}

def frequencia_nomes_por_seculo(arquivo):
    # Expressão regular para extrair a data de cada processo
    data_regex = re.compile(r'\d{4}-\d{2}-\d{2}')

    # Dicionário para contar a frequência de nomes por século
    nomes_por_seculo = {}

    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            # Extrai a data de cada linha
            data_str = data_regex.search(line)
            if data_str:
                data = int(data_str.group()[:4])

                # Determina o século a que o ano pertence
                seculo = (data - 1) // 100 + 1

                # Extrai o primeiro nome e o último sobrenome de cada nome completo
                campos = line.split('::')
                if len(campos) >= 4:
                    nome_completo = campos[2]
                    campos = line.strip().split("::")
                    nome_completo = campos[2]
                    if " " in nome_completo:
                        primeiro_nome, *_, ultimo_sobrenome = nome_completo.split()
                    else:
                        continue

                    # Conta a frequência de cada nome próprio e apelido por século
                    nomes_por_seculo.setdefault(seculo, {'nomes': Counter(), 'apelidos': Counter()})
                    nomes_por_seculo[seculo]['apelidos'][ultimo_sobrenome] += 1
                    nomes_por_seculo[seculo]['nomes'][primeiro_nome] += 1

    # Retorna os 5 nomes próprios e apelidos mais frequentes por século
    freq_nomes_por_seculo = {}
    for seculo, freq in sorted(nomes_por_seculo.items()):
        freq_nomes_por_seculo[seculo] = {
            'nomes': dict(freq['nomes'].most_common(5)),
            'apelidos': dict(freq['apelidos'].most_common(5))
        }

    return freq_nomes_por_seculo


def tipo_relacao():
    # Dicionário para armazenar a frequência de cada tipo de relação
    dic = {}
    file = open("processos.txt")
    # Expressão regular para extrair o tipo de relação
    exp = re.compile(r",(?P<Relacao>(?:Pai|Filho|Irmao|Avo|Neto|Tio|Sobrinho|Mae|Primo|Tia|Prima|Sobrinha|Irma|Filha)\b[^.]*).")

    # Iterar sobre as linhas do arquivo e extrair o tipo de relação
    for line in file.readlines():
        info = exp.findall(line)
        if info != []:
            for r in info:
                if r not in dic.keys():
                    dic[r] = 1
                else:
                    dic[r] +=1 
    file.close()
    # Retornar o dicionário com a frequência de cada tipo de relação
    return dic

def to_json():
    # Abre o arquivo de entrada e o arquivo de saída
    entrada = open('processos.txt', 'r')
    saida = open('primeiros_processos.json', 'w')

    # Cria uma lista vazia para armazenar os registros
    registros = []

    # Lê as primeiras 20 linhas do arquivo de entrada
    for i in range(20):
        linha = entrada.readline().strip()

        # Utiliza expressão regular para extrair os dados do registro
        dados = re.split(r'::', linha)

        # Cria um dicionário com os dados do registro
        registro = {
            'Pasta': dados[0],
            'Data': dados[1],
            'Nome': dados[2],
            'Pai': dados[3],
            'Mae': dados[4],
            'Observacoes': dados[5]
        }

        # Adiciona o registro à lista de registros
        registros.append(registro)

    # Escreve a lista de registros no arquivo de saída no formato JSON
    json.dump(registros, saida, indent = 2)

    # Fecha os arquivos de entrada e saída
    entrada.close()
    saida.close()

def main():
    arquivo = 'processos.txt'

    freq_por_ano_regex = frequencia_processos_por_ano_regex(arquivo)
    print('Frequência de processos por ano (usando expressões regulares):')
    for ano, freq in freq_por_ano_regex.items():
        print(f'{ano}: {freq}')
    freq_nomes_por_seculo = frequencia_nomes_por_seculo(arquivo)
    print('\nFrequência de nomes por século:')
        # Imprime os séculos em ordem crescente
    for seculo in sorted(freq_nomes_por_seculo.keys()):
        print(f'Século {seculo}:')
        nomes = freq_nomes_por_seculo[seculo]['nomes']
        apelidos = freq_nomes_por_seculo[seculo]['apelidos']
        print('Nomes próprios mais frequentes:')
        for nome, freq in nomes.items():
            print(f'{nome}: {freq}')
        print('Apelidos mais frequentes:')
        for apelido, freq in apelidos.items():
            print(f'{apelido}: {freq}')
        print()
    relacoes = tipo_relacao()
    for relacao, freq in relacoes.items():
        print(f'{relacao}: {freq}')
    to_json()
    

if __name__ == '__main__':
    main()

