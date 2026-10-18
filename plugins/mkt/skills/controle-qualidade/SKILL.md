---
name: controle-qualidade
description: Controle de qualidade técnico e independente de uma peça de marketing (vídeo, carrossel, legenda ou texto) antes da revisão estratégica e da publicação. Confere por checklist objetivo, aponta problemas com gravidade e local exato, e registra o que se repete como melhoria. Use quando o usuário pedir "revisa a peça", "controle de qualidade", "confere o vídeo/carrossel", "está pronto para ir ao ar?", ou quando editar-reels, carrossel ou rodar-semana-marketing chamarem a revisão técnica. Funciona melhor como agente separado (agente controle-qualidade), sem ter visto a produção.
---

# Controle de qualidade técnico

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

## Papel
Você confere, não opina sobre estratégia (isso é do estrategista). Seja objetivo e minucioso: cada problema com local exato (segundo do vídeo ou número da lâmina), gravidade e correção sugerida. Avalie só os arquivos finais, como alguém de fora.

## Antes de começar
1. Trabalhe a partir da pasta `Marketing`. Identifique a empresa e a peça (Pnnn) e a pasta dela em `03-producao/`.
2. Leia: `design.md`, `estilo-video.md` (se for vídeo), `tom-de-voz.md`, `provas.md`, `compliance.md` e as melhorias incorporadas (elas viram itens extras do checklist).
- Ferramenta de registro: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py"` (abreviada abaixo como `registro.py`), sempre a partir da pasta Marketing.

## Gravidade
- **Crítico:** não pode ir ao ar (texto sobre o rosto, número fora de provas.md, palavra proibida, erro de compliance, dessincronia, lâmina ilegível, dado pessoal exposto).
- **Importante:** prejudica a peça (erro de português, contraste baixo, área da plataforma invadida, legenda com palavra solta, cor fora do design).
- **Menor:** acabamento (alinhamento, espaçamento, pausa um pouco longa).
Aprovado = **zero críticos e zero importantes**.

## Checklist de vídeo
Use os scripts da skill editar-reels quando instalados (`${CLAUDE_PLUGIN_ROOT}/skills/editar-reels/scripts/revisar.py <video> --palavras <words.json>`) e olhe as folhas de quadros.
- Arquivo: 1080 × 1920, 9:16, áudio e vídeo com a mesma duração.
- Volume entre −14 e −15 LUFS, pico ≤ −1,5 dBTP.
- Nova transcrição bate ≥ 95% com o roteiro aprovado; nenhuma palavra cortada; nenhuma frase pela metade.
- Pausas: meio de frase ~0,2 s, entre frases ~0,35 s; nada congelado > 0,3 s (fora o final intencional).
- Nada sobre o rosto em nenhum quadro; áreas da plataforma livres (Reels: 14% de cima, borda direita, 35% de baixo).
- Legendas conforme estilo-video.md (grupos de 2 a 3 palavras, nunca uma sozinha, fora do rosto).
- Gancho visível no primeiro quadro; CTA no final; logo e cartela conforme estilo-video.md.
- Motion graphics conforme a "Linguagem de motion" do estilo-video.md e comparáveis à amostra de estilo (`00-contexto/referencias-video/amostra-estilo.mp4`): mesma tipografia, cores, entradas, transições e ritmo. Vídeo sem animação só se o responsável tiver pedido.
- Telas legíveis no celular em 1 segundo; dados pessoais borrados.
- Lábios sincronizados no começo, meio e fim.
- O checklist completo da skill editar-reels (`references/checklist.md`).

## Checklist de carrossel
- Lâminas 1080 × 1350, mesma quantidade do `texto.md` aprovado, numeradas na ordem.
- Capa: gancho com até 8 palavras, legível em miniatura.
- Uma ideia por lâmina; corpo com no máximo ~30 palavras; fonte do corpo com pelo menos 34 px.
- Contraste AA (4,5:1 para texto normal, 3:1 para títulos grandes). Na dúvida, calcule com as cores do `design.md`.
- Margens de pelo menos 80 px; nada cortado nas bordas; logo na posição do design.md.
- Cores e fonte só do `design.md`; fotos só do banco `fotos/` e sem rosto alterado.
- Proporção: no máximo 1 lâmina de problema; pelo menos 60% de lâminas de ação, cada uma com passos e exemplo prático; checklist de resumo antes da chamada final (importante se faltar).
- Última lâmina com CTA único.
- Ortografia e acentuação em todas as lâminas.
- Se houver PDF para LinkedIn, mesma ordem e conteúdo das imagens.

## Checklist de texto (legenda, LinkedIn, artigo)
- Ortografia, acentuação e pontuação.
- Primeira linha forte; legenda até 2.200 caracteres; 3 a 5 hashtags.
- Um CTA só, igual ao da peça.
- Todo número, case ou depoimento está em `provas.md`.
- Nenhuma palavra ou promessa proibida (`compliance.md` e briefing).
- Links funcionando e corretos.

## Entrega
1. Grave `revisao-qualidade.md` na pasta da peça:
   ```
   # Controle de qualidade — Pnnn — [data] — rodada [1/2]
   Veredito: APROVADO | REPROVADO · Nota técnica: x/10
   | # | Gravidade | Onde (tempo ou lâmina) | Problema | Correção sugerida |
   ```
2. Atualize a planilha: `registro.py atualizar empresas/<slug> publicacoes Pnnn '{"nota_qualidade": "x"}'`. Se reprovado, status "em produção".
3. Para problemas que podem se repetir, registre melhoria (origem "qualidade"), conferindo antes com `registro.py melhoria-parecida`. Se já existir, some 1 em `ocorrencias`.
4. Se aprovado: status "em revisão" e encaminhe para a skill **estrategista-marketing, modo revisão final**.
5. Na segunda reprovação da mesma peça, pare e leve a decisão ao responsável.
