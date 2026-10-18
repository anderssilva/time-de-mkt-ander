---
name: atualizar-time
description: Confere e aplica a atualização do Time de Marketing (o plugin mkt) e alinha as pastas das empresas com o modelo novo. Use quando o usuário disser "atualiza o time de marketing", "tem versão nova?", "qual versão está instalada", "atualizar as skills", ou quando outra skill avisar que há versão nova.
---

# Atualizar o Time de Marketing

1. Rode: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verificar-atualizacao.py"`.
2. **Se já estiver na última versão:** diga a versão e pare.
3. **Se houver versão nova:** mostre o que mudou (o programa traz o trecho do histórico) em linguagem simples, pergunte se atualiza agora e, com o ok:
   - rode o mesmo comando com `--aplicar`;
   - peça ao usuário para digitar `/reload-plugins` (ou abrir uma sessão nova). Esse comando só pode ser digitado por ele.
4. **Pastas das empresas:** para cada pasta em `empresas/` (menos `_modelo`), rode o programa com `--empresa empresas/<slug>`.
   - Arquivos novos do modelo faltando: ofereça copiar de `${CLAUDE_PLUGIN_ROOT}/modelos/empresa/` **sem sobrescrever nada** que já exista.
   - Depois, atualize a linha "Versão do modelo" no `status-implantacao.md` da empresa.
   - Planilhas de registro: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registro.py" iniciar empresas/<slug>` acrescenta colunas novas sem perder dados. No modo Planilha Google, acrescente as mesmas colunas no fim de cada aba.
5. Sem internet ou sem acesso ao GitHub: avise e siga; nada é bloqueado.

A atualização automática também pode ser ligada uma vez por computador: `/plugin` → Marketplaces → time-de-mkt → Enable auto-update.
