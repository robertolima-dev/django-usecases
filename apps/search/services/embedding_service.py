from typing import List

from sentence_transformers import SentenceTransformer

# Carrega o modelo só uma vez na inicialização
_model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_embedding(text: str) -> List[float]:
    """
    Gera o vetor de embedding para um texto dado.
    :param text: Texto de entrada
    :return: Lista de floats representando o vetor
    """
    if not text:
        return [0.0] * 384  # Retorna vetor neutro se texto vazio

    embedding = _model.encode(text)
    return embedding.tolist()
