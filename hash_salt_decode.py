import hashlib
from sys import argv

# Dichiarazioni Globali
usage = "Istruzioni per un uso corretto: ...."
##Opzioni##
opzioniPossibili = ["-A", "-S", "-H", "-O", "-W"]
##Algoritmi Supportati##
algoritmiHash = ["md5"]


def parametriScelti():
    """
    Verifica i parametri immessi dall'utente
    :return: tipo dizionario, opzioni impostate es.{'algorithm': 'md5', 'wordlist': 'dictTest.txt',
                                                    'hashString': '5f4dcc3b5aa765d61d8327deb882cf99'}
    """
    dictSelezione = {}
    for opzione in argv[1:]:
        if opzione in opzioniPossibili:
            match opzione:
                case '-A':
                    if argv[argv.index(opzione)+1] in algoritmiHash:
                        dictSelezione["algorithm"] = argv[argv.index(opzione)+1]
                    else:
                        print("ERROR: Problemi con l'algoritmo specificato")
                case '-W':
                    if argv[argv.index(opzione)+1].endswith(".txt"):
                        dictSelezione["wordlist"] = argv[argv.index(opzione)+1]
                case '-H':
                    dictSelezione["hashString"] = argv[argv.index(opzione)+1]
                case '-S':
                    dictSelezione["saltString"] = argv[argv.index(opzione)+1]
                case '-O':
                    if argv[argv.index(opzione)+1].endswith(".txt"):
                        dictSelezione["outputString"] = argv[argv.index(opzione)+1]
                    else:
                        print("ERROR: Il file di output deve avere estenzione .txt")
                        exit(usage)
    if not 'wordlist' in dictSelezione or not 'algorithm' in dictSelezione:
        print("ERROR: Rilevati problemi con i paramteri obligatori (wordlist.txt; algorithm)")
        exit(usage)
    else:
        return dictSelezione


def hdm5(wordlistTxt, dictSelezione):
    """
    Ricerca l'hash nelle password del dizionario che gli è stato passato convertendole in formazto md5, aggiungendo un salt
    passato come input a dx e a sx.
    :param wordlistTxt: tipo stringa, la path del dizionario di password
    :param dictSelezione: tipo dizionario, contiene l'input dell' utente
    :return: tipo dizionario, chiave password hash del dizionario e valore password in chiaro del dizionario es.
                            {'47eb752bac1c08c75e30d9624b3e58b7': 'simone', '5f4dcc3b5aa765d61d8327deb882cf99':
                            'password', '5ebe2294ecd0e0f08eab7690d2a6ee69': 'secret', '037c70dbc1c812f6b2091688804d7b17'
                            : 'giovanni', '95c1705c33e07aa8a5df5f65b6872886': 'amore', '33da09c39001c9ab716070b07a0d7f51
                            ': 'figlio'}
    """
    passwHashDict = {}
    cicli = 1
    if not 'saltString' in dictSelezione:
        salt = ""
    else:
        salt = dictSelezione['saltString']
        cicli = 2
    for n in range(cicli):
        with open(wordlistTxt, 'r') as filePw:
                for line in filePw:
                    line = line.strip("\n")
                    password = line
                    if n == 0:
                        password += salt
                    else:
                        password = salt + password
                    password = bytes(password, 'UTF-8')
                    m = hashlib.md5(password)
                    md5Hash = m.hexdigest()
                    passwHashDict[md5Hash] = line
    return passwHashDict

def hashCheker(passwHashDict, dictSelezione):
    """
    Verifica la presenza di un hash uguale e se c'è stampa la password in chiaro e l'hash associato
    es. PASSWORD: password       HASH: 5f4dcc3b5aa765d61d8327deb882cf99
    :param passwHashDict: tipo dizionario, associazione hash, password in chiaro
    :param dictSelezione:  tipo dizionario, input utente
    :return: null
    """
    if dictSelezione['hashString'] in passwHashDict:
        print(f"PASSWORD: {passwHashDict[dictSelezione['hashString']]}\t HASH: {dictSelezione['hashString']}")
    pass

def esportaHash(passwHashDict, dictSelezione):
    """
    Esporta un file con le password ed un file con gli hash
    :param passwHashDict:
    :param dictSelezione:
    :return:
    """
    with open(f"{dictSelezione['outputString']}", "w") as fileOut:
        for hashPw in passwHashDict.keys():
                fileOut.writelines(hashPw + "\n")
    with open(f"{dictSelezione['outputString']}_passw", "w") as filePasswOut:
        for passw in passwHashDict.values():
            filePasswOut.writelines(passw + "\n")

def main():
    dictSelezione = parametriScelti()
    print(dictSelezione)
    try:
        passwHashDict = hdm5(dictSelezione['wordlist'], dictSelezione)
        print(passwHashDict)
    except (FileNotFoundError, FileExistsError) as ex:
        print("ERROR: File Not Found")
        exit(usage)
    if "hashString" in dictSelezione:
        hashCheker(passwHashDict, dictSelezione)
    if "outputString" in dictSelezione:
        esportaHash(passwHashDict, dictSelezione)

if __name__ == "__main__":
    print("HASH_THE_PASSWORD")

    main()



