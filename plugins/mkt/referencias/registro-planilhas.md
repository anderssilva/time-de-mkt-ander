# Registro em Planilha Google

Use esta referência quando `registro/fonte.json` da pasta da empresa tiver `"tipo": "planilhas"`. O programa `registro.py` avisa quando for preciso.

## Como funciona
- **Fonte oficial:** uma Planilha Google com quatro abas: `publicacoes`, `ideias`, `plano` e `melhorias`. A equipe abre pelo link, consulta e edita direto no navegador ou no celular.
- **Espelho local:** os CSV em `registro/` continuam existindo. São a cópia que o `registro.py` usa para calcular (próximo número, repetição de pautas, melhorias parecidas) e a **cópia de segurança** que fica na pasta da empresa.
- **Ciclo de toda rotina:** **Baixar** (planilha → espelho) no início · trabalhar com o `registro.py` como sempre · **Enviar** (espelho → planilha) no fim.

## Requisito
O **conector do Google Planilhas** (Google Sheets) ligado na conta do Claude usada no Claude Code, com acesso à planilha. É por ele que o Claude lê e grava.
- Um link público serve para **ler** (exportação em CSV), mas **não** permite gravar. Sem o conector, use o modo CSV: `registro.py fonte . csv`.

## Implantação (Etapa 6)
1. Pergunte: "Prefere o registro numa **Planilha Google com link** (mais fácil para a equipe ver e editar) ou nos **arquivos da pasta**?"
2. Se for planilha:
   1. Crie uma planilha nova chamada `Registro de marketing — <Empresa>` (pelo conector ou pedindo ao usuário) e anote o link.
   2. Crie as quatro abas com os nomes exatos e, na linha 1 de cada uma, os cabeçalhos de `registro.py cabecalhos` (na ordem). Congele a linha 1.
   3. Compartilhamento: siga a escolha do usuário. Se ele quiser **"Qualquer pessoa com o link: Editor"**, explique uma vez, sem insistir: quem tiver o link pode editar e apagar, então o link não deve ir para grupos abertos nem para fora da equipe; o histórico de versões do Google (Arquivo → Histórico de versões) e o espelho local permitem recuperar o que for perdido.
   4. Registre: `registro.py fonte . planilhas "<link>"`.
   5. Rode `registro.py iniciar .` para criar o espelho e importe o histórico normalmente. Ao final, faça o passo **Enviar**.
   6. Anote o link no `LEIA-ME.md` da empresa e no `status-implantacao.md`.

## Passo "Baixar" (início de cada rotina)
1. `registro.py pendentes .`: se houver pendências de uma sessão anterior, faça primeiro o passo **Enviar**.
2. Para cada aba (`publicacoes`, `ideias`, `plano`, `melhorias`): leia todos os valores pelo conector (do A1 até a última coluna e linha usadas), salve a lista de linhas num arquivo temporário `.json` (a primeira linha é o cabeçalho) e rode:
   `registro.py espelhar . <aba> <arquivo.json>`
3. Se o programa avisar colunas faltando na planilha, acrescente-as no fim da aba (sem mudar as existentes) e baixe de novo.
4. Apague os `.json` temporários.

O espelho vale por 30 minutos; depois disso o `registro.py` volta a avisar.

## Passo "Enviar" (depois de gravar com o registro.py)
1. `registro.py pendentes .` lista cada alteração com `tabela`, `acao`, `id` e `valores` (na ordem das colunas).
2. Para cada pendência, na aba da `tabela`:
   - `acao = "adicionar"`: acrescente `valores` como nova linha no fim da aba.
   - `acao = "atualizar"`: ache a linha cujo `id` (coluna A) é igual ao da pendência e substitua a linha inteira por `valores`. Se não achar, acrescente no fim e avise.
   - Tabela `plano` (sem id): sempre acrescente.
3. Confira lendo a aba de novo e então rode `registro.py sincronizado .`.

## Regras
- Nunca apague linhas da planilha. Para descartar, mude o status.
- Se alguém editou a planilha e o mesmo item foi alterado localmente na mesma sessão, mostre as duas versões ao responsável e pergunte qual vale antes de enviar.
- Edições feitas por pessoas direto na planilha valem: elas entram no espelho no próximo **Baixar**.
