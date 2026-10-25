# Histórico de versões

Como atualizar (qualquer versão): no Claude Code, peça "atualiza o time de marketing" (`/mkt:atualizar-time`) e depois digite `/reload-plugins`. Pelo Terminal: `claude plugin marketplace update time-de-mkt && claude plugin update mkt@time-de-mkt`.

## 1.7.0 — 25/10/2026
**Como atualizar:** pelo jeito normal acima. Recomendado: conversa principal no Opus (`/model opus`) como gerente; se o limite apertar, `/model sonnet`.

- **Gerente e cargos (orquestração):** a conversa principal vira o gerente de marketing, que conversa, decide e distribui; a execução vai para os cargos (`referencias/orquestracao.md`).
- **Modelo certo para cada tarefa:** novos cargos `redator`, `designer` e `editor-video` (Sonnet), `operador` e `assistente-navegador` (Haiku); `estrategista-marketing` e `controle-qualidade` passam de Opus para Sonnet; `/mkt:atualizar-time` roda no Haiku.
- **Publicação pelo Chrome com o assistente de navegador (Haiku):** prepara cada post e para antes do botão final; o clique só acontece depois do ok do responsável, peça por peça.
- **Folha de revisão do carrossel:** o gerador cria `folha-revisao.jpg` com todas as lâminas lado a lado; revisão e controle de qualidade usam a folha e só abrem uma lâmina em tamanho real se houver problema.
- **Guia de economia** (`referencias/economia.md`): uma peça por conversa, texto antes de imagem, ajustes só nas lâminas alteradas, aprovações em lote.

## 1.6.0 — 25/10/2026
**Como atualizar:** pelo jeito normal acima. Na próxima semana planejada, o time cria `00-contexto/marcacoes.md` nas empresas e propõe organizar o que estiver solto na raiz.

- **Formatos atualizados do Instagram:** novo `referencias/formatos-redes.md`. Carrossel segue em 1080 × 1350 (4:5), com a regra da grade 3:4 do perfil (nada importante a menos de 60 px das laterais); capa de Reels com título e rosto na janela central 1080 × 1440 (o recorte 1:1 saiu do modelo); opção 3:4 só para publicação pelo aplicativo. O `design.md`, a edição de vídeo (agora entrega a capa) e o controle de qualidade seguem essas regras.
- **Modo Design para o padrão dos carrosséis:** ao montar o padrão visual pela primeira vez, o time sugere criar as lâminas-modelo no modo Design do Claude e depois replica o padrão no gerador.
- **Pasta sempre organizada:** regra em todos os comandos e cargos, novo `referencias/organizacao-pasta.md` e novo `scripts/organizar-pasta.py`, que lista o que está solto na raiz, sugere o destino e move com segurança (nunca sobrescreve; anota no índice de materiais). Roda no início e no fim de cada semana.
- **Publicar pelo Chrome sem Metricool:** com as contas do Instagram (ou Meta Business Suite) e do LinkedIn logadas pelo responsável, o Claude prepara cada publicação e só publica ou agenda depois do ok de cada peça.
- **Marcações e recompartilhamento:** novo `00-contexto/marcacoes.md` com os donos das empresas e os @ de cada rede; as publicações já saem com as marcações, e o time prepara as mensagens de recompartilhamento para o responsável enviar.

## 1.5.0 — 23/10/2026
**Como atualizar:** pelo jeito normal acima. Na próxima semana planejada, o próprio time confere e ajusta as pastas das empresas (cria `00-contexto/materiais/`).

- **Arquivos do chat guardados na pasta do projeto:** novo `scripts/guardar-arquivo.py` e regras em `referencias/arquivos-recebidos.md`. Todo arquivo enviado no chat é copiado para a pasta certa da empresa (marca, fotos, documentos, redes, referências, trilhas ou a pasta da peça), sem sobrescrever, e anotado em `00-contexto/materiais/indice.md`. A regra está em todos os comandos e cargos, e é lembrada ao abrir o Claude Code numa pasta de empresa.
- **Atualização em toda semana:** o Passo 0 do planejamento semanal consulta o GitHub na hora, mostra o que mudou e pergunta uma vez se atualiza; com o ok, atualiza o time e, depois do `/reload-plugins`, ajusta a pasta da empresa sem perguntar de novo.
- **Pastas ajustadas pelo próprio Claude:** novo `scripts/atualizar-pasta.py` (mostra o que mudaria; com `--aplicar`, cria pastas, copia arquivos novos, aplica as mudanças de estrutura de `modelos/migracoes.json`, acrescenta colunas no registro e anota tudo no `status-implantacao.md`). Nunca apaga nem sobrescreve.
- Nova pasta no modelo: `00-contexto/materiais/` (marca, documentos, redes, trilhas, outros).

## 1.4.0 — 23/10/2026
**Como atualizar:** pelo jeito normal acima. Empresas já implantadas não precisam mudar nada: as pastas antigas em `Marketing/empresas/<nome>/` continuam funcionando, basta abrir o Claude Code dentro delas.

- **Pasta da empresa = pasta do projeto:** a implantação cria `00-contexto/`, `01-plano/`, `02-pautas/`, `03-producao/`, `04-metricas/` e `registro/` direto na pasta onde o Claude Code foi aberto, sem criar `empresas/` nem uma subpasta com o nome da empresa. Antes de criar, confirma a pasta com o usuário.
- Todos os comandos e cargos passam a trabalhar dentro da pasta da empresa; nos programas, o caminho da empresa é `.` (pasta atual).
- `/mkt:atualizar-time` confere a pasta atual e pergunta os caminhos das outras empresas, quando houver.
- README atualizado com a nova estrutura.

## 1.3.0 — 19/10/2026
**Como atualizar:** pelo jeito normal acima. Empresas com o diagnóstico ainda em branco podem receber o modelo novo de `diagnostico.md` e `estrategia.md`; nas já preenchidas, nada é sobrescrito.

- **Diagnóstico novo, com exemplos:** passo a passo em `skills/estruturar-marketing-empresa/referencias/diagnostico.md`, em cinco blocos: objetivo do marketing (com exemplos de cada opção), qual jogo a empresa joga (monopólio, oligopólio, competição com diferenciação, competição pura — matriz da Kaiser Associates Latam), modelo de crescimento (pelo produto, pelo marketing ou pelo vendedor, com perguntas de apoio), maturidade nos 4 pilares de receita (Marca, Demanda, Vendas, Dados) e canais/operação/ferramentas. Novo modelo de `00-contexto/diagnostico.md`.
- **Pilar de crescimento na estratégia:** a IA avalia o diagnóstico e propõe um pilar foco para o trimestre, com o porquê, as ações e as estratégias do jogo (`referencias/pilar-crescimento.md`). O modelo de `01-plano/estrategia.md` ganha a seção "Pilar de crescimento do trimestre"; pilares de conteúdo, funil e metas passam a derivar dela.
- **Checklist da implantação** inclui o diagnóstico completo e o pilar de crescimento validado.

## 1.2.0 — 18/10/2026
**Como atualizar:** pelo jeito normal acima. Quem ainda está na 1.0.0 (catálogo antigo `zucchi`) precisa reinstalar uma vez, como descrito na 1.1.0. Depois, peça "configura o time de marketing" para fixar o português.

- **Português garantido:** regra de idioma (português do Brasil) no início de todos os comandos e cargos; ao abrir o Claude Code, o time avisa ao Claude que a conversa é em português quando o idioma ainda não está configurado; o comando `/mkt:atualizar-time` grava `"language": "portuguese"` nas configurações do Claude Code, com autorização.
- **Configurações iniciais:** `/mkt:atualizar-time` passa a conferir idioma, atualização automática, versão e pastas das empresas (inclusive pastas fora de `empresas/`). Novo programa `scripts/inicio-sessao.py`, chamado ao abrir, limpar ou compactar uma sessão.
- **Design com Refero Styles:** novo passo a passo do `design.md` (material existente → referências no Refero Styles, https://styles.refero.design/ → regras item a item → amostra visual com duas lâminas). O modelo de `design.md` ganha a seção de referências e a pasta `00-contexto/referencias-design/`. O estilo de vídeo herda cores e fontes do design; o What Ships continua sendo a referência de movimento.
- **README:** configuração inicial, garantia de português, design da marca e um guia de atualização mais direto.

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
