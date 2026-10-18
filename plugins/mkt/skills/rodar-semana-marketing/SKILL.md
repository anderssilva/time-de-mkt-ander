---
name: rodar-semana-marketing
description: Conduz a semana de marketing de uma empresa do grupo do começo ao fim, na ordem da jornada (radar, seleção do estrategista, roteiros e carrosséis, gravação, edição, controle de qualidade, revisão final, ok do responsável, agendamento, métricas e melhorias), mostrando um painel do que está em cada etapa e chamando a skill certa. Use quando o usuário disser "roda a semana", "roda a máquina", "o que falta essa semana", "painel do marketing", "começa a semana da [empresa]", ou pedir o próximo passo do marketing de uma empresa.
---

# Rodar a semana de marketing

## Antes de começar
1. Trabalhe a partir da pasta `Marketing`. Identifique a empresa (`empresas/<slug>/`). Se a implantação não estiver concluída (`status-implantacao.md`), ofereça continuar com a skill estruturar-marketing-empresa.
2. Defina a semana (`AAAA-Sxx`, padrão ISO; padrão: a semana atual).

## Painel
Monte e mostre o painel, lendo `registro/publicacoes.csv`, `02-pautas/` e as pastas das peças:
```
Semana AAAA-Sxx — [Empresa] — tema do mês: ...
Pautas: proposta? selecionada? escolhida?
| Peça | Formato | Status | Próximo passo | Quem |
Melhorias propostas aguardando decisão: n
```

## Ordem da jornada
| # | Etapa | Skill | Aprovação do responsável |
|---|---|---|---|
| 1 | Radar de pautas | radar-pautas | — |
| 2 | Seleção | estrategista-marketing (modo A) | escolhe as pautas |
| 3 | Roteiro ou texto | roteiro-video / carrossel | aprova |
| 4 | Gravação | responsável | — |
| 5 | Plano de edição e montagem | editar-reels | aprova o plano |
| 5b | Geração das lâminas | carrossel | — |
| 6 | Controle de qualidade | controle-qualidade | — |
| 7 | Revisão final | estrategista-marketing (modo B) | dá o ok final |
| 8 | Agendamento | agendar-publicacao | confirma |
| 9 | Métricas (sexta e fim do mês) | leitura-metricas | — |
| 10 | Melhorias do mês | estrategista-marketing (modo C) | aprova item a item |

## Como conduzir
- Faça uma etapa por vez e pare em cada aprovação. Não pule etapas, nem para "ganhar tempo".
- Nas etapas 2, 6, 7 e 10, use os **agentes separados** quando estiver no Claude Code e eles existirem (`estrategista-marketing` e `controle-qualidade`). Eles avaliam sem ter visto a produção e usam um modelo mais forte. Passe para o agente só a empresa, a peça e o modo; ele lê os arquivos.
- Peça reprovada volta à etapa de produção com as observações. Na segunda reprovação, a decisão é do responsável.
- Ao final de cada sessão, mostre o painel atualizado e o próximo passo.
- Se o responsável pedir para medir o tempo, registre início e fim de cada etapa em `02-pautas/tempo-AAAA-Sxx.md` com o comando date, separando o tempo de trabalho do tempo esperando aprovação.

## Fim do mês e do trimestre
- Último dia útil do mês: leitura mensal (leitura-metricas) e melhorias (estrategista-marketing, modo C).
- Última semana do trimestre: revisão com a skill estruturar-marketing-empresa (modo revisão).
