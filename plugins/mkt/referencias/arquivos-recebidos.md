# Arquivos enviados no chat

> **Idioma:** conduza tudo em português do Brasil.

**Regra:** todo arquivo que o usuário enviar no chat (ou indicar por caminho) é **guardado na pasta da empresa**, na pasta certa, antes de ser usado. Nada fica só na conversa.

## Como guardar
1. Descubra o caminho do arquivo. Arquivos arrastados para o chat ou citados pelo usuário vêm com o caminho no computador.
2. Escolha o destino pelo conteúdo:

| O que é | Destino (atalho) |
|---|---|
| Logo, manual de marca, paleta | `marca` |
| Foto real de pessoas, bastidores, eventos | `fotos` |
| Apresentação, PDF, texto, planilha | `documentos` |
| Exportação ou captura das redes sociais | `redes` |
| Referência de estilo, DESIGN.md | `design` |
| Vídeo de referência, gravação de tela de referência | `video-ref` |
| Música ou efeito sonoro licenciado | `trilhas` |
| Gravação ou tela de uma peça específica | pasta da peça, ex.: `03-producao/AAAA-MM/Sxx_Pnnn_tema/video-bruto` |
| Não se encaixa | `outros` |

3. Rode, de dentro da pasta da empresa:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/guardar-arquivo.py" "<caminho do arquivo>" <destino> "<descrição curta>"`
   O programa copia (o original fica onde estava), nunca sobrescreve e anota em `00-contexto/materiais/indice.md`.
4. Avise em uma linha onde ficou: "Guardei o logo em `00-contexto/materiais/marca/logo.png`."
5. Use **a cópia da pasta** dali em diante (nos arquivos de contexto, no design, nas peças).

## Quando não há caminho
Imagem colada direto no chat (captura de tela) às vezes chega sem arquivo. Nesse caso, diga: "Para eu guardar essa imagem na pasta do projeto, arraste o arquivo para o chat ou salve-o em `00-contexto/materiais/`." Continue o trabalho normalmente enquanto isso.

## Cuidados
- Não guarde senhas, documentos pessoais ou dados de cartão. Se aparecerem, avise e não copie.
- Arquivos muito grandes (vídeos brutos) vão direto para a pasta da peça, não para `materiais/`.
