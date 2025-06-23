# Consultas USP

**Participantes do Projeto:**

- João Pedro Daleffe Dias – nº USP: 15463342  
- Gustavo Ramos Santos Pires – nº USP: 15458030  
- Larissa Pires Moreira Rocha Duarte – nº USP: 15522358  

---

## 📌 Descrição

**Consultas USP** é um programa em Python para consulta e análise de informações públicas sobre cursos e disciplinas da Universidade de São Paulo, coletadas a partir do sistema JúpiterWeb.

O sistema possui uma interface de comandos simples para listar, buscar e visualizar dados sobre unidades, cursos e disciplinas.

---

## 🚀 Funcionalidades

### 🔹 Comandos de Listagem Geral
| Comando | Descrição |
|--------|-----------|
| `U` | Lista todas as unidades. |
| `C` | Lista todos os cursos, agrupados por unidade. |
| `D COMUM` | Lista disciplinas que pertencem a mais de um curso. |

---

### 🔹 Comandos de Consulta Específica
| Comando | Descrição |
|--------|-----------|
| `U [sigla ou nome]` | Mostra os cursos de uma unidade específica. |
| `C [sigla ou nome da unidade] [nº do curso]` | Mostra os dados de um curso específico. |
| `DC [sigla ou nome da unidade] [nº do curso]` | Lista todas as disciplinas de um curso específico. |
| `D [código ou nome da disciplina]` | Mostra os dados de uma disciplina específica. |

---

### 🔹 Comandos de Busca e Estatísticas
| Comando | Descrição |
|--------|-----------|
| `BUSCAR C [termo]` | Busca cursos que contenham o termo no nome. |
| `STATS` | Mostra estatísticas gerais sobre os dados coletados. |
| `AJUDA` | Mostra o menu de ajuda com todos os comandos. |
| `SAIR` | Encerra o programa. |

---

## ⚙️ Instalação

1. **Requisitos:**
   - Python 3.7+
   - Google Chrome instalado (versão compatível com o webdriver)

2. **Crie um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # (Linux/macOS)
   venv\Scripts\activate     # (Windows)

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```
   Caso não funcione você pode tentar baixar manualmente:
   ```bash
   pip install beautifulsoup4 selenium webdriver-manager
   ```

## 🖥️ Execução

   Após instalar as dependências, execute o programa com:
   ```bash
   python main.py
   ```
