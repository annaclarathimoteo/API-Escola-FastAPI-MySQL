from fastapi import FastAPI, HTTPException
from typing import List, Optional
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", "Margiana123."))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "db_escola")

# Conexão com o banco de dados
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}")

# Instância do FastAPI
app = FastAPI()

# ----------------------------
# CRUD PARA ENDEREÇOS
# ----------------------------

# Modelo Pydantic para inserir/atualizar endereço
class Endereco(BaseModel):
    cep: str
    endereco: str
    bairro: str
    cidade: str
    estado: str
    regiao: str

class EnderecoUpdate(BaseModel):
    cep: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    regiao: Optional[str] = None

# Listar todos os endereços
@app.get("/enderecos/", response_model=List[dict])
def listar_enderecos():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM tb_enderecos", conn)
    return df.to_dict(orient="records")

# Consultar endereço por ID
@app.get("/enderecos/{id}", response_model=dict)
def consultar_endereco(id: int):
    with engine.connect() as conn:
        query = text("SELECT * FROM tb_enderecos WHERE id = :id")
        df = pd.read_sql(query, conn, params={"id": id})

    if df.empty:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return df.to_dict(orient="records")[0]

# Inserir endereço
@app.post("/enderecos/", response_model=dict)
def inserir_endereco(dados: Endereco):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO tb_enderecos (cep, endereco, bairro, cidade, estado, regiao)
                VALUES (:cep, :endereco, :bairro, :cidade, :estado, :regiao)
            """),
            dados.dict()
        )
    return {"mensagem": "Endereço cadastrado com sucesso"}

# Atualizar endereço
@app.put("/enderecos/{id}", response_model=dict)
def atualizar_endereco(id: int, dados: EnderecoUpdate):
    update_data = {k: v for k, v in dados.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

    with engine.begin() as conn:
        query = text(f"""
            UPDATE tb_enderecos
            SET {', '.join([f"{k} = :{k}" for k in update_data.keys()])}
            WHERE id = :id
        """)
        result = conn.execute(query, {**update_data, "id": id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return {"mensagem": "Endereço atualizado com sucesso"}

# Deletar endereço
@app.delete("/enderecos/{id}", response_model=dict)
def deletar_endereco(id: int):
    with engine.begin() as conn:
        result = conn.execute(text("DELETE FROM tb_enderecos WHERE id = :id"), {"id": id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return {"mensagem": f"Endereço {id} deletado com sucesso"}


# ----------------------------
# CRUD PARA ALUNOS
# ----------------------------

# Modelo Pydantic para inserir aluno
class Aluno(BaseModel):
    matricula: str
    nome: str
    email: str
    endereco_id: int

# Modelo Pydantic para atualizar aluno (todos opcionais)
class AlunoUpdate(BaseModel):
    matricula: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    endereco_id: Optional[int] = None

# Listar todos os alunos
@app.get("/alunos/", response_model=List[dict])
def listar_alunos():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM tb_alunos", conn)
    return df.to_dict(orient="records")

# Consultar aluno por ID
@app.get("/alunos/{id}", response_model=dict)
def consultar_aluno(id: int):
    with engine.connect() as conn:
        query = text("SELECT * FROM tb_alunos WHERE id = :id")
        df = pd.read_sql(query, conn, params={"id": id})
    if df.empty:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return df.to_dict(orient="records")[0]

# Inserir aluno
@app.post("/alunos/", response_model=dict)
def inserir_aluno(dados: Aluno):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO tb_alunos (matricula, nome, email, endereco_id)
                VALUES (:matricula, :nome, :email, :endereco_id)
            """),
            dados.dict()
        )
    return {"mensagem": "Aluno cadastrado com sucesso"}

# Atualizar aluno
@app.put("/alunos/{id}", response_model=dict)
def atualizar_aluno(id: int, dados: AlunoUpdate):
    update_data = {k: v for k, v in dados.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    
    with engine.begin() as conn:
        query = text(f"""
            UPDATE tb_alunos
            SET {', '.join([f"{k} = :{k}" for k in update_data.keys()])}
            WHERE id = :id
        """)
        result = conn.execute(query, {**update_data, "id": id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"mensagem": "Aluno atualizado com sucesso"}

# Deletar aluno
@app.delete("/alunos/{id}", response_model=dict)
def deletar_aluno(id: int):
    with engine.begin() as conn:
        result = conn.execute(text("DELETE FROM tb_alunos WHERE id = :id"), {"id": id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"mensagem": f"Aluno {id} deletado com sucesso"}
