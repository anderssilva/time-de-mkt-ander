# Time de Marketing — catálogo `zucchi`

Repositório privado que distribui o plugin `mkt` do Claude Code: o "motor" do marketing das empresas do grupo.
Os dados de cada empresa ficam fora daqui (pasta da empresa no Drive) e nunca são sobrescritos.

## Instalar (uma vez por computador)
No Claude Code:
1. `/plugin marketplace add anderssilva/time-de-mkt-ander`
2. `/plugin install mkt@zucchi`
3. Em `/plugin` → Marketplaces, ligar a atualização automática.

## Estrutura
| Caminho | Conteúdo |
|---|---|
| `.claude-plugin/marketplace.json` | Catálogo (nome `zucchi`) |
| `plugins/mkt/.claude-plugin/plugin.json` | Ficha do plugin (versão) |
| `plugins/mkt/skills/` | Skills (comandos `/mkt:...`) |
| `plugins/mkt/agents/` | Cargos que rodam como agente separado |
| `plugins/mkt/scripts/` | Programas (registro, renderização, vídeo) |
| `plugins/mkt/modelos/empresa/` | Modelo de pasta de empresa |

## Nova versão
Subir o `version` em `plugin.json` e em `marketplace.json`, anotar no `CHANGELOG.md` e enviar para o GitHub.
