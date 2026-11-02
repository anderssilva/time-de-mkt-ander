---
name: roteiro-video
description: Escreve o roteiro de Reels, TikTok ou Shorts (30 a 90 segundos) de uma peça aprovada, na voz e no estilo da empresa, com orientações de gravação, legenda do post e texto derivado para LinkedIn. Use quando o usuário pedir roteiro de vídeo, roteiro de Reels, "escreve o vídeo da P012", texto para gravar, ou quando a skill rodar-semana-marketing chamar a etapa de roteiro. Vale para qualquer empresa com o marketing implantado.
---

# Roteiro de vídeo curto

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

> **Atualização (início de toda atividade):** antes de começar, rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verificar-atualizacao.py" --rapido --intervalo 1` (rápido, silencioso quando está tudo em dia). Se avisar versão nova: mostre o que mudou e pergunte uma vez se atualiza agora. Com o ok, rode o mesmo programa com `--aplicar`, peça ao usuário para digitar `/reload-plugins` e dizer "continua", rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atualizar-pasta.py" . --aplicar` (ajusta a pasta da empresa sem apagar nada) e retome a atividade. Se ele preferir depois, rode com `--adiar 12` e siga. Se você é um cargo (agente separado), pule esta verificação: o gerente já fez.

> **Quem executa:** na conversa principal (gerente), passe o trabalho ao cargo `redator`, que roda num modelo mais leve, e mostre ao responsável o que voltar (veja `${CLAUDE_PLUGIN_ROOT}/referencias/orquestracao.md`). Se você já é esse cargo, execute.

## Antes de começar
1. Trabalhe dentro da **pasta da empresa** (a pasta onde o Claude Code foi aberto, que tem `00-contexto/` e `registro/`). Se a pasta atual não for de uma empresa, pergunte qual é. Identifique a peça (Pnnn). A peça precisa estar com status "aprovado" em `registro/publicacoes.csv`; se não estiver, pergunte se deve seguir mesmo assim.
2. Leia: `contexto-ia.md`, `tom-de-voz.md`, `estilo-video.md`, `provas.md`, `compliance.md`, `01-plano/estrategia.md` (funil e CTA) e as melhorias incorporadas.
3. Pergunte se o responsável tem material para a peça (um vídeo de referência, um caso, uma tela para mostrar). Se houver vídeo de referência de outro criador, aproveite o gancho e a estrutura, nunca o conteúdo: o valor está na experiência da empresa.
- Ferramenta de registro: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py"` (abreviada abaixo como `registro.py`), sempre de dentro da pasta da empresa (o caminho da empresa nos comandos é `.`).

## Regras do roteiro
- Duração alvo: a do `estilo-video.md` da empresa; se não houver, **até 40 segundos** (vídeos curtos retêm mais). Fala natural: cerca de 155 palavras por minuto.
- **Gancho nos 3 primeiros segundos:** proponha **3 opções de fórmulas diferentes** (`${CLAUDE_PLUGIN_ROOT}/referencias/ganchos.md`), dê nota com `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gancho.py" "<gancho 1>" "<gancho 2>" "<gancho 3>"` e mostre a nota ao lado de cada uma. Gancho com eliminatório ou abaixo de 55 não vai para o responsável: reescreva.
- Uma ideia por vídeo. Frases curtas, como se fala, não como se escreve.
- **Mais ação que dor:** o problema ocupa no máximo os primeiros 20% do vídeo. O resto é como fazer, com pelo menos um exemplo concreto (uma frase-modelo, um caso, um número de referência).
- Indique onde entram telas, provas, cartelas ou números (só de `provas.md`).
- Um CTA só, coerente com o estágio do funil (ex.: "comente PALAVRA", "salve", "link na bio").
- Respeite o tom proibido e as palavras proibidas.

## Validar em duas rodadas curtas
1. **Esqueleto (aprovação 1):** mostre 2 opções de gancho e uma linha por bloco (`Bloco 2 · Ação 1 · enviar a pauta 48 h antes · ~10 s`), com a duração total estimada e o CTA. **Espere.** Não escreva a fala completa ainda.
2. **Fala bloco a bloco (aprovação 2):** com o esqueleto aprovado, escreva a fala completa de cada bloco, numerada. Antes de mostrar:
   - rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/humanizar.py" <arquivo>` e reescreva o que tiver "cara de IA" (nota mínima 80);
   - rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tempo-roteiro.py" <arquivo> --alvo <duração alvo>` e ajuste os trechos longos, o gancho acima de 3 s e o final que não retoma o gancho;
   - mostre a folha de tempo resumida junto com a fala.
   Ao ajustar, reescreva e mostre **só os blocos citados**.
3. Só depois da fala aprovada escreva a legenda do post e o derivado para LinkedIn, numa mensagem só. Confira a legenda com `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/legenda.py" <arquivo>` (mostra o que aparece antes do "... mais", hashtags, chamada para ação, links e cara de IA) e corrija os avisos antes de mostrar.

## Arquivo `roteiro.md` (na pasta da peça)
```
# Pnnn — [tema]
Empresa · Pilar · Estágio do funil · Duração alvo · CTA

## Gancho (escolher 1)
A) ... (nota)
B) ... (nota)
C) ... (nota)

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
(primeira linha forte, que segura sozinha nos 125 caracteres antes do "... mais"; até 2.200 caracteres; uma chamada para ação; até 3 hashtags específicas; sem link na legenda)

## Derivado para LinkedIn (publicação manual)
(texto de 800 a 1.300 caracteres, primeira linha forte, sem hashtags em excesso, em primeira pessoa do sócio quando fizer sentido)
```

## Depois de escrever
1. Grave o `roteiro.md` só com tudo aprovado (gancho escolhido, fala, legenda e LinkedIn).
2. Com a aprovação: crie a pasta `video-bruto/` na peça, atualize a planilha (`registro.py atualizar . publicacoes Pnnn '{"gancho": "<final>", "cta": "...", "status": "em produção"}'`) e avise que o próximo passo é gravar e soltar os arquivos em `video-bruto/`.
3. Depois da gravação, a skill **editar-reels** assume.
