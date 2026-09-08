# Especificação de interface e fluxos

Base: [spec.md](spec.md), §§5, 31–41, 50 e 56. Complementos: [architecture.md](architecture.md), [db.md](db.md), [api.md](api.md).

Interface web proposta em português brasileiro. Este documento descreve telas e comportamento para implementação, não protótipos já construídos. Tecnologia visual, layout e critérios adicionais são propostas; regras funcionais seguem a especificação e as consolidações da arquitetura.

## 1. Navegação e princípios

Menu principal: Dashboard executivo, Inventário, Sistemas, Operação, Governança, Relatórios e Administração. Auditoria global aparece apenas para quem possui audit.read. Administração reúne usuários/perfis, empresas/áreas/processos, equipes, sistemas, tipos/componentes de dependência, tecnologias, categorias e parâmetros.

Inventário é a entrada de trabalho cotidiana; dashboards permitem navegar para listas filtradas. Breadcrumbs situam a pessoa no ativo/processo atual. Cabeçalho mostra usuário, área de contexto quando aplicável e saída. O escopo é controlado pelo backend, não por um seletor que conceda acesso. Gestores e auditores podem consultar todas as áreas. Ao abrir automação de outra área, gestor vê o detalhe sem ações de edição para as quais não tenha concessão; auditor mantém interface somente leitura. O filtro de área não altera essas permissões.

Separar informações de negócio e técnicas. Usar o código permanente como referência principal, mantendo nome legível. Não oferecer “Executar automação”, editor de código ou deploy. A ação operacional chama-se **Registrar execução**; versão usa **Registrar versão implantada** ou **Definir como atual**.

Status, criticidade, risco e saúde têm rótulos próprios. “Criticidade crítica” não significa “saúde crítica”. Usar texto e ícone além de cor. SEM_DADOS aparece como “Sem dados”, nunca como 0% ou “Saudável”.

## 2. Mapa de telas e prioridade

| Tela | Conteúdo | Entrega |
| --- | --- | --- |
| Login | E-mail e senha locais; SSO posterior | Fundação/P0 |
| Inventário | Busca, filtros, ordenação, paginação e exportação | P0; exportação no MVP aceito |
| Cadastro/edição | Dados do ativo existente e versão inicial | P0 |
| Detalhe da automação | Doze abas especificadas abaixo | Progressivo P0/P1 |
| Sistemas | Cadastro, detalhes, participação e impacto | P0; impacto básico na etapa 3 |
| Dashboard executivo | Totais reais do inventário e expansão de indicadores | P0/P1 |
| Operação | Execuções, saúde e incidentes | P1 |
| Governança | Pendências, revisões, documentação e risco | P1 necessário ao aceite |
| Relatórios | Exportação e acompanhamento de geração | Necessário ao aceite §§50/59 |
| Administração | Cadastros, RBAC e parâmetros | P0, políticas conforme módulos |
| Auditoria global | Busca e detalhes imutáveis de eventos | P0 |

Funcionalidade ainda não entregue não deve aparecer como disponível. Integrações externas, alertas e grafo transitivo avançado são P2. Um MVP apenas P0 ainda não satisfaz todos os critérios §§50/59, conforme [architecture.md](architecture.md).

## 3. Login e sessão

Exibir formulário com e-mail, senha, controle de mostrar/ocultar senha e botão “Entrar”. Permitir gerenciadores de senha e colagem; usar autocomplete apropriado. Erro genérico para credencial inválida/conta inativa e mensagem de limite de tentativas. Não oferecer inscrição pública. Informar que recuperação inicial é solicitada ao administrador e oferecer formulário de definição de senha com token de uso único. A troca de senha exige a senha atual e novo login após conclusão. Preservar somente destino interno validado para retorno. “Entrar com conta corporativa” será adicionado quando o SSO estiver configurado, sem criar perfil administrativo automaticamente.

Em sessão expirada, solicitar novo login. Não reenviar mutação automaticamente nem descartar formulário em memória sem aviso. Evitar salvar conteúdo sensível em armazenamento persistente do navegador. Erro de autenticação deve oferecer tentar novamente e referência de atendimento, sem detalhes de tokens.

## 4. Inventário

Colunas obrigatórias (§36): Código, Automação, Área, Owner (Business Owner), Criticidade, Status, Saúde e Versão. Technical Owner pode ser coluna adicional selecionável. Código/nome abrem detalhes. Mostrar owners inativos como “Inativo”, sem remover o nome histórico.

Barra superior: busca, botão Filtros, filtros ativos removíveis, Limpar filtros, Exportar e Cadastrar automação conforme permissões. Buscar por código/nome/descrição e campos relacionados definidos na API. Filtros combináveis: área, processo/subprocesso, status, criticidade, qualquer owner, technical owner, equipe, sistema, dependência, classificação, saúde, última execução, revisão, risco e tecnologia.

Guardar busca/filtros/ordenação/página na URL para compartilhar o recorte sem transferir permissões. Ao mudar filtro, voltar à primeira página. Busca usa pequeno debounce e cancela resultados obsoletos. Paginação no servidor; não carregar o inventário completo para filtrar no navegador.

Wireframe funcional:

```text
Inventário                                  [Exportar] [Cadastrar automação]
[Buscar por código, nome ou descrição...]    [Filtros]
Área: Financeiro ×    Criticidade: Crítica ×  [Limpar filtros]

Código      Automação       Área       Owner  Criticidade Status Saúde    Versão
AUT-000001  Faturamento     Financeiro João   Crítica     Ativa  Saudável 2.1

25 por página                         1–25 de 120       [Anterior] [Próxima]
```

Estados: carregando com estrutura da tabela; inventário vazio com ação de cadastro para perfil autorizado; busca sem resultados com opção de limpar filtros; falha com tentar novamente; resultado atualizado com quantidade anunciada a tecnologias assistivas. Distinguir erro de rede de lista vazia.

## 5. Cadastro e edição

Cadastro de ativo já desenvolvido em quatro seções, com salvamento único e validação no backend:

| Seção | Campos |
| --- | --- |
| Identificação e negócio | Nome, descrição, objetivo, área, processo/subprocesso, status, data de entrada, frequência, gatilho e SLA opcional |
| Responsabilidade | Business owner, technical owner, backup owner e equipe |
| Informações técnicas e dados | Ambiente, criticidade, classificação, dados sensíveis, categorias/origem/retenção, URLs de repositório/monitoramento/documentação e tecnologias |
| Versão inicial | Rótulo da versão, data da versão, responsável, descrição, motivo e impacto/documentação opcionais |

Código é gerado após salvar. Próxima revisão é calculada e apresentada no detalhe. Campos da versão não iniciam workflow de desenvolvimento. Dependências/documentação complementar podem ser adicionadas após criação, com pendências de governança visíveis.

Regras de formulário:

- Campos obrigatórios identificados por texto/semântica, não só asterisco. Owners/equipe ativos são exigidos no cadastro.
- Seleção de área limita processos e equipe; mudar área invalida seleções incompatíveis e exige nova escolha antes de salvar.
- Criticidade ALTA ou CRITICA torna backup obrigatório imediatamente, mantendo validação no servidor.
- Classificação SENSIVEL marca dados sensíveis; não permitir indicador sensível com PUBLICO/INTERNO.
- URLs são referências, não campos de upload ou credenciais. Referência de Secret Manager não aceita senha, token ou chave.
- Datas e números são apresentados em pt-BR, transmitidos no formato da API. Frequência e SLA são descritivos; não prometer validação de calendário operacional.

Na edição, habilitar apenas grupos de campos autorizados pela matriz de [api.md](api.md). PUT completo é reservado a acesso integral; salvar seção envia PATCH. Mudanças críticas abrem campo obrigatório “Motivo da alteração”. Nome/código atuais permanecem no cabeçalho.

Ao salvar: desabilitar envio repetido, manter conteúdo se houver erro e focar resumo de validação com links para campos. Sucesso abre/atualiza detalhe e mostra confirmação. Resposta 412 informa que o registro mudou e permite recarregar/comparar os valores; não sobrescrever automaticamente. Avisar sobre alterações não salvas ao navegar.

## 6. Detalhe da automação

Cabeçalho fixo do contexto: código/nome, status, saúde, criticidade, risco e versão atual. Exibir business owner, technical owner, backup e equipe; destacar órfã, revisão vencida e documentação pendente. Ações de editar/alterar status dependem de capabilities retornadas pela API.

| Aba (§37) | Conteúdo e ações | API principal |
| --- | --- | --- |
| Resumo | Cards do ativo, owners, última execução, revisão, governança e links | GET automations/{id} |
| Informações de Negócio | Objetivo, área/processo, frequência, gatilho e SLA; validar processo/criticidade quando autorizado | PATCH automations/{id}; POST validations |
| Informações Técnicas | Ambiente, tecnologia, classificação, dados sensíveis, links e referências de credenciais com acesso restrito | PATCH automations/{id}; credential-references; technologies |
| Dependências | Listas nos dois sentidos, cadastro/edição/remoção e grafo | dependencies, dependents, dependency-graph |
| Sistemas | Sistemas participantes e vínculos | systems |
| Execuções | Histórico, filtros, duração, volume, erro sanitizado e registro manual | executions |
| Incidentes | Lista, abertura, tratamento, resolução e reabertura | incidents |
| Versões | Histórico, responsável, descrição/motivo/impacto e selo Atual | versions e activate |
| Documentação | Referências por tipo, títulos, links, edição/arquivamento | documents |
| Governança | Checklist, evidências, risco, validações e revisões | governance, mapping, reviews, validations, risk-assessments |
| Auditoria | Linha do tempo com ator, data, motivo e antes/depois | audit ou history sanitizado |

As rotas na tabela são relativas a `/api/automations/{id}` quando aplicável. A aba Auditoria mostra auditoria completa para audit.read e histórico sanitizado para history.read, com identificação clara do conteúdo disponível. Não expor campos técnicos restritos através de diffs.

Cada aba carrega seus dados sob demanda e mantém erro/vazio/carregamento próprios. Relação com destino indisponível ou excluído usa rótulo de estado autorizado; não fabricar link que exponha recurso fora do escopo.

## 7. Dependências e sistemas

Na aba Dependências, usar subtítulos “Depende de” e “Dependem desta”. Formulário: componente cadastrado, tipo informativo, criticidade da relação, obrigatória, descrição e motivo. Relação CRITICA obriga mandatory=true; explicar “A automação não funciona sem este componente”.

O grafo básico permite selecionar nós, abrir detalhes autorizados e alternar listas. Seta significa “depende de”: automação → componente. Incluir legenda fixa para evitar confusão com ordem de execução. Diferenciar automação/sistema/referência externa por rótulo e forma. Ciclos podem ser exibidos como alerta de topologia, sem travar renderização.

Quando houver muitos nós, mostrar indicação de recorte e acesso às listas paginadas; não apresentar contagens truncadas como totais. Oferecer tabela equivalente navegável por teclado. Não realizar análise indireta no MVP.

Tela de sistema: nome, tipo, owner, criticidade, status, fornecedor, versão, documentação, automações participantes e impacto direto. Impacto mostra total por criticidade, obrigatórias/opcionais e links de cada automação. Exemplo do §40 pode ser usado no seed visual, mas indicadores reais sempre vêm do banco.

Ao remover participação de sistema ainda usado como dependência, mostrar conflito e orientar revisar a dependência. Não remover relações em cascata pela interface.

## 8. Operação e versões

**Registrar execução:** diálogo com início/fim, status final, registros processados e erro opcional. Duração aparece calculada; texto “Registre o resultado de uma execução realizada fora da plataforma”. Após salvar, atualizar lista e indicadores. Não oferecer status “Em execução” sem extensão do contrato.

**Incidente:** título, descrição, severidade, início e referência de ticket opcional. Encerramento exige resolução e data válida; reabertura exige motivo. Ticket é referência externa, sem pressupor integração ITSM. Filtros por estado, severidade e período.

**Versões:** lista ordenada por data, versão atual marcada independentemente do maior rótulo. Registrar nova versão permite marcar “Definir como atual” explicitamente; padrão desmarcado. Ativar versão anterior pede motivo e avisa que apenas o inventário será atualizado. Não usar botões “Deploy” ou “Rollback” que sugiram execução externa.

Dashboard de operação: execuções hoje/7 dias, sucesso, erros, tempo médio, falhas consecutivas, sem utilização e incidentes abertos. Mostrar janela temporal, população e fuso. Saúde usa fórmula documentada; incidentes não alteram a cor automaticamente no cálculo inicial.

## 9. Governança e revisão

Tela de governança apresenta listas acionáveis: órfãs, documentação incompleta, revisão vencida/sem data, sem backup, dados sensíveis, alto/crítico risco, criticidade crítica e dependências pendentes. Cada card abre inventário com filtros equivalentes. Separar ausência de backup de owner principal inativo.

Checklist no detalhe apresenta item, estado, evidência e ação corretiva. Percentual é calculado no servidor. Não permitir marcar “Possui owner” manualmente se não existe owner ativo. Mapeamento de sistemas/dependências usa declaração de completude ou não aplicabilidade justificada; elementos críticos conhecidos não podem ser ignorados.

Documentação suficiente na proposta inicial exige referências funcionais e técnicas ativas. Plano de contingência tem item próprio. Referência arquivada não satisfaz checklist. Abrir link externo com proteção adequada e indicação de novo destino; não afirmar que o conteúdo do link foi validado automaticamente.

**Realizar revisão:** mostrar snapshot atual, pendências, data, participantes e observações. Ações “Registrar pendências” e “Concluir revisão” dependem das permissões. Conclusão informa próxima data calculada; pendência não renova prazo. Exibir autor/data de validação de processo/criticidade e aviso quando o valor mudou desde a validação.

**Risco:** formulário de impacto, probabilidade e exposição, escala vigente e justificativa. Prévia pode ajudar a pessoa, mas resultado confirmado vem do backend. Exibir score, faixa, data, avaliador e versão da política. Sem avaliação não é risco baixo. Coleta automática é futura.

## 10. Dashboard executivo

Grupos de cards e gráficos do §31:

- Inventário: total e distribuição por status, incluindo descontinuadas.
- Criticidade: baixa, média, alta e crítica.
- Governança: owners, documentação, dependências, revisão e classificação ausente em eventual base legada.
- Operação: saúde, erros e sem execução, com janela e exclusão de descontinuadas indicada.
- Risco: baixo, médio, alto, crítico e sem avaliação.

Filtros de área/processo/status preservam a mesma semântica da listagem. Cada gráfico tem valores textuais/tabela alternativa. Exibir instante de atualização e permitir recarregar. Se um grupo falhar, mostrar falha nesse grupo; não preencher com zero. Nenhum número demonstrativo permanece fixo na tela de produção.

## 11. Relatórios, administração e auditoria

**Relatórios:** selecionar tipo (inventário, críticas, área, owner, dependências, riscos, auditoria, versões, incidentes, execuções ou governança), formato CSV/XLSX/PDF e filtros. Confirmar o recorte e iniciar job. Estados: aguardando, gerando, concluído com download, falhou com referência de erro e expirado com gerar novamente. Mostrar validade do arquivo. Download depende das permissões atuais e não é link público.

**Administração:** cadastros com busca, criar, editar e inativar. Usuários permitem vincular identidade, roles e escopos; owners sem login são possíveis. Antes de inativar responsável/equipe, mostrar automações afetadas e exigir motivo/confirmar impacto. Não apagar pessoas referenciadas. Impedir remover último administrador ativo.

Parâmetros mostram valores atuais e nova versão de política: risco, saúde, revisão, inatividade e checklist. Validar intervalos sem sobreposição e avisar que avaliações históricas preservam a política original. Não expor parâmetros que não tenham suporte no backend.

**Auditoria:** filtros por ator, entidade, ação e período; detalhe com campos anteriores/novos e motivo. Somente leitura para todos os perfis. Exportação exige permissões correspondentes. “Alterar qualquer informação” do administrador não inclui reescrever auditoria.

## 12. Status, exclusão lógica e restauração

Alterar status pede motivo e explica que registra situação operacional já existente. Proposta de transições: qualquer status para outro, respeitando invariantes e autorização; retorno de DESCONTINUADA exige confirmação de retomada. Mesmo status não cria alteração fictícia. Não existe estado de desenvolvimento.

Excluir logicamente é ação administrativa separada, com motivo obrigatório. Havendo dependentes, apresentar impacto e exigir confirmação adicional. Registro sai das listas comuns e permanece em consulta histórica administrativa/auditoria. Restauração valida dados atuais e pode exigir saneamento de owners antes de concluir; API deve permitir correção administrativa de registro excluído sob acesso explícito. Não oferecer exclusão definitiva.

## 13. Acessibilidade e comportamento responsivo

Usar HTML semântico, labels associados, navegação integral por teclado, foco visível e mensagens anunciáveis. Diálogos gerenciam foco e o devolvem ao acionador ao fechar. Tabelas têm cabeçalhos; gráficos/grafo possuem alternativa textual. Contraste deve ser validado com a paleta escolhida; cor não é informação exclusiva.

Em telas estreitas, recolher menu, permitir formulários em uma coluna e tabela com rolagem horizontal identificada ou cartões equivalentes, preservando código/nome/status. Ações primárias permanecem alcançáveis. Não ocultar erros em seções fechadas: abrir a seção e focar o primeiro campo inválido.

Componentes reutilizáveis: seletor remoto paginado, filtro, tabela, badge de domínio, campo de URL, histórico de alterações, formulário de motivo, diálogo de confirmação, estados vazio/erro e cards com links de filtro.

## 14. Fluxos de aceite e testes de interface

| Fluxo | Resultado esperado |
| --- | --- |
| Login → Inventário | Apenas recursos autorizados; sessão inválida não expõe dados |
| Cadastro válido → Resumo | Código gerado, versão inicial atual e revisão agendada |
| Cadastro ALTA/CRITICA sem backup | Erro no campo e nenhuma gravação parcial |
| Edição por técnico/negócio | Somente campos permitidos; tentativa direta à API também rejeitada |
| Edição concorrente | Aviso de conflito sem sobrescrever mudança alheia |
| Dependência → Grafo → Sistema → Impacto | Mesmos vínculos e sentido das setas; escopo preservado |
| Registrar versão → Definir atual → Auditoria | Ponteiro atualizado, motivo e histórico visíveis |
| Execução → Operação | Duração/sucesso coerentes; sem comando de execução externa |
| Incidente → Resolver → Reabrir | Datas/estado válidos e trilha preservada |
| Revisão pendente → Concluída | Só conclusão renova prazo |
| Inativar owner → Governança | Ativo aparece órfão e nome histórico permanece |
| Filtrar → Exportar → Baixar | Relatório corresponde ao recorte autorizado; acesso revogado bloqueia download |
| Descontinuar / Excluir logicamente | Comportamentos distintos e histórico preservado |
| Teclado e tela estreita | Jornadas críticas utilizáveis, foco e erros compreensíveis |

Usar dados fictícios do §56 e casos adicionais de ausência de execução, revisão vencida, owner inativo e incidente aberto. Verificar estados vazio/erro/sem permissão além do caminho de sucesso. Critérios são para a implementação futura; este documento não afirma que testes já foram executados na aplicação.

Baseline de governança para implementação: DEC-008 em [decisions.md](decisions.md), com fórmulas e limites definidos na arquitetura. Valores configuráveis não equivalem a política corporativa já homologada.
