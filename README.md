# 📚 API Escola - FastAPI + MySQL

Este projeto implementa uma API RESTful utilizando **FastAPI** para gerenciar **alunos** e **endereços** em um banco de dados **MySQL**.  

Foram desenvolvidos endpoints para **CRUD completo** (Create, Read, Update, Delete) das tabelas `tb_enderecos` e `tb_alunos`.  

---

## 🚀 Tecnologias Utilizadas
- [Python 3.10+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pandas](https://pandas.pydata.org/)
- [MySQL](https://www.mysql.com/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Uvicorn](https://www.uvicorn.org/)
- [uv](https://docs.astral.sh/uv/) (gerenciador de dependências)

---

## 📂 Estrutura do Projeto
.
├── main.py # Código principal da API (endpoints)
├── .env # Variáveis de ambiente (configuração do banco)
├── pyproject.toml # Dependências declaradas
├── uv.lock # Lockfile do uv
└── README.md # Documentação do projeto

yaml
Copiar código

---

## ⚙️ Configuração do Ambiente

### 1️⃣ Clonar o repositório
```bash
git clone 
2️⃣ Instalar dependências com uv
bash
Copiar código
uv sync
3️⃣ Criar arquivo .env
Crie um arquivo chamado .env na raiz do projeto com as variáveis de conexão ao banco de dados:

ini
Copiar código
DB_USER=root
DB_PASSWORD=Margiana123.
DB_HOST=localhost
DB_NAME=db_escola
4️⃣ Criar tabelas no MySQL
sql
Copiar código
CREATE DATABASE db_escola;

USE db_escola;

CREATE TABLE tb_enderecos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cep VARCHAR(20),
    endereco VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    regiao VARCHAR(50)
);

CREATE TABLE tb_alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(20),
    nome VARCHAR(100),
    email VARCHAR(100),
    endereco_id INT,
    FOREIGN KEY (endereco_id) REFERENCES tb_enderecos(id)
);
▶️ Executando o Projeto
bash
Copiar código
uv run uvicorn main:app --reload
A API estará disponível em:
👉 http://127.0.0.1:8000

Documentação interativa:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

📌 Endpoints Disponíveis
🔹 Endereços (/enderecos)
GET /enderecos/ → Lista todos os endereços

GET /enderecos/{id} → Retorna um endereço pelo ID

POST /enderecos/ → Insere um novo endereço

PUT /enderecos/{id} → Atualiza dados de um endereço

DELETE /enderecos/{id} → Remove um endereço

📥 Exemplo de JSON (POST /enderecos/):

json
Copiar código
{
  "cep": "12345-678",
  "endereco": "Rua das Flores, 100",
  "bairro": "Centro",
  "cidade": "São Paulo",
  "estado": "SP",
  "regiao": "Sudeste"
}
🔹 Alunos (/alunos)
GET /alunos/ → Lista todos os alunos

GET /alunos/{id} → Retorna um aluno pelo ID

POST /alunos/ → Insere um novo aluno

PUT /alunos/{id} → Atualiza dados de um aluno

DELETE /alunos/{id} → Remove um aluno

📥 Exemplo de JSON (POST /alunos/):

json
Copiar código
{
  "matricula": "2025001",
  "nome": "Maria Silva",
  "email": "maria@email.com",
  "endereco_id": 1
}
🛠 Testando com Postman ou cURL
Criar novo endereço
bash
Copiar código
curl -X POST http://127.0.0.1:8000/enderecos/ \
-H "Content-Type: application/json" \
-d '{"cep": "12345-678", "endereco": "Rua A", "bairro": "Centro", "cidade": "Brasília", "estado": "DF", "regiao": "Centro-Oeste"}'
Criar novo aluno
bash
Copiar código
curl -X POST http://127.0.0.1:8000/alunos/ \
-H "Content-Type: application/json" \
-d '{"matricula": "2025002", "nome": "João Souza", "email": "joao@email.com", "endereco_id": 1}'

