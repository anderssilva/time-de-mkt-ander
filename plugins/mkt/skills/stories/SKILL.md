---
name: stories
description: Escreve a sequência de Stories do dia ou da semana — quadro a quadro, qual figurinha usar em cada um (enquete, caixa de perguntas, teste, contagem regressiva, link) e o caminho que leva a pessoa a mandar mensagem. Use quando o usuário pedir "stories", "o que posto no story", "sequência de stories", "ideia de enquete", "não tenho nada para o story", ou quiser vender algo sem fazer um post sobre isso.
---

# Stories

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

> **Atualização (início de toda atividade):** antes de começar, rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verificar-atualizacao.py" --rapido --intervalo 1` (rápido, silencioso quando está tudo em dia). Se avisar versão nova: mostre o que mudou e pergunte uma vez se atualiza agora. Com o ok, rode o mesmo programa com `--aplicar`, peça ao usuário para digitar `/reload-plugins` e dizer "continua", rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atualizar-pasta.py" . --aplicar` (ajusta a pasta da empresa sem apagar nada) e retome a atividade. Se ele preferir depois, rode com `--adiar 12` e siga. Se você é um cargo (agente separado), pule esta verificação: o gerente já fez.

> **Quem executa:** na conversa principal (gerente), passe a sequência ao cargo `redator` e mostre ao responsável o que voltar. Se você já é esse cargo, execute.

## Antes de começar
1. Trabalhe dentro da pasta da empresa. Leia `contexto-ia.md`, `tom-de-voz.md`, `01-plano/estrategia.md` (funil e palavra-chave), `design.md` e as peças da semana (`registro/publicacoes.csv`).
2. Pergunte se há material do dia: bastidor, foto, print de resultado, pergunta de cliente, evento. Material real vale mais que arte.

## Regras da sequência
- **3 a 7 quadros**, com começo, meio e fim. **Cada quadro tem um trabalho só**: prender, mostrar, provar, perguntar ou levar à mensagem.
- **Quadro 1 segura sozinho:** uma frase forte ou uma imagem que gere curiosidade (dê nota com `scripts/gancho.py`).
- **Pelo menos um quadro de interação** (figurinha), escolhido pelo trabalho:
| Figurinha | Para que serve |
|---|---|
| Enquete | Fazer a pessoa tocar pela primeira vez; descobrir preferência ou dor |
| Caixa de perguntas | Colher dúvidas reais (viram pautas e posts) |
| Teste (quiz) | Ensinar algo e medir o que o público sabe |
| Controle deslizante (emoji) | Medir intensidade de um sentimento ou opinião |
| Contagem regressiva | Lançamento, evento ou prazo |
| Link | Próximo passo do funil (página, agenda), sempre com o motivo para clicar |
- **Caminho para a mensagem direta:** o último quadro convida a mandar mensagem com uma **palavra-chave** ("me manda AGENDA que eu te envio o modelo"). Quem respondeu à enquete ou à caixa de perguntas pode receber uma mensagem pela skill **relacionamento**.
- **Área segura:** nada importante nos 14% de cima nem nos 35% de baixo do quadro (`referencias/formatos-redes.md`).
- Texto curto: até ~15 palavras por quadro. Rosto e bastidor real rendem mais que arte pronta.

## Entrega
Grave em `03-producao/AAAA-MM/stories-AAAA-MM-DD.md`:
| Quadro | Trabalho | Imagem ou vídeo (o que gravar ou qual arquivo usar) | Texto na tela | Figurinha | Observação |
|---|---|---|---|---|---|
Passe os textos pelo `scripts/humanizar.py`. Os stories saem pelo celular (o responsável publica) ou pelo Meta Business Suite com o `assistente-navegador`, sempre com o ok antes de publicar.
Depois de 24 horas, anote no mesmo arquivo: visualizações do quadro 1 e do último, respostas, toques na figurinha e mensagens recebidas.
