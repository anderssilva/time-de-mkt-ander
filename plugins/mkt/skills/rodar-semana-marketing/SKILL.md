---
name: rodar-semana-marketing
description: Conduz a semana de marketing de uma empresa do começo ao fim, na ordem da jornada (radar, seleção do estrategista, roteiros e carrosséis, gravação, edição, controle de qualidade, revisão final, ok do responsável, agendamento, métricas e melhorias), mostrando um painel do que está em cada etapa e chamando a skill certa. Use quando o usuário disser "roda a semana", "roda a máquina", "o que falta essa semana", "painel do marketing", "começa a semana da [empresa]", ou pedir o próximo passo do marketing de uma empresa.
---

# Rodar a semana de marketing

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

## Passo 0. Atualização do time e da pasta (sempre, no início de cada semana)
Faça sempre, antes de qualquer outra coisa, e sem pular mesmo que o usuário peça pressa (leva menos de um minuto):
1. **Versão:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verificar-atualizacao.py"`. Ele consulta o GitHub na hora.
   - **Há versão nova:** mostre em linguagem simples o que mudou e pergunte **uma única vez**: "Há uma versão nova do Time de Marketing (x.y.z). Quer atualizar agora? Eu atualizo o time e ajusto as pastas da empresa." Com o ok:
     1. rode o mesmo programa com `--aplicar`;
     2. peça ao usuário para digitar `/reload-plugins` e depois dizer "continua" (esse comando só ele pode digitar);
     3. ao continuar, faça o item 2 abaixo **sem perguntar de novo** (a autorização já foi dada).
   - **Sem versão nova, ou o usuário preferiu não atualizar agora:** siga para o item 2.
   - **Sem internet ou sem acesso:** avise em uma linha e siga.
2. **Pasta da empresa:** rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atualizar-pasta.py" .` para ver se a estrutura da pasta está igual à do modelo da versão instalada.
   - Se houver mudanças, **aplique você mesmo** com `--aplicar`: o programa cria pastas, copia arquivos novos, move o que mudou de lugar e acrescenta colunas no registro, sem apagar nem sobrescrever nada, e anota tudo no `status-implantacao.md`.
   - Mostre ao usuário a lista do que foi feito.
3. **Organização:** rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/organizar-pasta.py" .`. Se houver arquivos soltos na raiz, mostre a lista com os destinos sugeridos e, com o ok, mova cada um (`--mover`). Repita no fim da sessão.
4. **Registro:** se `registro/fonte.json` indicar Planilha Google, faça o passo **Baixar** de `${CLAUDE_PLUGIN_ROOT}/referencias/registro-planilhas.md` e, ao fim da sessão, o passo **Enviar**.

## Antes de começar
1. Trabalhe dentro da **pasta da empresa** (a pasta onde o Claude Code foi aberto, que tem `00-contexto/` e `registro/`). Se a pasta atual não for de uma empresa, pergunte qual é. Se a implantação não estiver concluída (`status-implantacao.md`), ofereça continuar com a skill estruturar-marketing-empresa.
2. Defina a semana (`AAAA-Sxx`, padrão ISO; padrão: a semana atual).

## Painel
Monte e mostre o painel, lendo `registro/publicacoes.csv` (no modo Planilha Google, depois do passo Baixar), `02-pautas/` e as pastas das peças:
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
- **Você é o gerente (orquestrador).** Não produza as peças você mesmo: passe cada etapa ao cargo certo, conforme a tabela de `${CLAUDE_PLUGIN_ROOT}/referencias/orquestracao.md`, e mostre ao responsável o resumo que voltar. Isso deixa o modelo mais forte só para conversar e decidir, e economiza o limite do plano.
- Faça uma etapa por vez e pare em cada aprovação. Não pule etapas, nem para "ganhar tempo".
- Nas etapas 2, 6, 7 e 10, use os **agentes separados** quando estiver no Claude Code e eles existirem (`estrategista-marketing` e `controle-qualidade`). Eles avaliam sem ter visto a produção. Passe para o agente só a empresa, a peça e o modo; ele lê os arquivos.
- Peça reprovada volta à etapa de produção com as observações. Na segunda reprovação, a decisão é do responsável.
- Ao final de cada sessão: no modo Planilha Google, faça o passo **Enviar**; depois mostre o painel atualizado e o próximo passo.
- Se o responsável pedir para medir o tempo, registre início e fim de cada etapa em `02-pautas/tempo-AAAA-Sxx.md` com o comando date, separando o tempo de trabalho do tempo esperando aprovação.

## Fim do mês e do trimestre
- Último dia útil do mês: leitura mensal (leitura-metricas) e melhorias (estrategista-marketing, modo C).
- Última semana do trimestre: revisão com a skill estruturar-marketing-empresa (modo revisão).
