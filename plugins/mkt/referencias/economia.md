# Economia do limite do plano

> **Idioma:** conduza tudo em português do Brasil.

No plano Pro, o limite de uso acaba rápido se tudo rodar no modelo mais forte. O time divide o trabalho por modelo e evita desperdícios.

## Gerente no Opus, equipe em modelos mais leves
A conversa principal é o **gerente de marketing** (orquestrador). Ele conversa com o responsável, decide, define padrões e distribui o trabalho; quem executa são os cargos (agentes), cada um no modelo certo:

| Cargo (agente) | Modelo | O que faz |
|---|---|---|
| **Gerente** (conversa principal) | **Opus** (`/model opus`) | Conversa, aprovações, decisões, padrões (diagnóstico, estratégia, design), distribuição das tarefas |
| `estrategista-marketing` | Sonnet | Seleção de pautas, revisão final, melhorias |
| `controle-qualidade` | Sonnet | Revisão técnica |
| `redator` | Sonnet | Roteiros, textos de carrossel, legendas, LinkedIn |
| `designer` | Sonnet | Lâminas, PDF, folha de revisão |
| `editor-video` | Sonnet | Plano de edição, montagem, capa |
| `operador` | Haiku | Organizar pasta, guardar arquivos, sincronizar planilha, pacotes, conferir versão |
| `assistente-navegador` | Haiku | Preparar publicações no Chrome (para antes do botão final), coletar números |
| Comando `/mkt:atualizar-time` | Haiku | Atualizar e configurar o time |

O que faz a economia: o Opus **não lê** os arquivos de contexto inteiros, **não abre imagens** e **não escreve** os textos longos. Ele só lê o resumo que cada cargo devolve e o mostra ao responsável.

Se o limite estiver apertado, rode também o gerente no Sonnet (`/model sonnet`): os cargos continuam nos mesmos modelos.

## Hábitos que mais economizam
1. **Uma peça por conversa.** Ao terminar uma peça, digite `/clear` (limpa a conversa; tudo já está salvo na pasta). Conversas longas ficam caras porque o Claude relê tudo a cada resposta.
2. **Texto antes de imagem.** As rodadas de texto custam pouco; gerar e olhar imagens custa muito. Só gere as lâminas com o texto aprovado.
3. **Folha de revisão.** Revise carrosséis pela `folha-revisao.jpg` (todas as lâminas numa imagem). Abra uma lâmina em tamanho real só se houver problema nela.
4. **Prova visual só quando precisar:** no primeiro carrossel da empresa ou quando o design mudar.
5. **Ajustes pontuais:** refaça só as lâminas alteradas (`--laminas 4,6`).
6. **Aprovações em lote:** escolha pautas e aprove textos de várias peças de uma vez, na segunda-feira.
7. **Esforço de raciocínio:** "Médio" para produção; "Baixo" basta para tarefas simples.

## Para o Claude
- Na conversa principal, você é o **gerente**: delegue produção, revisão, tarefas mecânicas e de navegador aos cargos (veja `referencias/orquestracao.md`). Só faça você mesmo o que exige conversa com o responsável ou decisão.
- Não abra imagens ou quadros de vídeo sem necessidade; prefira folhas de revisão e saídas de texto dos programas.
- Leia só os arquivos de contexto que a tarefa precisa.
- Ao terminar uma peça, sugira `/clear` antes da próxima.
