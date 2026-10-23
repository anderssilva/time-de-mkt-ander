---
name: estruturar-marketing-empresa
description: Implanta o departamento de marketing de uma empresa, do diagnóstico até as rotinas, criando a pasta da empresa, o contexto, a identidade, a estratégia, o plano trimestral, a planilha de registro e o guia de operação. Use quando o usuário pedir para estruturar, implantar, montar ou configurar o marketing de uma empresa, "começar o marketing da X", "montar o departamento de marketing", "replicar o modelo para outra empresa", retomar uma implantação ou fazer a revisão trimestral da estrutura. É a skill de entrada: ela chama a briefing-empresa e prepara o terreno para as skills de operação (radar, produção, agendamento, métricas).
---

# Estruturar o marketing de uma empresa

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

## Objetivo

Deixar uma empresa com o marketing pronto para rodar toda semana: pasta organizada, contexto completo, identidade visual e verbal, estratégia, plano do trimestre, registro do que já foi publicado e rotinas definidas. Ao final, o responsável pela empresa (sócio ou CEO) consegue operar sozinho seguindo o `LEIA-ME.md` da pasta.

Esta skill roda **uma vez por empresa** e é revisitada **a cada trimestre**. O trabalho semanal fica com as skills de operação.

## Onde as coisas ficam

- **Pasta da empresa = a pasta do projeto.** As pastas do marketing (`00-contexto/`, `01-plano/` etc.) são criadas **diretamente** na pasta da empresa, que normalmente é a pasta onde o Claude Code foi aberto (por exemplo, `Marketing-Sellou/`). **Não crie** pastas intermediárias como `empresas/` ou `<nome-da-empresa>/`.
- Se a pasta atual não for adequada (tem arquivos de outro projeto ou de outra empresa), pergunte em qual pasta criar e sugira abrir o Claude Code nela.
- Modelo: `${CLAUDE_PLUGIN_ROOT}/modelos/empresa/` (modelo que vem no plugin mkt). Nunca edite o modelo durante uma implantação; copie.
- Nome curto da empresa (slug): minúsculas, sem acento, com hífen (ex.: `padaria-central`). Ele vai só no `status-implantacao.md` e nos nomes de arquivos, não vira pasta.
- Trabalhe **somente** dentro da pasta da empresa em implantação. Não leia nem altere a pasta de outra empresa, salvo pedido explícito.
- Pastas antigas no formato `Marketing/empresas/<nome>/` continuam funcionando: basta abrir o Claude Code dentro delas.
- Todos os comandos dos programas (`registro.py`, `verificar-atualizacao.py`) rodam de dentro da pasta da empresa, por isso o caminho da empresa neles é `.`.

Estrutura esperada, direto na pasta da empresa (se o modelo não for encontrado, crie esta):
```
<pasta da empresa>/
├── LEIA-ME.md               guia de operação do responsável
├── status-implantacao.md    andamento desta skill
├── 00-contexto/             diagnostico, contexto-ia, design, estilo-video, tom-de-voz, provas, compliance, fotos/fotos.md
├── 01-plano/                estrategia, plano-AAAA-Tn, rotinas
├── 02-pautas/               pautas-AAAA-Sxx.md (radar semanal)
├── 03-producao/             AAAA-MM/Sxx_Pnnn_tema-curto/
├── 04-metricas/             leitura-AAAA-MM.md
└── registro/                publicacoes.csv, ideias.csv, plano.csv, melhorias.csv
```

## Regras de ouro

1. **Material existente primeiro.** No início de cada etapa, pergunte se já existe material (manual de marca, apresentações, textos antigos, planilhas, fotos, exportações das redes). Aproveite antes de criar do zero.
2. **Uma etapa por vez, com aprovação.** Ao final de cada etapa, mostre um resumo curto do que foi gravado e peça "ok" antes de seguir. Atualize o `status-implantacao.md` sempre.
3. **Nunca invente.** Número, case, depoimento, preço ou resultado só entra se o usuário disse ou se está em material fornecido. O que faltar fica marcado como `(não informado)` ou `(a confirmar)`.
4. **O arquivo é a memória.** Tudo o que for decidido vai para um arquivo da pasta. Não dependa do histórico da conversa.
5. **Português do Brasil.** Evite palavras em inglês; quando usar, coloque o significado prático entre parênteses.
6. **Nada é publicado ou agendado** nesta skill. Ela prepara; quem publica são as rotinas, sempre com aprovação.

## Passo 0. Versão do time de marketing
Antes de tudo, rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verificar-atualizacao.py"`. Se houver versão nova, mostre o que mudou e pergunte uma vez se atualiza antes de continuar. Com o ok: `--aplicar`, o usuário digita `/reload-plugins` e diz "continua". Se a pasta da empresa já existir (retomada), rode em seguida `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atualizar-pasta.py" . --aplicar` e mostre o que mudou. Sem internet, siga normalmente.

Se for a primeira vez neste computador, confira também as configurações iniciais (idioma em português e atualização automática) seguindo a skill atualizar-time.

## Retomada

Antes de continuar, verifique se `status-implantacao.md` existe na pasta da empresa.
- Se existir: leia, diga em 3 linhas onde parou e pergunte se continua dali.
- Se a última implantação tiver mais de 3 meses: ofereça a **revisão trimestral** (etapas 1, 4, 5 e 8, mais a atualização do briefing).

## Etapas

### Etapa 0. Preparação da pasta
1. Confirme o nome da empresa, o nome curto (slug) e a pasta: "Vou criar a estrutura do marketing direto nesta pasta: `<caminho atual>`. Pode ser?"
2. Copie o **conteúdo** de `${CLAUDE_PLUGIN_ROOT}/modelos/empresa/` para dentro da pasta da empresa (sem criar subpasta com o nome da empresa e sem sobrescrever arquivos que já existam).
3. Preencha o cabeçalho do `status-implantacao.md`, incluindo a **Versão do modelo** (a `version` de `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`), e marque a etapa 0 como concluída.

### Etapa 1. Diagnóstico (arquivo `00-contexto/diagnostico.md`)
Siga **exatamente** o passo a passo de `referencias/diagnostico.md` (nesta pasta da skill): um bloco por vez, sempre com exemplos e opções de múltipla escolha.
- **A. Objetivo** do marketing nos próximos 3 meses (um principal e até dois secundários, com exemplos), por que agora e como saber que deu certo.
- **B. Qual jogo a empresa joga:** monopólio, oligopólio, competição com diferenciação ou competição pura; número de concorrentes; por que ganha cliente.
- **C. Modelo de crescimento:** pelo produto, pelo marketing ou pelo vendedor (com perguntas de apoio sobre ciclo, valor médio e reunião).
- **D. Maturidade nos 4 pilares de receita** (Marca, Demanda, Vendas, Dados), nota de 0 a 2 por item.
- **E. Canais, operação, ferramentas e material** (Metricool: qual conta/e-mail; Canva; outras).
Feche com os 3 principais gargalos, nas palavras do usuário.

### Etapa 2. Briefing (arquivo `00-contexto/contexto-ia.md`)
Acione a skill **briefing-empresa**, informando que o arquivo final deve ser salvo em `00-contexto/contexto-ia.md`. Se já houver um contexto-ia.md da empresa em outro lugar, use-o como ponto de partida.

### Etapa 3. Identidade
Preencha, nesta ordem (design primeiro, porque o estilo de vídeo herda cores, fontes e elementos dele):
- **`design.md`:** siga **exatamente** o passo a passo de `referencias/design.md` (nesta pasta da skill): material existente primeiro → referências de estilo no **Refero Styles** (https://styles.refero.design/), sempre mostrando o link ao usuário → tradução em regras, item a item → amostra visual com duas lâminas → gravação do `design.md` e do `carrossel-marca.json`.
- **`estilo-video.md`:** o padrão do time é **gravação + motion graphics** (textos, números, listas e telas animados por cima do vídeo). Siga **exatamente** o passo a passo de `referencias/estilo-video.md` (nesta pasta da skill): vídeo próprio, se houver → referências de animação no **What Ships** (https://whatships.com/), sempre mostrando o link ao usuário → tradução em regras, item a item → amostra de estilo de 5 a 8 segundos → gravação do arquivo.
- **`tom-de-voz.md`:** peça 3 textos reais que representam a marca e 1 que não representa. Extraia o padrão (frases, tratamento, expressões) e mostre para confirmação.
- **`provas.md`:** transfira números e cases do briefing; para cada um, pergunte a fonte e se há autorização para citar.
- **`compliance.md`:** transfira do briefing e aprofunde com perguntas específicas do setor (exemplos: investimentos — oferta a investidores e promessa de rentabilidade; energia — regras do setor e promessa de economia; saúde — regras do conselho profissional e proibição de antes e depois; alimentos — alegações nutricionais).
- **`fotos/fotos.md`:** peça de 15 a 20 fotos reais (pessoas da empresa, bastidores, eventos). Para cada foto colocada na pasta, preencha uma linha do índice. Não altere rosto ou corpo com IA.

### Etapa 4. Estratégia (arquivo `01-plano/estrategia.md`)
Primeiro, o **pilar de crescimento do trimestre**: siga `referencias/pilar-crescimento.md` (nesta pasta da skill). A IA avalia (não pergunta) com base nos blocos A a D do diagnóstico e no briefing, propõe **um** pilar foco (Marca, Demanda, Vendas ou Dados) com o porquê, as ações e as estratégias do jogo, e pede validação. Os itens abaixo derivam desse foco.

Depois, proponha, com base no diagnóstico, no briefing e no pilar foco, e peça validação:
- **3 a 5 pilares de conteúdo**, com o porquê e a porcentagem do conteúdo (pelo menos 40% servindo ao pilar de crescimento).
- **Funil:** o que cada estágio faz, em qual canal, em qual formato e com qual chamada para ação (a padrão vem do modelo de crescimento).
- **Metas do trimestre:** pelo menos uma de entrada (alcance, salvamentos, seguidores qualificados) e uma de saída (contatos, reuniões, vendas). Peça o valor atual antes de propor a meta.
- **Cadência realista:** proporcional ao tempo semanal declarado. Com até 2 horas por semana, não proponha mais de 3 peças por semana.
- Lembre que o **Metricool Free** agenda uma marca e **não tem LinkedIn**: o LinkedIn entra como publicação manual.

### Etapa 5. Plano trimestral (arquivo `01-plano/plano-AAAA-Tn.md`)
- Renomeie o modelo para o trimestre corrente (ex.: `plano-2026-T4.md`).
- Para cada um dos 3 meses: tema do mês, pilar foco, peça-mãe (o conteúdo principal do qual saem os derivados), derivados e datas relevantes do setor.
- Se for revisão, preencha antes a seção "Revisão do trimestre anterior" com base em `04-metricas/` e na planilha.

### Etapa 6. Registro e histórico
1. **Escolha onde guardar.** Pergunte: "Prefere o registro numa **Planilha Google com link** (a equipe vê e edita pelo navegador ou celular) ou nos **arquivos da pasta**?"
   - **Planilha Google:** siga a seção "Implantação" de `${CLAUDE_PLUGIN_ROOT}/referencias/registro-planilhas.md` (cria a planilha com as quatro abas, define o compartilhamento escolhido e registra o link). Requer o conector do Google Planilhas.
   - **Arquivos da pasta:** os quatro CSV em `registro/` são a fonte oficial e sincronizam pelo Drive; para ver, abra no Google Planilhas e não edite com o Excel.
   Em ambos os casos, crie o registro local (de dentro da pasta da empresa):
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py" iniciar .`
2. **Importe o histórico** dos últimos 6 meses, por um destes caminhos (pergunte qual):
   - exportação de dados feita pelo usuário na própria rede social;
   - leitura pelo conector do Metricool (se já conectado);
   - leitura do perfil pelo navegador, com a conta do usuário logada e com a autorização dele.
3. Para cada publicação antiga, grave uma linha com `registro.py adicionar . publicacoes '{...}'`, com pelo menos: data_publicacao, canal, formato, **gancho**, **angulo**, resumo, link e status "publicado", em ordem de data (os ids P001, P002… são gerados sozinhos). Gancho e ângulo são o que evita repetir conteúdo.
4. Grave na aba plano os 3 meses do plano trimestral (`registro.py adicionar . plano '{...}'`).
5. No modo Planilha Google, termine com o passo **Enviar** da referência e confira as quatro abas.

### Etapa 7. Ferramentas e rotinas (arquivo `01-plano/rotinas.md`)
1. **Metricool:** confirme que a conta está no e-mail da empresa (não no pessoal de um sócio), que a marca foi criada e quais redes estão conectadas. Se o conector do Metricool estiver disponível, teste listando as marcas.
2. **Canva:** confirme se será usado para ajustes manuais dos carrosséis.
3. **Rotinas:** ajuste a tabela do modelo (dias, horários, quem aprova). Pergunte quais devem virar tarefa agendada. Crie tarefas agendadas **somente** com aprovação explícita, e explique que, para ler a pasta do computador, o computador precisa estar ligado com o app do Claude aberto.

### Etapa 8. Passagem e validação
1. Preencha o `LEIA-ME.md` da empresa: responsável, datas, links, a semana típica e os pedidos de exemplo.
2. Rode o checklist abaixo e mostre o resultado.
3. Marque a implantação como concluída no status e registre a data da próxima revisão (3 meses).
4. Sugira o primeiro passo da operação: rodar o radar de pautas da semana.

## Checklist de validação

- [ ] `contexto-ia.md` sem campos essenciais vazios (nome, setor, proposta de valor, perfil 1, dor comum, produto, tom principal, o que não pode dizer)
- [ ] `design.md` com cores em hex, fonte, arquivos de logo localizados, referências (Refero) e amostra visual aprovada
- [ ] `tom-de-voz.md` com pelo menos 3 textos de referência reais
- [ ] `provas.md` com fonte e autorização em cada linha
- [ ] `compliance.md` preenchido ou marcado "validar com o responsável"
- [ ] `diagnostico.md` com objetivo, jogo, modelo de crescimento e notas dos 4 pilares
- [ ] Estratégia com pilar de crescimento validado, pilares de conteúdo, funil, metas com valor atual e cadência
- [ ] Plano do trimestre com os 3 meses preenchidos
- [ ] `estilo-video.md` com 2 ou 3 referências de motion graphics, tabela de regras aprovada e amostra de estilo aprovada (ou marcada como pendente)
- [ ] Registro iniciado (Planilha Google com link ou CSV), histórico importado com gancho e ângulo, plano do trimestre na aba plano
- [ ] Metricool na conta da empresa, marca criada, redes conectadas
- [ ] Rotinas definidas (e agendadas, se aprovado)
- [ ] `LEIA-ME.md` pronto para o responsável operar sozinho

## Convenções que as skills de operação usam

- **Peça:** número `Pnnn` sequencial por empresa, igual ao `id` em `registro/publicacoes.csv`. Ideias usam `Innn`; melhorias, `Mnnn`.
- **Pasta da peça:** `03-producao/AAAA-MM/Sxx_Pnnn_tema-curto/` (Sxx = semana do ano).
- **Pautas da semana:** `02-pautas/pautas-AAAA-Sxx.md`.
- **Leitura mensal:** `04-metricas/leitura-AAAA-MM.md`.
- **Status da peça:** ideia → aprovado → em produção → em revisão → pronto → agendado → publicado (ou descartado).
- **Ferramenta de registro:** `${CLAUDE_PLUGIN_ROOT}/scripts/registro.py` (iniciar, proximo, adicionar, atualizar, listar, repeticao, melhoria-parecida; no modo Planilha Google também fonte, espelhar, pendentes e sincronizado).
- **Registro em Planilha Google:** toda rotina começa com **Baixar** e termina com **Enviar** (`${CLAUDE_PLUGIN_ROOT}/referencias/registro-planilhas.md`). O `registro.py` avisa quando faltar um dos dois.
- **Jornada e skills de operação:** radar-pautas → estrategista-marketing (seleção) → roteiro-video / carrossel → editar-reels → controle-qualidade → estrategista-marketing (revisão final) → ok do responsável → agendar-publicacao → leitura-metricas. A skill rodar-semana-marketing conduz tudo na ordem.
- **Regra de saída:** nada vai ao ar sem controle de qualidade aprovado, estrategista aprovado e ok do responsável.
