# Sistema de Chamados — Nexa Solutions

API REST em Django para abertura, consulta e acompanhamento de chamados de suporte, com uma interface HTML simples para consumo da API.

## Sumário

- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Configuração do ambiente (.env)](#configuração-do-ambiente-env)
- [Executando com Docker (recomendado)](#executando-com-docker-recomendado)
- [Executando localmente sem Docker](#executando-localmente-sem-docker)
- [Executando os testes](#executando-os-testes)
- [Endpoints da API](#endpoints-da-api)
- [Frontend](#frontend)
- [Problemas comuns](#problemas-comuns)

## Tecnologias

- Python 3.12
- Django 5.x
- Django REST Framework
- PostgreSQL 16 (via Docker) / SQLite (execução local sem Docker)
- django-cors-headers
- Docker e Docker Compose

## Estrutura do projeto

```text
nexa-solutions/
├── backend/            # API Django
│   ├── config/         # Configurações do projeto (settings, urls, wsgi/asgi)
│   ├── chamados/       # App principal: models, views, serializers, urls, testes
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   └── index.html      # Interface HTML simples para consumir a API
├── docs/                # Documentação complementar e demandas (issues.md)
├── .env.example         # Modelo de variáveis de ambiente
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Pré-requisitos

Escolha um dos dois caminhos abaixo:

- **Com Docker (recomendado):** Docker e Docker Compose instalados. Não é necessário instalar Python ou PostgreSQL na máquina.
- **Sem Docker:** Python 3.12+ instalado.

## Configuração do ambiente (.env)

O projeto usa variáveis de ambiente para configurações sensíveis (chave secreta do Django, credenciais do banco de dados). Nenhum valor real deve ser versionado no Git — apenas o arquivo `.env.example`, que serve de modelo.

1. Copie o arquivo de exemplo para `.env` na raiz do projeto:

   ```bash
   cp .env.example .env
   ```

2. Abra o `.env` e ajuste os valores conforme necessário. As variáveis disponíveis são:

   | Variável | Descrição | Exemplo |
   |---|---|---|
   | `DJANGO_SECRET_KEY` | Chave secreta do Django. Troque por um valor único e privado, especialmente em produção. | `troque-esta-chave-em-producao` |
   | `DEBUG` | Ativa o modo de depuração do Django (`True`/`False`). Use `False` em produção. | `True` |
   | `ALLOWED_HOSTS` | Hosts permitidos, separados por vírgula. | `localhost,127.0.0.1` |
   | `POSTGRES_DB` | Nome do banco de dados PostgreSQL. | `nexa_chamados` |
   | `POSTGRES_USER` | Usuário do PostgreSQL. | `postgres` |
   | `POSTGRES_PASSWORD` | Senha do PostgreSQL. | `postgres` |
   | `POSTGRES_HOST` | Host do banco de dados. Use `db` ao rodar via Docker Compose (nome do serviço). | `db` |
   | `POSTGRES_PORT` | Porta do PostgreSQL. | `5432` |

   > O `.env` está no `.gitignore` e nunca deve ser commitado. Se `POSTGRES_HOST` não estiver definido, o backend usa SQLite automaticamente (útil para execução local rápida, sem banco de dados externo).

## Executando com Docker (recomendado)

Com o `.env` já criado (passo anterior), na raiz do projeto:

```bash
docker compose up --build
```

Esse comando irá:

- Subir um container PostgreSQL (serviço `db`), com dados persistidos em um volume.
- Aguardar o banco ficar saudável (healthcheck) antes de iniciar a API.
- Construir a imagem da API, instalar as dependências e aplicar as migrações automaticamente (`migrate --noinput`).
- Iniciar o servidor Django em `http://localhost:8000`.

Para rodar em segundo plano:

```bash
docker compose up --build -d
```

Para parar os containers:

```bash
docker compose down
```

Para parar e também remover os dados do banco (volume):

```bash
docker compose down -v
```

## Executando localmente sem Docker

Útil para desenvolvimento rápido ou diagnóstico. Nesse modo, se `POSTGRES_HOST` não estiver definido no `.env`, o projeto usa SQLite.

```bash
cp .env.example .env      # se ainda não tiver feito
cd backend
python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

A API estará disponível em `http://localhost:8000/api/`.

Para acessar o Django Admin, crie um superusuário:

```bash
python manage.py createsuperuser
```

e acesse `http://localhost:8000/admin/`.

## Executando os testes

Com o ambiente virtual ativado (execução local) ou dentro do container da API:

```bash
cd backend
python manage.py test
```

Via Docker, é possível executar os testes dentro do container em execução:

```bash
docker compose exec api python manage.py test
```

Os testes cobrem, entre outros casos: criação válida de chamado, rejeição de cadastro sem título (com erro 400, não 500), filtro de chamados por status e o endpoint de indicadores.

## Endpoints da API

Base URL: `http://localhost:8000/api/`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/chamados/` | Lista os chamados, ordenados do mais recente para o mais antigo. Aceita filtro opcional `?status=ABERTO`, `EM_ANDAMENTO` ou `CONCLUIDO`. Um status inválido retorna `400`. |
| `POST` | `/api/chamados/` | Cria um novo chamado. Campos: `titulo` (obrigatório), `descricao` (opcional), `status` (opcional, padrão `ABERTO`). Retorna `201` em caso de sucesso ou `400` com mensagem de erro se `titulo` estiver ausente/em branco. |
| `GET` | `/api/chamados/<id>/` | Retorna os detalhes de um chamado específico. |
| `PUT` / `PATCH` | `/api/chamados/<id>/` | Atualiza total (`PUT`) ou parcialmente (`PATCH`) um chamado existente. |
| `GET` | `/api/indicadores/` | Retorna um resumo com `total`, `abertos`, `em_andamento` e `concluidos`. |
| `GET`/`POST` | `/admin/` | Django Admin, para gestão administrativa dos chamados (requer superusuário). |

### Exemplo — criar um chamado

```bash
curl -X POST http://localhost:8000/api/chamados/ \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Falha no acesso", "descricao": "Usuário não consegue entrar."}'
```

### Exemplo — listar chamados abertos

```bash
curl "http://localhost:8000/api/chamados/?status=ABERTO"
```

### Exemplo — indicadores

```bash
curl http://localhost:8000/api/indicadores/
```

```json
{
  "total": 4,
  "abertos": 2,
  "em_andamento": 1,
  "concluidos": 1
}
```

## Frontend

Uma interface HTML simples está disponível em `frontend/index.html` para listar e cadastrar chamados. Basta abrir o arquivo em um navegador com a API rodando em `http://localhost:8000` (a URL da API está configurada diretamente no arquivo, em `API_URL`).

## Problemas comuns

- **`sqlite3.OperationalError` / tabela não existe:** rode `python manage.py makemigrations chamados` seguido de `python manage.py migrate` (ao rodar via Docker Compose, as migrações já são aplicadas automaticamente na inicialização).
- **Erro de CORS ao chamar a API pelo frontend:** confirme que `corsheaders` está em `INSTALLED_APPS`, que `corsheaders.middleware.CorsMiddleware` está no topo de `MIDDLEWARE` em `config/settings.py`, e que a origem do frontend está liberada (por padrão o projeto usa `CORS_ALLOW_ALL_ORIGINS = True` em desenvolvimento).
- **`KeyError: 'DJANGO_SECRET_KEY'` ou variável de ambiente ausente:** confirme que o arquivo `.env` existe na raiz do projeto e que foi criado a partir do `.env.example`.
- **Banco de dados indisponível ao subir via Docker:** o `docker-compose.yml` já configura um healthcheck para o serviço `db`; a API só sobe depois que o banco estiver pronto. Se o erro persistir, rode `docker compose down -v` e depois `docker compose up --build` novamente.