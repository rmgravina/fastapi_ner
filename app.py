import spacy
from fastapi import FastAPI, File, UploadFile
import uvicorn
from secrets import token_hex
import base64

# Carregar o modelo NER ('lener' é um modelo customizado pela equipe)
NER = spacy.load('lener')

# Criar o App FastAPI
app = FastAPI(title="E-Notifica API", description="Reconhecimento de Entidades Nomeadas - NER")

# Criar função que identifica as entidades nomeadas
@app.post("/")
def ner_pessoas(file_uploaded: UploadFile = File(...)):

    file_ext = file_uploaded.filename.split(".").pop()
    if file_ext not in ["pdf", "docx", "doc", "txt"]:
        return "Formato de arquivo não suportado"

    conteudo = str(file_uploaded.file.read().decode('utf-8').replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("__________________________", ""))



    document = NER(conteudo)

    ents_unique = set()

    for ent in document.ents:
        if ent.label_ == 'PER':
            ents_unique.add(ent.text)

    dict_final = {"pessoas": list(ents_unique)}

    return dict_final



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
