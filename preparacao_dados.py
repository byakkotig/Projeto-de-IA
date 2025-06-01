import os
from PyPDF2 import PdfReader
from PyPDF2.errors import DependencyError

# Termos médicos e categorias
TERMOS_MEDICOS = {
    "sintomas": [
        "dor", "febre", "náusea", "vômito", "tontura", "cefaleia", "confusão",
        "fraqueza", "paralisia", "dificuldade de falar", "batimento cardíaco acelerado",
        "dor no peito", "equimose", "espasmos", "tiques", "garganta inflamada",
        "convulsões", "coceiras", "manchas vermelhas", "dificuldade de respirar",
        "erupção cutânea", "urticária", "transpiração", "dor no estômago",
        "desânimo", "cansaço", "cãibra", "boca seca", "visão borrada",
        "perda de peso", "perda de cabelo", "alucinações", "movimentos bruscos",
        "movimentos contorcidos", "degustação", "bolhas na pele", "prurido",
        "rash", "fadiga", "edema", "hemorragia", "icterícia", "parestesia",
        "vertigem", "síncope", "dispneia", "palpitação", "taquicardia",
        "hipertensão", "hipotensão", "diarreia", "constipação", "flatulência",
        "pirose", "dispepsia", "anorexia", "astenia", "mialgia", "artralgia",
        "rigidez", "tremor", "poliúria", "oligúria", "anúria", "disúria",
        "hematúria", "proteinúria", "tosse", "expectoração", "rinorreia",
        "epistaxe", "otalgia", "tinnitus", "fotofobia", "diplopia", "xerostomia",
        "gengivorragia", "glossodinia", "linfadenopatia", "hepatomegalia",
        "esplenomegalia", "ascite", "cianose", "pallor", "eritema", "petéquias",
        "púrpura", "necrose", "úlcera", "fissura", "descamação", "hiperqueratose"
    ],
    "sistemas": [
        "gastrointestinal", "respiratório", "cardiovascular", "neurológico",
        "dermatológico", "hematológico", "hepático", "renal", "endócrino",
        "musculoesquelético", "imunológico", "oftalmológico", "otorrinolaringológico",
        "geniturinário", "psiquiátrico"
    ],
    "frequencia": {
        "muito_comum": ["muito comum", "≥10%", "10%", "muito frequente"],
        "comum": ["comum", "≥1%", "1%", "frequente"],
        "incomum": ["incomum", "≥0.1%", "0.1%", "pouco frequente"],
        "raro": ["raro", "≤0.01%", "0.01%", "muito raro"]
    }
}

SINONIMOS = {
    "dor de cabeça": "cefaleia",
    "enjoo": "náusea",
    "coceira": "prurido",
    "mancha na pele": "rash",
    "cansaço": "fadiga",
    "tonturas": "vertigem",
    "desmaio": "síncope",
    "falta de ar": "dispneia",
    "azia": "pirose",
    "indigestão": "dispepsia",
    "sangramento": "hemorragia",
    "amarelecimento": "icterícia",
    "formigamento": "parestesia"
}

# Categorias de gravidade ampliadas
CATEGORIAS = {
    'leve': TERMOS_MEDICOS["frequencia"]["muito_comum"] + 
            TERMOS_MEDICOS["frequencia"]["comum"] +
            ["leve", "suave", "moderado", "transitório", "temporário", "benigno"],
    'grave': TERMOS_MEDICOS["frequencia"]["incomum"] + 
             TERMOS_MEDICOS["frequencia"]["raro"] +
             ["grave", "severa", "severos", "reação", "reações", "adversa", 
              "anafilaxia", "choque", "hospitalização", "emergência", "morte",
              "fatal", "irreversível", "crônico", "progressivo", "maligno",
              "toxicidade", "overdose", "intoxicação", "insuficiência"]
}

def extrair_texto(pdf_path):
    """Extrai texto de arquivos PDF com tratamento de erros"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            
            if reader.is_encrypted:
                try:
                    reader.decrypt('')
                except Exception:
                    return None
            
            texto = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    texto += page_text + "\n"
            return texto if texto.strip() else None
    
    except DependencyError:
        return None
    except Exception as e:
        return None

def normalizar_termos(texto):
    """Normaliza termos médicos usando a lista de sinônimos"""
    if not texto:
        return ""
        
    texto = texto.lower()
    for termo, sinonimo in SINONIMOS.items():
        texto = texto.replace(termo, sinonimo)
    return texto

def separar_secoes(texto):
    """Identifica e separa as seções relevantes das bulas"""
    texto = normalizar_termos(texto)
    secoes_relevantes = {
        'Reações Adversas': '',
        'Efeitos Colaterais': '',
        'Advertências': '',
        'Precauções': '',
        'Interações': '',
        'Contraindicações': ''
    }
    
    secao_atual = None
    linhas = texto.split('\n')
    
    for linha in linhas:
        linha_limpa = linha.strip().lower()
        
        # Identificar seções pelo título
        if 'reações adversas' in linha_limpa:
            secao_atual = 'Reações Adversas'
        elif 'efeitos colaterais' in linha_limpa:
            secao_atual = 'Efeitos Colaterais'
        # ... (demais seções)
        elif secao_atual and linha:
            secoes_relevantes[secao_atual] += linha + " "
        else:
            secao_atual = None
    
    return secoes_relevantes