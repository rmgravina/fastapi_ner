import spacy
from fastapi import FastAPI, File, UploadFile
import uvicorn
from secrets import token_hex
import base64
import fitz

# Carregar o modelo NER ('lener' é um modelo customizado pela equipe)
NER = spacy.load('lener')

# Criar o App FastAPI
app = FastAPI(title="E-Notifica API", description="Reconhecimento de Entidades Nomeadas - NER")





# Criar função que identifica as entidades nomeadas
@app.post("/pdf")
def ner_pessoas(pdf_file: UploadFile = File(...)):

    file_ext = pdf_file.filename.split(".").pop()
    if file_ext not in ["pdf"]:
        return "Formato de arquivo não suportado"
    
    

#    conteudo = str(pdf_file.file.read().decode('utf-8').replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("__________________________", ""))
    doc =  fitz.open(stream=pdf_file.file.read(), filetype="pdf")
    conteudo = ""
    for page in doc:
        conteudo += page.get_text().replace("\n", " ").replace("\r", " ").replace("\t", " ")

    document = NER(str(conteudo))

    ents_unique = set()

    for ent in document.ents:
        if ent.label_ == 'PER':
            ents_unique.add(ent.text)

    dict_final = {"pessoas": list(ents_unique)}

    return dict_final


# broken doc
@app.post("/pdf_base64")
def ner_pessoas(pdf_file64: UploadFile = File(...)):
    temp = "./documents/output/" + token_hex(12) + ".pdf"
    base64_bytes = str(pdf_file64).encode('ascii')
    b64 = base64.b64decode(base64_bytes + b'==')
    with open(temp, "wb") as f:
        f.write(b64)
        f.close()

    doc =  fitz.open(temp, filetype="pdf")
    conteudo = ""
    for page in doc:
        conteudo += page.get_text().replace("\n", " ").replace("\r", " ").replace("\t", " ")

    document = NER(str(conteudo))

    ents_unique = set()

    for ent in document.ents:
        if ent.label_ == 'PER':
            ents_unique.add(ent.text)

    dict_final = {"pessoas": list(ents_unique)}

    return dict_final

'''

def get_pdfbase64(pdf_file64: str.encode('ascii') = File(...)):
    temp = token_hex(12) + ".pdf"
    b64 = base64.b64decode(pdf_file64)
    with open(temp, "wb") as f:
        f.write(b64)
        f.close()
    return temp

'''

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
