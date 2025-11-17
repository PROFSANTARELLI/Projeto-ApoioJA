import os
import random

# Tenta importar SDK do Gemini (pode falhar se não instalado)
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except Exception:
    HAS_GEMINI = False

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def init_gemini():
    if not GEMINI_API_KEY or not HAS_GEMINI:
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel("gemini-pro")
    except Exception:
        return None

def build_prompt(user_message, context=None):
    base = (
        "Você é um assistente empático e acolhedor para a plataforma ApoioJá.\n"
        "Responda de forma breve, empática e segura. Não dê diagnósticos ou conselhos médicos.\n\n"
    )
    if context:
        base += f"Contexto: {context}\n\n"
    base += f"Usuário: {user_message}\nResposta:"
    return base

FALLBACK_RESPONSES = [
    "Sinto muito que esteja passando por isso. Se quiser, me conte mais — estou aqui para ouvir.",
    "Se você estiver em perigo, por favor, busque um local seguro e peça ajuda imediata. Posso listar contatos de apoio.",
    "Obrigado por compartilhar. Gostaria de orientações sobre serviços de apoio ou contatos de emergência?",
    "Entendo. Deseja que eu explique como proceder para registrar essa ocorrência com segurança?"
]

def get_fallback_response():
    return random.choice(FALLBACK_RESPONSES)

def get_gemini_response(user_message, context=None):
    model = init_gemini()
    if not model:
        return None
    prompt = build_prompt(user_message, context)
    try:
        response = model.generate_content(prompt)
        # dependendo da versão do SDK, adaptar leitura do texto
        return getattr(response, "text", str(response))
    except Exception:
        return None
