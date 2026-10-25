# Formatos das redes (conferido em outubro de 2026)

> **Idioma:** conduza tudo em português do Brasil.

Os formatos mudam com frequência. Na revisão trimestral, confira se este quadro continua valendo e, se mudou, registre uma melhoria.

## Instagram
| Peça | Tamanho | Proporção | Regra de corte e área segura |
|---|---|---|---|
| **Carrossel e post único (padrão do time)** | 1080 × 1350 | 4:5 | A grade do perfil mostra cada post num retângulo **3:4**, então corta cerca de **34 px de cada lado** do 4:5. Mantenha texto, rosto e logo a pelo menos 60 px das laterais (o gerador usa 96 px). |
| Carrossel 3:4 (opcional) | 1080 × 1440 | 3:4 | Só fica inteiro quando publicado **pelo aplicativo** do Instagram. Agendadores e publicação pela API limitam o feed a 4:5. Use apenas se a publicação for feita no celular e o responsável pedir. |
| Lâminas por carrossel | — | — | Até 20 no aplicativo; até 10 pelos agendadores. O padrão do time é 7 a 10. Todas as lâminas têm a mesma proporção da primeira. |
| **Reels** | 1080 × 1920 | 9:16 | Evite texto nos 14% de cima (~270 px), nos 35% de baixo (~670 px) e nos 6% das laterais (~65 px): ali ficam os botões e a legenda do aplicativo. |
| **Capa de Reels** | 1080 × 1920 | 9:16 | Na grade do perfil aparece só a **janela central 3:4 (1080 × 1440)**, cortando **240 px em cima e 240 px embaixo**. Título e rosto da capa sempre dentro dessa janela. |
| Story | 1080 × 1920 | 9:16 | Mesmas áreas livres do Reels (em cima e embaixo). |

O recorte **1:1 (quadrado) da grade não existe mais** desde janeiro de 2025.

## LinkedIn
| Peça | Tamanho | Observação |
|---|---|---|
| Carrossel (documento) | PDF das lâminas 1080 × 1350 | O gerador já entrega `carrossel-linkedin.pdf`. |
| Imagem | 1080 × 1350 ou 1200 × 1500 | Vertical ocupa mais espaço no feed do celular. |
| Vídeo | 1080 × 1920 ou 1080 × 1350 | Legenda embutida, porque muita gente assiste sem som. |
