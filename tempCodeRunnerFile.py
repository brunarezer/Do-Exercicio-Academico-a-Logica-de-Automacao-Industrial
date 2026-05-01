import os

from colorama import Fore, Style, init

init ()

banco_de_dados = [
    {"id": "P0001", "peso": 100, "cor": "azul", "comprimento": 15, "status": "aprovada", "motivos_reprovacao": [], "numero_caixa": "C0001"},
    {"id": "P0002", "peso": 110, "cor": "vermelha", "comprimento": 9, "status": "reprovada", "motivos_reprovacao": ["Peso fora do padrão", "cor inválida", "comprimento fora do padrão"], "numero_caixa": None}
    ]

proximo_id = "P0003"

caixa_atual = []
caixas_fechadas = []
proxima_caixa = 2

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    print ("_" *50)
    print ("1 - Cadastrar uma peça")
    print ("2 - Listar peças")
    print ("3 - Remover uma peça")
    print ("4 - Listar caixas fechadas")
    print ("5 - Gerar relatório")
    print ("0 - Sair")
    print ("_" *50)

def armazenar_peca_em_caixa(peca):
    global caixa_atual, caixas_fechadas, proxima_caixa

    numero_caixa = "C" + str(proxima_caixa) .zfill(4)
    peca["numero_caixa"] = numero_caixa
    caixa_atual.append(peca)

    if len(caixa_atual) == 10:
        caixas_fechadas.append({
            "numero_caixa": numero_caixa, 
            "pecas": caixa_atual.copy()
        })
        caixa_atual.clear()
        proxima_caixa += 1

def buscar_peca_por_id(id_escolhido):
    for item in banco_de_dados:
        if item["id"] == id_escolhido:
            return item
    return False

def listar_pecas():
    limpar_tela()
    print (f'{"ID":<7} "|" {"PESO":<7} "|" {"COR":<15} "|" {"COMPRIMENTO":<7} "|" {"STATUS":<15} "|" {"MOTIVOS REPROVAÇÃO":<30} "|" {"NUMERO CAIXA":<7}')
    print ("_" * 120)

    for item in banco_de_dados:
        if item["status"] == "aprovada":
            status = f"{Fore.GREEN}Aprovada{Style.RESET_ALL}"
        else:
            status = f"{Fore.RED}Reprovada{Style.RESET_ALL}"

        if len(item["motivos_reprovacao"]) == 0:
            motivos_texto = "-"
        else:
            motivos_texto = ", ".join(item["motivos_reprovacao"])

        if item["numero_caixa"] is not None:
            numero_caixa_texto = item["numero_caixa"]
        else:
            numero_caixa_texto = "-"

        print (f'{item["id"]:<7} "|" {item["peso"]:<7} "|" {item["cor"]:<15} "|" {item["comprimento"]:<7} "|" {status} "|" {motivos_texto:<30} "|" {numero_caixa_texto:<7}')

    print ("_" * 120)

def exibir_cor_peca():
    print ("_" * 50)
    print (f"{Fore.CYAN}1 - Azul{Style.RESET_ALL}")
    print (f"{Fore.GREEN}2 - Verde{Style.RESET_ALL}")
    print (f"{Fore.RED}3 - Vermelha{Style.RESET_ALL}")
    print (f"{Fore.YELLOW}4 - Amarela{Style.RESET_ALL}")
    print (f"{Fore.BLACK}5 - Preta{Style.RESET_ALL}")
    print (f"{Fore.WHITE}6 - Branca{Style.RESET_ALL}")
    print ("_" * 50)


def cadastrar_peca():
    global proximo_id
    peso = int(input("Digite o peso da peça: "))
    while True:
        exibir_cor_peca()
        cor_escolhida = input("Digite o número correspondente à cor: ")

        if cor_escolhida == "1":
            cor = "azul"
            break
        elif cor_escolhida == "2":
            cor = "verde"
            break
        elif cor_escolhida == "3":
            cor = "vermelha"
            break 
        elif cor_escolhida == "4":
            cor = "amarela"
            break
        elif cor_escolhida == "5":
            cor = "preta"
            break
        elif cor_escolhida == "6":
            cor = "branca"
            break
        else:
            print(f"{Fore.RED}Opção de cor inválida. Tente novamente.{Style.RESET_ALL}")

    comprimento = int(input("Digite o comprimento da peça: "))

    nova_peca = {
        "id": proximo_id,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
        "status": "aprovada",
        "motivos_reprovacao": [],
        "numero_caixa": None
    }

    if peso >= 95 and peso <= 105:
        nova_peca["status"] = "aprovada"
    else:
        nova_peca["status"] = "reprovada"
        nova_peca["motivos_reprovacao"].append("Peso fora do padrão")

    if cor.lower() not in ["azul", "verde"]:
        nova_peca["status"] = "reprovada"
        nova_peca["motivos_reprovacao"].append("Cor inválida")

    if comprimento < 10 or comprimento > 20:
        nova_peca["status"] = "reprovada"
        nova_peca["motivos_reprovacao"].append("Comprimento fora do padrão")

    if nova_peca["status"] == "aprovada":
        armazenar_peca_em_caixa(nova_peca)

    banco_de_dados.append(nova_peca)
    numero = int(proximo_id[1:]) + 1
    proximo_id = "P" + str(numero).zfill(4)

    print(f"{Fore.BLUE}Peça cadastrada com sucesso!{Style.RESET_ALL}")
    listar_pecas()

def remover_peca():
    listar_pecas()
    id_escolhido = input('Escolha o ID da peça que deseja remover: ')
    peça = buscar_peca_por_id(id_escolhido)
    if peça:
        banco_de_dados.remove(peça)
        print(f"{Fore.BLUE}Peça removida com sucesso!{Style.RESET_ALL}")
        listar_pecas()
    else:
        print(f"{Fore.RED}ID não encontrado!{Style.RESET_ALL}")

def listar_caixas_fechadas():
    limpar_tela()
    print (f"{Fore.MAGENTA}CAIXAS FECHADAS:{Style.RESET_ALL}")
    print ("_" * 50)

    if len(caixas_fechadas) == 0:
        print(f"{Fore.YELLOW}Nenhuma caixa fechada no momento.{Style.RESET_ALL}")
        return

    else:
        for caixa in caixas_fechadas:
            print (f'Caixa {caixa["numero_caixa"]}')
            print("Peças:", end=" ")

            for peca in caixa["pecas"]:
                print (f'{peca["id"]} ', end="")

            print()
            print ("_" * 50)

def app():
    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            cadastrar_peca()
        elif escolha == "2":
            listar_pecas()
        elif escolha == "3":
            remover_peca()
        elif escolha == "4":
            listar_caixas_fechadas()
        elif escolha == "5":
            gerar_relatorio()
        elif escolha == "0":
            print(f"{Fore.YELLOW}Saindo do programa...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Opção inválida. Tente novamente.{Style.RESET_ALL}")

app()
