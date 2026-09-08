# Ambiente de desenvolvimento

Referências: [decisions.md](decisions.md), [implementation-plan.md](implementation-plan.md) e [evidências da fundação](validation/foundation-2026-09-07.md).

## Estado atual

Backend FastAPI executável com endpoints de saúde, configuração validada, erros padronizados e logs estruturados. Frontend React com navegação inicial, consulta de disponibilidade, carregamento/erro e nova tentativa. Login, inventário, RBAC, auditoria e migrations ainda não estão implementados. Não existe banco de demonstração preenchido.

Compose e Dockerfiles incluem PostgreSQL, backend e frontend. Configuração estática validada; builds e execução em containers ainda não verificados porque o ambiente nega acesso ao daemon Docker, inclusive fora do sandbox. Testes da API usam banco substituído por um objeto controlado: não comprovam integração PostgreSQL.

## Ferramentas e estrutura

- Python 3.12, uv 0.12.10 e `backend/uv.lock`.
- Node.js 24, npm 11 e `frontend/package-lock.json`.
- Docker/Compose para executar os três serviços; Git local inicializado, sem commits criados.
- CI definida em `.github/workflows/ci.yml`, com jobs independentes para backend, frontend e validação estática do Compose. A execução remota depende de conectar o repositório a um provedor de CI.
- Backend em `backend/app/`, testes em `backend/tests/`; frontend em `frontend/src/`, estilos locais e testes junto dos componentes.
- Scripts de configuração/verificação em `scripts/`; imagens em `backend/Dockerfile` e `frontend/Dockerfile`; inicialização do banco em `docker/postgres/`.

Versões exatas de bibliotecas estão nos manifests/lockfiles e DEC-007. uv foi instalado somente em `.local/bin`, sem alterar o Python do sistema ou o PATH do usuário. Instalar a mesma versão pelo [instalador oficial](https://docs.astral.sh/uv/getting-started/installation/) em outro ambiente; se já estiver no PATH, usar `UV=uv python3 scripts/check.py`.

## Preparação local

Executar na raiz antes de qualquer comando `docker compose`:

```bash
python3 scripts/init-dev-env.py
.local/bin/uv sync --directory backend --frozen --cache-dir "$PWD/.local/uv-cache"
npm --prefix frontend ci --cache .local/npm-cache
docker compose config --quiet
```

Como alternativa, `scripts/compose-up.sh` executa a preparação automaticamente e depois sobe os serviços:

```bash
scripts/compose-up.sh
```

O script aceita os mesmos serviços do Compose, por exemplo `scripts/compose-up.sh db`. Se um comando `docker compose up` for executado diretamente em uma máquina nova, rode primeiro `python3 scripts/init-dev-env.py`; o Compose não cria arquivos referenciados por secrets do tipo bind automaticamente.

O script cria `.env` sem sobrescrever arquivo existente e gera duas senhas independentes em `.local/secrets/`: `postgres_password` (administrador do banco) e `app_db_password` (conexão da API). Arquivos têm permissão 0600, diretório privado e conteúdo nunca impresso. `.env`, `.local`, ambientes virtuais e node_modules são ignorados pelo Git.

Dockerfiles e scripts copiam secrets para caminhos privados com o proprietário correto dentro dos containers; não dependem de liberar o arquivo do host. A API abandona privilégios de root antes de iniciar Uvicorn. Esse fluxo ainda precisa de validação no Docker real. Não modificar permissões do socket Docker para contornar restrições do ambiente.

## Verificações executadas

```bash
python3 scripts/check.py --part backend
python3 scripts/check.py --part frontend
python3 scripts/check.py
docker compose --env-file .env.example config --quiet
```

O verificador executa Ruff, formatação, mypy e pytest no backend; ESLint, Prettier, Vitest e build TypeScript/Vite no frontend. O comando sem `--part` reúne as duas sequências e interrompe no primeiro erro. Cada processo tem timeout de 120 segundos para não deixar testes travados indefinidamente.

As duas sequências por parte foram executadas com sucesso. No sandbox desta sessão, TestClient travou na comunicação entre threads; fora do sandbox os oito testes passaram em 1,28 segundo. Não confundir a restrição com teste aprovado no sandbox. Nenhum teste de banco real foi executado. Avisos de depreciação de dependências estão registrados nas evidências.

Para formatar alterações:

```bash
backend/.venv/bin/ruff format backend
npm --prefix frontend run format
```

## Executar a aplicação em containers

Com daemon disponível e configuração preparada:

```bash
scripts/compose-up.sh
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1;"'
docker compose logs --tail=50 backend
docker compose stop
```

Instruções preparadas, ainda não executadas neste ambiente. Interface prevista em `http://127.0.0.1:8080` (APP_PORT configurável). Só o frontend publica porta, vinculada ao loopback; o proxy encaminha `/api` ao backend. Banco e API permanecem na rede interna do Compose. Acessibilidade on-premises por DNS/HTTPS será configurada antes do deploy.

`inventory_bootstrap` administra a inicialização; `inventory_app` tem somente conexão e uso do esquema neste estágio. Permissões de tabelas serão concedidas explicitamente nas migrations futuras, incluindo restrição de auditoria. O script de inicialização só roda em volume vazio; não remove dados nem altera silenciosamente um volume existente.

## Aplicar migrations

Depois que o Compose estiver saudável, reconstruir a imagem da API caso o Dockerfile tenha mudado e aplicar o esquema pelo container:

```bash
sudo docker compose build backend
sudo docker compose up -d --wait backend
sudo docker compose exec -T backend .venv/bin/alembic upgrade head
sudo docker compose exec -T backend .venv/bin/alembic current
```

O rebuild é necessário porque `alembic.ini` e `migrations/` precisam estar dentro da imagem. O primeiro comando de Alembic aplica as migrations pendentes usando `APP_DB_PASSWORD_FILE`; o segundo confirma a revisão instalada. Todos exigem acesso administrativo ao Docker para este ambiente. O bootstrap administrativo cria a extensão `pgcrypto`; a migration `0001_foundation` usa `gen_random_uuid()` e cria as tabelas iniciais de organização, usuários, roles, permissões e auditoria. Não executar downgrade em um banco com dados sem revisar o impacto. O usuário confirmou a aplicação e a revisão `0001_foundation` no banco real.

Se um volume existente retornar erro de privilégio no schema ou na extensão `pgcrypto`, execute uma vez os comandos abaixo com o usuário de inicialização e repita o upgrade:

```bash
sudo docker compose exec -T db sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "GRANT CREATE ON SCHEMA public TO inventory_app;"'
sudo docker compose exec -T db sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"'
sudo docker compose exec -T backend .venv/bin/alembic upgrade head
```

Instalações novas recebem a extensão, `USAGE` e `CREATE` pelo bootstrap. A migration apenas usa `gen_random_uuid()` e não cria privilégios elevados. Antes da produção, separar o usuário de migration do usuário de runtime e revogar `CREATE` da API após o esquema ser criado.

PostgreSQL 18 usa volume em `/var/lib/postgresql`, conforme a [imagem oficial](https://hub.docker.com/_/postgres). As imagens usam tags de linha de versão; resolver e registrar digests antes da liberação. Não trocar a versão principal nem remover volumes para corrigir falhas rotineiras. Regenerar um arquivo de senha não troca a senha de um banco já inicializado.

## Desenvolvimento sem containers

Com dependências e secrets locais preparados:

```bash
APP_DB_PASSWORD_FILE="$PWD/.local/secrets/app_db_password" .local/bin/uv run --directory backend --frozen uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000 --no-access-log
```

Em outro terminal:

```bash
npm --prefix frontend run dev
```

Fluxo de inicialização manual preparado; execução dos processos HTTP ainda não foi verificada. Vite encaminha `/api` para `127.0.0.1:8000`. A API requer uma fonte de senha mesmo para inicialização. `/api/health/live` responde enquanto o processo está ativo; `/api/health/ready` só retorna 200 após `SELECT 1`, ou 503 sem detalhes internos se o banco estiver inacessível. Sem PostgreSQL local, a UI deve mostrar indisponibilidade.

Para conexão a PostgreSQL já disponível, configurar `APP_DB_HOST`, `APP_DB_PORT`, `APP_DB_NAME`, `APP_DB_USER` e exatamente uma fonte entre `APP_DB_PASSWORD_FILE` e `APP_DB_PASSWORD`. Não inserir valores reais em arquivos versionados. Documentação OpenAPI: `/api/docs` e `/api/openapi.json` apenas fora de `APP_ENVIRONMENT=production`.

## Pendências

Acesso administrativo ao daemon, aplicação/verificação das migrations, CI remota e reprodução completa em ambiente limpo seguem pendentes no plano. A prontidão HTTP e a execução dos containers foram confirmadas pelo usuário; inspeção administrativa via Docker neste shell exige senha sudo. O destino on-premises está confirmado; características do servidor, DNS/TLS, retenção e responsáveis operacionais ainda serão levantados. Não há implantação em produção autorizada ou realizada.
