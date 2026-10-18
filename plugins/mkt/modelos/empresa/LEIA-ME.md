# Marketing — [EMPRESA]

Responsável pela operação: [nome] · Implantado em: [dd/mm/aaaa] · Próxima revisão: [dd/mm/aaaa]
Metricool: conta [e-mail da empresa] · marca [nome] · redes conectadas: [lista]

## A jornada de cada peça

| # | Etapa | Skill | Sua aprovação |
|---|---|---|---|
| 1 | Radar de pautas (confere repetição na planilha) | radar-pautas | — |
| 2 | Seleção estratégica das pautas | estrategista-marketing | ✅ escolhe |
| 3 | Roteiro (vídeo) ou texto (carrossel) | roteiro-video / carrossel | ✅ aprova |
| 4 | Gravação dos vídeos → `video-bruto/` | você | — |
| 5 | Plano de edição a partir do bruto | editar-reels | ✅ aprova o plano |
| 6 | Montagem (vídeo) ou geração das lâminas (carrossel) | editar-reels / carrossel | — |
| 7 | Controle de qualidade técnico | controle-qualidade | — |
| 8 | Revisão estratégica final | estrategista-marketing | — |
| 9 | Seu ok final | você | ✅ aprova |
| 10 | Agendamento no Metricool (LinkedIn manual) e registro | agendar-publicacao | ✅ confirma |
| 11 | Leitura de métricas e melhorias | leitura-metricas | ✅ aprova melhorias |

Para rodar a semana inteira em ordem, peça: **"Roda a semana de marketing da [empresa]."** (skill rodar-semana-marketing)

## Onde fica cada coisa

| Pasta / arquivo | Para que serve |
|---|---|
| `00-contexto/` | Quem é a empresa: briefing, design, estilo de vídeo, tom de voz, provas, compliance, fotos. |
| `01-plano/` | Estratégia, plano do trimestre e rotinas. |
| `02-pautas/` | Radar semanal: pautas propostas e decisão. |
| `03-producao/AAAA-MM/Sxx_Pnnn_tema/` | Uma pasta por peça (roteiro, legenda, carrossel, vídeo, revisões). |
| `04-metricas/` | Leituras semanais e mensais dos resultados. |
| `registro/` | As quatro planilhas (publicações, ideias, plano, melhorias). |
| `status-implantacao.md` | Andamento da implantação. |

## Sua semana (tempo estimado)
- **Segunda:** aprovar 3 a 5 pautas selecionadas pelo estrategista (15 min).
- **Terça:** aprovar roteiros e textos de carrossel (20 min).
- **Quarta:** gravar os vídeos e soltar os brutos na pasta da peça (30 min).
- **Quinta:** aprovar os planos de edição (10 min).
- **Sexta:** dar o ok final nas peças revisadas e confirmar os agendamentos (20 min).

## Mês e trimestre
- **Último dia útil do mês:** leitura mensal das métricas e revisão das melhorias (o que vira regra).
- **Última semana do trimestre:** revisão do plano e novo plano trimestral (skill estruturar-marketing-empresa, modo revisão).

## Regras da casa
1. Nada vai ao ar sem: controle de qualidade aprovado, estrategista aprovado e o seu ok.
2. Peça reprovada volta para a produção com as observações; depois de 2 voltas, a decisão é sua.
3. Toda peça tem número (Pnnn) e linha na planilha `registro/publicacoes.csv`.
4. Números, cases e depoimentos só saem de `00-contexto/provas.md`.
5. Aprendizado aprovado vira regra no arquivo certo (estilo-video, tom-de-voz, design ou na skill). Se não virar regra, nada muda.
6. Contexto desatualizado gera conteúdo errado: avise quando algo mudar na empresa.
