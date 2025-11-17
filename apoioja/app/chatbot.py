import google.generativeai as genai
import os

# Obtém a chave da API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configura o Gemini somente se houver chave
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️ AVISO: GEMINI_API_KEY não configurada. O chatbot usará fallback.")

# -----------------------------
# RESPOSTA PRINCIPAL DO CHATBOT
# -----------------------------
def get_gemini_response(message: str) -> str:
    """Retorna resposta da IA Gemini"""
    if not GEMINI_API_KEY:
        return get_fallback_response(message)

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(message)
        return response.text
    except Exception:
        return get_fallback_response(message)


# -----------------------------
# FUNÇÃO DE FALLBACK (SEM IA)
# -----------------------------
def get_fallback_response(message: str) -> str:
    """Resposta padrão quando a IA falha ou não existe chave"""
    return (
        "Estou aqui para ajudar. "
        "Se você está em situação de risco imediato, ligue para 190. "
        "Sua segurança é prioridade."
    )
