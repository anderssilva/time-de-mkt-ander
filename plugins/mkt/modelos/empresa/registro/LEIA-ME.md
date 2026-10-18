# Registro

Quatro planilhas em CSV, fonte oficial do marketing desta empresa. Ficam aqui, sincronizadas pelo Google Drive.
Para visualizar, abra no Google Planilhas. **Não edite com o Excel** (ele costuma estragar acentos e vírgulas): peça ao Claude ou use o Google Planilhas.

| Arquivo | O que guarda |
|---|---|
| `publicacoes.csv` | Uma linha por peça (Pnnn), do status "ideia" até "publicado", com notas de avaliação e métricas |
| `ideias.csv` | Todas as pautas propostas pelo radar (Innn), inclusive descartadas, com o motivo |
| `plano.csv` | Temas e metas por mês do trimestre |
| `melhorias.csv` | Aprendizados (Mnnn) do estrategista e do controle de qualidade, até virarem regra |

Status da peça: ideia → aprovado → em produção → em revisão → pronto → agendado → publicado (ou descartado).
Status da melhoria: proposta → aprovada → incorporada (ou recusada).

As skills usam o programa `registro.py` do plugin mkt (pasta `scripts/`) para ler e gravar aqui. Gancho e ângulo são obrigatórios: é por eles que se confere repetição.
