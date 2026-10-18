---
name: estruturar-marketing-empresa
description: Implanta o departamento de marketing de uma empresa do grupo (ZUCCHI, ConselhoPRO, 3Hub Capital, Sellou, Carbon Smart ou outra), do diagnóstico até as rotinas, criando a pasta da empresa, o contexto, a identidade, a estratégia, o plano trimestral, a planilha de registro e o guia de operação. Use quando o usuário pedir para estruturar, implantar, montar ou configurar o marketing de uma empresa, "começar o marketing da X", "montar o departamento de marketing", "replicar o modelo para outra empresa", retomar uma implantação ou fazer a revisão trimestral da estrutura. É a skill de entrada: ela chama a briefing-empresa e prepara o terreno para as skills de operação (radar, produção, agendamento, métricas).
---

# Estruturar o marketing de uma empresa

## Objetivo

Deixar uma empresa com o marketing pronto para rodar toda semana: pasta organizada, contexto completo, identidade visual e verbal, estratégia, plano do trimestre, registro do que já foi publicado e rotinas definidas. Ao final, o responsável pela empresa (sócio ou CEO) consegue operar sozinho seguindo o `LEIA-ME.md` da pasta.

Esta skill roda **uma vez por empresa** e é revisitada **a cada trimestre**. O trabalho semanal fica com as skills de operação.

## Onde as coisas ficam

- Pasta-raiz do marketing: a pasta `Marketing` (sincronizada no Google Drive do usuário). Se não souber onde está, pergunte.
- Modelo: `${CLAUDE_PLUGIN_ROOT}/modelos/empresa/` (modelo que vem no plugin mkt). Nunca edite o modelo durante uma implantação; copie.
- Empresa: `Marketing/empresas/<slug>/` (slug em minúsculas, sem acento, com hífen: `conselhopro`, `zucchi`, `3hub-capital`, `sellou`, `carbon-smart`).
- Trabalhe **somente** dentro da pasta da empresa em implantação. Não leia nem altere a pasta de outra empresa, salvo pedido explícito.

Estrutura esperada (se o modelo não for encontrado, crie esta):
```
empresas/<slug>/
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

## Retomada

Antes de tudo, verifique se `empresas/<slug>/status-implantacao.md` existe.
- Se existir: leia, diga em 3 linhas onde parou e pergunte se continua dali.
- Se a última implantação tiver mais de 3 meses: ofereça a **revisão trimestral** (etapas 1, 4, 5 e 8, mais a atualização do briefing).

## Etapas

### Etapa 0. Preparação da pasta
1. Confirme o nome da empresa e o slug.
2. Copie `${CLAUDE_PLUGIN_ROOT}/modelos/empresa/` para `empresas/<slug>/` (sem sobrescrever arquivos que já existam).
3. Preencha o cabeçalho do `status-implantacao.md` e marque a etapa 0 como concluída.

### Etapa 1. Diagnóstico (arquivo `00-contexto/diagnostico.md`)
Pergunte, em blocos curtos:
- **Objetivo principal** do marketing agora: gerar contatos, construir autoridade, vender direto ou outro. Peça para escolher **um**.
- **Canais atuais:** links, frequência, o que funcionou e o que não funcionou.
- **Operação:** quem opera, quanto tempo por semana, quem aprova, se grava vídeo, orçamento de mídia paga.
- **Ferramentas:** Metricool (qual conta/e-mail), Canva, outras.
- **Material existente.**
Feche com os 3 principais gargalos, nas palavras do usuário.

### Etapa 2. Briefing (arquivo `00-contexto/contexto-ia.md`)
Acione a skill **briefing-empresa**, informando que o arquivo final deve ser salvo em `00-contexto/contexto-ia.md`. Se já houver um contexto-ia.md da empresa em outro lugar, use-o como ponto de partida.

### Etapa 3. Identidade
Preencha, nesta ordem:
- **`design.md`:** se houver manual de marca ou `design.md` antigo (inclusive em .docx), converta para o modelo. Se não houver, entreviste: cores (com código hex), fonte, versões do logo e onde ficam os arquivos, elementos gráficos, formatos padrão. Mostre as cores e a fonte numa amostra visual simples para validação.
- **`estilo-video.md`:** peça um vídeo antigo que represente bem a empresa (de preferência o arquivo original). Olhe uma folha de quadros e descreva com o usuário: logo e posição, legendas (tamanho, posição, cor de destaque), cartela de abertura e de encerramento, ritmo, zoom, música, CTA padrão. Se a marca mudou desde o vídeo, use a marca atual e aproveite só o formato.
- **`tom-de-voz.md`:** peça 3 textos reais que representam a marca e 1 que não representa. Extraia o padrão (frases, tratamento, expressões) e mostre para confirmação.
- **`provas.md`:** transfira números e cases do briefing; para cada um, pergunte a fonte e se há autorização para citar.
- **`compliance.md`:** transfira do briefing e aprofunde com perguntas específicas do setor (exemplos: 3Hub Capital — ofertas a investidores e promessa de rentabilidade; Carbon Smart — regras do setor de energia e promessa de economia).
- **`fotos/fotos.md`:** peça de 15 a 20 fotos reais (pessoas da empresa, bastidores, eventos). Para cada foto colocada na pasta, preencha uma linha do índice. Não altere rosto ou corpo com IA.

### Etapa 4. Estratégia (arquivo `01-plano/estrategia.md`)
Proponha, com base no diagnóstico e no briefing, e peça validação:
- **3 a 5 pilares de conteúdo**, com o porquê e a porcentagem do conteúdo.
- **Funil:** o que cada estágio faz, em qual canal, em qual formato e com qual chamada para ação.
- **Metas do trimestre:** pelo menos uma de entrada (alcance, salvamentos, seguidores qualificados) e uma de saída (contatos, reuniões, vendas). Peça o valor atual antes de propor a meta.
- **Cadência realista:** proporcional ao tempo semanal declarado. Com até 2 horas por semana, não proponha mais de 3 peças por semana.
- Lembre que o **Metricool Free** agenda uma marca e **não tem LinkedIn**: o LinkedIn entra como publicação manual.

### Etapa 5. Plano trimestral (arquivo `01-plano/plano-AAAA-Tn.md`)
- Renomeie o modelo para o trimestre corrente (ex.: `plano-2026-T4.md`).
- Para cada um dos 3 meses: tema do mês, pilar foco, peça-mãe (o conteúdo principal do qual saem os derivados), derivados e datas relevantes do setor.
- Se for revisão, preencha antes a seção "Revisão do trimestre anterior" com base em `04-metricas/` e na planilha.

### Etapa 6. Registro e histórico
1. Crie as planilhas da empresa (a partir da pasta Marketing):
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py" iniciar empresas/<slug>`
   São quatro CSV em `registro/` (publicações, ideias, plano, melhorias). Elas são a fonte oficial e sincronizam pelo Google Drive; para ver, o usuário abre no Google Planilhas. Explique que não deve editar com o Excel.
2. **Importe o histórico** dos últimos 6 meses, por um destes caminhos (pergunte qual):
   - exportação de dados feita pelo usuário na própria rede social;
   - leitura pelo conector do Metricool (se já conectado);
   - leitura do perfil pelo navegador, com a conta do usuário logada e com a autorização dele.
3. Para cada publicação antiga, grave uma linha com `registro.py adicionar empresas/<slug> publicacoes '{...}'`, com pelo menos: data_publicacao, canal, formato, **gancho**, **angulo**, resumo, link e status "publicado", em ordem de data (os ids P001, P002… são gerados sozinhos). Gancho e ângulo são o que evita repetir conteúdo.
4. Grave na aba plano os 3 meses do plano trimestral (`registro.py adicionar empresas/<slug> plano '{...}'`).

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
- [ ] `design.md` com cores em hex, fonte e arquivos de logo localizados
- [ ] `tom-de-voz.md` com pelo menos 3 textos de referência reais
- [ ] `provas.md` com fonte e autorização em cada linha
- [ ] `compliance.md` preenchido ou marcado "validar com o responsável"
- [ ] Estratégia com pilares, funil, metas com valor atual e cadência
- [ ] Plano do trimestre com os 3 meses preenchidos
- [ ] `estilo-video.md` preenchido a partir de um vídeo de referência
- [ ] Registro iniciado, histórico importado com gancho e ângulo, plano do trimestre na aba plano
- [ ] Metricool na conta da empresa, marca criada, redes conectadas
- [ ] Rotinas definidas (e agendadas, se aprovado)
- [ ] `LEIA-ME.md` pronto para o responsável operar sozinho

## Convenções que as skills de operação usam

- **Peça:** número `Pnnn` sequencial por empresa, igual ao `id` em `registro/publicacoes.csv`. Ideias usam `Innn`; melhorias, `Mnnn`.
- **Pasta da peça:** `03-producao/AAAA-MM/Sxx_Pnnn_tema-curto/` (Sxx = semana do ano).
- **Pautas da semana:** `02-pautas/pautas-AAAA-Sxx.md`.
- **Leitura mensal:** `04-metricas/leitura-AAAA-MM.md`.
- **Status da peça:** ideia → aprovado → em produção → em revisão → pronto → agendado → publicado (ou descartado).
- **Ferramenta de registro:** `${CLAUDE_PLUGIN_ROOT}/scripts/registro.py` (iniciar, proximo, adicionar, atualizar, listar, repeticao, melhoria-parecida).
- **Jornada e skills de operação:** radar-pautas → estrategista-marketing (seleção) → roteiro-video / carrossel → editar-reels → controle-qualidade → estrategista-marketing (revisão final) → ok do responsável → agendar-publicacao → leitura-metricas. A skill rodar-semana-marketing conduz tudo na ordem.
- **Regra de saída:** nada vai ao ar sem controle de qualidade aprovado, estrategista aprovado e ok do responsável.
