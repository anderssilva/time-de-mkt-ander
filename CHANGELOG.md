# Histórico de versões

## 1.0.0 — 18/10/2026
Migração do que existia em `Marketing/_grupo/`, sem reestruturar.
- 11 skills: estruturar-marketing-empresa, briefing-empresa, rodar-semana-marketing, radar-pautas, estrategista-marketing, roteiro-video, carrossel (com `scripts/renderizar.py`), editar-reels (com `scripts/` de transcrição, cortes e revisão), controle-qualidade, agendar-publicacao, leitura-metricas.
- 2 cargos que rodam como agente separado (modelo opus): estrategista-marketing e controle-qualidade.
- `scripts/registro.py` (antes em `_grupo/ferramentas/`).
- `modelos/empresa/` (antes em `empresas/_modelo/`).
- Caminhos trocados para `${CLAUDE_PLUGIN_ROOT}`; a regra de mudança em skill passa a ser "editar no repositório, subir a versão e enviar", no lugar do `instalar.sh`.
