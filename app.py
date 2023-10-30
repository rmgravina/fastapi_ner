import spacy
from fastapi import FastAPI, File, UploadFile
import uvicorn
from secrets import token_hex
import base64
import fitz
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Criar Class para receber o Base64
class Base64(BaseModel):

    pdf_base64: str = ""

# Carregar o modelo NER ('lener' é um modelo customizado pela equipe)
NER = spacy.load('lener')

# Criar o App FastAPI
app = FastAPI(title=os.getenv('TITLE'), description=os.getenv('DESCRIPTION'))


# Rota raiz
@app.get("/")
def root():
    return {"message": "go to /docs to see the documentation"}


# Rota da API_NER
@app.post("/pdf_base64") 
def ner_pdfb64(item: Base64):

    temp = "./documents/output/" + token_hex(12) + ".pdf" # Criar destino/nome do arquivo temporário para salvar o Base64
    base64_bytes = item.pdf_base64.encode('ascii') # Converter os bytes do Base64 para sequencia de caracteres ASCII (em base64)
    b64 = base64.b64decode(base64_bytes + b'==') # Decodificar o Base64 para o formato original

    # Salvar o arquivo temporário
    with open(temp, "wb") as f:
        f.write(b64)

    # Abrir o arquivo temporário
    doc =  fitz.open(temp, filetype="pdf")

    # Extrair o texto do PDF
    conteudo = ""
    for page in doc:
        conteudo += page.get_text().replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # Fechar o arquivo temporário
    doc.close()

    # Identificar as entidades nomeadas
    document = NER(str(conteudo))

    # Criar um conjunto para armazenar as entidades únicas
    ents_unique = set()

    # Identificar todas as entidades nomeadas referentes apenas à pessoas
    for ent in document.ents:
        if ent.label_ == 'PER':
            ents_unique.add(ent.text)

    ents_unique = list(ents_unique) # Converter o conjunto para lista

    # Remover os prefixos dos nomes, tipo Sr., Sra., Dr., etc.
    prefixos = ["Sr.",
                "Sra.",
                "Dr.",
                "Dra.",
                "Prof.",
                "Profª.",
                "Profº.",
                "Vossa Excelência",
                "Conselheiro",
                "Conselheira",
                "Relator",
                "Relatora",
                "Desembargador",
                "Desembargadora",
                "Ministro",
                "Ministra",
                "Senador",
                "Senadora",
                "Deputado",
                "Deputada",
                "Vereador",
                "Vereadora",
                "Prefeito",
                "Prefeita",
                "Governador",
                "Governadora",
                "Presidente",
                "Presidenta",
                "Secretário",
                "Secretária",
                "Procurador",
                "Procuradora",
                "Promotor",
                "Promotora",
                "Juiz",
                "Juíza",
                "Desembargador",
                "Desembargadora",
                "Diretor",
                "Diretora",
                "Professor",
                "Professora"]
    for prefixo in prefixos:
        ents_unique = {nome.replace(prefixo, "").strip() for nome in ents_unique}

    # Remover nomes que não possuem sobrenome
    ents_unique = [nome for nome in ents_unique if " " in nome]

     # Remover nomes que não possuem apenas letras no nome
#    ents_unique = {nome for nome in ents_unique if nome.split(" ")[0].isalpha()}

    # Remover nomes que possuem o primeiro nome abreviado, tipo A. B. C. ou iciando  com -
    ents_unique = [nome for nome in ents_unique if "." not in nome.split(" ")[0]]
    ents_unique = [nome for nome in ents_unique if "-" not in nome.split(" ")[0]]




    # Criar um dicionário para armazenar as entidades únicas
    dict_final = {"pessoas": ents_unique}
    
    os.remove(temp) # Remove o arquivo temporário

    return dict_final


@app.post("/pdf") 
def ner_pdf(pdf_file: UploadFile = File(...)):
    
    file_ext = pdf_file.filename.split(".").pop()
    if file_ext not in ["pdf"]:
        return "Formato de arquivo não suportado"

    doc =  fitz.open(stream=pdf_file.file.read(), filetype="pdf")

    # Extrair o texto do PDF
    conteudo = ""
    for page in doc:
        conteudo += page.get_text().replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # Fechar o arquivo temporário
    doc.close()

    # Identificar as entidades nomeadas
    document = NER(str(conteudo))

    # Criar um conjunto para armazenar as entidades únicas
    ents_unique = set()

    # Identificar todas as entidades nomeadas referentes apenas à pessoas
    for ent in document.ents:
        if ent.label_ == 'PER':
            ents_unique.add(ent.text)

    ents_unique = list(ents_unique) # Converter o conjunto para lista

    # Remover os prefixos dos nomes, tipo Sr., Sra., Dr., etc.
    prefixos = ["Sr.",
                "Sra.",
                "Dr.",
                "Dra.",
                "Prof.",
                "Profª.",
                "Profº.",
                "Vossa Excelência",
                "Conselheiro",
                "Conselheira",
                "Relator",
                "Relatora",
                "Desembargador",
                "Desembargadora",
                "Ministro",
                "Ministra",
                "Senador",
                "Senadora",
                "Deputado",
                "Deputada",
                "Vereador",
                "Vereadora",
                "Prefeito",
                "Prefeita",
                "Governador",
                "Governadora",
                "Presidente",
                "Presidenta",
                "Secretário",
                "Secretária",
                "Procurador",
                "Procuradora",
                "Promotor",
                "Promotora",
                "Juiz",
                "Juíza",
                "Desembargador",
                "Desembargadora",
                "Diretor",
                "Diretora",
                "Professor",
                "Professora"]
    for prefixo in prefixos:
        ents_unique = {nome.replace(prefixo, "").strip() for nome in ents_unique}

    # Remover nomes que não possuem sobrenome
    ents_unique = [nome for nome in ents_unique if " " in nome]

     # Remover nomes que não possuem apenas letras no nome
#    ents_unique = {nome for nome in ents_unique if nome.split(" ")[0].isalpha()}

    # Remover nomes que possuem o primeiro nome abreviado, tipo A. B. C. ou iciando  com -
    ents_unique = [nome for nome in ents_unique if "." not in nome.split(" ")[0]]
    ents_unique = [nome for nome in ents_unique if "-" not in nome.split(" ")[0]]




    # Criar um dicionário para armazenar as entidades únicas
    dict_final = {"pessoas": ents_unique}
    
    return dict_final


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
