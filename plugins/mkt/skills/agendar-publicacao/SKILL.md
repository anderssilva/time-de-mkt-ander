---
name: agendar-publicacao
description: Agenda no Metricool as peças aprovadas de uma empresa do grupo (status "pronto") e mantém o registro atualizado, preparando a publicação manual no LinkedIn quando necessário. Use quando o usuário pedir "agenda as peças", "programa as publicações", "sobe no Metricool", "marca como publicado", ou quando a skill rodar-semana-marketing chegar à etapa de agendamento. Nunca agenda nada sem confirmação explícita.
---

# Agendar e registrar publicações

## Antes de começar
1. Trabalhe a partir da pasta `Marketing`. Identifique a empresa.
2. Liste as peças prontas: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py" listar empresas/<slug> publicacoes status=pronto`.
   Só entram peças com `aprovado_por` e `data_aprovacao` preenchidos e com `revisao-qualidade.md` e `revisao-estrategica.md` aprovados na pasta. Se faltar algo, pare e diga o quê.
3. Leia `01-plano/rotinas.md` e `01-plano/estrategia.md` (canais e horários).

## Metricool
- Verifique se o conector do Metricool está disponível nesta sessão. Liste as marcas e confirme qual é a da empresa. **Nunca agende na marca de outra empresa.**
- Plano gratuito: uma marca por conta, sem LinkedIn e com limite de publicações por mês (confira o limite atual na conta). Avise se a semana passar do limite.
- Para cada peça, monte um resumo antes de agendar:
  | Peça | Canal | Formato | Data e hora | Arquivo | Legenda (início) |
  Horário: o definido nas rotinas ou o melhor horário sugerido pelo Metricool.
- **Espere a confirmação do responsável.** Só então agende.
- Se o conector não aceitar o envio do arquivo de vídeo ou das imagens, crie o rascunho com a legenda e peça ao responsável para anexar a mídia no planejador do Metricool, pelo link retornado.
- Se não houver conector, gere um pacote por peça (`publicar/` dentro da pasta da peça, com mídia, legenda e horário) e um passo a passo para agendar à mão.

## LinkedIn (publicação manual no plano gratuito)
- Gere `linkedin.md` na pasta da peça (texto do derivado aprovado) e indique o arquivo de mídia (imagem ou PDF do carrossel).
- Lembre o responsável de publicar e de colar o link aqui para registrar.

## Registro
- Ao agendar: `registro.py atualizar empresas/<slug> publicacoes Pnnn '{"status": "agendado", "data_publicacao": "AAAA-MM-DD HH:MM", "link": "<link do planejador>"}'`.
- Ao confirmar a publicação (pelo Metricool ou pelo responsável): status "publicado" e `link` do post publicado.
- Nunca apague linhas; peça cancelada vira "descartado" com o motivo em `observacoes`.
