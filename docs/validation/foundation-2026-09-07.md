# Evidências — Fundação em 07/09/2026

Itens relacionados: E0-02, E0-05, E1-01, E1-02, E1-03, E1-06 e E1-07 de [implementation-plan.md](../implementation-plan.md).

## Verificações concluídas

- [x] VAL-01 — Dependências instaladas em ambiente isolado: uv 0.12.10, Python 3.12.3 e Node 24.13.0; manifests com versões diretas exatas e lockfiles gerados.
- [x] VAL-02 — `python3 scripts/check.py --part backend`: Ruff, formatação e mypy aprovados; pytest com 8 testes aprovados fora do sandbox.
- [x] VAL-03 — `python3 scripts/check.py --part frontend`: ESLint, Prettier, 2 testes Vitest e build TypeScript/Vite aprovados.
- [x] VAL-04 — `docker compose --env-file .env.example config --quiet`: configuração dos três serviços aprovada estaticamente.
- [x] VAL-05 — Scripts shell passaram em `sh -n`; bootstrap Python compilou sem erro.
- [x] VAL-06 — Git local inicializado; configuração e arquivos gerados protegidos por .gitignore, sem commit criado.

## Cobertura observada

Backend: processo vivo com banco indisponível; prontidão positiva/negativa com probe controlado; fechamento de recurso; erro interno sanitizado; validação sem repetir entrada sensível; request_id inválido substituído; 404 padronizado; fonte de senha obrigatória/exclusiva; documentação desabilitada em produção; formatter de log sem campos sensíveis arbitrários.

Frontend: carregamento, falha de consulta, nova tentativa com recuperação e resposta inesperada sem indicar disponibilidade. A interface informa que o acesso ainda está em preparação e não oferece login fictício.

Esses testes verificam a fundação; não comprovam autenticação, autorização, auditoria nem acesso a PostgreSQL real. Ainda não houve inspeção visual em navegador real ou ensaio de acessibilidade completo.

## Limitações e resultados não aprovados

- TestClient travou dentro do sandbox; diagnóstico mostrou espera entre threads e event loop. A mesma suíte passou fora do sandbox. A primeira execução foi interrompida, não contabilizada como sucesso.
- Docker info retornou acesso negado ao socket, mesmo fora do sandbox. Não houve download/build das imagens, inicialização do banco, teste dos scripts de usuário/secret dentro dos containers nem preservação de dados após reinício.
- Duas depreciações emitidas pelas dependências: Starlette recomenda httpx2 em lugar de httpx e usa um alias BlockingPortal em depreciação. Não houve falha de teste; acompanhar na evolução das dependências, sem suprimir avisos.
- A migration `0001_foundation` foi criada e sua aplicação/verificação no PostgreSQL real foi confirmada pelo usuário. CI remota, login e jornada de inventário ainda não foram concluídos. A primeira tentativa no container falhou porque a imagem anterior não incluía `alembic.ini`/`migrations`; o Dockerfile foi corrigido e exigiu rebuild.
- A primeira aplicação alcançou o PostgreSQL, mas falhou com `permission denied for schema public`: o bootstrap concedia apenas `USAGE`. O script foi corrigido para conceder `CREATE` em instalações novas; o volume existente precisa do `GRANT` administrativo documentado antes da reaplicação.
- Após a concessão do schema, a migration revelou que `pgcrypto` também exige privilégio de criação no banco. A extensão foi removida da migration de runtime e movida para o bootstrap administrativo; o volume existente precisa do comando `CREATE EXTENSION` documentado.
- Imagens ainda usam tags de versão sem digest. Esse limite deve ser resolvido na validação da implantação.

## Próxima evidência necessária

Banco real saudável com role de aplicação, aplicação/verificação das migrations e leitura persistida após reinício. Depois, testes de integração da identidade/auditoria. A inspeção administrativa depende de `sudo docker`; o bloqueio de senha do sudo não impede continuar o código e testes isolados.
