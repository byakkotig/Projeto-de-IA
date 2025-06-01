import torch
from transformers import BertTokenizer, BertForSequenceClassification
import streamlit as st

@st.cache_resource
def carregar_modelo():
    """Carrega o modelo BERT e tokenizer com cache"""
    MODEL_NAME = 'neuralmind/bert-base-portuguese-cased'
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    return tokenizer, model

def classificar_frase(frase, tokenizer, model):
    """Classifica uma frase como 'leve' ou 'grave' usando BERT"""
    inputs = tokenizer(
        frase, 
        return_tensors="pt", 
        truncation=True, 
        max_length=512,
        padding=True
    )
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    predicao = torch.argmax(outputs.logits, dim=1).item()
    return 'leve' if predicao == 0 else 'grave'