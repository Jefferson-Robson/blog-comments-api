from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db
from app.services import notificar_comentario

# Cria as tabelas no banco ao iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog Comments API",
    description="API leve para comentários em blog com notificação via Telegram.",
    version="1.0.0",
    contact={
        "name": "Jefferson Robson",
        "url": "https://github.com/Jefferson-Robson",
    },
)

# CORS — permite embarcar o widget em qualquer site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend estático (widget embeddável)
try:
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
except Exception:
    pass  # diretório pode não existir em dev


# ─── HEALTH CHECK ─────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "app": "blog-comments-api", "version": "1.0.0"}


# ─── COMENTÁRIOS ──────────────────────────────────────────────

@app.get("/api/comentarios/{post_slug}")
def listar_comentarios(post_slug: str, db: Session = Depends(get_db)):
    """Retorna todos os comentários de um post, ordenados por data."""
    comentarios = (
        db.query(models.Comment)
        .filter(models.Comment.post_slug == post_slug)
        .order_by(models.Comment.data_criacao)
        .all()
    )
    return [
        {
            "id": c.id,
            "autor": c.autor,
            "texto": c.texto,
            "data_criacao": c.data_criacao.strftime("%d/%m/%Y %H:%M"),
        }
        for c in comentarios
    ]


@app.post("/api/comentarios/", response_model=schemas.CommentResponse)
def criar_comentario(
    comentario: schemas.CommentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Cria um novo comentário e dispara notificação via Telegram
    em segundo plano.
    """
    db_comment = models.Comment(**comentario.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    background_tasks.add_task(notificar_comentario, db_comment.id)
    return db_comment