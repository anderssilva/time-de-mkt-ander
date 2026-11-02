---
name: leitura-metricas
description: Lê os resultados das publicações de uma empresa (pelo Metricool ou por exportação), atualiza o registro e produz a leitura semanal ou mensal com aprendizados e melhorias propostas. Use quando o usuário pedir métricas, resultados, desempenho, "como foram os posts", "leitura do mês", relatório de marketing, ou quando a skill rodar-semana-marketing chegar à etapa de métricas. Os aprendizados seguem para o estrategista-marketing (modo melhorias).
---

# Leitura de métricas

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

> **Atualização (início de toda atividade):** antes de começar, rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verificar-atualizacao.py" --rapido --intervalo 1` (rápido, silencioso quando está tudo em dia). Se avisar versão nova: mostre o que mudou e pergunte uma vez se atualiza agora. Com o ok, rode o mesmo programa com `--aplicar`, peça ao usuário para digitar `/reload-plugins` e dizer "continua", rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atualizar-pasta.py" . --aplicar` (ajusta a pasta da empresa sem apagar nada) e retome a atividade. Se ele preferir depois, rode com `--adiar 12` e siga. Se você é um cargo (agente separado), pule esta verificação: o gerente já fez.

## Antes de começar
1. Trabalhe dentro da **pasta da empresa** (a pasta onde o Claude Code foi aberto, que tem `00-contexto/` e `registro/`). Se a pasta atual não for de uma empresa, pergunte qual é. Identifique o período (semanal: últimos 7 dias; mensal: mês fechado).
2. Leia `01-plano/estrategia.md` (metas), o plano do trimestre e a leitura anterior em `04-metricas/`.
- Ferramenta de registro: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py"` (abreviada abaixo como `registro.py`), sempre de dentro da pasta da empresa (o caminho da empresa nos comandos é `.`).

## Coletar (nunca invente números)
- **Com o conector do Metricool:** busque as métricas por publicação da marca da empresa: alcance, curtidas, comentários, salvamentos, compartilhamentos, cliques, seguidores ganhos.
- **Sem conector:** peça a exportação (CSV do Metricool ou da rede) ou prints. O que não vier fica vazio, nunca estimado.
- Associe cada post a uma peça (Pnnn) pelo link ou pela data e legenda. Post sem peça no registro: crie a linha com status "publicado" e marque `origem` = "fora do fluxo".
- Atualize cada peça: `registro.py atualizar . publicacoes Pnnn '{"alcance": "...", "salvamentos": "...", ...}'`.

## Como comparar (sempre)
Rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/desempenho.py" . --dias 30` (semanal) ou `--dias 90` (mensal). Ele compara cada post com a **própria conta**, não com números brutos:
- **Múltiplo:** alcance do post ÷ alcance mediano da conta (2,0x = o dobro do normal). É o que mostra o que realmente funcionou.
- **Envios por mil de alcance:** compartilhamentos ÷ alcance. É o sinal mais forte de conteúdo que circula.
- **Salvamentos por mil de alcance:** conteúdo útil, de guardar.
Use esse ranking para escolher melhores e piores peças. Visualização bruta não decide nada.

## Leitura semanal (curta, no chat)
- Números da semana contra a média das 4 semanas anteriores.
- Melhor e pior peça da semana pelo múltiplo e pelos envios por mil de alcance, com uma hipótese para cada (gancho, formato, pilar, horário).
- Um ajuste sugerido para o próximo radar.

## Leitura mensal (`04-metricas/leitura-AAAA-MM.md`, a partir do modelo)
1. Tabela de métricas do mês contra o mês anterior e a meta da estratégia.
2. As 3 melhores e as 3 piores peças pelo `desempenho.py` (múltiplo, envios e salvamentos por mil de alcance), com hipóteses. Compare notas do estrategista e do controle de qualidade com o desempenho: as notas altas performaram melhor? Se não, os critérios precisam de ajuste.
3. Padrões: qual pilar, formato, tipo de gancho e horário vão melhor.
4. Até 3 ajustes para o próximo mês, por impacto.
5. Registre cada aprendizado como melhoria (origem "metricas"), conferindo antes com `registro.py melhoria-parecida`.
6. Encaminhe para a skill **estrategista-marketing, modo melhorias do mês**.

## Regras
- Diferencie fato (o número) de hipótese (a explicação). Use "provavelmente" quando for hipótese.
- Amostra pequena não vira regra: com menos de 4 peças comparáveis, registre como observação, não como conclusão.
