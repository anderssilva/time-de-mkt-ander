---
name: radar-pautas
description: Pesquisa e propõe as pautas da semana para uma empresa, conferindo o plano trimestral, as métricas e o histórico para não repetir conteúdo. Use quando o usuário pedir "radar da semana", "pautas da semana", "o que vamos publicar", "ideias de conteúdo para a [empresa]", ou quando a skill rodar-semana-marketing chamar a etapa de pautas. Não escolhe as pautas finais: entrega para a skill estrategista-marketing (modo seleção).
---

# Radar de pautas

## Antes de começar
1. Trabalhe a partir da pasta `Marketing`. Identifique a empresa (`empresas/<slug>/`); se houver dúvida, pergunte. Trabalhe só nela.
2. Se não existirem `00-contexto/contexto-ia.md` e `01-plano/estrategia.md`, pare e sugira a skill estruturar-marketing-empresa.
3. Leia: `contexto-ia.md`, `tom-de-voz.md`, `compliance.md`, `01-plano/estrategia.md`, o plano do trimestre atual (`01-plano/plano-AAAA-Tn.md`), a última leitura em `04-metricas/` e as melhorias aprovadas ou incorporadas (`registro.py listar empresas/<slug> melhorias`).
4. Defina a semana no formato `AAAA-Sxx` (semana do ano, padrão ISO). Padrão: a próxima semana.

## Passo 1. Entender a semana
- Tema do mês e pilar foco (do plano trimestral).
- Cadência: quantas peças por canal e formato (da estratégia).
- O que funcionou: as 3 peças com mais salvamentos e compartilhamentos nos últimos 60 dias (`registro.py listar ... publicacoes status=publicado`). Anote gancho, formato e pilar delas.
- Datas e eventos relevantes do setor na semana.

## Passo 2. Pesquisar
Use a busca na web. Para cada achado útil, guarde a fonte (link).
- Notícias e mudanças do setor nas últimas 2 semanas.
- Perguntas e dores frequentes do público prioritário (fóruns, comentários, buscas).
- Concorrentes listados no briefing: o que publicaram recentemente (só para não repetir e achar lacunas; nunca copiar).
- Se o usuário trouxer um vídeo ou post de referência, use como ponto de partida e registre a origem.

## Passo 3. Propor candidatas
Proponha o dobro da cadência semanal (ex.: cadência de 4 peças → 8 candidatas). Para cada uma:
- **Gancho:** a frase de abertura, até 12 palavras, concreta.
- **Ângulo:** a ideia específica que diferencia esta peça (o que ela defende ou ensina).
- Pilar, formato sugerido (reels, carrossel, LinkedIn), estágio do funil, por que agora, fonte.
Equilibre pilares e formatos conforme a estratégia. Nada de número, case ou depoimento que não esteja em `provas.md`.

## Passo 4. Conferir repetição (obrigatório)
Para cada candidata:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py" repeticao empresas/<slug> "<gancho>" "<ângulo>"`
- Nota ≥ 0,65 (REPETIÇÃO): troque o ângulo ou descarte. Nunca proponha repetição sem dizer.
- Nota entre 0,45 e 0,65 (atenção): mantenha só se o ângulo for realmente novo e diga qual peça é parecida (Pnnn ou Innn).

## Passo 5. Gravar
1. Crie `02-pautas/pautas-AAAA-Sxx.md` a partir de `02-pautas/_modelo-pautas-semana.md` com a tabela de candidatas (gancho, ângulo, pilar, formato, por que agora, peça parecida, fonte).
2. Registre cada candidata na aba ideias:
   `registro.py adicionar empresas/<slug> ideias '{"ideia": "...", "gancho": "...", "angulo": "...", "pilar": "...", "formato": "...", "origem": "radar AAAA-Sxx", "decisao": "proposta"}'`
3. Entregue para a skill **estrategista-marketing, modo seleção**. Se estiver no Claude Code e existir o agente `estrategista-marketing`, use-o (ele avalia sem ter visto a pesquisa).

## Regras
- Português do Brasil; termos em inglês com o significado entre parênteses.
- Pauta boa é específica e prática: "4 ajustes para a reunião de diretoria decidir" é melhor que "3 sinais de que sua reunião é perda de tempo" (só dor) ou "dicas de reunião" (genérico). Todo ângulo precisa deixar claro o que a pessoa vai conseguir fazer depois.
- Não escolha as pautas finais: isso é do estrategista e do responsável.
