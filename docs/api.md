# Especificação da API REST

Base: [spec.md](spec.md), especialmente §§5, 42, 44–46 e 49. Complementos: [architecture.md](architecture.md), [db.md](db.md), [ui.md](ui.md).

Os endpoints conceituais do §42 são preservados. Contratos adicionais, nomes de campos, códigos de erro e políticas abaixo são propostas de detalhamento para implementação. A API ainda não está implementada. Gerar OpenAPI a partir dos schemas e verificar compatibilidade durante o desenvolvimento.

## 1. Convenções de contrato

- Base `/api`; JSON UTF-8; nomes `snake_case`; enums sem acentos conforme [db.md](db.md).
- UUIDs em rotas e relações; código AUT-000001 para exibição/busca, sem substituir a PK.
- Instantes ISO 8601 com offset, retornados em UTC (`2026-09-07T12:00:00Z`); datas civis `YYYY-MM-DD`.
- Recursos individuais retornam objeto direto; listas retornam `{items, page, page_size, total}`. Página inicial 1, tamanho padrão 25, máximo 100.
- Ordenação `sort=name,-created_at`; desempate por id. Lista permitida por endpoint; campo inválido retorna 422.
- Filtros distintos combinam com AND; valores repetidos do mesmo filtro combinam com OR. `q` é busca textual, sem aceitar SQL ou expressões arbitrárias.
- POST criado: 201 + Location; GET/PATCH/PUT: 200; DELETE lógico ou remoção de vínculo: 204; job de exportação: 202.
- Payloads rejeitam campos desconhecidos e somente de leitura. PATCH aceita objeto parcial, não JSON Patch; ausência preserva campo e null só limpa campo opcional.
- PUT substitui todos os campos editáveis do recurso e exige permissão sobre todos eles; não altera metadados do servidor nem coleções filhas. Responsáveis com edição parcial usam PATCH.
- Limites propostos: descrições 10.000 caracteres; URL 2.048; listas de IDs até 100 por requisição; arquivo exportado limitado por política operacional.
- Links externos usam HTTPS e não podem conter usuário/senha. Exceções corporativas de esquema/host devem ser configuradas explicitamente. O backend não visita URLs cadastradas.

## 2. Identidade, autorização e escopos

Decisão do usuário: e-mail/senha locais no MVP, SSO corporativo posteriormente (DEC-003). Usar sessão de backend com cookie HttpOnly/SameSite e Secure em HTTPS, proteção CSRF em mutações e frontend/API sob a mesma origem. O navegador não persiste tokens em localStorage.

| Método e rota | Contrato inicial |
| --- | --- |
| GET /api/auth/csrf | Emite desafio CSRF vinculado à sessão anônima/autenticada; não autentica usuário |
| POST /api/auth/login | email, password; valida CSRF/origem, limita tentativas, troca sessão após sucesso e retorna usuário/capabilities |
| POST /api/auth/logout | Revoga sessão atual e limpa cookie; exige CSRF |
| GET /api/me | Identidade local, permissões e escopos; nunca hash/senha/token de sessão |
| POST /api/auth/change-password | current_password, new_password; requer sessão, CSRF e confirmação da senha atual; revoga sessões e exige novo login |
| POST /api/users/{id}/password-reset | Admin emite token de recuperação com prazo/uso único e motivo; entrega controlada, sem logs do token |
| POST /api/auth/reset-password | token, new_password; valida token, proteção CSRF/origem e limites; consome token atomicamente e revoga sessões |

Sem cadastro público. Administrador cria usuários e inicia provisionamento de acesso; primeiro administrador é criado por comando administrativo com entrada protegida. Não usar senha fixa no seed. Hash Argon2id é persistido separadamente dos dados de usuário e nunca aparece em API/auditoria. Login inválido/inativo retorna a mesma mensagem genérica; limitação retorna 429. Recuperação não presume envio de e-mail integrado; detalhar o procedimento administrativo e validade na E2 antes de expor endpoints.

SSO futuro adiciona rotas próprias de início/callback e vínculo verificado de identidade externa, preservando UUIDs e RBAC. Não associar contas automaticamente apenas pelo e-mail. Contas de integração ficam para contratos futuros. Não disponibilizar autenticação simulada ou bypass em produção.

### Matriz inicial

A matriz detalha os perfis do §5. O usuário confirmou consulta a todas as áreas para gestor e auditor (DEC-005 em [decisions.md](decisions.md)); edição do gestor continua restrita às áreas atribuídas e auditor permanece somente leitura. Concessões são cumulativas, sempre respeitando os escopos correspondentes. Administrador tem acesso a todos os registros, mas não pode violar invariantes ou editar AuditLog.

| Ação | Administrador | Gestor | Técnico | Negócio | Auditor/Consulta |
| --- | --- | --- | --- | --- | --- |
| Consultar inventário | Todos | Todos | Owner técnico ou backup | Owner de negócio ou processos atribuídos | Todos |
| Criar automação | Qualquer área | Áreas atribuídas | Não | Não | Não |
| Editar informações gerais/status/owners | Todos | Áreas atribuídas | Não | Não | Não |
| Editar informações técnicas | Todos | Áreas atribuídas | Automações atribuídas | Não | Não |
| Editar informações de negócio | Todos | Áreas atribuídas | Não | Processos/automações atribuídos | Não |
| Dependências, versões, documentos | Todos | Áreas atribuídas | Automações atribuídas | Consulta | Consulta |
| Execuções e incidentes | Todos | Áreas atribuídas | Automações atribuídas | Consulta | Consulta |
| Avaliação manual de risco | Todos | Áreas atribuídas | Consulta | Consulta | Consulta |
| Validar processo/criticidade | Todos | Áreas atribuídas | Não | Processos/automações atribuídos | Não |
| Registrar revisão/participação | Todos | Áreas atribuídas | Automações atribuídas | Processos/automações atribuídos | Não |
| Concluir revisão | Todos | Áreas atribuídas | Não | Processos/automações atribuídos | Não |
| Excluir/restaurar logicamente | Sim | Não | Não | Não | Não |
| Histórico de alterações | Todos | No escopo de consulta | No escopo de consulta | No escopo de consulta | Todos |
| Auditoria completa | Sim | Não | Não | Não | Sim |
| Exportar | Todos | No escopo de consulta | Não por padrão | Não por padrão | Todos |
| Gerenciar cadastros, usuários e parâmetros | Sim | Não | Não | Não | Não |

Permissões mínimas do spec: `automation.read/create/update/delete/approve/export`, `audit.read`, `admin.manage`. Complementar com `automation.restore`, `automation.update.business`, `automation.update.technical`, `dependency.manage`, `version.manage`, `document.manage`, `execution.create`, `incident.manage`, `review.create`, `review.complete`, `risk.manage` e `history.read`. Seeds traduzem a matriz em roles/permissões; nunca comparar somente o nome da role no service.

Grupos editáveis: negócio = objective, business_process_id, sla, frequency, trigger e notes; técnico = environment, repository_url, monitoring_url, tecnologias, credenciais, data_classification, contains_sensitive_data, data_categories, data_retention e data_source; geral = name, description, department_id, status, criticality, owners, team_id, entry_date e categorias. Referências de credenciais são visíveis apenas a quem pode editar informações técnicas ou auditar, por proposta de minimização. Classificação e indicador de dados sensíveis permanecem visíveis no escopo de consulta; dados executivos não revelam caminhos de credenciais.

Mudança de processo por responsável de negócio só pode usar processo autorizado da mesma área. Alteração de área, com processo/equipe correspondentes, exige permissão sobre origem e destino. `automation.approve` permite validar processo/criticidade, não aprovar desenvolvimento nem ignorar requisitos de backup.

Verificar autorização antes de retornar totais, metadados ou destinos. Recurso inexistente ou fora do escopo: 404; ação proibida em recurso visível: 403. Histórico resumido omite campos técnicos restritos; auditoria completa requer audit.read. Coleções relacionadas não ampliam permissões sobre o destino.

## 3. Concorrência, auditoria e erros

Recursos mutáveis retornam `ETag: "<revision>"`. PUT/PATCH/DELETE exigem `If-Match`; ausente: 428; desatualizado: 412. Mutações nas coleções de uma automação usam a revisão do pai e incrementam essa revisão, exceto inserção independente de execução/incidente, que não deve conflitar com edição cadastral. Atualização de incidente usa sua própria revisão.

Alterações de status, criticidade, owners, versão atual, relações, permissões, política e exclusão/restauração exigem `change_reason` ou `X-Change-Reason` quando não houver corpo. O motivo não é coluna genérica editável da automação: integra o comando e a auditoria. Auditoria é transacional, incluindo valores anteriores/novos e ator autenticado.

Formato de erro proposto:

```json
{
  "error": {
    "code": "BACKUP_OWNER_REQUIRED",
    "message": "Informe um responsável substituto para criticidade alta ou crítica.",
    "details": [{"field": "backup_owner_id", "rule": "required_for_criticality"}],
    "request_id": "req-demo-001"
  }
}
```

| HTTP | Uso / códigos de domínio exemplificativos |
| --- | --- |
| 400 | JSON inválido |
| 401 | Sessão ausente/expirada |
| 403 | FORBIDDEN, FIELD_FORBIDDEN |
| 404 | NOT_FOUND, inclusive recursos fora do escopo |
| 409 | DUPLICATE_VERSION, DUPLICATE_DEPENDENCY, ACTIVE_DEPENDENTS, RESOURCE_IN_USE |
| 412 | REVISION_CONFLICT |
| 422 | VALIDATION_ERROR, OWNER_INACTIVE, BACKUP_OWNER_REQUIRED, INVALID_DEPENDENCY, INVALID_DATE_RANGE |
| 428 | PRECONDITION_REQUIRED |
| 429 | Limite de requisições excedido, se habilitado |
| 500 | INTERNAL_ERROR sem stack trace/dados internos |

POSTs humanos não são repetidos automaticamente após timeout: consultar resultado antes de reenviar. A unicidade de versão/dependência evita duplicação desses recursos. Ingestão externa futura exige chave idempotente/external_id; não prometer idempotência geral de POST no MVP.

## 4. Inventário

| Método e rota | Contrato |
| --- | --- |
| GET /api/automations | Lista paginada e filtrada no escopo |
| POST /api/automations | Cadastro atômico com initial_version, owners e revisão inicial |
| GET /api/automations/{id} | Dados, relações resumidas, revision, indicadores e capabilities |
| PUT /api/automations/{id} | Substitui campos cadastrais editáveis |
| PATCH /api/automations/{id} | Atualiza campos autorizados, valida estado final |
| DELETE /api/automations/{id} | Soft delete; X-Change-Reason obrigatório; nunca remove histórico |
| POST /api/automations/{id}/restore | Admin restaura visibilidade, corpo change_reason; valida invariantes atuais |
| GET /api/automations/{id}/history | Histórico resumido sanitizado, paginado |

`include_deleted=true` apenas para admin/auditor; detalhe excluído exige esse parâmetro e permissão. DELETE repetido com revisão atual pode retornar 204 sem novo evento; com revisão antiga retorna 412. Admin pode corrigir campos de registro excluído com PATCH e `include_deleted=true`, com motivo e If-Match, para sanar pendências antes de restaurar; isso não remove deleted_at. DESCONTINUADA é atualizada por PATCH e permanece nas listagens normais. Se houver dependentes, DELETE retorna 409 com contagem autorizada; admin pode reenviar com `acknowledge_dependents=true` e motivo, mantendo relações históricas.

Filtros: `q`, `department_id`, `business_process_id` (processo exato; `include_subprocesses=true` expande descendentes), `status`, `criticality`, `owner_id` (qualquer owner), `business_owner_id`, `technical_owner_id`, `team_id`, `system_id`, `dependency_component_id`, `data_classification`, `technology_id`, `version`, `health`, `risk_level`, `review_status`, `orphan`, `without_documentation`, `without_dependencies`, `contains_sensitive_data`, `last_execution_from`, `last_execution_to`, `never_executed`, `unused_days`, `governance_issue` (ORPHAN, DOCUMENTATION, DEPENDENCIES_MAPPING, SYSTEMS_MAPPING, BACKUP_OWNER, REVIEW_OVERDUE, REVIEW_MISSING, DATA_CLASSIFICATION_MISSING). Intervalos de timestamp usam início inclusivo/fim exclusivo. Filtros health/risk/review seguem cálculos centrais, nunca cálculo distinto no frontend.

Ordenações iniciais: code, name, created_at, updated_at, criticality (ordem de domínio), status, next_review_date, last_execution_at. Resumo de listagem contém id, code, name, department, business_owner, technical_owner, criticality, status, health, current_version, risk e revision.

### Exemplo de cadastro

UUIDs abaixo são ilustrativos e precisam corresponder a cadastros existentes no ambiente.

```json
{
  "name": "Faturamento Diário",
  "description": "Consolida os dados de faturamento do dia anterior.",
  "objective": "Disponibilizar a consolidação para a equipe financeira.",
  "business_process_id": "10000000-0000-4000-8000-000000000001",
  "department_id": "20000000-0000-4000-8000-000000000001",
  "status": "ATIVA",
  "environment": "PRODUCAO",
  "criticality": "CRITICA",
  "data_classification": "CONFIDENCIAL",
  "frequency": "Diária",
  "trigger": "Agendamento no orquestrador externo",
  "business_owner_id": "30000000-0000-4000-8000-000000000001",
  "technical_owner_id": "30000000-0000-4000-8000-000000000002",
  "backup_owner_id": "30000000-0000-4000-8000-000000000003",
  "team_id": "40000000-0000-4000-8000-000000000001",
  "entry_date": "2026-09-07",
  "contains_sensitive_data": false,
  "data_categories": ["Faturamento"],
  "initial_version": {
    "version": "2.1",
    "release_date": "2026-09-01",
    "responsible_id": "30000000-0000-4000-8000-000000000002",
    "description": "Versão já implantada em produção.",
    "change_reason": "Registro inicial do ativo existente"
  }
}
```

Retorno 201: representação completa de GET individual com id/code gerados, `current_version: "2.1"`, next_review_date calculada, timestamps, revision=1 e indicadores sem observações como null/SEM_DADOS. Campos opcionais e limites correspondem ao dicionário de [db.md](db.md). Não aceitar current_version_id diretamente no cadastro/edição genérica.

## 5. Dependências, sistemas e impacto

| Método e rota | Entrada/saída |
| --- | --- |
| GET /api/automations/{id}/dependencies | Relações diretas: id, component, criticality, mandatory, description |
| POST /api/automations/{id}/dependencies | dependency_component_id, criticality, mandatory, description, change_reason |
| PATCH /api/automations/{id}/dependencies/{dependencyId} | Altera criticality/mandatory/description e exige motivo |
| DELETE /api/automations/{id}/dependencies/{dependencyId} | Remove vínculo com auditoria e motivo |
| GET /api/automations/{id}/dependents | Automações que dependem diretamente desta |
| GET /api/automations/{id}/dependency-graph | nodes/edges diretos nos dois sentidos, escopo filtrado |
| GET /api/dependency-components/{id}/impact | Automações diretamente dependentes e contagens por criticidade |
| GET /api/automations/{id}/systems | Sistemas participantes |
| POST /api/automations/{id}/systems | system_id, purpose, change_reason |
| DELETE /api/automations/{id}/systems/{systemId} | Remove participação se não houver dependência vigente |
| GET /api/systems/{id}/impact | Mesmo contrato de impacto direto, para o componente do sistema |

Direção canônica da aresta: `source` = automação dependente; `target` = componente do qual depende. A UI traduz como “Depende de” e “Dependem desta”, sem inferir fluxo de execução. Nodes contêm id, kind, label e estado; edges contêm id, source, target, mandatory e criticality. Limite proposto de 200 nós por resposta, com `truncated` e links para listas paginadas. Nenhum nó ou contagem oculta pode vazar pelo grafo.

Impacto inclui dependências opcionais e obrigatórias, distinguindo mandatory; é potencial, não garantia de indisponibilidade. Query `mandatory=true` restringe a análise. Retorno `{component, depth:1, counts_by_criticality, items, page, page_size, total, as_of}`. Profundidade maior que 1 é rejeitada no MVP. Incluir DESCONTINUADA mediante filtro explícito na análise operacional.

## 6. Versões, execuções e incidentes

| Método e rota | Regras |
| --- | --- |
| GET /api/automations/{id}/versions | Lista versões e is_current, sem ordenar numericamente o rótulo |
| POST /api/automations/{id}/versions | version, release_date, responsible_id, description, change_reason, impact?, documentation_url?, make_current=false |
| POST /api/automations/{id}/versions/{versionId}/activate | Torna versão existente atual; change_reason obrigatório; não executa deploy |
| GET /api/automations/{id}/executions | Lista; filtros status, started_from, started_to, source |
| POST /api/automations/{id}/executions | started_at, finished_at, status, error_code?, error_message?, records_processed?; source=MANUAL e duration_ms calculados |
| GET /api/automations/{id}/incidents | Lista; filtros status/severity e período |
| POST /api/automations/{id}/incidents | title, description, severity, started_at, ticket_reference?; status inicial ABERTO |
| PATCH /api/automations/{id}/incidents/{incidentId} | Atualiza dados/estado; RESOLVIDO exige resolved_at/resolution; motivo em transição |

Não há DELETE/edição de execução ou versão histórica no MVP. Identificador filho deve pertencer à automação da rota. Registro manual de execução recebe 201 com id, duration_ms e source, nunca comando para executar código. Transições propostas de incidente: ABERTO → EM_TRATAMENTO/RESOLVIDO/CANCELADO; EM_TRATAMENTO → RESOLVIDO/CANCELADO; RESOLVIDO/CANCELADO → ABERTO com motivo. Reabertura limpa data de resolução atual e mantém histórico.

## 7. Documentação, revisões e risco

| Método e rota | Regras |
| --- | --- |
| GET/POST /api/automations/{id}/documents | Listar/criar referência: type, title, url, description? |
| PATCH /api/automations/{id}/documents/{documentId} | Corrigir metadados ou arquivar com is_active=false e motivo |
| GET /api/automations/{id}/governance | Score, itens, evidências, pendências, revisão e política aplicada |
| PATCH /api/automations/{id}/mapping | dependencies_mapping_status, systems_mapping_status, mapping_justification, change_reason; permissão dependency.manage |
| GET/POST /api/automations/{id}/reviews | Listar/registrar: reviewed_on, result, notes?, participant_ids; checklist calculado no servidor |
| POST /api/automations/{id}/validations | field=criticality/business_process_id, value, change_reason; exige automation.approve |
| GET/POST /api/automations/{id}/risk-assessments | Listar/criar: impact, probability, exposure, justification; score/level/policy calculados |
| GET /api/governance/policy | Política vigente, sem segredos |
| POST /api/governance/policies | Admin cria nova versão validada e auditada |

CONCLUIDA exige review.complete; PENDENTE_CORRECAO exige review.create e não renova prazo. Não permite cliente forjar percentual nem passar checklist satisfeito sem evidência. Validar item informado contra os dados atuais e guardar snapshot. Na conclusão, próxima revisão = reviewed_on + periodicidade. Alteração de criticidade recalcula prazo a partir da última revisão ou entrada, sem prorrogar automaticamente um prazo anterior mais curto; nova revisão pode defini-lo conforme a política vigente.

Validação confirma o valor atual: se value divergir, retornar 409 e solicitar atualização da tela. Não muda criticidade/processo através desse endpoint. Evidência fica desatualizada após mudança do campo.

## 8. Cadastros auxiliares

Para `companies`, `departments`, `business-processes`, `users`, `teams`, `systems`, `dependency-types`, `dependency-components`, `credential-references`, `technologies` e `categories`: `GET /api/{resource}`, `GET /api/{resource}/{id}`, `POST /api/{resource}`, `PATCH /api/{resource}/{id}`. Campos seguem [db.md](db.md); criação/edição exigem admin.manage. Consultas para seletores retornam somente dados necessários e autorizados; usuário não administrador não recebe roles/identificadores de identidade de outras pessoas.

Inativação usa PATCH is_active=false, ou status no cadastro System; sem DELETE físico. Inativar owner/equipe retorna contagem de automações afetadas e exige confirmação/motivo explícitos quando houver vínculos. Isso não remove FKs, e as automações afetadas passam a aparecer como órfãs.

Membros de equipe: `GET/PUT /api/teams/{id}/members` com user_ids. Referências da automação: `GET/PUT /api/automations/{id}/credential-references`, `/technologies` e `/categories`, com listas de IDs e motivo; PUT substitui a coleção atomicamente, sob permissões de edição técnica ou geral correspondentes.

RBAC: `GET/POST /api/roles`, `PATCH /api/roles/{id}`, `GET /api/permissions`, `PUT /api/roles/{id}/permissions`, `PUT /api/users/{id}/roles`, `PUT /api/users/{id}/scopes`. Mutação administrativa com motivo, concorrência e auditoria. Impedir remover/inativar o último administrador ativo. Não aceitar permissões arbitrárias inexistentes no catálogo.

## 9. Dashboards, auditoria e relatórios

`GET /api/dashboards/executive`, `/operations`, `/governance`: filtros compartilhados de inventário, janela `from`/`to` e resposta com `as_of`, `timezone`, `population`, `policy_version`, `metrics`. Consultas aplicam o mesmo escopo dos recursos; gráficos são agregados dos registros visíveis.

Executivo: totais por status/criticidade, pendências, saúde e risco incluindo SEM_AVALIACAO. Operação: execuções hoje/7 dias, taxa de sucesso, erros, média, falhas consecutivas, sem utilização e incidentes abertos. Governança: órfãs, documentação, revisão, backup, sensíveis, alto risco e dependências pendentes. Cada métrica inclui filtros ou link para detalhamento reproduzível. Fórmulas em [architecture.md](architecture.md).

`GET /api/audit-logs`: filtros entity_type, entity_id, user_id, action, from, to; ordenação por timestamp/id; exige audit.read. `GET /api/automations/{id}/audit` aplica adicionalmente o vínculo com a automação, incluindo alterações de filhos.

| Método e rota | Contrato de exportação |
| --- | --- |
| POST /api/exports | report_type, format e filters; 202 com id/status |
| GET /api/exports/{id} | Estado, created_at, expires_at, erro sanitizado e download disponível |
| GET /api/exports/{id}/download | Arquivo privado após revalidar autorização e validade; 409 se ainda não concluído; 410 se expirado |

Tipos: INVENTORY, CRITICAL_AUTOMATIONS, BY_DEPARTMENT, BY_OWNER, DEPENDENCIES, RISKS, AUDIT, VERSIONS, INCIDENTS, EXECUTIONS, GOVERNANCE. Formatos CSV, XLSX, PDF. AUDIT exige audit.read além de exportação. Job só pode ser consultado/baixado pelo solicitante ou admin autorizado; perda de escopo invalida artefato e exige nova geração. Worker usa a mesma política de acesso sem salvar tokens.

CSV/XLSX devem neutralizar interpretação de células como fórmulas; PDF deve escapar conteúdo textual. Informar filtros, geração e autor; não exportar segredos/referências restritas por padrão. Arquivos expiram segundo configuração (proposta inicial: 24 horas). Para reproduzir o recorte, gerar cada relatório sobre leitura consistente do banco e registrar o instante da coleta.

## 10. Aceite dos contratos

Validar por integração: criação válida/422, autorização por campo/escopo, UUID filho de outra automação, auditoria em mutações, conflito If-Match, soft delete e restauração, promoção de versão, dependência crítica obrigatória, revisão concluída versus pendente, indicadores sem dados e exportação com acesso revogado. OpenAPI deve conter schemas completos de todos os endpoints implementados e exemplos de sucesso/erro; tabela de rotas não substitui essa validação.

Baseline de governança para implementação: DEC-008 em [decisions.md](decisions.md), com fórmulas e limites definidos na arquitetura. Valores configuráveis não equivalem a política corporativa já homologada.
