---
name: referencias-nicho
description: Pesquisa o que está funcionando de verdade no nicho da empresa — vídeos e carrosséis de outros perfis que superaram muito a própria média — e monta o arquivo de referências com o gancho, a fórmula e a nota de cada um, para alimentar o radar de pautas. Use quando o usuário pedir "o que está funcionando no meu nicho", "acha vídeos que viralizaram", "analisa esse perfil", "monta um arquivo de referências", "por que esse vídeo bombou", ou quando o radar não tiver evidência do que produzir.
---

# Referências do nicho

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

> **Atualização (início de toda atividade):** antes de começar, rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verificar-atualizacao.py" --rapido --intervalo 1` (rápido, silencioso quando está tudo em dia). Se avisar versão nova: mostre o que mudou e pergunte uma vez se atualiza agora. Com o ok, rode o mesmo programa com `--aplicar`, peça ao usuário para digitar `/reload-plugins` e dizer "continua", rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atualizar-pasta.py" . --aplicar` (ajusta a pasta da empresa sem apagar nada) e retome a atividade. Se ele preferir depois, rode com `--adiar 12` e siga. Se você é um cargo (agente separado), pule esta verificação: o gerente já fez.

> **Quem executa:** na conversa principal (gerente), passe a coleta ao `assistente-navegador` (Haiku, só leitura) e a análise ao cargo `pesquisador` (Sonnet); mostre ao responsável o que voltar. Se você já é esse cargo, execute.

## Princípio
**Visualização bruta não é prova.** Um perfil de 2 milhões de seguidores com 400 mil visualizações teve um dia comum; um de 4 mil seguidores com 400 mil achou algo. O que se estuda é o **múltiplo**: visualizações do vídeo ÷ visualizações típicas (mediana) do próprio perfil.

## Passo 1. Quem observar
Com o responsável, liste **8 a 15 perfis**: concorrentes diretos, referências do setor em outros estados ou países, perfis que o público da empresa segue e criadores fora do setor com o mesmo público. Guarde a lista em `02-pautas/referencias-nicho.tsv` (só a coluna perfil, no início).

## Passo 2. Coletar
Para cada perfil, colete os **12 vídeos mais recentes** (ou carrosséis): visualizações (ou curtidas, se não houver), o gancho (primeira frase falada ou o texto da capa), o formato e o link. Calcule a **mediana** do perfil com esses 12 números. Caminhos:
- o `assistente-navegador` abre os perfis públicos no Chrome **só para ler** e preenche a tabela;
- o responsável cola prints ou números;
- dados públicos de concorrentes por um conector (por exemplo, Windsor.ai), se a empresa usar.
Preencha `02-pautas/referencias-nicho.tsv` (colunas: perfil, seguidores, mediana, visualizacoes, gancho, formato, link; separadas por tabulação).

## Passo 3. Ordenar e analisar
1. Rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/referencias.py" 02-pautas/referencias-nicho.tsv --saida 02-pautas/arquivo-referencias.md`.
2. Para os 5 a 10 de maior múltiplo (acima de 3x), anote: por que funcionou (gancho, tema, formato, momento), a fórmula do gancho (`referencias/ganchos.md`) e **como a empresa faria a versão dela**, com a experiência e as provas dela.
3. Mostre ao responsável os achados em 5 linhas e as 3 ideias mais fortes. Com o ok, registre as ideias (`registro.py adicionar . ideias '{..., "origem": "referências do nicho"}'`), conferindo repetição antes.

## Regras
- Inspiração na estrutura e no gancho, **nunca** cópia de conteúdo, roteiro, imagem ou marca de terceiros.
- Refaça a cada mês (ou quando o radar pedir); o arquivo antigo vai para `_lixeira/` com a data.
