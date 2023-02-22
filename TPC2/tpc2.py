import sys

def main():
    is_summing = True  # variável que indica se estamos a somar ou não
    result = 0  # variável que guarda o resultado da soma
    for line in sys.stdin:
        line = line.strip()
        if not is_summing:  # se não estivermos a somar, procuramos por "On"
            if "on" in line.lower():
                is_summing = True
        elif "off" in line.lower():  # se estivermos a somar, procuramos por "Off"
            is_summing = False
        else:  # se não encontramos "On" nem "Off", procuramos por sequências de dígitos
            for word in line.split():
                if word.isdigit():
                    result += int(word)
        if "quit" in line.lower():  # se encontramos "Quit", saímos do programa
            break
        if "=" in line:  # se encontramos "=", imprimimos o resultado
            print(result)

if __name__ == '__main__':
    main()