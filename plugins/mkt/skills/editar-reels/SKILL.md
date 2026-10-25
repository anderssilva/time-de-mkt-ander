---
name: editar-reels
description: Edita vídeos curtos verticais (Reels, TikTok, Shorts, anúncios) de qualquer empresa a partir dos takes brutos e do roteiro aprovado — lê o bruto, propõe o plano de cortes, telas, animações e legendas para aprovação, e só então monta com o HyperFrames, mantendo áudio e vídeo sincronizados, sem cobrir o rosto e no estilo de vídeo da empresa. Use quando o usuário pedir para editar um vídeo, "edita o reels da P012", "monta o vídeo", "gravei, pode editar", ou quando rodar-semana-marketing chegar à edição. Adaptada do Kit de Edição com Claude.
---

# Editar Reels

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

> **Quem executa:** na conversa principal (gerente), passe o trabalho ao cargo `editor-video`, que roda num modelo mais leve, e mostre ao responsável o que voltar (veja `${CLAUDE_PLUGIN_ROOT}/referencias/orquestracao.md`). Se você já é esse cargo, execute.

Edição de vídeo curto vertical (9:16) com apresentador. O objetivo é uma peça que prenda nos primeiros segundos, prove o que é dito com material real, seja legível no celular e termine numa chamada para ação clara, sem nunca cobrir o rosto e sem cortar o que a pessoa disse.

Por padrão: **uma única versão**, na **duração natural da fala**, **sem mexer na cor**.

## Onde as coisas ficam
- Trabalhe dentro da **pasta da empresa** (a pasta onde o Claude Code foi aberto, que tem `00-contexto/` e `registro/`). Se a pasta atual não for de uma empresa, pergunte qual é. Identifique a peça (Pnnn).
- Pasta da peça: `03-producao/AAAA-MM/Sxx_Pnnn_tema/`
  - `roteiro.md` (aprovado) · `video-bruto/` (takes) · `edicao/` (trabalho: transcrição, cortes.json, aroll, composição) · `video-final/` (entrega `Pnnn-v1.mp4`, `Pnnn-v2.mp4`…)
- Leia **antes de tudo**: `00-contexto/estilo-video.md` (como a empresa gosta da edição), `design.md` (cores, fonte, logo), `tom-de-voz.md`, `provas.md`, `compliance.md` e as melhorias incorporadas. O estilo-video.md manda sobre as preferências padrão desta skill; se houver conflito com uma regra técnica (rosto, sincronia, áreas da plataforma), a regra técnica vence e você avisa.
- Se `estilo-video.md` estiver vazio, pergunte as preferências principais (legenda, logo, cartela final, música) e ofereça gravar as respostas nele.
- **Motion graphics são o padrão:** todo vídeo leva animações por cima da gravação (títulos, números, listas, telas), seguindo a seção "Linguagem de motion" do `estilo-video.md` e a **amostra de estilo** em `00-contexto/referencias-video/amostra-estilo.mp4`. Olhe a amostra antes de compor e mantenha o mesmo padrão. Vídeo sem animação só quando o responsável pedir.
- Se não houver referências nem amostra aprovadas, avise que a Etapa 3 da implantação ficou incompleta e ofereça fazer agora o passo a passo de referências (What Ships, https://whatships.com/) antes de editar.

## Ferramentas
- Composição e render: **HyperFrames** (skill `/hyperframes`; para recorte de vídeo falado, o fluxo `/talking-head-recut`; legendas com `/embedded-captions`). Licença Apache 2.0. Requer Node 22+ e ffmpeg.
- Cortes e análise: `scripts/` desta skill (Python + ffmpeg). Leia o cabeçalho de cada script antes de usar.
  - `scripts/transcrever.py`: transcrição local com tempo por palavra (Parakeet via `hyperframes transcribe`).
  - `scripts/cortes.py`: corta, encurta silêncios, mantém áudio e vídeo exatos, gera `aroll.mp4`, `segments.json`, `words.json`.
  - `scripts/revisar.py`: revisão do vídeo final (pausas, sincronia, nova transcrição, folha de quadros).
- Checklist de revisão: `references/checklist.md`.
- Antes do primeiro uso, confira os requisitos (Node 22+, ffmpeg/ffprobe, plugin HyperFrames, modelo Parakeet: `npx hyperframes models install parakeet`). Se faltar algo, diga o que vai instalar e **espere autorização**.

Fluxo típico dos scripts:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/editar-reels/scripts/transcrever.py" <peça>/video-bruto <peça>/edicao/transcricao
# escolha os trechos e escreva <peça>/edicao/cortes.json (formato no cabeçalho de cortes.py)
python3 "${CLAUDE_PLUGIN_ROOT}/skills/editar-reels/scripts/cortes.py" <peça>/edicao/cortes.json --palavras <peça>/edicao/transcricao --saida <peça>/edicao/aroll
# monte o visual sobre o aroll com o HyperFrames, usando words.json para sincronizar tudo
python3 "${CLAUDE_PLUGIN_ROOT}/skills/editar-reels/scripts/revisar.py" <peça>/video-final/Pnnn-v1.mp4 --palavras <peça>/edicao/aroll/<versao>/words.json
```

## Entrada esperada
Localize na pasta da peça e pergunte só o que faltar: takes brutos, roteiro aprovado, telas ou provas a mostrar (prints, gravação de tela, link) ou "não há", destino (Reels, TikTok, Shorts, anúncio) e chamada para ação (do roteiro).

**Medição de tempo (quando pedirem):** registre início e fim de cada etapa em `edicao/tempo.md` com o comando date, separando o tempo de trabalho do tempo esperando aprovação.

## 1. Entender e perguntar (antes de editar)

1. Leia todo o material: roteiro, regras, identidade e referências visuais.
2. Transcreva todos os takes com tempo por palavra (`transcrever.py`) e monte uma transcrição
   indexada. Escolha o melhor take de cada frase pela transcrição, não pelo nome do arquivo.
3. Olhe os takes de verdade (folhas de quadros). Descubra onde está o rosto em cada trecho — detecte
   a cada ~0,2 s e suavize só dentro de cada trecho contínuo, nunca atravessando um corte —, onde há
   espaço livre no quadro, e se há tela, objeto ou gesto que a fala aponta.
4. Pergunte só o que muda o resultado e não dá para deduzir, sempre com uma opção recomendada:
   - **Layout das telas/provas:** sobrepostas na área livre (acima da cabeça, ao lado); tela dividida;
     apresentador em janela (picture in picture); ou só câmera com textos. Recomende a partir do
     enquadramento gravado.
   - **Movimento intencional:** um gesto, entrar no quadro ou sentar pode ser o gancho visual. Pergunte antes de cortar.
   - **Números reais** (faturamento, vendas, métricas): mostrar como estão ou borrar?
   - **Música:** existe trilha licenciada? Se não, só voz e efeitos sonoros suaves.
   - **Telas de sistema com login:** a própria pessoa faz o login. Nunca digite senha. Para capturas em
     alta resolução, abra uma janela separada de navegador com depuração remota e capture com 2x de densidade.
5. Apresente um **plano em tabela** e espere aprovação antes de montar. Por grupo de frases: tempo, fala,
   take escolhido, visual (sincronizado ao início das palavras), movimento/zoom. Liste junto os desvios
   das regras com o motivo e os takes descartados com o motivo. Se houver uma frase mais forte que o
   gancho do roteiro, sugira — não troque por conta própria.

## 2. Cortes e áudio

6. **Não corte falas para caber numa duração.** Remova só repetições, recomeços, sons soltos e erros
   (um "a" ou "é" isolado antes da frase) e silêncios. Frases inteiras só saem se for pedida uma versão
   mais curta — e nunca no meio da frase.
7. **Pontos de corte:** sempre no silêncio entre palavras, nunca dentro de uma palavra. Folga de ~50 ms
   antes da primeira palavra e ~60 ms depois da última (~160 ms se termina frase). A transcrição estica
   o fim das palavras antes das pausas: refine os cortes pelo volume do áudio.
8. **Silêncios:** meça o ruído de fundo de cada take e use um limite um pouco acima dele (em geral −38 a
   −40 dBFS, janelas de 10–20 ms). Proteja o início de cada palavra transcrita (palavras faladas baixo
   caem abaixo do limite). Pausas no meio da frase viram ~0,2 s; entre frases, ~0,35 s. Uma rajada curta
   e isolada de som antes da fala costuma ser erro e deve sair.
9. Termine antes de a pessoa desviar o olhar ou se mexer. Se precisar de respiro, congele o último quadro ~0,5 s.
10. **Sincronia:** arredonde cortes para quadros inteiros; cada pedaço tem áudio e vídeo com exatamente a
    mesma duração (fades de 8–10 ms, sem sobreposição). Diferenças de milissegundos por pedaço somam e
    dessincronizam o fim. Meça a diferença acumulada depois de emendar (deve ser 0) e confira no arquivo
    final que áudio e vídeo têm a mesma duração.
11. **Cor: não mexa.** Sem correção, grade, LUT, brilho, contraste ou saturação. Material HDR do celular:
    preserve a aparência; se o formato de entrega exigir conversão técnica, use a mais neutra, compare um
    quadro lado a lado com o original e pergunte se a aparência mudou.
12. **Áudio:** normalize em −14 a −15 LUFS, pico −1,5 dBTP. Um filtro de graves leve (70–80 Hz) pode
    limpar ruído; outro tratamento (EQ, compressão, redução de ruído) só se pedirem.
13. Transcreva de novo o áudio montado e compare com o texto pretendido. Corrija fragmentos que vazaram e
    inícios de palavra cortados; repita até ficar limpo.

## 3. Composição e leitura

14. **Nunca ponha texto, legenda ou tela sobre o rosto.** Posicione tudo a partir da medida do rosto, no
    pior caso (a pessoa se inclinando).
15. **Áreas da plataforma:** no Reels, deixe livres os 14% de cima, a borda direita e os 35% de baixo para
    texto. Se for inevitável invadir a área de baixo, avise e recomende checar no preview da plataforma.
16. **Layout escolhido**, com estas regras em qualquer modo:
    - Sobreposição: use o espaço livre do enquadramento e mantenha o apresentador em tela cheia.
    - Tela dividida: prova numa metade, rosto na outra, recompondo o enquadramento (não só recortar).
    - Picture in picture: só se pedirem — deixa o apresentador pequeno.
    - Mais de um modo no mesmo vídeo: transição suave de ~0,7 s, não um salto.
    - Se a pessoa aponta para a tela ou diz "isso aqui", a tela tem que estar visível naquele momento.
17. **Telas e provas reais:** captura em alta resolução (2x); borre dados pessoais (nomes, telefones,
    e-mails de clientes e os dados da própria pessoa no cabeçalho); recorte só o trecho falado e mostre
    grande; teste de 1 segundo (legível no celular); sem títulos redundantes acima da tela; o zoom chega
    ~0,25 s antes da palavra; em telas longas algo muda a cada 1–2 s; telas consecutivas trocam sem
    transição de opacidade; nunca invente interface.
18. **Gráficos explicativos** (sem tela, ou para complementar): números grandes contando até o valor,
    listas que revelam um item por vez no item falado, diagramas que se desenham, antes/depois,
    comparações. Cada gráfico entra no início da palavra que o motiva, nunca antes.
19. **Legendas:** grupos de 2 a 3 palavras pelo tempo de cada palavra; **nunca uma palavra sozinha** — a
    que ficaria isolada se junta ao grupo anterior ou seguinte; fundo escuro translúcido; fora do rosto;
    escondidas quando a tela já mostra o mesmo texto; grafia corrigida quando pedirem.
20. **Frases de destaque (cartões):** a frase inteira aparece de uma vez, sem espaço vazio reservado; a
    palavra de destaque acende na cor de ênfase quando é falada.
21. **Cartelas de tela cheia:** curtas, como respiro entre blocos; texto centralizado revelado linha por
    linha; a primeira linha entra no primeiro quadro (sem quadro vazio).
22. **Claro e escuro:** adapte a identidade para os dois tons (tokens de fundo, texto, ênfase); ênfase mais
    clara no escuro e mais escura no claro, mantendo contraste AA; alterne em blocos, com corte seco.
23. **Zoom na câmera:** punch-in de 1,1–1,2x nas frases de impacto; alternância 100% ↔ ~105–107% nos cortes
    secos dentro de um mesmo trecho; zoom progressivo no rosto durante o CTA. Sempre em torno do centro do rosto.
24. **CTA:** frase-chave em destaque entrando na palavra falada, um elemento apontando para o botão da
    plataforma, um som suave de confirmação.
25. **Efeitos sonoros suaves:** whoosh nos cortes de cena e mudanças de layout, clique nos zooms, pop nas
    revelações, sino no CTA — bem abaixo da voz e com licença comercial.
26. **Música (só se houver trilha):** abaixe 9–12 dB sob a voz; não repita a trilha do vídeo anterior; a
    nova transcrição do áudio final deve bater ≥95% das palavras.

## 4. Conteúdo e responsabilidade

27. Números e afirmações exatamente como falados. Nada de estatística, depoimento ou resultado inventado.
28. Confira a grafia de nomes de ferramentas e marcas antes de colocar na tela.
29. Texto na tela curto e concreto, sem clichês de IA.
30. Nunca publique, agende ou envie nada sem OK explícito.

## 5. Versões

31. **Padrão: uma única versão.**
32. Só se pedirem mais de uma (teste A/B): além da duração, cada versão muda pelo menos uma variável
    declarada (título do gancho como afirmação vs. pergunta, paleta abrindo no claro vs. no escuro) — diga
    exatamente o que difere.
33. **Título do gancho:** no primeiro quadro, 3–8 palavras vendendo o resultado, onde não cubra a prova nem o rosto.

## 6. Revisão e entrega

34. Assista ao vídeo final de verdade (`revisar.py` + olhar os quadros): folhas a 2 fps e quadros em
    tamanho de celular. Procure texto sobre o rosto, telas ilegíveis, quadros vazios e trechos congelados
    >0,3 s, elementos antes da fala, transições semitransparentes, palavras cortadas, pausas mortas,
    dessincronia e final com a pessoa desviando o olhar.
35. Quando pedirem revisão, **liste os problemas antes de corrigir**, do mais grave ao menos grave, com tempo exato.
36. Na entrega: duração real, volume (LUFS), o que mudou, o que ficou fora das regras e por quê, o que
    conferir no preview da plataforma. Mantenha versões anteriores com sufixo (v1, v2…). Se útil, entregue
    um `.srt` gerado do tempo das palavras.
    **Capa do Reels:** entregue `video-final/Pnnn-capa.png` (1080 × 1920) com o gancho e o rosto dentro da janela central 1080 × 1440 (3:4), que é o que aparece na grade do perfil; nada importante nos 240 px de cima e de baixo. Regras em `${CLAUDE_PLUGIN_ROOT}/referencias/formatos-redes.md`.
37. **Reprodutível:** cortes num arquivo de dados (`cortes.json`) e visual gerado por script, para que
    ajustes de texto, tempo e layout não exijam refazer do zero.

## 7. Integração com a jornada
38. **O plano de edição (etapa 5) é obrigatório e precisa de aprovação** antes de qualquer montagem. Grave-o também em `edicao/plano.md`.
39. Ao terminar a montagem e a sua própria revisão: atualize a planilha (`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py" atualizar . publicacoes Pnnn '{"status": "em revisão"}'`) e encaminhe para a skill **controle-qualidade** (de preferência o agente separado) e depois **estrategista-marketing, revisão final**.
40. Correções pedidas pelo responsável que valem para os próximos vídeos ("sempre faça assim") viram melhoria: registre com `registro.py adicionar . melhorias '{...}'` (origem "responsável") e ofereça atualizar o `estilo-video.md`.
41. Nunca publique, agende ou envie nada. O agendamento é da skill agendar-publicacao, depois do ok final.
