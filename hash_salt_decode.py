import hashlib
from sys import argv

usage = "Istruzioni per un uso corretto: ...."
opzioniPossibili = ["-A", "-S", "-H", "-O", "-W"]
algoritmiHash = ["md5"]

def parametriScelti():
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
    if dictSelezione['hashString'] in passwHashDict:
        print(f"PASSWORD: {passwHashDict[dictSelezione['hashString']]}\t HASH: {dictSelezione['hashString']}")
    pass

def esportaHash(passwHashDict, dictSelezione):
    with open(f"{dictSelezione['outputString']}", "w") as fileOut:
        for hashPw in passwHashDict.keys():
                fileOut.writelines(hashPw + "\n")
    with open(f"{dictSelezione['outputString']}_passw", "w") as filePasswOut:
        for passw in passwHashDict.values():
            filePasswOut.writelines(passw + "\n")

def main():
    dictSelezione = parametriScelti()
    try:
        passwHashDict = hdm5(dictSelezione['wordlist'], dictSelezione)
    except (FileNotFoundError, FileExistsError) as ex:
        print("ERROR: File Not Found")
        exit(usage)
    if "hashString" in dictSelezione:
        hashCheker(passwHashDict, dictSelezione)
    if "outputString" in dictSelezione:
        esportaHash(passwHashDict, dictSelezione)

if __name__ == "__main__":
    main()



