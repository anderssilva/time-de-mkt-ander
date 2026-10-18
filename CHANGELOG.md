# Histórico de versões

## 1.1.0 — 18/10/2026
**Atenção, reinstalação necessária:** o catálogo mudou de nome. Em quem já tinha instalado, rode uma vez:
`claude plugin marketplace remove zucchi`, depois `claude plugin marketplace add anderssilva/time-de-mkt-ander` e `claude plugin install mkt@time-de-mkt`, e ligue a atualização automática em `/plugin` → Marketplaces.

- **Material neutro:** catálogo `time-de-mkt`, autor genérico, exemplos sem nomes de empresas reais, paleta de exemplo neutra no gerador de carrosséis.
- **Vídeo com motion graphics como padrão:** novo passo a passo da identidade de vídeo (vídeo próprio → referências no What Ships → regras item a item → amostra de estilo de 5 a 8 s), com novo modelo de `estilo-video.md` e pasta `00-contexto/referencias-video/`. A edição e o controle de qualidade passam a seguir a amostra aprovada.
- **Registro em Planilha Google com link:** opção na implantação; a planilha vira a fonte oficial e os CSV, espelho local e cópia de segurança. Novos comandos no `registro.py`: `fonte`, `cabecalhos`, `espelhar`, `pendentes` e `sincronizado`; aviso automático quando o espelho está velho ou há envio pendente. Guia em `referencias/registro-planilhas.md`.
- **Atualização sempre em dia:** novo `scripts/verificar-atualizacao.py`; aviso ao abrir o Claude Code (no máximo uma consulta por dia); passo 0 na implantação e na semana; novo comando `/mkt:atualizar-time`, que também alinha as pastas das empresas com o modelo novo sem sobrescrever nada. A pasta da empresa passa a registrar a "Versão do modelo".
- **Documentação:** `README.md` completo com o mapa da jornada (`docs/`), `LICENSE` de uso restrito e versão declarada só no `plugin.json`.

## 1.0.0 — 18/10/2026
Migração do que existia em `Marketing/_grupo/`, sem reestruturar.
- 11 skills: estruturar-marketing-empresa, briefing-empresa, rodar-semana-marketing, radar-pautas, estrategista-marketing, roteiro-video, carrossel (com `scripts/renderizar.py`), editar-reels (com `scripts/` de transcrição, cortes e revisão), controle-qualidade, agendar-publicacao, leitura-metricas.
- 2 cargos que rodam como agente separado (modelo opus): estrategista-marketing e controle-qualidade.
- `scripts/registro.py` (antes em `_grupo/ferramentas/`).
- `modelos/empresa/` (antes em `empresas/_modelo/`).
- Caminhos trocados para `${CLAUDE_PLUGIN_ROOT}`; a regra de mudança em skill passa a ser "editar no repositório, subir a versão e enviar", no lugar do `instalar.sh`.
