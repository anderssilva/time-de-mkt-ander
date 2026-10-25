---
name: briefing-empresa
description: Conduz o briefing (levantamento de contexto) de uma empresa ANTES de qualquer trabalho de marketing, conteúdo ou copy, e entrega o arquivo contexto-ia.md pronto. É chamada pela skill estruturar-marketing-empresa na etapa 2, mas também pode ser usada sozinha. Use sempre que o usuário pedir para "fazer o briefing", "descrever a empresa", "montar o contexto da empresa", "atualizar o contexto", ou colar/anexar um contexto-ia.md existente. Acione também quando o usuário pedir qualquer peça de marketing e ainda não houver contexto da empresa na conversa nem na pasta da empresa.
---

# Briefing da Empresa (contexto da empresa para a IA)

> **Idioma:** responda sempre em **português do Brasil**: perguntas, resumos, avisos de andamento, arquivos e comentários, mesmo que a conversa, uma ferramenta ou um erro apareçam em inglês. Evite termos em inglês; quando precisar usar um, coloque o significado prático entre parênteses.

> **Arquivos recebidos:** todo arquivo que o usuário enviar no chat é guardado na pasta da empresa antes de ser usado, com `scripts/guardar-arquivo.py` (veja `${CLAUDE_PLUGIN_ROOT}/referencias/arquivos-recebidos.md`).

> **Pasta organizada:** nada fica solto na raiz da pasta da empresa; salve cada arquivo direto no lugar certo (tudo de uma peça vai na pasta da peça). Veja `${CLAUDE_PLUGIN_ROOT}/referencias/organizacao-pasta.md`.

> **Economia:** siga `${CLAUDE_PLUGIN_ROOT}/referencias/economia.md` (modelo certo para cada tarefa, folha de revisão em vez de abrir cada imagem, uma peça por conversa).

## Objetivo

Antes de escrever qualquer texto, roteiro, post, e-mail ou estratégia para uma empresa, a IA precisa conhecê-la. Esta skill transforma a conversa com o usuário em um arquivo `contexto-ia.md` completo, no mesmo formato do formulário `briefing-empresa.html`. Esse arquivo vira a base de todo o trabalho seguinte.

Quem usa: o sócio ou responsável pelo marketing de cada empresa atendida.

**Onde salvar:** em `00-contexto/contexto-ia.md`, dentro da pasta da empresa. Se a skill foi chamada pela estruturar-marketing-empresa, use o caminho que ela indicar. Se a pasta da empresa ainda não existir, pergunte se o usuário quer rodar a implantação completa antes.

## Regras de ouro

1. **Briefing primeiro, conteúdo depois.** Se o usuário pedir uma peça (post, copy, e-mail, roteiro) e não houver contexto da empresa na conversa, diga em uma frase que vai levantar o briefing antes e comece o passo 1. Não produza a peça antes.
2. **Nunca invente.** Só entra no arquivo o que o usuário disse, o que está em material fornecido por ele ou o que foi lido em fonte pública que ele autorizou. O que faltar fica como `(não informado)`.
3. **Separe fato de suposição.** Se algo veio de pesquisa no site/redes e não foi confirmado pelo usuário, pergunte antes de gravar: "Isso a empresa confirmou ou é leitura do site?". Informação não confirmada vai marcada com `(a confirmar)`.
4. **Uma conversa leve.** Pergunte um bloco por vez, com perguntas curtas. Aceite respostas soltas, desorganizadas ou transcritas de áudio; você organiza. Não despeje as 45 perguntas de uma vez.
5. **Idioma.** Tudo em português do Brasil. Evite palavras em inglês; se usar, coloque o significado prático entre parênteses (ex.: lead (contato interessado), CRM (sistema de gestão de clientes)).

## Passo a passo

### Passo 1: Ponto de partida
Pergunte, em uma mensagem curta:
- Qual é o nome da empresa?
- Já existe um `contexto-ia.md` dessa empresa (de outra conversa ou gerado pelo formulário)? Se sim, peça para colar ou anexar.
- Você tem material de base para me passar? (site, apresentação comercial, proposta, perfis de redes sociais, textos antigos, áudio de reunião). Ou prefere que eu monte tudo a partir das suas respostas?

Se o usuário já tem o arquivo: leia, mostre em 5 linhas o que está preenchido e o que está `(não informado)`, e pergunte o que mudou ou o que quer completar. Pule para o passo 3 só nos blocos incompletos.

Se ele passar material ou autorizar pesquisa no site/redes: extraia o que der, apresente como "rascunho do que encontrei" e peça correção. Depois siga para o passo 2 apenas nos pontos que o material não cobre.

### Passo 2: Entrevista por blocos
Siga esta ordem. Em cada bloco, faça só as perguntas dos campos vazios, em linguagem de conversa. Ao final de cada bloco, devolva um mini resumo de 2 a 4 linhas ("Entendi assim: ...") e pergunte se está certo antes de avançar.

**Bloco 1. Identidade** (campos: nome, site, setor/nicho, proposta de valor única, missão, história)
- Setor: peça específico. "Consultoria" é fraco; "consultoria de gestão para indústrias de médio porte no Sul" é bom.
- Proposta de valor única: "O que só essa empresa entrega, em uma frase?"
- História: busque o momento de virada que criou a autoridade.

**Bloco 2. Redes sociais** (Instagram, LinkedIn, TikTok, YouTube, X, Facebook, Threads, outras)
- Só @ ou link. Se a rede não é usada, deixe `(não informado)`.

**Bloco 3. Público-alvo** (3 perfis por ordem de prioridade, dor comum, desejos, objeções)
- Perfil precisa ter: cargo ou papel, porte/idade, região, e o gatilho que faz a pessoa procurar a empresa.
- Se vier "pequenas e médias empresas", aprofunde: quem dentro da empresa decide? Qual o momento de dor?
- Desejos: o que querem alcançar (não o que querem evitar).
- Objeções: por que NÃO compram (preço, tempo, desconfiança, já tentaram antes).

**Bloco 4. Produto ou serviço** (descrição, preço, modelo de cobrança, garantia, features, benefícios)
- Modelo de cobrança: ofereça as opções Assinatura mensal, Assinatura anual, Pagamento único, Gratuito com plano pago (freemium), Por uso/consumo ou Híbrido. No arquivo, grave o código correspondente (ver tabela de códigos no Passo 4).
- Features = o que o produto FAZ. Benefícios = o que o cliente GANHA. Se o usuário misturar, separe e confirme.

**Bloco 5. Fluxo de venda** (topo, meio e fundo de funil, ferramentas)
- Topo de funil = como atrai contatos. Meio = como nutre e convence. Fundo = como fecha a venda.
- Ferramentas: sistema de gestão de clientes (CRM), pagamento, automação de e-mail, agenda etc.

**Bloco 6. Tom de voz** (tom principal, tom proibido, slogans, palavras-chave do setor)
- Tom principal, escolher entre: Profissional / Corporativo; Conversacional / Amigável; Ousado / Provocativo; Empático / Consultivo; Urgente / Direto; Autoritário / Especialista; Divertido / Descontraído. No arquivo, grave o código correspondente (ver tabela de códigos no Passo 4). Se o tom da empresa for uma mistura, escolha o dominante como principal e descreva o resto em "Slogans/frases de efeito" ou nas observações do usuário.
- Tom proibido: o que a empresa jamais quer soar.
- Palavras-chave: termos que o público do setor reconhece, separadas por vírgula.

**Bloco 7. Prova social** (números, cases/depoimentos, reconhecimentos)
- Peça números concretos (quantos clientes, quanto de resultado, em quanto tempo). Sem número, registre `(não informado)`. Nunca arredonde ou melhore.

**Bloco 8. Mercado e concorrência** (concorrentes diretos, diferencial, posicionamento)
- Concorrente = com quem o cliente final compara. Posicionamento: premium, acessível, inovador, tradicional etc.

**Bloco 9. Compliance e restrições** (o que não pode dizer, requisitos legais, palavras proibidas)
- Pergunte sempre, mesmo que pareça óbvio: promessas de resultado, termos regulados do setor, LGPD (lei de proteção de dados), avisos obrigatórios.
- Se o usuário não souber, registre `(não informado)` e sinalize no fechamento que este bloco precisa ser validado com a empresa.

**Bloco 10. Links** (site, página de preços, cases, avaliações)

### Passo 3: Checagem de qualidade
Antes de gerar o arquivo, verifique os campos essenciais: nome, setor, proposta de valor única, perfil 1, dor comum, descrição do produto, tom principal, o que não pode dizer.
- Se faltar algum, avise com clareza: "Faltam estes pontos essenciais: ... Quer completar agora ou seguimos assim mesmo?".
- Se o usuário optar por seguir, gere o arquivo mesmo assim e liste ao final o que ficou em aberto.

### Passo 4: Gerar o contexto-ia.md
- Use **exatamente** o modelo do fim deste arquivo (mesmos emojis, rótulos, marcadores e ordem). O formulário `briefing-empresa.html` lê esse arquivo pelo botão "Carregar do .md"; qualquer mudança de rótulo quebra a leitura.
- Data de geração no formato dd/mm/aaaa.
- Dois campos usam códigos fixos, porque é assim que o formulário os lê. Grave exatamente o código, sem acento e em minúsculas:

  | Campo | Opção na conversa | Código a gravar |
  |---|---|---|
  | Modelo | Assinatura mensal | `assinatura` |
  | Modelo | Assinatura anual | `anual` |
  | Modelo | Pagamento único | `unico` |
  | Modelo | Gratuito com plano pago (freemium) | `freemium` |
  | Modelo | Por uso/consumo | `usage` |
  | Modelo | Híbrido | `hibrido` |
  | Tom principal | Profissional / Corporativo | `profissional` |
  | Tom principal | Conversacional / Amigável | `conversacional` |
  | Tom principal | Ousado / Provocativo | `bold` |
  | Tom principal | Empático / Consultivo | `empatico` |
  | Tom principal | Urgente / Direto | `urgente` |
  | Tom principal | Autoritário / Especialista | `autoritario` |
  | Tom principal | Divertido / Descontraído | `divertido` |

  Ao mostrar o arquivo para conferência, diga em português o que cada código significa (ex.: "Modelo: assinatura = assinatura mensal").
- Campos de lista (desejos, objeções, features, benefícios): um item por linha, começando com dois espaços e hífen.
- Campos vazios: `(não informado)`. Nas listas vazias, a linha `  (não informado)`.
- Redes sociais: só as que existem, no formato `• Instagram: @perfil`.
- Mostre o arquivo completo ao usuário para conferência e salve em `00-contexto/contexto-ia.md` da pasta da empresa.

### Passo 5: Fechamento
Em poucas linhas:
1. Confirme que o contexto está pronto.
2. Liste o que ficou em aberto ou `(a confirmar)`.
3. Lembre que, em qualquer conversa futura sobre essa empresa, a IA deve ler o `contexto-ia.md` da pasta dela antes de começar.
4. Pergunte qual é a demanda de hoje e siga com ela usando o contexto.

Se esta skill foi chamada pela estruturar-marketing-empresa, em vez do item 4 volte para a etapa 3 (Identidade) daquela skill.

## Depois do briefing: como usar o contexto

Enquanto o contexto da empresa estiver na conversa:
- Use-o como base de TODAS as respostas.
- Respeite o tom de voz, as restrições de compliance e as palavras proibidas.
- Nunca invente dados que não constam nele (números, cases, preços, prazos).
- Se faltar informação para a tarefa, pergunte ao usuário em vez de supor.
- Se surgir informação nova e relevante durante o trabalho, ofereça atualizar o `contexto-ia.md`.

## Atualização de um contexto existente

Quando o usuário trouxer um arquivo antigo e quiser atualizar: mantenha tudo que não foi alterado, mude só o que ele indicar, atualize a data de geração e devolva o arquivo completo (não só as mudanças).

## Modelo do contexto-ia.md

Copie a estrutura abaixo. As linhas de exemplo (`@perfil`, `desejo 1`, `termo 1`...) mostram o formato e devem ser substituídas ou trocadas por `(não informado)`.

```
=== CONTEXTO DA EMPRESA ===
Gerado em: DD/MM/AAAA

🏢 IDENTIDADE
• Nome: (não informado)
• Site: (não informado)
• Setor/Nicho: (não informado)
• Proposta de valor única: (não informado)
• Missão: (não informado)
• História / Minibio: (não informado)

📱 REDES SOCIAIS
• Instagram: @perfil
• LinkedIn: link da página

🎯 PÚBLICO-ALVO (3 perfis, em ordem de prioridade)
• Perfil 1 (prioridade máxima): (não informado)
• Perfil 2 (prioridade secundária): (não informado)
• Perfil 3 (prioridade terciária): (não informado)
• Dor comum a todos: (não informado)
• Desejos principais:
  - desejo 1
  - desejo 2
• Objeções comuns:
  - objeção 1
  - objeção 2

🛒 PRODUTO/SERVIÇO
• Descrição: (não informado)
• Preço: (não informado)
• Modelo: (código: assinatura | anual | unico | freemium | usage | hibrido; ou vazio)
• Garantia: (não informado)
• Features principais:
  - o que o produto faz 1
  - o que o produto faz 2
• Benefícios traduzidos:
  - o que o cliente ganha 1
  - o que o cliente ganha 2

🛍️ FLUXO DE VENDA (funil)
• Topo de funil — TOFU (atração/geração de leads): (não informado)
• Meio de funil — MOFU (nutrição/consideração): (não informado)
• Fundo de funil — BOFU (decisão/fechamento): (não informado)
• Ferramentas/plataformas: (não informado)

🎨 TOM DE VOZ
• Tom principal: (código: profissional | conversacional | bold | empatico | urgente | autoritario | divertido; ou vazio)
• Tom proibido: (não informado)
• Slogans/frases de efeito: (não informado)
• Palavras-chave do setor: termo 1, termo 2, termo 3

🏆 PROVA SOCIAL
• Números/métricas: (não informado)
• Cases/depoimentos: (não informado)
• Reconhecimentos: (não informado)

⚔️ MERCADO
• Concorrentes diretos: (não informado)
• Diferencial competitivo: (não informado)
• Posicionamento: (não informado)

🛡️ COMPLIANCE
• O que não pode dizer: (não informado)
• Requisitos legais: (não informado)
• Palavras proibidas: (não informado)

🔗 LINKS
• Site: (não informado)
• Preços: (não informado)
• Cases: (não informado)
• Reviews: (não informado)

=== INSTRUÇÃO PARA A IA ===
Use o contexto acima como base para TODAS as respostas de copywriting.
Nunca invente dados que não constam aqui.
Sempre respeite o tom de voz, as restrições de compliance e as palavras proibidas.
Quando não souber algo, pergunte ao usuário em vez de supor.
```
