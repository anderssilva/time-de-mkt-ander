# Pasta da empresa sempre organizada

> **Idioma:** conduza tudo em português do Brasil.

**Regra:** nenhum arquivo fica solto na raiz da pasta da empresa. Cada arquivo tem um lugar.

## Onde fica cada coisa
| O quê | Onde |
|---|---|
| Guia do responsável e andamento | `LEIA-ME.md` e `status-implantacao.md` (os únicos arquivos na raiz) |
| Contexto, marca, referências, materiais recebidos | `00-contexto/` (materiais em `00-contexto/materiais/`) |
| Estratégia, plano do trimestre, rotinas | `01-plano/` |
| Pautas de cada semana | `02-pautas/pautas-AAAA-Sxx.md` |
| **Tudo de uma peça** (roteiro, texto, lâminas, PDF, vídeo bruto, edição, vídeo final, capa, legenda) | `03-producao/AAAA-MM/Sxx_Pnnn_tema/` |
| Leituras de métricas | `04-metricas/` |
| Registro (CSV, `fonte.json`, atalho da Planilha Google) | `registro/` |
| Arquivos temporários do trabalho | `03-producao/.../edicao/` da peça, ou apagados ao terminar |
| O que for descartado | `_lixeira/` (nunca apague de vez) |

Outras pastas numeradas que a empresa já tenha (por exemplo, `05-canais/`) são mantidas.

## Na prática
- **Ao gerar qualquer arquivo**, salve direto no lugar certo. Lâminas de carrossel saem em `<pasta da peça>/carrossel/`, nunca na raiz.
- **No início e no fim de cada sessão**, rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/organizar-pasta.py" .`. Ele lista o que está fora do lugar e sugere o destino.
- Mostre a lista ao usuário e, com o ok, mova cada item: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/organizar-pasta.py" . --mover "<arquivo>" "<destino>"`. O programa nunca sobrescreve e anota tudo em `00-contexto/materiais/indice.md`.
- Imagens soltas que pertencem a uma peça (por exemplo, `q_01.png`… `q_12.png`): pergunte de qual peça são e mova para `<pasta da peça>/carrossel/`.
