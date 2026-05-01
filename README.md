# Sistema de Inspeção e Controle de Qualidade de Peças

**Disciplina:** Algoritmos e Lógica de Programação — UniFECAF  
**Aluna:** Bruna A. S. Pellegrini Rezer


## Sobre o Projeto

Protótipo de um sistema de automação industrial desenvolvido em Python que simula o controle de qualidade de uma linha de produção. O sistema recebe dados de peças, aplica critérios de inspeção automaticamente, organiza as aprovadas em caixas e gera relatórios consolidados, simulando a lógica de um módulo de controle de qualidade de um MES (Manufacturing Execution System).

## Funcionalidades

| Opção | Funcionalidade |
|-------|---------------|
| `1` | Cadastrar nova peça (com validação automática) |
| `2` | Listar todas as peças em tabela formatada |
| `3` | Remover uma peça pelo ID |
| `4` | Listar caixas fechadas e suas peças |
| `5` | Gerar relatório de produção no terminal |
| `6` | Exportar dados (CSV + TXT + relatório) |
| `0` | Sair do sistema |

### Critérios de aprovação automática

-  **Peso:** entre 95g e 105g
-  **Cor:** azul ou verde
-  **Comprimento:** entre 10cm e 20cm

Uma peça pode acumular múltiplos motivos de reprovação caso descumpra mais de um critério.

### Armazenamento em caixas

Peças aprovadas são automaticamente alocadas em caixas de até **10 unidades**. Ao atingir a capacidade, a caixa é fechada e uma nova é iniciada automaticamente. Os números de caixa seguem o formato `C0001`, `C0002`, etc.

### Exportação de dados

Ao acionar a opção `6`, três arquivos são gerados automaticamente com timestamp no nome:

```
pecas_auditadas_AAAAMMDD_HHMMSS.csv   → compatível com Excel e Google Sheets
pecas_auditadas_AAAAMMDD_HHMMSS.txt   → tabela formatada + resumo de caixas
relatorio_producao_AAAAMMDD_HHMMSS.txt → relatório consolidado de produção
```


## Tecnologias utilizadas

- **Python 3.x**
- `os` — limpeza de tela multiplataforma
- `datetime` — registro de data/hora de cadastro e exportação
- `colorama` — cores no terminal (verde = aprovada, vermelho = reprovada)

---

## Como rodar o projeto

### 1. Pré-requisitos

Tenha o **Python 3** instalado. Verifique com:

```bash
python --version
```

### 2. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 3. Instale a dependência externa

O único pacote externo necessário é o `colorama`:

```bash
pip install colorama
```

### 4. Execute o programa

```bash
python codigo.py
```

---

## Exemplos de uso

### Cadastrando uma peça aprovada

```
Digite o peso da peça: 100
Digite o número correspondente à cor: 1   (azul)
Digite o comprimento da peça: 15

 Peça cadastrada com sucesso!
```

Resultado na listagem:
```
ID      | PESO    | COR             | COMPRIMENTO  | STATUS          | MOTIVOS REPROVAÇÃO   | NUMERO CAIXA | DATA CAD.
P0003   | 100     | azul            | 15           | Aprovada        | -                    | C0001        | 01/05/2026 09:00:00
```

### Cadastrando uma peça reprovada (múltiplos motivos)

```
Digite o peso da peça: 120
Digite o número correspondente à cor: 3   (vermelha)
Digite o comprimento da peça: 7

Peça cadastrada com sucesso!
```

Resultado na listagem:
```
P0004   | 120     | vermelha        | 7            | Reprovada       | Peso fora do padrão, Cor fora do padrão, Comprimento fora do padrão | - | 01/05/2026 09:01:00
```

### Relatório gerado (opção 5)

```
RELATÓRIO DE PRODUÇÃO:
____________________________________________________________
Total de peças produzidas: 10
Total de peças aprovadas: 7
Total de peças reprovadas: 3
Quantidade de caixas fechadas: 0
Quantidade total de caixas utilizadas (fechadas + atual): 1
Peças na caixa atual: 7
____________________________________________________________
Motivos de reprovação:
Peso fora do padrão: 2 peças
Cor fora do padrão: 1 peça
Comprimento fora do padrão: 2 peças
```

---

## Estrutura do projeto

```
/
├── codigo.py                  # Código fonte principal
├── README.md                  # Este arquivo
└── (arquivos gerados ao exportar)
    ├── pecas_auditadas_*.csv
    ├── pecas_auditadas_*.txt
    └── relatorio_producao_*.txt
```

---

## Visão de futuro

Este protótipo implementa o núcleo lógico de um módulo de controle de qualidade de um MES industrial. Evoluções naturais incluem:

- **Banco de dados persistente** (SQLite/PostgreSQL) para histórico entre sessões.
- **Integração com sensores** via porta serial (balança, encoder, câmera).
- **API REST** (FastAPI) para integração com ERP e dashboards.
- **IA preditiva** (scikit-learn) para antecipar reprovações em série.

> A lógica que decide se uma peça está aprovada ou reprovada é a mesma. A complexidade muda — a base, não.

---

*Trabalho desenvolvido para a disciplina de Algoritmos e Lógica de Programação — UniFECAF.*
