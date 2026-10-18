---
name: carrossel
description: Cria carrosséis para Instagram e LinkedIn de qualquer empresa, do texto às lâminas prontas — escreve lâmina a lâmina, espera aprovação e gera as imagens 1080x1350 na identidade da empresa (cores, fonte, logo, fotos reais), mais um PDF para o LinkedIn. Use quando o usuário pedir carrossel, post de carrossel, slides para Instagram, lâminas, "faz o carrossel da P013", documento para LinkedIn, ou quando rodar-semana-marketing chegar à produção de um carrossel. Substitui a antiga mkt-carrossel-instagram, que só gerava texto.
---

# Carrossel (texto + lâminas prontas)

## Antes de começar
1. Trabalhe a partir da pasta `Marketing`. Identifique a empresa e a peça (Pnnn, status "aprovado"). Pasta da peça: `03-producao/AAAA-MM/Sxx_Pnnn_tema/`.
2. Leia: `contexto-ia.md`, `design.md`, `tom-de-voz.md`, `provas.md`, `compliance.md`, `fotos/fotos.md`, `01-plano/estrategia.md` e as melhorias incorporadas.
3. Pergunte se o responsável já tem material para esta peça (artigo, roteiro de vídeo do mesmo tema, rascunho, foto específica) ou se quer do zero.
- Ferramenta de registro: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py"` (abreviada abaixo como `registro.py`), sempre a partir da pasta Marketing.

## Regra de ouro do conteúdo: mais ação que dor
O cliente salva e compartilha o que consegue **aplicar**. A dor só serve para abrir a conversa.
- **Problema:** no máximo 1 lâmina (cerca de 20% do carrossel). Pode citar vários sintomas juntos, nunca um por lâmina.
- **Ação:** pelo menos 60% das lâminas. Cada ação é uma lâmina do tipo `acao` com três partes: **o que fazer** (título), **como fazer** (2 a 4 passos concretos) e **na prática** (um exemplo real, uma frase-modelo, um número de referência).
- **Resumo:** uma lâmina de checklist antes da chamada final, para a pessoa salvar.
- Prefira ganchos de solução ("4 ajustes para...", "Como fazer...") a ganchos só de problema ("3 sinais de que...").

## Passo 1. Escolher o formato
| Formato | Quando usar |
|---|---|
| Ajustes ou ações | "4 ajustes para...", "5 práticas que..." (o mais salvo: cada ação detalhada) |
| Passo a passo | método ou processo em sequência que a pessoa vai aplicar |
| Antes e depois | mostrar a mudança que o produto ou o método traz |
| Mito e verdade | corrigir uma crença comum do público, sempre com o que fazer no lugar |
| Número | um dado forte (só de `provas.md`) explicado |
| Caso | história real de cliente (só com autorização registrada em `provas.md`) |

## Passo 2. Validar o texto em duas rodadas curtas (antes de qualquer imagem)
Nunca gere imagens antes de o texto estar aprovado lâmina por lâmina. Cada rodada é curta de propósito: corrigir texto é barato, refazer imagens não.

### Rodada 1 — Esqueleto (aprovação 1)
Mostre só:
- formato escolhido e quantidade de lâminas;
- **2 opções de gancho** para a capa;
- uma linha por lâmina: `Lâmina 3 · ação · Envie tudo 48 horas antes`.
Pergunte: "Aprova o esqueleto? Quer trocar, juntar ou tirar alguma lâmina?". **Espere.** Não escreva os textos completos ainda.

### Rodada 2 — Texto lâmina a lâmina (aprovação 2)
Com o esqueleto aprovado, escreva o texto completo de cada lâmina, numerado:
```
Lâmina 3 · ação · claro
Título: Envie tudo *48 horas antes*
Passos: Pauta com no máximo 5 itens... / Números e anexos no mesmo envio / ...
Na prática: Item da pauta: "Aprovar ou não..."
```
Peça a aprovação por número ("ok", ou "lâmina 4: troque o exemplo"). Ao ajustar, **reescreva só as lâminas citadas** e mostre só elas; não repita o carrossel inteiro. Repita até tudo estar aprovado.

Regras do texto:
- **7 a 10 lâminas.** Estrutura padrão: capa → 1 lâmina de problema → 3 a 5 lâminas de ação → resumo em checklist → chamada final.
- **Capa:** gancho com até 8 palavras, concreto, legível em miniatura. Subtítulo curto com a promessa.
- **Uma ideia por lâmina.** Lâminas comuns até ~35 palavras; lâminas de ação até ~60 (título + passos + exemplo).
- **Destaque:** no máximo um trecho por lâmina, marcado com `*asteriscos*`.
- **Ritmo de cor:** capa escura, conteúdo claro, um respiro escuro no meio ou antes do fechamento, chamada final clara. Respeite a proporção de cores do `design.md`.
- **Última lâmina:** uma chamada para ação só (salvar, comentar uma palavra, link na bio), coerente com o funil.
- Números, cases e depoimentos só de `provas.md`. Nada do `compliance.md`.

Com tudo aprovado, grave o `texto.md` na pasta da peça (é ele que o controle de qualidade compara com as imagens):
```
# Pnnn — [tema] — carrossel [formato] — texto aprovado em [data]
| Lâmina | Tipo | Tema | Conteúdo |
|---|---|---|---|
| 1 | capa | escuro | rótulo: ... / título: ... / subtítulo: ... / foto: (arquivo do banco ou nenhuma) |
| 2 | conteudo | claro | rótulo: O problema / título: ... / texto: ... |
| 3 | acao | claro | número: 01 / título: ... / passos: ...; ...; ... / na prática: ... |
...
## Legenda do post
## Derivado para LinkedIn (texto do post que acompanha o PDF)
```
A legenda e o derivado para LinkedIn são escritos **depois** do texto das lâminas aprovado e validados numa mensagem só.

## Passo 3. Identidade da empresa (uma vez por empresa)
Se ainda não existir `00-contexto/carrossel-marca.json`, crie a partir do `design.md`:
```json
{
  "cores": {"fundo": "#...", "fundo_alt": "#...", "escuro": "#...", "escuro_2": "#...", "texto": "#...",
            "texto_suave": "#...", "destaque": "#...", "destaque_2": "#...", "linha": "#..."},
  "fonte": "Montserrat",
  "fonte_url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap",
  "logo": "caminho/logo-para-fundo-claro.png",
  "logo_claro": "caminho/logo-para-fundo-escuro.png",
  "marca_dagua": "caminho/simbolo.png",
  "assinatura": "site ou @ da empresa",
  "numeros_cor": "texto"
}
```
- Caminhos relativos ao próprio arquivo (ex.: `logos/logo-colorido.png`).
- Sem logo para fundo escuro? Avise o responsável e peça a versão branca oficial. Não invente logo.
- Mostre ao responsável uma lâmina de teste antes de seguir. Esse arquivo garante que todos os carrosséis da empresa saiam iguais.

## Passo 4. Gerar as lâminas
1. Requisitos (confira; se faltar, peça autorização antes de instalar): Python 3, `pip install playwright pillow` e `python3 -m playwright install chromium`.
2. Crie `carrossel/laminas.json` na pasta da peça, com `"marca_arquivo"` apontando para `00-contexto/carrossel-marca.json` e as lâminas aprovadas (tipos: capa, conteudo, acao, lista, numero, citacao, comparacao, cta). O formato completo está no cabeçalho do script.
   - Foto na capa: use o banco (`fotos/fotos.md`); ajuste o enquadramento com `"foto_posicao"` (ex.: `"center 20%"`). Prefira retrato de meio corpo, vertical, em alta resolução.
3. **Valide sem gerar imagens:** `python3 "${CLAUDE_PLUGIN_ROOT}/skills/carrossel/scripts/renderizar.py" <pasta da peça>/carrossel/laminas.json --so-validar`
   O script confere contraste, quantidade de palavras, tamanho da capa e arquivos ausentes. Corrija os erros antes de seguir.
4. **Prova visual (rodada 3, só quando precisar):** no primeiro carrossel da empresa, quando o design mudar ou quando houver foto na capa, gere só a capa e uma lâmina de ação (`--laminas 1,3`) e peça aprovação do visual. Nos carrosséis seguintes, pule esta etapa.
5. **Gere todas:** o mesmo comando sem `--laminas`. Saem `01.png`, `02.png`… e `carrossel-linkedin.pdf`. Leia os avisos (por exemplo, texto encostando no rodapé) e corrija.
6. **Ajustes depois de gerado:** refaça só as lâminas alteradas com `--laminas 4,6` e, no fim, gere tudo uma vez para atualizar o PDF.
   - Se o destaque da marca não tiver contraste em fundo claro, o script troca automaticamente por marca-texto. Isso é esperado; informe o responsável na primeira vez.

## Passo 5. Olhar antes de entregar
Abra cada imagem e confira: leitura no tamanho do celular, nada cortado, destaque no lugar certo, foto bem enquadrada, logo correto para o fundo, numeração. Monte uma folha com todas as lâminas lado a lado para o responsável ver a sequência.

## Passo 6. Encaminhar
- Atualize a planilha: `registro.py atualizar empresas/<slug> publicacoes Pnnn '{"status": "em revisão", "pasta": "..."}'`.
- Encaminhe para a skill **controle-qualidade** e depois **estrategista-marketing (revisão final)**.

## Alternativa editável (Canva)
Se o responsável quiser ajustar à mão, e o conector do Canva estiver disponível, crie o design no Canva a partir do `texto.md` e do `design.md`, e entregue o link. As lâminas geradas pelo script continuam como referência.
