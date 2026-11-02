---
name: reaproveitar
description: Transforma um conteúdo longo (vídeo do YouTube, podcast, live, palestra, artigo, newsletter, gravação de reunião ou aula) numa semana de peças — Reels, carrosséis e posts de LinkedIn — em que cada uma se sustenta sozinha. Use quando o usuário disser "reaproveita isso", "transforma em Reels", "tenho um vídeo/podcast/transcrição", "corta isso em peças", "conteúdo-mãe", ou colar um texto longo para virar conteúdo.
---

# Reaproveitar (conteúdo-mãe)

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

> **Atualização (início de toda atividade):** antes de começar, rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verificar-atualizacao.py" --rapido --intervalo 1` (rápido, silencioso quando está tudo em dia). Se avisar versão nova: mostre o que mudou e pergunte uma vez se atualiza agora. Com o ok, rode o mesmo programa com `--aplicar`, peça ao usuário para digitar `/reload-plugins` e dizer "continua", rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atualizar-pasta.py" . --aplicar` (ajusta a pasta da empresa sem apagar nada) e retome a atividade. Se ele preferir depois, rode com `--adiar 12` e siga. Se você é um cargo (agente separado), pule esta verificação: o gerente já fez.

> **Quem executa:** na conversa principal (gerente), passe a leitura e as propostas ao cargo `redator` (Sonnet) e os cortes de vídeo ao `editor-video`; mostre ao responsável o que voltar. Se você já é esse cargo, execute.

## Passo 1. Receber o material
- Guarde o arquivo na pasta da empresa (`guardar-arquivo.py ... documentos`, ou `video-ref` para vídeo). Gravações do Plaud ou de reuniões: use só com autorização de quem aparece.
- Precisa de texto: transcrição pronta, ou transcreva o vídeo ou áudio com os programas da skill editar-reels (`scripts/transcrever.py`), que dão o tempo de cada palavra (útil para cortar trechos depois).

## Passo 2. Garimpar
Leia tudo e liste os **momentos aproveitáveis**, cada um com o trecho (e o tempo, se for vídeo):
- uma opinião forte ou contrária ao senso comum;
- uma história com começo, meio e fim;
- um número ou resultado (só se puder ir para `provas.md`, com fonte);
- um passo a passo ou método;
- uma pergunta frequente bem respondida;
- uma frase de efeito que serve de gancho.

## Passo 3. Propor a semana
Monte de 5 a 8 peças, **cada uma completa sozinha** (quem não viu o original entende tudo):
| # | Formato | Momento usado (trecho/tempo) | Gancho (nota) | Ideia em 1 linha | Pilar |
|---|---|---|---|---|---|
Distribuição sugerida: 3 a 4 Reels (corte do próprio vídeo, quando houver, ou roteiro novo para gravar), 1 a 2 carrosséis (método ou lista), 1 a 2 posts de LinkedIn (opinião ou história) e uma sequência de stories.
- Dê nota aos ganchos com `scripts/gancho.py` e confira repetição com `registro.py repeticao`.
- Mostre ao responsável e peça a escolha.

## Passo 4. Registrar e produzir
- As escolhidas viram ideias aprovadas (`registro.py adicionar . ideias '{..., "origem": "conteúdo-mãe: <nome do material>"}'`) e seguem a rotina normal: estrategista, roteiro ou carrossel, qualidade, revisão final e o seu ok.
- Corte de vídeo do próprio material: a skill **editar-reels** usa os tempos anotados no passo 2.
