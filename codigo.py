import os

from datetime import datetime
from colorama import Fore, Style, init

init ()

banco_de_dados = [
    {"id": "P0001", "peso": 100, "cor": "azul", "comprimento": 15, "status": "aprovada", "motivos_reprovacao": [], "numero_caixa": "C0001", "data_cadastro": "28/04/2026 10:00:00"},
    {"id": "P0002", "peso": 110, "cor": "vermelha", "comprimento": 9, "status": "reprovada", "motivos_reprovacao": ["Peso fora do padrão", "Cor fora do padrão", "Comprimento fora do padrão"], "numero_caixa": None, "data_cadastro": "28/04/2026 10:05:00"}
    ]

proximo_id = "P0003"

# já temos uma peça aprovada na C0001
caixa_atual = [banco_de_dados[0]]
caixas_fechadas = []
proxima_caixa = 1

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    print ("_" *30)
    print ("1 - Cadastrar uma peça")
    print ("2 - Listar peças")
    print ("3 - Remover uma peça")
    print ("4 - Listar caixas fechadas")
    print ("5 - Gerar relatório")
    print ("6 - Exportar dados")
    print ("0 - Sair")
    print ("_" *30)

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

# ---------- FUNÇÃO AUXILIAR: DADOS DAS PEÇAS PARA EXPORTAÇÃO ----------

def obter_dados_pecas():
    dados = []
    for item in banco_de_dados:
        status = item["status"]

        if len(item["motivos_reprovacao"]) == 0:
            motivos_texto = "-"
        else:
            motivos_texto = ", ".join(item["motivos_reprovacao"])

        if item["numero_caixa"] is not None:
            numero_caixa_texto = item["numero_caixa"]
        else:
            numero_caixa_texto = "-"

        data_cadastro = item.get("data_cadastro", "-")

        dados.append({
            "id": item["id"],
            "peso": item["peso"],
            "cor": item["cor"],
            "comprimento": item["comprimento"],
            "status": status,
            "motivos": motivos_texto,
            "numero_caixa": numero_caixa_texto,
            "data_cadastro": data_cadastro
        })
    return dados

# ------------------------ LISTAGEM NO TERMINAL ------------------------

def listar_pecas():
    limpar_tela()
    print (f'{"ID":<7} | {"PESO":<7} | {"COR":<15} | {"COMPRIMENTO":<12} | {"STATUS":<15} | {"MOTIVOS REPROVAÇÃO":<72} | {"NUMERO CAIXA":<7} | {"DATA CAD.":<16}')
    print ("_" * 157)

    dados = obter_dados_pecas()

    for item in dados:
        if item["status"] == "aprovada":
            status = f"{Fore.GREEN}Aprovada{Style.RESET_ALL}"
        else:
            status = f"{Fore.RED}Reprovada{Style.RESET_ALL}"

        linha = (
            f'{item["id"]:<7} | '
            f'{item["peso"]:<7} | '
            f'{item["cor"]:<15} | '
            f'{item["comprimento"]:<12} | '
            f'{status:<15} | '
            f'{item["motivos"]:<72} | '
            f'{item["numero_caixa"]:<7} | '
            f'{item["data_cadastro"]:<16}'
        )
        print(linha)

    print ("_" * 157)

# ------------------ EXPORTAÇÃO PARA PLANILHA (CSV) -------------------

def exportar_pecas_para_csv(nome_arquivo_pecas_csv="pecas_auditadas.csv"):
    dados = obter_dados_pecas()
    data_exportacao = datetime.now()
    timestamp_arquivo = data_exportacao.strftime("%Y%m%d_%H%M%S")
    data_texto = data_exportacao.strftime("%d/%m/%Y %H:%M:%S")

    nome_arquivo_pecas_csv = f"pecas_auditadas_{timestamp_arquivo}.csv"

    with open(nome_arquivo_pecas_csv, "w", encoding="utf-8") as f:
        f.write(f"# Arquivo gerado em: {data_texto}\n")
        f.write("ID,PESO,COR,COMPRIMENTO,STATUS,MOTIVOS_REPROVACAO,NUMERO_CAIXA,DATA_CADASTRO\n")
        for item in dados:
            motivos_csv = item["motivos"].replace(",", ";")
            linha = (
                f'{item["id"]},'
                f'{item["peso"]},'
                f'{item["cor"]},'
                f'{item["comprimento"]},' 
                f'{item["status"]},'
                f'"{motivos_csv}",' 
                f'{item["numero_caixa"]},'
                f'"{item["data_cadastro"]}"\n'
            )
            f.write(linha)

    print (f"{Fore.BLUE}Arquivo '{nome_arquivo_pecas_csv}' gerado na pasta do programa.{Style.RESET_ALL}")

# ------------------ EXPORTAÇÃO PEÇAS + CAIXAS EM TXT -------------------

def exportar_pecas_para_txt():
    dados = obter_dados_pecas()
    data_exportacao = datetime.now()
    timestamp_arquivo = data_exportacao.strftime("%Y%m%d_%H%M%S")
    data_texto = data_exportacao.strftime("%d/%m/%Y %H:%M:%S")

    nome_arquivo_pecas_txt = f'pecas_auditadas_{timestamp_arquivo}.txt'

    with open(nome_arquivo_pecas_txt, "w", encoding="utf-8") as f: 
        f.write("PEÇAS AUDITADAS\n")
        f.write(f"Arquivo gerado em: {data_texto}\n")
        # Seção 1: peças
        cabecalho = f'{"ID":<6}| {"PESO":<5}| {"COR":<10}| {"COMPRIMENTO":<12}| {"STATUS":<10}| {"MOTIVOS REPROVAÇÃO":<72}| {"NUMERO CAIXA":<13}| {"DATA CAD.":<20}'

        f.write(cabecalho + "\n")
        f.write("_" * len(cabecalho) + "\n")

        for item in dados:
            linha = (
                f'{item["id"]:<6}| '
                f'{item["peso"]:<5}| '
                f'{item["cor"]:<10}| '
                f'{item["comprimento"]:<12}| '
                f'{item["status"]:<10}| '
                f'{item["motivos"]:<72}| '
                f'{item["numero_caixa"]:<13}| '
                f'{item["data_cadastro"]:<20}'
            )
            f.write(linha + "\n")

        f.write("_" * len(cabecalho) + "\n\n")

        # Seção 2: caixas
        f.write("CAIXAS UTILIZADAS\n")
        f.write("-" * 40 + "\n")

        if len(caixas_fechadas) == 0 and len(caixa_atual) == 0:
            f.write("Nenhuma caixa utilizada.\n")
        else:
            if len(caixas_fechadas) > 0:
                f.write("Caixas fechadas:\n")
                for caixa in caixas_fechadas:
                    f.write(f'- Caixa {caixa["numero_caixa"]}: ')
                    ids = [peca["id"] for peca in caixa["pecas"]]
                    f.write(", ".join(ids) + "\n")
            else:
                f.write("Nenhuma caixa fechada.\n")

            f.write("\n")

            if len(caixa_atual) > 0:
                numero_caixa_atual = caixa_atual[0]["numero_caixa"]
                f.write(f'Caixa atual (em preenchimento) {numero_caixa_atual}: ')
                ids_atual = [peca["id"] for peca in caixa_atual]
                f.write(", ".join(ids_atual) + "\n")
            else:
                f.write("Nenhuma peça na caixa atual.\n")

        f.write("\n" + "_" * 40 + "\n")

    print(f"{Fore.BLUE}Arquivo '{nome_arquivo_pecas_txt}' gerado na pasta do programa.{Style.RESET_ALL}")


# -------------------------- COR DA PEÇA ----------------------------

def exibir_cor_peca():
    print ("_" * 30)
    print (f"{Fore.CYAN}1 - Azul{Style.RESET_ALL}")
    print (f"{Fore.GREEN}2 - Verde{Style.RESET_ALL}")
    print (f"{Fore.RED}3 - Vermelha{Style.RESET_ALL}")
    print (f"{Fore.YELLOW}4 - Amarela{Style.RESET_ALL}")
    print (f"{Fore.BLACK}5 - Preta{Style.RESET_ALL}")
    print (f"{Fore.WHITE}6 - Branca{Style.RESET_ALL}")
    print ("0 - Sair")
    print ("_" * 30)


def cadastrar_peca():
    global proximo_id
    limpar_tela()

    while True:
        try:
            peso = int(input("Digite o peso da peça: "))
            break
        except ValueError:
            print(f"{Fore.RED}Entrada inválida. Por favor, digite um número inteiro.{Style.RESET_ALL}")

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
        elif cor_escolhida == "0":
            print(f"{Fore.YELLOW}Cadastro da peça cancelado.{Style.RESET_ALL}")
            return
        else:
            print(f"{Fore.RED}Opção de cor inválida. Tente novamente.{Style.RESET_ALL}")

    while True:
        try:
            comprimento = int(input("Digite o comprimento da peça: "))
            break
        except ValueError:
            print(f"{Fore.RED}Entrada inválida. Por favor, digite um número inteiro.{Style.RESET_ALL}")

    nova_peca = {
        "id": proximo_id,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
        "status": "aprovada",
        "motivos_reprovacao": [],
        "numero_caixa": None,
        "data_cadastro": datetime.now() .strftime("%d/%m/%Y %H:%M:%S")
    }

    if peso >= 95 and peso <= 105:
        nova_peca["status"] = "aprovada"
    else:
        nova_peca["status"] = "reprovada"
        nova_peca["motivos_reprovacao"].append("Peso fora do padrão")

    if cor.lower() not in ["azul", "verde"]:
        nova_peca["status"] = "reprovada"
        nova_peca["motivos_reprovacao"].append("Cor fora do padrão")

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
    id_escolhido = input("Escolha o ID da peça que deseja remover: ").upper()
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

def gerar_relatorio():
    limpar_tela()

    total_pecas = 0
    total_aprovadas = 0
    total_reprovadas = 0
    motivos_reprovacao_count = {}

    for item in banco_de_dados:
        if item["status"] == "aprovada":
            total_aprovadas += 1
        else:
            total_reprovadas += 1
            for motivo in item["motivos_reprovacao"]:
                if motivo in motivos_reprovacao_count:
                    motivos_reprovacao_count[motivo] += 1
                else:
                    motivos_reprovacao_count[motivo] = 1

    total_pecas = total_aprovadas + total_reprovadas

    quantidade_caixas_fechadas = len(caixas_fechadas)
    quantidade_caixas = quantidade_caixas_fechadas
    if len(caixa_atual) > 0:
        quantidade_caixas += 1

    print (f"{Fore.CYAN}RELATÓRIO DE PRODUÇÃO:{Style.RESET_ALL}")
    print ("_" * 60)
    print (f"Total de peças produzidas: {total_pecas}")
    print (f"Total de peças aprovadas: {total_aprovadas}")
    print (f"Total de peças reprovadas: {total_reprovadas}")
    print (f"Quantidade de caixas fechadas: {quantidade_caixas_fechadas}")
    print (f"Quantidade total de caixas utilizadas (fechadas + atual): {quantidade_caixas}")
    print (f"Peças na caixa atual: {len(caixa_atual)}")
    print ("_" * 60)

    print (f"{Fore.YELLOW}Motivos de reprovação:{Style.RESET_ALL}")
    
    if len(motivos_reprovacao_count) == 0:
        print(f"{Fore.GREEN}Nenhuma peça reprovada!{Style.RESET_ALL}")
    else:
        for motivo, count in motivos_reprovacao_count.items():
            print (f"{motivo}: {count} peças")

    print ("_" * 60)

def exportar_relatorio_para_txt():

    total_aprovadas = 0
    total_reprovadas = 0
    motivos_reprovacao_count = {}

    for item in banco_de_dados:
        if item["status"] == "aprovada":
            total_aprovadas += 1
        else:
            total_reprovadas += 1
            for motivo in item["motivos_reprovacao"]:
                if motivo in motivos_reprovacao_count:
                    motivos_reprovacao_count[motivo] += 1
                else:
                    motivos_reprovacao_count[motivo] = 1

    total_pecas = total_aprovadas + total_reprovadas

    quantidade_caixas_fechadas = len(caixas_fechadas)
    quantidade_caixas = quantidade_caixas_fechadas
    if len(caixa_atual) > 0:
        quantidade_caixas += 1

    data_exportacao = datetime.now()
    timestamp_arquivo = data_exportacao.strftime("%Y-%m-%d_%H-%M-%S")
    data_texto =data_exportacao.strftime("%d/%m/%Y %H:%M-%S")

    nome_arquivo_relatorio = f"relatorio_producao_{timestamp_arquivo}.txt"

    with open(nome_arquivo_relatorio, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE PRODUÇÃO\n")
        f.write("_" * 60 + "\n")
        f.write(f"Total de peças produzidas: {total_pecas}\n")
        f.write(f"Total de peças aprovadas: {total_aprovadas}\n")
        f.write(f"Total de peças reprovadas: {total_reprovadas}\n")
        f.write(f"Quantidade de caixas fechadas: {quantidade_caixas_fechadas}\n")
        f.write(f"Quantidade total de caixas utilizadas (fechadas + atual): {quantidade_caixas}\n")
        f.write(f"Peças na caixa atual: {len(caixa_atual)}\n")
        f.write("_" * 60 + "\n")
        f.write("Motivos de reprovação:\n")

        if len(motivos_reprovacao_count) == 0:
            f.write("Nenhuma peça reprovada!\n")
        else:
            for motivo, count in motivos_reprovacao_count.items():
                f.write(f"{motivo}: {count} peça(s)\n")

        f.write("_" * 60 + "\n")

    print (f"{Fore.BLUE}Arquivo '{nome_arquivo_relatorio}' gerado na pasta do programa.{Style.RESET_ALL}")

def exportar_dados():
    exportar_pecas_para_csv()
    exportar_pecas_para_txt()
    exportar_relatorio_para_txt()
    print(f"{Fore.CYAN}Exportação concluída com sucesso!{Style.RESET_ALL}")


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
        elif escolha == "6":
            exportar_dados()
        elif escolha == "0":
            print(f"{Fore.YELLOW}Saindo do programa...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Opção inválida. Tente novamente.{Style.RESET_ALL}")

app()
