import json
import re

def sumat(lista):
    soma = 0
    for e in lista: soma += int(e) 
    return soma 

def mediat(lista):
    soma = 0
    t = 0
    for e in lista: 
        soma += int(e) 
        t += 1
    return soma/t

def parseFicheiro(file):
    
    f = open(file,"r", encoding='utf-8')
    j = open("output.json", "w", encoding='utf-8')
    flag = 0
    functs = {}
    i = 0
    regex = "^"


    result = re.findall("(\w+)(\d+|\{\d+\}|\{\d+,\d+\})?(\:\:\w+)?", f.readline())
    print(result)

    
    for resultado in result:
        regex += f"(?P<{resultado[0]}>" + "([\w\s]+"
        flag = 0
        if resultado[1] != "":
            print(resultado[1])
            regex += f"\,?){resultado[1]}(?:,*)?"
            flag = 1
        if resultado[2] != "":
            functs[i] = resultado[2][2:]

        if flag == 1:
            regex += "),"
        else:
            regex += ")),"
        i += 1

    
    regex = regex [:-1]
    regex += "$"
    print(regex)
    linhas = f.readlines()

    for linha in linhas:
        resultt = re.match(regex,linha)
        dictG = resultt.groupdict()

        i = 0
        for param in dictG:
            listaa = dictG[param].split(",")
            if (len(listaa) > 1):
                listatemp = []
                for elemento in listaa:
                    if elemento != "":
                        listatemp.append(elemento)
                if (i in functs):
                    if functs[i] == "sum":
                        listatemp = sumat(listatemp)
                    elif functs[i] == "media":
                        listatemp = mediat(listatemp)
                dictG[param] = listatemp
            i += 1

        json.dump(dictG, j, ensure_ascii=False, indent = 4)

parseFicheiro("input.csv")