---
name: atualizar-time
description: Confere e aplica a atualização do Time de Marketing (o plugin mkt), faz as configurações iniciais do computador (respostas em português, atualização automática) e alinha as pastas das empresas com o modelo novo. Use quando o usuário disser "atualiza o time de marketing", "configura o time de marketing", "tem versão nova?", "qual versão está instalada", "atualizar as skills", "o Claude está respondendo em inglês", ou quando outra skill avisar que há versão nova.
---

# Atualizar e configurar o Time de Marketing

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

## Configurações iniciais (conferir sempre)
1. **Idioma:** rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inicio-sessao.py" --ver-idioma`.
   Se não estiver em português, explique: "Vou configurar o Claude Code para responder sempre em português, em todas as sessões deste computador." Com o ok, rode o mesmo programa com `--configurar-idioma`. Vale a partir da próxima sessão.
2. **Atualização automática:** pergunte se já está ligada. Se não, oriente: digitar `/plugin` → **Marketplaces** → **time-de-mkt** → **Enable auto-update** (ativar atualização automática). Só o usuário consegue fazer esse passo.

## Versão
1. Rode: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verificar-atualizacao.py"`.
2. **Se já estiver na última versão:** diga a versão e pare.
3. **Se houver versão nova:** mostre o que mudou (o programa traz o trecho do histórico) em linguagem simples, pergunte se atualiza agora e, com o ok:
   - rode o mesmo comando com `--aplicar`;
   - peça ao usuário para digitar `/reload-plugins` (ou abrir uma sessão nova). Esse comando só pode ser digitado por ele.

## Pastas das empresas
4. Pasta da empresa: normalmente é a pasta atual (a que tem `status-implantacao.md`). Se o usuário cuidar de outras empresas, pergunte os caminhos das pastas delas. Para cada uma, rode o programa com `--empresa <caminho da pasta>` (`.` para a pasta atual).
   - Arquivos novos do modelo faltando: ofereça copiar de `${CLAUDE_PLUGIN_ROOT}/modelos/empresa/` **sem sobrescrever nada** que já exista.
   - Depois, atualize a linha "Versão do modelo" no `status-implantacao.md` da empresa.
   - Planilhas de registro: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py" iniciar .` acrescenta colunas novas sem perder dados. No modo Planilha Google, acrescente as mesmas colunas no fim de cada aba.
5. Sem internet ou sem acesso ao GitHub: avise e siga; nada é bloqueado.

Ao terminar, mostre um resumo: idioma, atualização automática, versão instalada e situação de cada pasta de empresa.
