import nltk
nltk.download('punkt')  # Garante que o tokenizer de frases está disponível

from textblob import TextBlob
from spellchecker import SpellChecker

def grade_ufrgs(texto, tema_keywords):
    detalhes_expressao = {}
    blob = TextBlob(texto)
    n_frases = len(blob.sentences)
    n_palavras = len(blob.words)
    detalhes_expressao['n_frases'] = n_frases
    detalhes_expressao['n_palavras'] = n_palavras

    # Expressão (0-50) proporcional
    media_ideal = 16  # média ideal de palavras por frase
    media_palavras = n_palavras / n_frases if n_frases > 0 else 1
    expressao_total_50 = min((media_palavras / media_ideal) * 50, 50)

    # Estrutura & Conteúdo (0-50) proporcional
    contagem_keywords = sum(texto.lower().count(k.lower()) for k in tema_keywords)
    detalhes_estrutura_conteudo = {'palavras_chave_achadas': contagem_keywords}
    total_keywords = len(tema_keywords) if len(tema_keywords) > 0 else 1
    estrutura_conteudo_total_50 = min((contagem_keywords / total_keywords) * 50, 50)

    # Total
    total_100 = expressao_total_50 + estrutura_conteudo_total_50
    total_escala_25 = round(total_100 * 25 / 100, 2)

    return {
        'expressao_total_50': round(expressao_total_50, 2),
        'estrutura_conteudo_total_50': round(estrutura_conteudo_total_50, 2),
        'total_100': round(total_100, 2),
        'total_escala_25': total_escala_25,
        'detalhes_expressao': detalhes_expressao,
        'detalhes_estrutura_conteudo': detalhes_estrutura_conteudo
    }

def detectar_erros(texto):
    erros = []
    spell = SpellChecker(language='pt')
    palavras = texto.split()
    for palavra in palavras:
        p = palavra.strip('.,;:!?()[]{}\"')
        if p and p.lower() not in spell:
            erros.append(f"Possível erro de ortografia: '{palavra}'")

    if "os jovem" in texto or "a jovem" in texto or "os menino" in texto:
        erros.append("Possível erro de concordância: revise plural/singular")

    frases = texto.split(".")
    for f in frases:
        if len(f.split()) > 30:
            erros.append(f"Frase muito longa (mais de 30 palavras): '{f.strip()[:50]}...'")

    return erros
