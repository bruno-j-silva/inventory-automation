# Registro de decisões do projeto

Referências: [spec.md](spec.md), [architecture.md](architecture.md), [implementation-plan.md](implementation-plan.md).

## DEC-001 — Escopo e ordem de entrega

Data: 07/09/2026. Estado: consolidado a partir dos documentos e da autorização para iniciar o plano. Item: E0-01.

A primeira entrega demonstrável é Login → Cadastro com versão inicial → Listagem → Detalhe → Edição → Histórico. O marco P0 inclui ainda sistemas, dependências, classificação, RBAC, auditoria e dashboard básico. Esse marco não equivale ao aceite de todo o MVP.

| Divergência ou fronteira | Decisão de planejamento | Origem |
| --- | --- | --- |
| Exportação classificada como P1 e exigida no pronto | Incluir no MVP; implementação em E7 | Spec §§41, 50, 51 e 59 |
| Revisão, documentação e identificação de pendências exigidas no aceite | Incluir E5 e identificação de inatividade em E6 | Spec §§50–51 |
| Execuções, saúde e incidentes classificados como P1 | Manter E6 no escopo já planejado; registrar execução não executa código externo | Spec §§23–25, plano §1 |
| Dashboards básico versus consolidado | Inventário básico em E3; consolidação dos três dashboards em E7 | Spec §§31–33 e 51 |
| Dados “importados/cadastrados” | Cadastro manual atende o MVP; importação em lote permanece P2 | Spec §59 |
| Integrações e grafo avançado | Permanecem P2, exceto autenticação necessária à própria plataforma | Spec §§43–44 e 51 |

Consequência: não declarar o MVP concluído apenas com P0. Não introduzir requisitos de desenvolvimento ou execução de automações. Alteração futura do escopo será registrada com impacto nos checklists e critérios de aceite.

## DEC-002 — Organização e isolamento

Data: 07/09/2026. Estado: confirmado pelo usuário (resposta 1A). Item: E0-04, consolidado pela resposta complementar sobre consulta global.

Uso interno de uma organização/grupo, com empresas, áreas e processos na mesma instalação. Não criar produto SaaS multi-inquilino. Gestores e auditores podem consultar todas as áreas, conforme resposta complementar do usuário. Gestor continua criando/editando somente nas áreas atribuídas; auditor permanece somente leitura, com exportação e auditoria autorizadas. Técnicos e responsáveis de negócio mantêm os escopos de responsabilidade/processo previstos na API. Consulta global não concede edição global nem acesso a campos restritos.

## DEC-003 — Login local agora; SSO posteriormente

Data: 07/09/2026. Estado: confirmado pelo usuário (resposta 2B e posteriormente A). Item: E0-03.

Primeiro implementar login por e-mail e senha próprios da plataforma. OIDC/SSO corporativo é evolução posterior, com provedor a definir; não bloqueia o MVP. Identidade local permanece em app_user e o futuro vínculo externo não muda IDs de owners ou histórico. Não vincular contas SSO automaticamente apenas por coincidência de e-mail.

Detalhamento técnico: senha somente como hash Argon2id; sessões opacas revogáveis no backend; cadastro por administrador, sem inscrição pública; alteração de senha revoga sessões; recuperação por token de uso único, com hash persistido, prazo curto e entrega fora dos logs. Não pressupor serviço de e-mail configurado: entrega administrativa inicial por canal controlado; a implementação deve evitar exposição de tokens em auditoria. Proteção contra tentativas repetidas e mensagens genéricas fazem parte do login real, sem bypass.

Desenvolvimento/homologação usam contas fictícias locais sem senha fixa versionada. Bootstrap do primeiro administrador por comando explícito e entrada protegida, sem credenciais padrão. Configuração de cookie seguro/TLS depende do ambiente; produção exige HTTPS. Propostas de limites e fluxo administrativo serão detalhadas na etapa E2.

Essa escolha altera a preferência de SSO do spec §44 por decisão explícita do usuário. A proibição de secrets de automações continua: hashes de senhas da própria plataforma ficam separados de CredentialReference.

## DEC-004 — Stack e containers

Data: 07/09/2026. Estado: stack e Docker confirmados pelo usuário (resposta 3B, dockerizado). Itens: E0-02 e E0-06, parcialmente definidos.

Manter Python/FastAPI, React/TypeScript e PostgreSQL em monólito modular. Preparar Dockerfiles e Docker Compose para ambiente reproduzível, com banco persistente em volume, configuração por ambiente e publicação local da interface. Destino confirmado pelo usuário: servidor interno on-premises. Sistema operacional, capacidade, domínio e configuração do servidor ainda precisam ser levantados. Não presumir Kubernetes, serviço pago ou infraestrutura já contratada.

Versões e ferramentas de dependências serão fixadas e verificadas na fundação antes de concluir E0-02. O frontend e a API usarão a mesma origem por proxy; banco não será publicado externamente por padrão.

## DEC-005 — Consulta entre áreas

Data: 07/09/2026. Estado: confirmado pelo usuário (“todas as áreas”). Item: E0-04.

A matriz de [api.md](api.md) passa a ser a referência consolidada para implementação. Gestor e Auditor/Consulta possuem leitura global das áreas da organização/grupo. Gestor mantém edição por áreas atribuídas; auditor não altera registros. Administrador mantém acesso global; responsáveis técnico/backup e de negócio mantêm consulta/edição conforme responsabilidade e processo.

Aplicar o mesmo escopo de leitura a inventário, busca, gráficos, impacto, relatórios e histórico. Permissões específicas continuam necessárias: gestor não recebe audit.read por consultar todas as áreas; referências de credenciais permanecem restritas por campo. Seleção de área é filtro de consulta, nunca concessão de permissão. Usuário com múltiplos perfis recebe a união das concessões aplicáveis, sem transformar concessão global de leitura em concessão global de escrita.

Aceite para a implementação E2/E3: gestor da área A consulta um ativo da área B, mas não o edita; auditor consulta/exporta dados autorizados e lê auditoria sem mutações; responsáveis não consultam ativos fora de suas atribuições. Contagens e filtros refletem esses mesmos limites.

## DEC-006 — Implantação interna on-premises

Data: 07/09/2026. Estado: destino confirmado pelo usuário (“on-premisses interno”). Item: E0-06 em levantamento.

Preparar execução dockerizada em infraestrutura interna. Docker Compose é a base inicial de empacotamento/execução; não presumir Kubernetes nem serviços em nuvem. Manter frontend/API sob a mesma origem, com HTTPS no ponto de entrada interno e banco acessível apenas pela rede de containers. Acesso interno não elimina autenticação, autorização, proteção de sessões ou auditoria.

Separar desenvolvimento, homologação e produção por configuração, volumes, credenciais e dados. A topologia inicial de um host não comprova alta disponibilidade. Dimensionamento e necessidade de redundância dependerão dos objetivos operacionais definidos pela organização. Artefatos de relatórios ficam em armazenamento privado persistente interno, com expiração e controle de acesso.

### Levantamento operacional pendente

Responsabilidades abaixo são funções propostas, não pessoas/equipes já designadas pelo usuário. A indicação do responsável efetivo ainda é necessária para fechar E0-06; não bloqueia a fundação local.

| Definição | Responsabilidade proposta | Necessária antes de | Estado |
| --- | --- | --- | --- |
| Host, SO compatível, CPU/RAM/disco, acesso ao Docker e registro de imagens | Infraestrutura interna | Primeiro deploy em homologação | A levantar |
| DNS interno, certificado TLS, proxy e regras de rede | Infraestrutura/redes | Login em homologação e produção | A levantar |
| Local e capacidade dos volumes de banco e relatórios | Infraestrutura + responsável técnico | Primeiro deploy persistente | A levantar |
| Retenção de auditoria, execuções e backups | Responsável pelo produto + operação | E8-06 / produção | A definir |
| RPO/RTO, disponibilidade e teste de restauração | Operação + responsável pelo produto | E8-06 / produção | A definir |
| Destino de logs, alertas e responsável de suporte | Operação | E8-08 / produção | A definir |

### Entrevista inicial concluída

Q-01–Q-05 respondidas: organização/grupo único; login local com SSO futuro; stack proposta em Docker; consulta global de gestor/auditor; hospedagem interna on-premises. Perguntas de infraestrutura detalhada serão feitas antes do deploy, quando houver procedimento concreto e necessidade das informações. Não solicitar credenciais na entrevista.

## Referências técnicas consultadas

- [FastAPI — hashing de senhas](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/): suporte a pwdlib/Argon2; a escolha local usa sessões opacas, sem adotar o exemplo JWT como contrato.
- [Vite — requisitos de execução](https://vite.dev/guide/): verificar compatibilidade do Node ao fixar dependências.
- [Imagem oficial PostgreSQL](https://hub.docker.com/_/postgres): seguir o caminho de volume correspondente à versão principal escolhida.

## Diagnóstico local inicial

Consultas realizadas em 07/09/2026:

- Python disponível: 3.12.3.
- Node.js disponível: 24.13.0; npm: 11.6.2.
- Git disponível: 2.43.0; histórico do repositório não disponível na inspeção anterior.
- uv não encontrado no PATH.
- Docker CLI: 29.6.1; Docker Compose: v5.3.1, consultados fora do sandbox após restrição do Snap. A disponibilidade do daemon e a execução de containers ainda não foram verificadas.

Essas versões são observações do ambiente, não seleção definitiva de dependências. Nenhum serviço foi instalado/iniciado e nenhum teste de aplicação foi executado nesta etapa. Em consulta posterior, docker info retornou acesso negado ao socket mesmo fora do sandbox; o daemon e a execução de containers não puderam ser validados. Compose e script de inicialização estão preparados; evidências em [development.md](development.md).

## Alteração do plano por DEC-003

E0-03 foi reformulado para registrar a estratégia local escolhida, mantendo o total de 85 itens E0–E8. E2-02 passa a incluir credenciais locais e recuperação; E8-05 valida esse modo no MVP. Integração corporativa foi isolada em P2-08. Isso registra mudança de requisito autorizada, sem declarar autenticação implementada.

## DEC-007 — Versões e ferramentas da fundação

Data: 07/09/2026. Estado: decisão técnica de implementação, validada pelas verificações locais. Item: E0-02.

Manter Python 3.12 e Node.js 24, compatíveis com o ambiente disponível e a stack confirmada. Gerenciar Python com uv 0.12.10 e `backend/uv.lock`; frontend com npm 11 e `frontend/package-lock.json`. Dependências diretas ficam exatas nos manifests; instalar com `uv sync --frozen` e `npm ci`. React usa Vite e TypeScript; testes de interface usam Vitest/Testing Library; backend usa pytest, Ruff e mypy. Não depender de Make, indisponível neste ambiente: `python3 scripts/check.py` reúne as verificações.

| Componente | Versão escolhida |
| --- | --- |
| alembic | 1.19.2 |
| fastapi | 0.141.1 |
| psycopg[binary] | 3.3.5 |
| pydantic-settings | 2.15.0 |
| sqlalchemy | 2.0.52 |
| uvicorn | 0.52.4 |
| react | 19.2.8 |
| react-dom | 19.2.8 |
| typescript | 6.0.3 |
| vite | 8.2.2 |
| vitest | 5.0.0 |
| eslint | 10.10.0 |
| prettier | 3.9.6 |

Imagens de runtime: Python 3.12 slim, Node 24 alpine, PostgreSQL 18 alpine e nginx-unprivileged 1.28 alpine. O estágio de uv fixa 0.12.10. Essas tags selecionam linhas de runtime; ainda não estão travadas por digest. Resolver imagens, registrar digests e validar build nos containers quando o daemon estiver disponível, antes da liberação. Não confundir seleção de dependências com imagem já construída.

Justificativa: monólito modular e ferramentas com lockfile mantêm a base reproduzível; linters, tipos e testes verificam a compatibilidade do código com as versões instaladas. Alembic já está disponível, mas migrations e integração PostgreSQL ainda serão implementadas/validadas.

Fontes: [uv — instalação](https://docs.astral.sh/uv/getting-started/installation/), [FastAPI em containers](https://fastapi.tiangolo.com/deployment/docker/), [Vite — ambiente](https://vite.dev/guide/). Versões exatas acima vêm dos manifests/lockfiles efetivamente gerados, não de estimativas.

## DEC-008 — Parâmetros iniciais de governança

Data: 07/09/2026. Estado: baseline técnica adotada para implementação, configurável; não constitui política corporativa homologada. Item: E0-05.

Adotar os valores já propostos na arquitetura §6: fatores de risco 1–5, faixas 1–20/21–40/41–60/61–125; saúde observada em 30 dias com limites 95%/80%, SEM_DADOS sem execuções; revisão em 12 meses para BAIXA/MEDIA e 6 para ALTA/CRITICA; aviso de revisão próxima em 30 dias; inatividade inicial >30 dias e faixas >30/>60/>90 sem duplicação; falhas consecutivas com limite inicial 3. Não incorporar atraso/SLA, incidentes ou disponibilidade à fórmula de saúde sem contrato próprio.

Backup é obrigatório para ALTA/CRITICA. Inativação de owner/equipe preserva vínculos e sinaliza órfãs; não impede registrar incidentes/execuções. Documentação mínima calculada exige referências FUNCIONAL e TECNICA ativas, com contingência como item separado. Evidências e política ficam em snapshot na revisão; percentuais atuais são calculados pelo backend. Ausência de dados não significa conformidade.

Essas escolhas consolidam arquitetura, banco, API e UI para desenvolvimento; parâmetros operacionais podem ser revistos com justificativa e auditoria. Na E5, implementar políticas versionadas em vez de espalhar constantes pelos módulos. A organização valida a baseline no aceite antes de produção; nenhuma funcionalidade de governança foi implementada neste ciclo.
