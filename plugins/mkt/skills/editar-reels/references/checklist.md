# Checklist de revisão — editar-reels

Rode antes de entregar e a cada nova versão. Marque cada item olhando o arquivo final, não a pré-visualização.

## Fala e cortes
- [ ] Nova transcrição do áudio final bate ≥ 95% com o texto pretendido (`revisar.py --palavras` ou `--texto`).
- [ ] Nenhuma fala cortada que não devia (versão completa mantém todas as falas).
- [ ] Nenhum erro solto, recomeço ou repetição que sobrou.
- [ ] Nenhuma frase cortada no meio.
- [ ] Pausas: meio de frase ~0,2 s, entre frases ~0,35 s; nenhuma pausa morta além disso (fora o respiro final).
- [ ] Final termina antes de a pessoa desviar o olhar ou se mexer.

## Sincronia, cor e áudio
- [ ] Deriva A/V acumulada = 0 ms (`cortes.py`), áudio e vídeo do arquivo final com a mesma duração (±1 quadro AAC).
- [ ] Lábios batem com a fala no começo, no meio e no fim (olhar nos últimos 10 s).
- [ ] Cor igual à original (quadro lado a lado). Nenhuma correção aplicada sem OK.
- [ ] Volume −14 a −15 LUFS, pico ≤ −1,5 dBTP; efeitos e música bem abaixo da voz.

## Composição
- [ ] Nada sobre o rosto em nenhum quadro (inclusive quando a pessoa se inclina).
- [ ] Nada importante nas áreas da plataforma (Reels: 14% de cima, borda direita, 35% de baixo para texto) — ou aviso dado.
- [ ] Telas legíveis no celular em 1 s; recorte no trecho falado; sem título redundante.
- [ ] Dados pessoais borrados (clientes e a própria pessoa).
- [ ] Quando a fala aponta ("isso aqui"), a tela está visível.
- [ ] Nenhum quadro vazio, nenhum trecho congelado > 0,3 s (fora o congelamento final intencional).
- [ ] Nenhum elemento aparece antes da palavra que o motiva.
- [ ] Nenhuma transição semitransparente entre telas consecutivas.

## Texto
- [ ] Legendas em grupos de 2–3 palavras, nunca uma palavra sozinha.
- [ ] Legendas escondidas quando a tela já mostra o mesmo texto.
- [ ] Frases de destaque aparecem inteiras, destaque acende na palavra.
- [ ] Cartelas centralizadas, primeira linha no primeiro quadro.
- [ ] Contraste AA em claro e escuro.
- [ ] Números e nomes exatamente como falados; grafia de marcas conferida.

## Entrega
- [ ] Uma versão (a menos que pedissem mais) — se mais de uma, a variável que muda está declarada.
- [ ] Relatório: duração real, LUFS, o que mudou, desvios das regras e motivo, o que checar no preview da plataforma.
- [ ] Versões anteriores mantidas com sufixo; nada publicado sem OK.
