# Plano de implementação e acompanhamento

Base funcional: [spec.md](spec.md), versão 1.0. Referências técnicas: [architecture.md](architecture.md), [db.md](db.md), [api.md](api.md) e [ui.md](ui.md).

Criado em: 07/09/2026. Última atualização: 07/09/2026.

Estado atual: fundação local implementada e verificada; E0 com versões e políticas consolidadas. E1-04 foi validado pelo ambiente em execução; migrations ainda precisam ser aplicadas ao banco.

## 1. Objetivo e limites

Entregar uma plataforma de inventário, governança e acompanhamento operacional de automações existentes, com controle de acesso, histórico e auditoria. O primeiro resultado executável será a jornada **Login → Cadastro com versão inicial → Listagem → Detalhe → Edição → Histórico**.

A plataforma registra versões e resultados de execuções realizadas externamente. Não desenvolver editor de código, execução de automações, pipeline de automações ou integrações completas no MVP. Testes e automação de entrega da própria plataforma fazem parte de sua qualidade de engenharia.

O MVP inclui P0 e os recursos P1 necessários aos critérios dos §§50 e 59 do spec: documentação, revisões, governança, identificação de inatividade e exportação. Este plano também contempla operação, saúde, incidentes e os três dashboards definidos nos documentos. P2 permanece separado do aceite do MVP.

## 2. Regra obrigatória para todos os planos

Este documento é a fonte central de acompanhamento. Todo plano futuro de etapa, sprint, módulo, teste ou implantação deverá conter checklist com identificadores estáveis, critérios de conclusão, dependências e evidências. Planos adicionais ficam em `docs/` e devem ser vinculados ao item correspondente deste plano.

Usar somente a sintaxe Markdown:

- `[ ]`: trabalho pendente, em andamento ou bloqueado; descrever o estado ao lado quando necessário.
- `[x]`: trabalho concluído e verificado, com evidência registrada.

Não marcar parcialmente um item. Quando o escopo for grande, dividi-lo em itens rastreáveis antes de executá-lo. Um teste apenas escrito não conta como teste aprovado; código criado não equivale a funcionalidade validada. Bloqueio mantém a caixa desmarcada e registra causa, impacto e condição de desbloqueio.

### Rotina de atualização e apresentação

1. No início de cada ciclo de trabalho, consultar o plano, identificar os IDs em execução e apresentar o recorte que será tratado.
2. Durante o trabalho, comunicar conclusões, falhas relevantes e mudanças de direção. Não apresentar o plano inteiro a cada atualização.
3. Após verificar uma entrega, marcar os itens correspondentes e registrar data, arquivos/artefatos, comandos de validação e resultado real.
4. Ao encerrar o ciclo, atualizar painel, histórico e próximo passo no próprio arquivo. Apresentar ao usuário os itens concluídos, os pendentes relevantes, testes executados e eventuais bloqueios.
5. Se houver regressão ou mudança que invalide o aceite, reabrir o item, preservar a evidência histórica e explicar o motivo.
6. Revisões de escopo devem registrar itens incluídos, substituídos ou retirados e sua justificativa; não marcar como concluído um trabalho cancelado.

O progresso quantitativo é `itens concluídos / itens ativos da etapa`. É contagem de checklist, não estimativa de esforço ou prazo. O painel conta apenas os itens com IDs E0–E8. Preparação documental, marcos e backlog P2 não entram novamente no denominador. Se existir subplano, o item pai só fecha quando seu aceite e os itens aplicáveis do subplano estiverem concluídos.

Modelo de apresentação ao usuário:

```text
Etapa: E2 — Identidade, organização e auditoria
Concluídos neste ciclo: <IDs e resultado observável>
Validação: <comandos/verificações e resultado>
Progresso da etapa: <concluídos>/<total de itens ativos>
Pendentes/bloqueios: <IDs, causa e impacto, ou nenhum>
Próximo passo: <ID e ação concreta>
Plano atualizado: docs/implementation-plan.md
```

Modelo de registro de evidência, a repetir no histórico quando houver entrega:

```text
Data:
IDs:
Resultado:
Arquivos/artefatos:
Validação executada e resultado:
Limitações ou verificações ainda pendentes:
Próximo item:
```

## 3. Preparação documental realizada

Estes itens comprovam preparação, não implementação nem aprovação das propostas técnicas.

- [x] DOC-01 — Especificação funcional disponível em spec.md.
- [x] DOC-02 — Arquitetura, banco, API e interface documentados.
- [x] DOC-03 — Documentos reunidos em docs/ com links relativos válidos.
- [x] DOC-04 — Plano de implementação criado com etapas, checklists e rotina de acompanhamento.

Evidência inicial: arquivos Markdown existentes, links locais conferidos e checklists estruturados neste documento. Não há resultado de execução de aplicação associado a DOC-01–04.

## 4. Painel de evolução

| Etapa | Resultado | Dependências | Estado | Concluídos |
| --- | --- | --- | --- | --- |
| E0 | Decisões e escopo consolidados | Documentação | Em andamento — responsáveis operacionais pendentes | 5/6 |
| E1 | Fundação executável | Decisões técnicas pertinentes de E0 | Em andamento — fundação e migration inicial verificadas; CI e ambiente limpo pendentes | 7/9 |
| E2 | Identidade, organização e auditoria | E1 | Não iniciada | 0/10 |
| E3 | Primeira jornada e inventário P0 | E2 | Não iniciada | 0/13 |
| E4 | Sistemas, dependências e impacto direto | E3 | Não iniciada | 0/9 |
| E5 | Governança, documentação e revisões | E3; E4 para checklist completo | Não iniciada | 0/10 |
| E6 | Operação e saúde | E3; políticas de E5 | Não iniciada | 0/9 |
| E7 | Dashboards consolidados e exportações | E4, E5 e E6 | Não iniciada | 0/9 |
| E8 | Homologação e preparação para produção | E0–E7 | Não iniciada | 0/10 |

Progresso do plano: **12/85 itens concluídos**. E0: 5/6; E1: 7/9. API, frontend, containers, prontidão do banco e migration inicial foram verificados; login e inventário ainda não implementados. Próximos itens: E1-08/E1-09 (CI e ambiente limpo) e E2 (identidade/auditoria). E0-06 depende da indicação dos responsáveis operacionais. Evidências em [validation/foundation-2026-09-07.md](validation/foundation-2026-09-07.md) e comandos em [development.md](development.md).

Não fixar datas ou duração de sprints sem conhecer capacidade da equipe e infraestrutura. Cada ciclo deve selecionar poucos itens com resultado demonstrável. Uma dependência externa deve bloquear apenas o trabalho que depende dela: domínio, migrations e testes isolados podem avançar enquanto a configuração de identidade de produção é providenciada.

## 5. E0 — Decisões e escopo

Referências: arquitetura §§1–4 e 10; spec §§44, 47, 50–51 e 59. Objetivo: tornar explícitas as decisões que orientarão a implementação, preservando a distinção entre proposta e requisito.

- [x] E0-01 — Consolidar o limite do MVP e mapear divergências P0/P1 contra §§50/59; registrar a decisão nos documentos. Evidência: DEC-001 em [decisions.md](decisions.md), comparada com spec §§50/51/59 em 07/09/2026.
- [x] E0-02 — Definir stack e versões compatíveis, estrutura modular e ferramentas de dependências; registrar justificativa e versões escolhidas. Evidência: DEC-007 e manifests/lockfiles instalados; verificações locais aprovadas. Digests e builds de imagens permanecem pendentes de Docker.
- [x] E0-03 — Definir estratégia de autenticação inicial e evolução corporativa: login local real com e-mail/senha, contas fictícias em desenvolvimento/homologação e SSO posterior sem bypass. Evidência: decisão explícita do usuário em DEC-003, refletida em arquitetura/banco/API/UI; provedor externo será definido na evolução SSO.
- [x] E0-04 — Consolidar matriz de permissões, escopos e campos editáveis; esclarecer consulta global do gestor/auditor e segregação dos dados técnicos. Evidência: DEC-005, confirmação do usuário e matriz sincronizada em API/arquitetura/UI; leitura global não amplia escrita ou campos restritos.
- [x] E0-05 — Consolidar regras propostas: backup ALTA/CRITICA, owners inativados, revisão, documentação suficiente, risco, saúde e inatividade; sincronizar arquitetura, banco, API e UI. Evidência: DEC-008 consolida baseline configurável; arquitetura/banco/API/UI sincronizados. Homologação corporativa dos parâmetros continua no aceite.
- [ ] E0-06 — Registrar decisões de operação ainda externas: ambientes, armazenamento de relatórios, retenção, disponibilidade e recuperação; atribuir responsável e etapa em que cada definição será necessária. Em andamento: on-premises confirmado, levantamento e funções propostas em DEC-006; responsáveis efetivos ainda não designados.

Aceite: decisões necessárias à fundação registradas; pendências restantes com impacto e momento de resolução explícitos. Não tratar escolha técnica ainda proposta como aprovada pelo usuário. Resolver escolhas rotineiras dentro da autorização vigente e solicitar informação apenas quando depender do contexto organizacional indisponível.

Evidência esperada: alterações nos documentos e registro de decisões com data, contexto, escolha, consequência e estado. E0-06 pode concluir com levantamento documentado de pendências; sua resolução operacional efetiva é verificada em E8.

## 6. E1 — Fundação executável

Referências: arquitetura §§2–3 e 8; spec §§52–55. Objetivo: qualquer desenvolvedor conseguir preparar e verificar o ambiente a partir das instruções do repositório.

- [x] E1-01 — Preparar estrutura backend/frontend/tests e controle de versão local; configurar arquivos ignorados sem incluir secrets ou artefatos gerados indevidos. Evidência: backend/app, backend/tests, frontend/src e scripts criados; Git inicializado e .gitignore conferido, sem commit.
- [x] E1-02 — Criar backend mínimo com configuração por ambiente, validação da configuração e endpoints de vivacidade/prontidão. Evidência: API de saúde, configuração por ambiente/arquivo de senha e oito testes de fundação aprovados; prontidão positiva usa probe controlado, sem comprovar PostgreSQL real.
- [x] E1-03 — Criar frontend mínimo com navegação base, cliente HTTP e tratamento comum de carregamento/erro. Evidência: navegação inicial, cliente HTTP e estados carregando/erro/recuperação; dois testes e build aprovados.
- [x] E1-04 — Disponibilizar PostgreSQL local e procedimento reproduzível de inicialização; fornecer configuração de exemplo sem credenciais reais. Evidência: usuário confirmou execução dos itens 1–3; `/api/health/live` e `/api/health/ready` responderam 200 em 07/09/2026, indicando API e consulta ao banco ativas. `scripts/compose-up.sh`, Compose e secrets locais preparados. Inspeção administrativa via Docker neste shell ainda exige senha sudo.
- [x] E1-05 — Configurar persistência e migrations; demonstrar criação do esquema inicial em banco vazio. Evidência: usuário confirmou execução do bootstrap administrativo, `alembic upgrade head` e `alembic current`, com revisão `0001_foundation`; schema/migration inicial validados no banco real. Migration usa extensão criada pelo bootstrap e a imagem copia `alembic.ini`/`migrations`.
- [x] E1-06 — Configurar logs estruturados, request_id e resposta padronizada de erro sem dados internos ou sensíveis. Evidência: logging JSON, X-Request-ID e envelopes de erro testados sem exposição de entradas sensíveis.
- [x] E1-07 — Configurar lint, formatação, checagem de tipos aplicável, testes e build; fixar dependências em arquivos reproduzíveis. Evidência: uv.lock/package-lock.json, versões diretas exatas e scripts/check.py; lint, formatação, tipos, testes e build aprovados.
- [ ] E1-08 — Criar verificações automatizadas da própria plataforma no mecanismo de CI escolhido; validar os comandos localmente e registrar execução remota quando disponível.
- [ ] E1-09 — Documentar instalação, configuração, execução, migrations, testes e solução de problemas em docs/development.md; verificar o procedimento em ambiente limpo. Documentação atualizada; reprodução completa, containers e migrations ainda pendentes.

Aceite: backend, frontend e banco iniciam conforme documentação; verificações de fundação passam. A execução remota da CI, quando indisponível, deve permanecer identificada como pendente e impedir o fechamento de E1-08; isso não impede o desenvolvimento local dos módulos.

Evidência esperada: comandos e resultados de instalação, migrations, verificações e build; configuração de CI e execução correspondente. Documentar decisões de estrutura sem criar módulos vazios que aparentem funcionalidade pronta.

## 7. E2 — Identidade, organização e auditoria

Referências: API §§2–3 e 8; banco §§3 e 9; spec §§5, 10–11, 21–22 e 44–45.

- [ ] E2-01 — Implementar migrations de usuários, roles, permissões, escopos, empresas, áreas, processos, equipes e membros, com restrições referenciais.
- [ ] E2-02 — Implementar login local/sessão, login/logout/me, bootstrap administrativo, hash Argon2id, alteração/recuperação de senha com revogação, limitação de tentativas, expiração e proteção das mutações; preparar vínculo de identidade para SSO futuro.
- [ ] E2-03 — Implementar autorização por ação, escopo e campo no backend, reutilizável em consultas e mutações.
- [ ] E2-04 — Implementar cadastro e manutenção administrativa de usuários, roles e escopos, com proteção do último administrador ativo.
- [ ] E2-05 — Implementar cadastros organizacionais e seletores paginados; validar processo/subprocesso sem ciclos e coerência de área/equipe.
- [ ] E2-06 — Implementar AuditLog imutável na mesma transação de cada alteração relevante, inclusive permissões e cadastros; falha de auditoria deve reverter a mudança.
- [ ] E2-07 — Implementar consulta de auditoria autorizada e histórico sanitizado, preservando diferenças de visibilidade.
- [ ] E2-08 — Entregar telas de login, acesso negado, sessão expirada e administração, respeitando permissões reais da API.
- [ ] E2-09 — Criar seed idempotente de usuários fictícios dos cinco perfis, áreas, processos e equipes; não incluir identidades/segredos reais.
- [ ] E2-10 — Validar autenticação, expiração, acesso cruzado entre áreas, permissões de campos, cadastros e atomicidade da auditoria com testes de integração.

Aceite: uma pessoa autorizada autentica e gerencia cadastros dentro de seu perfil; acesso indevido é rejeitado pela API; alterações administrativas geram auditoria que nenhum perfil pode editar. Testes do MVP devem comprovar login local e recuperação/troca segura de senha; identidade simulada não comprova autenticação real. Integração corporativa será verificada quando o SSO futuro for implementado.

Evidência esperada: migrations, testes de isolamento e auditoria, contratos OpenAPI, seed e demonstração das telas. Auditoria deve estar operacional antes de expor qualquer CRUD aos usuários.

## 8. E3 — Primeira jornada e inventário P0

Referências: spec §§6–11, 16, 18–22, 34–38 e 46; API §§3–4 e 6; banco §§4–5; UI §§4–6 e 12.

- [ ] E3-01 — Implementar Automation e AutomationVersion com UUID, código permanente, versão atual da própria automação e vínculos obrigatórios.
- [ ] E3-02 — Implementar cadastro transacional: automação, versão inicial, revisão inicial e auditoria; validar owners/equipe, backup, criticidade e dados sensíveis.
- [ ] E3-03 — Implementar listagem, detalhe, busca, paginação, ordenação e filtros cadastrais com escopo aplicado antes de contar/agregar.
- [ ] E3-04 — Implementar PUT/PATCH por campo autorizado, motivo para alterações críticas e ETag/If-Match sem sobrescrita silenciosa.
- [ ] E3-05 — Implementar alteração de status, soft delete, consulta histórica, saneamento administrativo e restauração, preservando código e relações.
- [ ] E3-06 — Implementar histórico de versões, registro de nova versão e definição explícita da atual, incluindo versão anterior e auditoria correspondente.
- [ ] E3-07 — Implementar tecnologias, categorias e referências de credenciais com seus vínculos; impedir armazenamento/exposição de conteúdo secreto.
- [ ] E3-08 — Entregar listagem e formulário de cadastro/edição com validação, filtros na URL e tratamento de conflito e alterações não salvas.
- [ ] E3-09 — Entregar detalhe com resumo, informações de negócio/técnicas, versões e histórico; habilitar demais abas conforme entregues.
- [ ] E3-10 — Exibir dashboard básico de inventário por status/criticidade com dados reais e escopo correto; ampliar outros indicadores em E7.
- [ ] E3-11 — Criar as quatro automações fictícias do §56, com owners, backup e versão válidos; verificar que o seed pode ser repetido.
- [ ] E3-12 — Testar código concorrente, cadastro inválido sem gravação parcial, versão de outro ativo rejeitada, owners inativos, soft delete, edição concorrente e auditoria.
- [ ] E3-13 — Demonstrar Login → Cadastro → Listagem → Detalhe → Edição → Histórico pela interface, incluindo perfil sem permissão e estados de erro.

Aceite: primeira jornada funciona com persistência real, autorização e auditoria; não depende de dados fixos na UI. RN-001–011 e RN-015 aplicáveis são verificadas. Próxima revisão inicial usa política mínima versionada criada nesta etapa; tela de administração e cálculo completo de governança chegam em E5.

Evidência esperada: testes unitários/integrados e de interface, registros auditados, filtros reproduzíveis e demonstração da jornada. Indicadores ainda não implementados não podem ser exibidos como resultados calculados.

## 9. E4 — Sistemas, dependências e impacto direto

Referências: spec §§12–15, 39–40; banco §§5–6; API §5; UI §7.

- [ ] E4-01 — Implementar cadastro de sistemas, responsáveis, criticidade, estado e referências de documentação.
- [ ] E4-02 — Implementar tipos/componentes de dependência com integridade do destino e cadastro configurável de tipos.
- [ ] E4-03 — Implementar inclusão, alteração e remoção auditada de dependências; rejeitar autorrelação, duplicação e relação CRITICA opcional.
- [ ] E4-04 — Implementar participação de sistemas e sua consistência com dependências; impedir remoção de vínculo ainda necessário.
- [ ] E4-05 — Implementar listas “Depende de”/“Dependem desta” e análise direta de impacto com contagens autorizadas por criticidade.
- [ ] E4-06 — Entregar grafo básico clicável, direção documentada, limite de nós, aviso de truncamento e alternativa tabular acessível.
- [ ] E4-07 — Integrar telas de sistemas e abas de dependências/sistemas ao detalhe, com filtros de inventário correspondentes.
- [ ] E4-08 — Tratar ciclos reais, destinos inativados/excluídos e exclusão com dependentes sem apagar histórico ou vazar destinos fora do escopo.
- [ ] E4-09 — Testar integridade, relações reversas, impacto, obrigatoriedade, ciclos, paginação e permissões; demonstrar Automação → Sistema → Impacto.

Aceite: RN-012 validada; relações coerentes no banco, API, listas e grafo. Impacto é direto e potencial, incluindo distinção entre dependências obrigatórias e opcionais. Não apresentar alcance transitivo como implementado.

Evidência esperada: testes de relações e isolamento, consultas de impacto e demonstração do grafo/listas com seed de sistemas e dependências.

## 10. E5 — Governança, documentação, risco e revisões

Referências: spec §§17–19 e 26–29, 33; API §7; banco §8; UI §9.

- [ ] E5-01 — Implementar referências documentais por tipo, edição/arquivamento e validação de URL, sem upload ou leitura automática de conteúdo externo.
- [ ] E5-02 — Implementar políticas versionadas configuráveis de governança, risco, saúde, revisão e inatividade, com validação de limites e auditoria.
- [ ] E5-03 — Implementar checklist calculado por evidências, completude de documentação e declarações justificadas de mapeamento/não aplicabilidade.
- [ ] E5-04 — Implementar avaliações manuais de risco com fatores, cálculo/faixas no servidor, justificativa e snapshot da política utilizada.
- [ ] E5-05 — Implementar revisão com participantes, snapshot e resultado; apenas conclusão autorizada atualiza última/próxima revisão.
- [ ] E5-06 — Implementar validação de processo/criticidade vinculada ao valor atual, indicando quando uma alteração invalida a evidência.
- [ ] E5-07 — Implementar identificação de órfãs, backup ausente e responsáveis/equipes inativados, preservando histórico e permitindo correção.
- [ ] E5-08 — Implementar revisão próxima/vencida, regras de calendário e mudança de criticidade sem prorrogação silenciosa de prazo.
- [ ] E5-09 — Entregar abas de documentação/governança, formulários de revisão/risco e tela de pendências com filtros reproduzíveis.
- [ ] E5-10 — Testar faixas e limites de políticas, ausência de evidência, fim de mês, revisão pendente/concluída, owner inativado e permissões de aprovação.

Aceite: RN-013 e itens de governança dos §§50/59 atendidos; percentual e risco calculados no backend; dados ausentes não representam conformidade ou risco baixo.

Evidência esperada: testes determinísticos com datas controladas, política/snapshot históricos e demonstração de pendência corrigida mediante alteração auditada.

## 11. E6 — Operação, saúde e incidentes

Referências: spec §§23–25, 30 e 32; API §6; banco §7; UI §8.

- [ ] E6-01 — Implementar registro manual de execuções finalizadas, source=MANUAL, datas válidas, duração calculada e volume não negativo.
- [ ] E6-02 — Implementar consulta e filtros de execuções sem expor payloads/erros contendo dados sensíveis.
- [ ] E6-03 — Implementar saúde, taxa de sucesso, erros, tempo médio e falhas consecutivas conforme janela/política, com SEM_DADOS explícito.
- [ ] E6-04 — Implementar inatividade a partir da última execução ou entrada, limiar configurável e faixas sem contagem duplicada.
- [ ] E6-05 — Implementar incidentes, severidade, transições, resolução e reabertura com motivo e histórico preservado.
- [ ] E6-06 — Entregar abas de execuções/incidentes, registro manual e visualização de saúde; não disponibilizar comando de execução externa.
- [ ] E6-07 — Integrar filtros de saúde/última execução/inatividade à busca e entregar a visão operacional com dados do banco.
- [ ] E6-08 — Expandir seed com sucesso, erro, timeout, sem execução, falhas consecutivas e incidentes abertos/resolvidos.
- [ ] E6-09 — Testar datas-limite, fuso, denominador de sucesso, ausência de dados, inatividade, transições e manutenção do registro operacional quando owner estiver inativo.

Aceite: RN-014 atendida; indicadores e listagens apresentam mesma janela e população; nenhuma ação executa a automação real. Saúde inicial não presume calendário/SLA nem incorpora incidentes fora da fórmula documentada.

Evidência esperada: cálculos verificados contra dados conhecidos e demonstração Registro manual → Histórico → Indicadores.

## 12. E7 — Dashboards consolidados e exportações

Referências: spec §§31–33 e 41; API §9; banco §9; UI §§10–11.

- [ ] E7-01 — Consolidar dashboard executivo com inventário, criticidade, governança, operação e risco, incluindo estados sem dados/avaliação.
- [ ] E7-02 — Consolidar dashboards de operação/governança e seus links para listas com filtros equivalentes, as_of, fuso e população.
- [ ] E7-03 — Implementar export_job e worker com aquisição atômica, tratamento de falha, timeout e recuperação de trabalho interrompido.
- [ ] E7-04 — Implementar relatórios CSV, XLSX e PDF dos tipos definidos na API, com filtros e leitura consistente registrados.
- [ ] E7-05 — Implementar armazenamento privado, validade, consulta/download autorizado e revalidação de escopo antes de gerar/baixar.
- [ ] E7-06 — Neutralizar fórmulas de planilha e escapar conteúdo de PDF; preservar restrições de campos e exigir audit.read para auditoria.
- [ ] E7-07 — Entregar tela de relatórios e acompanhamento de jobs, incluindo geração, falha, download e expiração.
- [ ] E7-08 — Testar agregações contra o banco, filtros, diferenças de população, erros parciais de dashboard e ausência de vazamento por contagem.
- [ ] E7-09 — Testar os formatos/tipos de exportação, expiração, acesso revogado, repetição de jobs e equivalência entre inventário filtrado e relatório.

Aceite: dashboards exibem dados reais; exportação exigida pelos §§50/59 funciona; artefatos não são públicos e não ampliam acesso a dados.

Evidência esperada: testes, relatórios fictícios abertos nos formatos correspondentes, demonstração dos estados do job e tentativa de download após revogação de acesso.

## 13. E8 — Homologação e preparação para produção

Referências: spec §§47, 50 e 54–59; arquitetura §§7–9; UI §§13–14.

- [ ] E8-01 — Executar a matriz de aceite dos §§50/59, mapear cada critério à evidência e corrigir lacunas; criar docs/acceptance-plan.md com checklist por critério.
- [ ] E8-02 — Executar regressão unitária, de integração e jornadas críticas de interface, incluindo cenários negativos de todos os perfis.
- [ ] E8-03 — Validar teclado, foco, rótulos, contraste, tabela alternativa do grafo, responsividade e estados vazio/erro nos fluxos críticos.
- [ ] E8-04 — Executar carga com 10.000+ automações e concorrência documentada; medir p95 de busca contra a meta consolidada em E0 e corrigir gargalos relevantes.
- [ ] E8-05 — Validar autenticação local, bootstrap/recuperação, revogação, CSRF, TLS, proteção de dados/logs e criptografia de banco/backups no ambiente de destino; autenticação corporativa será validada em sua evolução.
- [ ] E8-06 — Definir e verificar retenção, RPO/RTO e backup/restauração; registrar ensaio de recuperação com dados fictícios e resultado medido.
- [ ] E8-07 — Preparar procedimento versionado de implantação, migrations, reversão e configuração por ambiente em docs/deployment-plan.md, com checklist e verificações de saúde.
- [ ] E8-08 — Configurar observabilidade e procedimentos de suporte para falhas de API, banco e exportação; documentar responsáveis e diagnóstico.
- [ ] E8-09 — Atualizar documentação técnica/OpenAPI, instruções de uso e seed; registrar versão candidata e limitações conhecidas com impacto sobre o aceite.
- [ ] E8-10 — Apresentar demonstração do MVP e relatório de aceite com evidências; registrar retorno do responsável pelo produto e próximos passos de liberação.

Aceite: critérios funcionais satisfeitos e preparação operacional comprovada, sem defeito aberto que invalide autorização, integridade, auditoria ou jornada essencial. Não marcar prontidão de produção com base apenas em execução local. E8-10 só pode ser concluído quando houver retorno efetivo, não presumido.

A criação deste plano não autoriza implantação em produção ou publicação externa. Preparar artefatos, verificações e procedimento concreto antes de qualquer decisão de liberação; usar a autorização vigente quando a execução for solicitada. O checklist de implantação registrará a execução real em seu próprio ambiente.

## 14. Marcos de entrega

Os marcos resumem as etapas e não entram novamente na contagem de implementação.

- [ ] M1 — Fundação utilizável: E1 e E2 concluídas com decisões necessárias de E0 registradas.
- [ ] M2 — Primeira jornada: E3 concluída, com login/cadastro/consulta/edição/histórico demonstrados.
- [ ] M3 — Inventário P0 com dependências: E4 concluída sobre M2, incluindo sistemas, grafo e dashboard básico.
- [ ] M4 — Governança e operação: E5 e E6 concluídas.
- [ ] M5 — MVP funcional candidato: E7 concluída e critérios funcionais conferidos em E8-01.
- [ ] M6 — MVP homologado e preparado para liberação: E8 concluída com retorno real do responsável pelo produto.

## 15. Rastreabilidade das regras e critérios

| Requisito | Itens responsáveis | Evidência principal |
| --- | --- | --- |
| RN-001: código único | E3-01, E3-12 | Unicidade sob concorrência e permanência após exclusão |
| RN-002–004: owners/equipe | E3-02, E3-12, E5-07 | Validação de cadastro e identificação após inativação |
| RN-005: backup | E0-05, E3-02, E5-07 | ALTA/CRITICA sem backup rejeitadas no cadastro |
| RN-006: preservação histórica | E3-05, E3-12 | Descontinuação e soft delete preservam dados |
| RN-007: sem secrets | E1-06, E3-07, E8-05 | Campos, logs e exposição de referências verificados |
| RN-008: auditoria | E2-06, E2-10 e testes dos módulos | Mutação e evento na mesma transação |
| RN-009–010: criticidade/classificação | E3-02, E3-12 | Campos obrigatórios e coerência de sensibilidade |
| RN-011: versão atual | E3-01, E3-02, E3-06, E3-12 | FK do próprio ativo e promoção auditada |
| RN-012: dependências críticas | E4-03, E4-09, E5-03 | Obrigatoriedade e declaração de mapeamento |
| RN-013: revisão vencida | E5-05, E5-08, E5-10, E7-02 | Calendário e indicadores reproduzíveis |
| RN-014: sem execução | E6-04, E6-09, E7-02 | Limiares e ausência de execução |
| RN-015: mudança de criticidade | E3-04, E3-12 | Antes/depois e motivo no histórico |
| §50: cadastros e inventário | E2-04–05, E3, E4 | API e jornadas de cadastro/consulta |
| §50: documentação e revisão | E5-01, E5-05, E5-09–10 | Registro, conclusão e evidências |
| §§50/59: controle de acesso | E2-03, E2-10, E8-02 | Perfis e isolamento no backend |
| §§50/59: indicadores e exportação | E3-10, E7 | Dados reais, recorte e arquivos |
| §55: qualidade e testes | Testes de cada etapa, E8-02–04 | Resultados executados, não só casos escritos |
| §56: demonstração | E2-09, E3-11, E4-09, E6-08 | Seed fictício, consistente e repetível |
| §59: documentação e prontidão | E1-09, E8-01, E8-07–10 | Ambiente reproduzível e aceite registrado |

## 16. Evolução P2 — fora da contagem do MVP

Cada item deve receber subplano com contrato, escopo, checklist e aceite antes de ser implementado. Prioridade futura depende de necessidade confirmada; não há prazo nem execução autorizada por este backlog.

- [ ] P2-01 — Integrações com RPA/orquestradores e ingestão idempotente de execuções.
- [ ] P2-02 — Integrações com monitoramento, ITSM, CMDB e diretórios corporativos conforme contratos externos.
- [ ] P2-03 — Impacto indireto e grafo avançado com regras para profundidade/ciclos e desempenho.
- [ ] P2-04 — Alertas configuráveis e canais de notificação com destinatários/regras definidos.
- [ ] P2-05 — Coleta automática de fatores de risco e calendário operacional para atrasos/SLA.
- [ ] P2-06 — Indicadores de eficiência, valor, custos e portfólio com fontes e fórmulas confirmadas.
- [ ] P2-07 — Importação em lote com validação, relatório de inconsistências e saneamento de registros legados.
- [ ] P2-08 — SSO corporativo com provedor definido, vínculo verificado de contas e migração que preserve owners/UUIDs/histórico.

## 17. Histórico de acompanhamento

| Data | Itens | Resultado e evidência | Pendências / próximo passo |
| --- | --- | --- | --- |
| 07/09/2026 | DOC-01–04 | Documentação em docs/ e plano estruturado; links, IDs de checklist e contagens conferidos | Implementação 0/85; próximo E0-01 |
| 07/09/2026 | E0-01; E0-02–04 em levantamento | Escopo consolidado em [DEC-001](decisions.md); entrevista iniciada e ferramentas locais consultadas | 1/85; respostas sobre organização, identidade e stack/hospedagem pendentes |
| 07/09/2026 | E0-03 concluído; E0-02/04/06 e E1-04 em andamento | Usuário confirmou organização única, login local com SSO futuro e stack dockerizada; documentos sincronizados e Compose preparado. Script de configuração verificado sem expor secrets; verificação estática do Compose registrada em development.md | 2/85; acesso entre áreas e destino da hospedagem em entrevista; Docker sem acesso ao daemon |
| 07/09/2026 | E0-04 concluído; E0-06 em levantamento | Usuário confirmou consulta a todas as áreas para gestor/auditor e implantação interna on-premises; DEC-005/006 registradas e API/arquitetura/UI sincronizadas | 3/85; próximos E0-02/E0-05; especificações do host e responsáveis operacionais pendentes |
| 07/09/2026 | E0-02/05 e E1-01/02/03/06/07 concluídos | Fundação entregue: Git, API, UI, lockfiles, Dockerfiles/Compose e verificações locais; [evidências](validation/foundation-2026-09-07.md): 8 testes backend, 2 frontend, lint/tipos/build e Compose estático aprovados | 10/85; containers/banco/migrations, CI e ambiente limpo pendentes; Docker sem acesso ao daemon |
| 07/09/2026 | E1-04 concluído; E1-05 em andamento | Usuário confirmou containers no ar; endpoints live/ready retornaram 200 e o ready comprovou acesso da API ao banco. Primeira tentativa de Alembic falhou por ausência de arquivos na imagem; Dockerfile corrigido para copiá-los | 11/85; rebuild do backend, aplicar migration e confirmar persistência; CI e ambiente limpo pendentes |
| 07/09/2026 | E1-05 em andamento | Alembic alcançou PostgreSQL, mas `inventory_app` não podia criar `alembic_version` no schema public. Bootstrap corrigido e comando de concessão para volume existente documentado | 11/85; executar GRANT, reaplicar migration e confirmar revisão/tabelas |
| 07/09/2026 | E1-05 em andamento | Após corrigir o schema, `pgcrypto` exigiu privilégio de criação no banco. Extensão movida para bootstrap administrativo e removida da migration de runtime | 11/85; executar CREATE EXTENSION como administrador, reaplicar migration e confirmar revisão/tabelas |
| 07/09/2026 | E1-05 concluído | Usuário confirmou execução bem-sucedida de `alembic upgrade head` e revisão `0001_foundation` no banco real após conceder privilégios e criar `pgcrypto` | 12/85; próximo E2-01: ampliar migrations/entidades de identidade e concluir E1-08/E1-09 |
| 07/09/2026 | E1-08 em andamento | Workflow `.github/workflows/ci.yml` criado com jobs de backend, frontend e Compose; Dependabot configurado. Checks locais equivalentes já passaram | 12/85; executar CI remotamente após conectar o repositório a um provedor; depois validar E1-09 em ambiente limpo |

Registrar novas linhas por ciclo de trabalho. Para evidências extensas, usar seção abaixo ou documento em docs/ referenciado pela linha, com checklist quando se tratar de outro plano. Não armazenar credenciais, dados reais de produção ou tokens em relatórios de validação.
