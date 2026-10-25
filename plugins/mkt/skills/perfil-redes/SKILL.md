---
name: perfil-redes
description: Avalia e melhora como a empresa aparece nas redes e no site — nome pesquisável, bio, link, destaques e capas, posts fixados e foto no Instagram; título, "Sobre", banner e botão no LinkedIn da empresa e dos sócios; chamada da primeira tela do site — a partir dos prints guardados no diagnóstico e de todo o contexto da empresa, com nota por item, propostas e as artes prontas na marca. Use quando o usuário pedir para avaliar a bio, o perfil, os destaques, as capas, o banner, "melhorar o Instagram", "revisar o LinkedIn", ou quando a implantação chegar à etapa de perfil das redes ou na revisão trimestral.
---

# Perfil das redes

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

> **Quem executa:** na conversa principal (gerente), passe a avaliação e as propostas ao cargo `social-media` (Sonnet) e a geração das artes ao `designer`; mostre ao responsável o que voltar. Se você já é esse cargo, execute.

## Quando usar
- **Implantação:** depois da Etapa 4 (Estratégia), quando já há posicionamento, público, pilares e chamada para ação definidos.
- **Revisão trimestral**, e sempre que o design, a oferta ou o público mudarem.
- Quando o usuário pedir.

## Passo 1. Reunir o material (antes de avaliar)
1. Leia: `00-contexto/diagnostico.md` (seção F, com o que está escrito hoje), `contexto-ia.md`, `tom-de-voz.md`, `design.md`, `provas.md`, `compliance.md`, `01-plano/estrategia.md` (pilar de crescimento, público, funil e chamada para ação).
2. Confira os prints em `00-contexto/materiais/perfis/`. **Se faltar alguma rede ou o site**, peça de uma vez, com a mesma tabela do Bloco F do diagnóstico (topo do perfil, grade, "Sobre", banner, primeira tela do site). Guarde cada um com `guardar-arquivo.py ... perfis` e transcreva na seção F do diagnóstico.
3. Pergunte, se ainda não souber: 2 ou 3 perfis de concorrentes ou de referência para comparar (o @ ou o link).
4. Se o usuário preferir, o `assistente-navegador` pode abrir os perfis **só para ler** e tirar os prints (sem alterar nada).

## Passo 2. Avaliar (nota de 0 a 10 por item, com o porquê em uma linha)
**Instagram**
| Item | O que conferir |
|---|---|
| Nome pesquisável | O campo "nome" tem a palavra que o público busca (ex.: "Gestão e Governança"), não só a marca |
| @ | Curto, fácil de ditar, igual ou parecido nas outras redes |
| Bio | Em até 150 caracteres: o que faz, para quem, uma prova (número ou resultado) e a chamada para ação do funil |
| Link | Leva para o próximo passo do funil (página, WhatsApp, agenda), com o mínimo de cliques |
| Foto | Logo ou rosto legível no círculo pequeno |
| Destaques | 4 a 6, na ordem do funil (ex.: Comece aqui, Cases, Método, Dúvidas, Contato), com capas no padrão da marca |
| Posts fixados | 3 posts que apresentam, provam e convidam (ex.: quem somos, melhor case, conteúdo mais salvo) |
| Grade | Primeiros 9 posts coerentes com a marca e legíveis no recorte 3:4 da grade |

**LinkedIn (empresa e sócios)**
| Item | O que conferir |
|---|---|
| Título | O que faz e para quem, com palavras que o público busca |
| "Sobre" | Problema, método, prova e chamada, em parágrafos curtos |
| Banner | 1584 × 396 (empresa e pessoal), com posicionamento legível e sem texto atrás da foto |
| Botão | Leva ao próximo passo do funil |
| Destaques / em destaque | Posts ou materiais que provam o que a empresa diz |

**Site (primeira tela)**: em 5 segundos dá para entender o que faz, para quem e qual o próximo passo? A mensagem é a mesma das redes?

Compare com os concorrentes indicados e aponte os 3 pontos que mais pesam (do maior para o menor impacto).

## Passo 3. Propor (o responsável escolhe)
- **2 ou 3 versões** de nome pesquisável, bio e título do LinkedIn, no tom de voz da empresa, com contagem de caracteres, e só com provas que estejam em `provas.md`. Respeite `compliance.md`.
- **Link da bio** e botão do LinkedIn: destino recomendado.
- **Destaques:** quais ter, a ordem e o conteúdo de cada um.
- **Posts fixados:** quais (pelo registro: os mais salvos ou que mais geraram contato) ou quais criar.
- **"Sobre" do LinkedIn** completo para a empresa e para cada sócio.
- **Primeira tela do site:** frase principal e chamada sugeridas (o responsável leva para quem cuida do site).

## Passo 4. Artes na marca
Com as escolhas aprovadas, gere as capas dos destaques e o banner do LinkedIn:
1. Crie `05-canais/artes-perfil/artes.json` com `"marca_arquivo": "../../00-contexto/carrossel-marca.json"`, a lista de destaques (`titulo` e `icone`: um símbolo, número ou letra) e o banner (`titulo`, `subtitulo`).
2. Rode `python3 "${CLAUDE_PLUGIN_ROOT}/skills/perfil-redes/scripts/artes-perfil.py" 05-canais/artes-perfil/artes.json`.
3. Revise pela `folha-perfil.jpg` e mostre ao responsável. Se ele preferir montar no modo Design do Claude, use as escolhas aprovadas como base.

## Passo 5. Aplicar e registrar
1. Quem altera o perfil é o responsável, ou o `assistente-navegador` no Chrome com a conta já logada, **item por item e só com o ok antes de salvar**. Nunca digite senha.
2. Registre em `05-canais/perfil-redes.md`: data, notas de antes, o que mudou (antes → depois) e o que ficou para depois.
3. Na leitura mensal de métricas, compare visitas ao perfil, cliques no link e seguidores antes e depois da mudança.
