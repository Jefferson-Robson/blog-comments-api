# 💬 Blog Comments API

> API leve para comentários em blog com notificação em tempo real via Telegram. Projetada para rodar em hardware modesto com deploy em contêiner Docker.

![Status](https://img.shields.io/badge/Status-Em%20Produção-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white&style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white&style=flat-square)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=flat-square)

---

## 📌 O Problema

Blogs estáticos (Jekyll, Hugo, geradores de site estático) não têm sistema de comentários nativo. Soluções como Disqus são pesadas, rastreiam usuários e custam caro. Este projeto oferece uma alternativa **leve, própria e gratuita** com menos de 300 linhas de código.

## ✅ A Solução

Uma API REST em FastAPI que:

- Recebe comentários via POST
- Retorna comentários de um post via GET
- Notifica o dono do blog **em tempo real** via Telegram quando alguém comenta
- Vem com um **widget HTML/CSS/JS** que você embarca em qualquer página com uma tag `<script>`

Tudo roda em **SQLite** — sem PostgreSQL, sem Redis, sem dependência externa além do Telegram.

---

## ⚙️ Tech Stack

| Camada | Tecnologia |
|--------|-----------|
| **API** | Python 3.11 + FastAPI |
| **ORM** | SQLAlchemy 2.0 |
| **Banco** | SQLite (leve, zero config) |
| **Notificação** | Telegram Bot API |
| **Container** | Docker (imagem slim: 130 MB) |
| **Deploy** | Docker Compose (1 serviço) |

---

## 🚀 Como Rodar Localmente

### Com Docker (recomendado)

```bash
# 1. Clone
git clone https://github.com/Jefferson-Robson/blog-comments-api.git
cd blog-comments-api

# 2. Configure o Token do Telegram (opcional — sem isso a API funciona, só não notifica)
cp .env.example .env
# Edite .env com seu TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID

# 3. Suba
docker compose up -d --build

# 4. Acesse
curl http://localhost:8000/health
```

### Sem Docker (ambiente local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data
uvicorn app.main:app --reload --port 8000
```

---

## 📡 Como Usar o Widget

No seu post HTML, adicione:

```html
<script
  src="https://seu-dominio.com/static/widget.html"
  data-post-slug="meu-post"
  data-api-base="https://seu-dominio.com"
  defer>
</script>
```

O widget carrega os comentários existentes e permite envio de novos com notificação automática no Telegram do dono.

### Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/comentarios/{post_slug}` | Lista comentários de um post |
| `POST` | `/api/comentarios/` | Cria novo comentário |
| `GET` | `/health` | Health check |

**Exemplo de POST:**

```bash
curl -X POST http://localhost:8000/api/comentarios/ \
  -H "Content-Type: application/json" \
  -d '{
    "post_slug": "meu-post",
    "autor": "Maria Silva",
    "email": "maria@email.com",
    "texto": "Artigo excelente! Me ajudou muito."
  }'
```

---

## 📁 Estrutura do Projeto

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # Rotas FastAPI
│   ├── models.py        # Modelo Comment (SQLAlchemy)
│   ├── schemas.py       # Schemas Pydantic (validação)
│   ├── database.py      # Conexão SQLite
│   └── services.py      # Notificação Telegram
├── frontend/
│   └── widget.html      # Widget embeddável HTML/CSS/JS
├── .env.example         # Template de variáveis de ambiente
├── .gitignore
├── Dockerfile
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📄 Licença

MIT © Jefferson Robson

---

*Parte do portfólio de Jefferson Robson — construindo soluções reais com infraestrutura enxuta.*