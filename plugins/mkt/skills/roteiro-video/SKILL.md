---
name: roteiro-video
description: Escreve o roteiro de Reels, TikTok ou Shorts (30 a 90 segundos) de uma peça aprovada, na voz e no estilo da empresa, com orientações de gravação, legenda do post e texto derivado para LinkedIn. Use quando o usuário pedir roteiro de vídeo, roteiro de Reels, "escreve o vídeo da P012", texto para gravar, ou quando a skill rodar-semana-marketing chamar a etapa de roteiro. Vale para qualquer empresa com o marketing implantado.
---

# Roteiro de vídeo curto

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

## Antes de começar
1. Trabalhe dentro da **pasta da empresa** (a pasta onde o Claude Code foi aberto, que tem `00-contexto/` e `registro/`). Se a pasta atual não for de uma empresa, pergunte qual é. Identifique a peça (Pnnn). A peça precisa estar com status "aprovado" em `registro/publicacoes.csv`; se não estiver, pergunte se deve seguir mesmo assim.
2. Leia: `contexto-ia.md`, `tom-de-voz.md`, `estilo-video.md`, `provas.md`, `compliance.md`, `01-plano/estrategia.md` (funil e CTA) e as melhorias incorporadas.
3. Pergunte se o responsável tem material para a peça (um vídeo de referência, um caso, uma tela para mostrar). Se houver vídeo de referência de outro criador, aproveite o gancho e a estrutura, nunca o conteúdo: o valor está na experiência da empresa.
- Ferramenta de registro: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py"` (abreviada abaixo como `registro.py`), sempre de dentro da pasta da empresa (o caminho da empresa nos comandos é `.`).

## Regras do roteiro
- Duração alvo de 30 a 60 segundos (até 90 se o conteúdo pedir). Fala natural: cerca de 140 palavras por minuto.
- **Gancho nos 3 primeiros segundos:** uma frase que crie tensão, curiosidade ou promessa concreta. Proponha 2 opções.
- Uma ideia por vídeo. Frases curtas, como se fala, não como se escreve.
- **Mais ação que dor:** o problema ocupa no máximo os primeiros 20% do vídeo. O resto é como fazer, com pelo menos um exemplo concreto (uma frase-modelo, um caso, um número de referência).
- Indique onde entram telas, provas, cartelas ou números (só de `provas.md`).
- Um CTA só, coerente com o estágio do funil (ex.: "comente PALAVRA", "salve", "link na bio").
- Respeite o tom proibido e as palavras proibidas.

## Validar em duas rodadas curtas
1. **Esqueleto (aprovação 1):** mostre 2 opções de gancho e uma linha por bloco (`Bloco 2 · Ação 1 · enviar a pauta 48 h antes · ~10 s`), com a duração total estimada e o CTA. **Espere.** Não escreva a fala completa ainda.
2. **Fala bloco a bloco (aprovação 2):** com o esqueleto aprovado, escreva a fala completa de cada bloco, numerada. Ao ajustar, reescreva e mostre **só os blocos citados**.
3. Só depois da fala aprovada escreva a legenda do post e o derivado para LinkedIn, numa mensagem só.

## Arquivo `roteiro.md` (na pasta da peça)
```
# Pnnn — [tema]
Empresa · Pilar · Estágio do funil · Duração alvo · CTA

## Gancho (escolher 1)
A) ...
B) ...

## Roteiro
| Bloco | Fala (exatamente como gravar) | Visual (tela, prova, cartela, zoom) | Tempo estimado |
|---|---|---|---|
| Gancho | | | 0–3 s |
| Desenvolvimento 1 | | | |
| ... | | | |
| CTA | | | |

## Orientações de gravação
- Enquadramento e cenário conforme estilo-video.md
- Gravar cada bloco 2 vezes, com 2 segundos de silêncio antes e depois
- Olhar para a lente; microfone de lapela; luz de frente
- Salvar os arquivos em video-bruto/ dentro desta pasta

## Legenda do post
(primeira linha forte; até 2.200 caracteres; CTA; 3 a 5 hashtags do setor)

## Derivado para LinkedIn (publicação manual)
(texto de 800 a 1.300 caracteres, primeira linha forte, sem hashtags em excesso, em primeira pessoa do sócio quando fizer sentido)
```

## Depois de escrever
1. Grave o `roteiro.md` só com tudo aprovado (gancho escolhido, fala, legenda e LinkedIn).
2. Com a aprovação: crie a pasta `video-bruto/` na peça, atualize a planilha (`registro.py atualizar . publicacoes Pnnn '{"gancho": "<final>", "cta": "...", "status": "em produção"}'`) e avise que o próximo passo é gravar e soltar os arquivos em `video-bruto/`.
3. Depois da gravação, a skill **editar-reels** assume.
