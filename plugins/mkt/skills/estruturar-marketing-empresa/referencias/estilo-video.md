# Estilo de vídeo — passo a passo (Etapa 3 da implantação)

Resultado: `00-contexto/estilo-video.md` preenchido e uma **amostra de estilo** aprovada. A partir daí, a skill editar-reels cria as animações (motion graphics, ou seja, textos, números, ícones e telas animados) sempre nesse estilo.

**Padrão do time:** todo vídeo é **gravação + motion graphics**. A pessoa fala para a câmera (ou aparece a tela do produto) e, por cima, entram títulos animados, números, listas, telas e transições no estilo da marca. Vídeo só com a pessoa falando, sem animação, é exceção e precisa ser pedido.

Faça **um passo por vez**, mostre o resultado e espere o "ok" antes do próximo. Grave cada decisão no arquivo assim que for aprovada.

---

## Passo 1. Vídeo da própria empresa (se existir)
Pergunte: "Você tem algum vídeo da empresa de que goste do jeito que ficou? Pode ser um Reels antigo, um vídeo institucional ou uma demonstração."
- **Se tiver:** peça o arquivo original (melhor que o baixado da rede). Coloque em `00-contexto/referencias-video/`. Gere uma folha de quadros (1 quadro a cada 1 a 2 segundos) e descreva com o usuário: logo e posição, legendas, abertura, encerramento, ritmo, zoom, música e chamada para ação. Pergunte o que **manter** e o que **mudar**.
- **Se não tiver:** siga para o passo 2. Não é problema.

## Passo 2. Referências de motion graphics (obrigatório)

As **cores, fontes e elementos** já vêm do `design.md` (definido com as referências do Refero Styles, https://styles.refero.design/). Aqui o foco é o **movimento**: como textos, números e telas entram, saem e trocam. Se o design ainda não estiver aprovado, faça-o antes.
Explique ao usuário, com estas palavras ou parecidas:

> "Para eu criar as animações dos seus vídeos num estilo de que você goste, preciso de 2 ou 3 vídeos de referência. O jeito mais fácil é o **What Ships** (https://whatships.com/), um catálogo gratuito com mais de 2.000 vídeos de lançamento de produtos de empresas de tecnologia. É a referência mais usada para mostrar ao Claude o estilo de animação desejado."

Conduza assim:
1. Peça para abrir **https://whatships.com/**.
2. Sugira a categoria conforme a empresa: **Motion** (animação pura) e **Design** para marcas visuais; **Productivity** ou **AI** para software e serviços; **Consumer** para produto físico ou varejo.
3. Peça para assistir a alguns vídeos e escolher **2 ou 3** cujo estilo combine com a marca. O assunto do vídeo não importa, só o estilo: tipografia, cores, ritmo, transições.
4. Peça o **link** de cada um (o link abre o post original). Também valem links de Instagram, YouTube ou TikTok, ou um perfil que o usuário admire.
5. Para cada referência, pergunte em uma frase **o que chamou a atenção**.

**Como olhar a referência:**
- Tente abrir o link pelo navegador (com autorização do usuário) e tirar capturas em sequência.
- Se não conseguir assistir pelo link (rede fechada, login, vídeo que não carrega), peça ao usuário para **baixar o vídeo ou gravar a tela** enquanto ele toca e colocar o arquivo em `00-contexto/referencias-video/`. Então gere a folha de quadros com o ffmpeg.
- Nunca descreva um vídeo que você não viu. Sem acesso, diga isso e peça o arquivo.

## Passo 3. Traduzir em regras, item a item
Monte uma tabela e confirme **linha por linha** com o usuário (sim, não ou ajustar):

| Item | O que a referência faz | Proposta para a marca | Ok? |
|---|---|---|---|
| Tipografia animada | ex.: palavras entram uma a uma, de baixo para cima | fonte do design.md, peso 800 | |
| Cores | ex.: fundo escuro, um único destaque | cores do design.md (Refero + marca) | |
| Entrada e saída dos textos | ex.: deslizar + esmaecer, 0,3 s | | |
| Transições entre cenas | ex.: corte seco / zoom / máscara | | |
| Ritmo | ex.: troca de elemento a cada 1,5 a 2 s | | |
| Números e dados | ex.: contador subindo até o valor | | |
| Listas e passos | ex.: itens aparecem um por vez com marcador | | |
| Telas do produto | ex.: tela dentro de moldura de celular, com zoom no ponto citado | | |
| Ícones e formas | ex.: traço fino, cantos arredondados | | |
| Efeitos sonoros | ex.: estalo suave a cada entrada de texto | | |
| Música | clima (sério, inspirador, leve) e só trilha licenciada | | |

Regras que não mudam com a referência: nunca cobrir o rosto, respeitar as áreas reservadas da plataforma, legendas legíveis e marca atual (cores e fonte do `design.md`, mesmo que a referência use outras).

## Passo 4. Amostra de estilo (prova visual)
Com os itens aprovados e o `design.md` pronto, crie uma **amostra de 5 a 8 segundos** com o HyperFrames (as mesmas ferramentas da skill editar-reels) contendo:
- um título animado;
- um número em destaque;
- uma lista curta de 3 itens;
- a cartela final com o logo.

Salve como `00-contexto/referencias-video/amostra-estilo.mp4` e mostre ao usuário. Ajuste até ele aprovar. Essa amostra vira o **padrão de comparação** do controle de qualidade.

Se as ferramentas de vídeo ainda não estiverem instaladas, explique o que falta, peça autorização para instalar e, se o usuário preferir deixar para depois, marque a amostra como pendente no `status-implantacao.md`.

## Passo 5. Gravar o arquivo
Preencha `00-contexto/estilo-video.md`:
- referências: links, o que copiar de cada uma e o que **não** copiar;
- a tabela aprovada do passo 3;
- o caminho da amostra aprovada;
- legendas, marca, abertura, encerramento, som e chamada para ação padrão.

Mostre o resumo final e peça o ok para marcar a parte de vídeo da Etapa 3 como concluída.
