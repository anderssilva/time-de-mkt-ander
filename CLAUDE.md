# Regras deste repositório

- Responda sempre em português do Brasil.
- **Commits e pull requests sem atribuição ao Claude:** nunca acrescente linhas como "Co-Authored-By: Claude…", "Claude-Session: …" ou links de sessão nas mensagens de commit nem na descrição de pull requests. A configuração `.claude/settings.json` deste repositório já desliga essa atribuição.
- A cada entrega: subir o `version` em `plugins/mkt/.claude-plugin/plugin.json`, registrar no `CHANGELOG.md` (com "Como atualizar") e validar com `claude plugin validate .` e `claude plugin validate ./plugins/mkt`.
