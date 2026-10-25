---
name: agendar-publicacao
description: Agenda ou publica as peças aprovadas de uma empresa (status "pronto") pelo Metricool ou, sem ele, pelo Chrome com as contas do Instagram e do LinkedIn já logadas; marca os donos e pessoas da lista de marcações, prepara as mensagens de recompartilhamento e mantém o registro atualizado. Use quando o usuário pedir "agenda as peças", "programa as publicações", "posta no Instagram", "sobe no Metricool", "marca como publicado", ou quando a skill rodar-semana-marketing chegar à etapa de agendamento. Nunca publica nem agenda nada sem confirmação explícita.
---

# Agendar e registrar publicações

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

## Antes de começar
1. Trabalhe dentro da **pasta da empresa** (a pasta onde o Claude Code foi aberto, que tem `00-contexto/` e `registro/`). Se a pasta atual não for de uma empresa, pergunte qual é.
2. Liste as peças prontas: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py" listar . publicacoes status=pronto`.
   Só entram peças com `aprovado_por` e `data_aprovacao` preenchidos e com `revisao-qualidade.md` e `revisao-estrategica.md` aprovados na pasta. Se faltar algo, pare e diga o quê.
3. Leia `01-plano/rotinas.md` e `01-plano/estrategia.md` (canais e horários).

## Marcações (sempre)
- Leia `00-contexto/marcacoes.md`. Para cada peça, proponha quem marcar (donos das empresas e pessoas autorizadas, conforme o tema) com o @ de cada rede.
- Se a lista estiver vazia, peça uma vez: "Quem devo marcar nas publicações? Me passe os donos das empresas e outras pessoas autorizadas, com o @ do Instagram e o perfil do LinkedIn, que eu guardo em `00-contexto/marcacoes.md` para as próximas."
- Inclua as marcações no resumo da peça para confirmação.

## Qual caminho usar
1. **Conector do Metricool disponível nesta sessão:** use a seção Metricool.
2. **Sem Metricool:** use a seção **Publicar pelo Chrome**.
3. **Sem Metricool e sem Chrome:** gere o pacote manual (fim da seção Metricool).

## Metricool
- Verifique se o conector do Metricool está disponível nesta sessão. Liste as marcas e confirme qual é a da empresa. **Nunca agende na marca de outra empresa.**
- Plano gratuito: uma marca por conta, sem LinkedIn e com limite de publicações por mês (confira o limite atual na conta). Avise se a semana passar do limite.
- Para cada peça, monte um resumo antes de agendar:
  | Peça | Canal | Formato | Data e hora | Arquivo | Legenda (início) |
  Horário: o definido nas rotinas ou o melhor horário sugerido pelo Metricool.
- **Espere a confirmação do responsável.** Só então agende.
- Se o conector não aceitar o envio do arquivo de vídeo ou das imagens, crie o rascunho com a legenda e peça ao responsável para anexar a mídia no planejador do Metricool, pelo link retornado.
- Se não houver conector, gere um pacote por peça (`publicar/` dentro da pasta da peça, com mídia, legenda e horário) e um passo a passo para agendar à mão.

## Publicar pelo Chrome (quando não há Metricool)
Requer o Claude no Chrome (extensão) ligado e o Chrome aberto.
1. **Contas logadas:** peça ao responsável para entrar, no próprio Chrome, nas contas da empresa no **Instagram** (de preferência pelo **Meta Business Suite**, que permite agendar Instagram e Facebook) e no **LinkedIn**. O login é sempre dele: nunca digite senha nem códigos.
2. **Uma peça por vez, com o assistente de navegador (modelo leve, economiza o limite do plano):** passe ao agente `assistente-navegador` a tarefa fechada: rede e conta, caminhos das mídias na ordem (lâminas ou vídeo e capa), legenda aprovada, marcações e se é para publicar agora ou agendar (data e hora; o LinkedIn e o Meta Business Suite permitem agendar). Ele prepara tudo e **para antes do botão final**. Se o agente não estiver disponível, faça você mesmo, do mesmo jeito.
3. **Confirmação peça por peça.** Mostre ao responsável o resumo que o agente devolveu (rede, mídia, início da legenda, marcações, data e hora). Só depois do "pode publicar" chame o agente de novo com "o usuário autorizou publicar esta peça" para clicar em **Publicar** ou **Agendar**.
4. Se a página pedir algo inesperado (verificação, novo login, aceite de termos), pare e peça para o responsável resolver.
5. Ao terminar, copie o link do post ou do agendamento para o registro.

## Recompartilhamento
Depois de publicado, prepare em `publicar/recompartilhar.md` (na pasta da peça) uma mensagem curta e pronta para cada dono da lista de marcações, com o link do post e o pedido de recompartilhamento. O envio é feito pelo responsável; não envie mensagens em nome dele.

## LinkedIn (publicação manual no plano gratuito)
- Gere `linkedin.md` na pasta da peça (texto do derivado aprovado) e indique o arquivo de mídia (imagem ou PDF do carrossel).
- Lembre o responsável de publicar e de colar o link aqui para registrar.

## Registro
- Ao agendar: `registro.py atualizar . publicacoes Pnnn '{"status": "agendado", "data_publicacao": "AAAA-MM-DD HH:MM", "link": "<link do planejador>"}'`.
- Ao confirmar a publicação (pelo Metricool ou pelo responsável): status "publicado" e `link` do post publicado.
- Nunca apague linhas; peça cancelada vira "descartado" com o motivo em `observacoes`.
