import os
import httpx

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_telegram(mensagem: str):
    """Envia mensagem via bot do Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram não configurado — notificação ignorada.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(
                url,
                json={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": mensagem,
                    "parse_mode": "HTML",
                },
            )
            print(f"Telegram: {resp.status_code}")
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")


def notificar_comentario(comment_id: int):
    """
    Busca o comentário no banco e dispara notificação no Telegram.
    Função chamada em BackgroundTasks para não travar a resposta da API.
    """
    from app.database import SessionLocal
    from app.models import Comment

    db = SessionLocal()
    try:
        c = db.query(Comment).filter(Comment.id == comment_id).first()
        if not c:
            return
        texto_curto = c.texto[:300] + ("..." if len(c.texto) > 300 else "")
        msg = (
            f"💬 <b>Novo comentário no blog</b>\n"
            f"👤 {c.autor}\n"
            f"📝 {texto_curto}\n"
            f"🔗 Post: /{c.post_slug}/"
        )
        enviar_telegram(msg)
    finally:
        db.close()