---
name: leitura-metricas
description: Lê os resultados das publicações de uma empresa (pelo Metricool ou por exportação), atualiza o registro e produz a leitura semanal ou mensal com aprendizados e melhorias propostas. Use quando o usuário pedir métricas, resultados, desempenho, "como foram os posts", "leitura do mês", relatório de marketing, ou quando a skill rodar-semana-marketing chegar à etapa de métricas. Os aprendizados seguem para o estrategista-marketing (modo melhorias).
---

# Leitura de métricas

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

## Antes de começar
1. Trabalhe dentro da **pasta da empresa** (a pasta onde o Claude Code foi aberto, que tem `00-contexto/` e `registro/`). Se a pasta atual não for de uma empresa, pergunte qual é. Identifique o período (semanal: últimos 7 dias; mensal: mês fechado).
2. Leia `01-plano/estrategia.md` (metas), o plano do trimestre e a leitura anterior em `04-metricas/`.
- Ferramenta de registro: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py"` (abreviada abaixo como `registro.py`), sempre de dentro da pasta da empresa (o caminho da empresa nos comandos é `.`).

## Coletar (nunca invente números)
- **Com o conector do Metricool:** busque as métricas por publicação da marca da empresa: alcance, curtidas, comentários, salvamentos, compartilhamentos, cliques, seguidores ganhos.
- **Sem conector:** peça a exportação (CSV do Metricool ou da rede) ou prints. O que não vier fica vazio, nunca estimado.
- Associe cada post a uma peça (Pnnn) pelo link ou pela data e legenda. Post sem peça no registro: crie a linha com status "publicado" e marque `origem` = "fora do fluxo".
- Atualize cada peça: `registro.py atualizar . publicacoes Pnnn '{"alcance": "...", "salvamentos": "...", ...}'`.

## Leitura semanal (curta, no chat)
- Números da semana contra a média das 4 semanas anteriores.
- Melhor e pior peça da semana, com uma hipótese para cada (gancho, formato, pilar, horário).
- Um ajuste sugerido para o próximo radar.

## Leitura mensal (`04-metricas/leitura-AAAA-MM.md`, a partir do modelo)
1. Tabela de métricas do mês contra o mês anterior e a meta da estratégia.
2. As 3 melhores e as 3 piores peças, com hipóteses. Compare notas do estrategista e do controle de qualidade com o desempenho: as notas altas performaram melhor? Se não, os critérios precisam de ajuste.
3. Padrões: qual pilar, formato, tipo de gancho e horário vão melhor.
4. Até 3 ajustes para o próximo mês, por impacto.
5. Registre cada aprendizado como melhoria (origem "metricas"), conferindo antes com `registro.py melhoria-parecida`.
6. Encaminhe para a skill **estrategista-marketing, modo melhorias do mês**.

## Regras
- Diferencie fato (o número) de hipótese (a explicação). Use "provavelmente" quando for hipótese.
- Amostra pequena não vira regra: com menos de 4 peças comparáveis, registre como observação, não como conclusão.
