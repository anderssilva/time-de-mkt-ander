# Design da marca — passo a passo (Etapa 3 da implantação)

> **Idioma:** conduza tudo em português do Brasil.

Resultado: `00-contexto/design.md` preenchido, `00-contexto/carrossel-marca.json` pronto e uma **amostra visual** aprovada. Tudo o que o time produzir (carrosséis, capas, telas e animações dos vídeos) segue este arquivo.

Faça **um passo por vez**, mostre o resultado e espere o "ok" antes do próximo.

---

## Passo 1. O que a empresa já tem
Pergunte: "A empresa tem manual de marca, guia de identidade, `design.md` antigo ou pelo menos o logo e as cores oficiais?"
- **Manual ou design.md (inclusive .docx ou PDF):** converta para o modelo e pule para o passo 4. O manual sempre prevalece.
- **Só logo e cores:** anote cores (com código hex), fonte (se souber) e onde estão os arquivos do logo. Siga para o passo 2 para completar o estilo.
- **Nada definido:** siga para o passo 2.

## Passo 2. Referências de estilo no Refero (mostre sempre o link)
Explique ao usuário, com estas palavras ou parecidas:

> "Para definir o visual da marca, a forma mais prática é escolher referências no **Refero Styles** (https://styles.refero.design/). É uma biblioteca com mais de 2.000 estilos de sites reais, e cada um já vem com um arquivo DESIGN.md (cores, fontes, espaçamentos e componentes) feito para a IA ler. Você escolhe o que gosta e eu adapto para a sua marca."

Conduza assim:
1. Peça para abrir **https://styles.refero.design/**.
2. Sugira por onde procurar, conforme a empresa: as coleções da página inicial (por exemplo, editorial, minimalista, papel creme com serifa) ou a busca por um site cujo visual ele admire.
3. Peça para escolher **2 ou 3 estilos** e enviar o **link** de cada um. Se ele conseguir, que baixe também o DESIGN.md de cada estilo e coloque em `00-contexto/referencias-design/`.
4. Para cada referência, pergunte em uma frase **o que chamou a atenção** (cores, fonte, sensação de sério ou leve, espaço em branco).

**Como olhar a referência:** abra o link (pelo navegador, com autorização) ou leia o DESIGN.md baixado. Nunca descreva um estilo que você não viu; sem acesso, peça o arquivo ou capturas de tela.

## Passo 3. Traduzir em regras, item a item
Confirme **linha por linha** (sim, não ou ajustar):

| Item | O que a referência faz | Proposta para a marca | Ok? |
|---|---|---|---|
| Paleta | | cores oficiais da empresa sempre prevalecem | |
| Proporção de uso das cores | ex.: 70% fundo, 25% principal, 5% destaque | | |
| Tipografia | família, pesos, caixa alta nos rótulos | fonte disponível no Google Fonts | |
| Espaço e respiro | margens, espaço entre blocos | | |
| Cantos e bordas | retos, arredondados, traço fino | | |
| Elementos gráficos | linhas, formas, texturas, ícones | | |
| Fotos | com pessoas reais, recorte, tratamento | | |
| Sensação geral | ex.: sério e confiável, moderno, acolhedor | | |

Regras que não mudam: logo e cores oficiais da empresa vêm antes de qualquer referência; contraste legível (o gerador de carrossel confere); nada copiado de marca de terceiros (logos, nomes, ilustrações próprias).

## Passo 4. Amostra visual
1. Monte o `00-contexto/carrossel-marca.json` com as cores, a fonte e os logos aprovados (formato no cabeçalho do `renderizar.py` da skill carrossel).
2. Gere uma prova com duas lâminas de exemplo, uma capa e uma lâmina de ação, usando `renderizar.py --laminas 1,2`.
3. Mostre ao usuário e ajuste até aprovar.

## Passo 5. Gravar
Preencha `00-contexto/design.md`: cores com hex e uso, proporção, tipografia, logos e onde ficam, elementos gráficos, fotos, formatos padrão e a seção **Referências** (links do Refero, o que usar de cada uma e o que não usar). Mostre o resumo e peça o ok.

Este design também alimenta o **estilo de vídeo**: as animações herdam cores, fontes e elementos daqui. O movimento (como as coisas entram, saem e trocam) é definido no passo a passo de vídeo, com as referências do What Ships.
