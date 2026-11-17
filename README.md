# Calcula Fácil: site de calculadoras para gerar renda extra

Site com calculadoras trabalhistas e financeiras (salário líquido, 13º, férias, horas extras e juros compostos), atualizadas para 2026. Milhares de brasileiros pesquisam essas contas no Google todos os dias. A ideia é receber essas visitas e ganhar dinheiro com **anúncios (Google AdSense)** e **links de afiliado**.

**Custo: R$ 0.** A hospedagem é grátis no GitHub Pages. Domínio próprio (opcional, mas recomendado): cerca de R$ 40/ano no registro.br.

---

## Passo 1: colocar o site no ar (10 minutos, grátis)

1. Abra este repositório no GitHub e vá em **Settings → Pages**.
2. Em "Branch", escolha o branch principal e a pasta **/docs**. Clique em **Save**.
3. Em 1 ou 2 minutos aparece o endereço do site, algo como `https://seu-usuario.github.io/repository1/`.
4. Peça ao Claude para trocar `SITE_URL` em `ferramentas/gerar_paginas.py` por esse endereço e gerar as páginas de novo.

> Dica: com um domínio próprio (ex.: `calculafacil.com.br`), o Google confia mais no site e o AdSense aprova com mais facilidade. Compre no registro.br e configure em **Settings → Pages → Custom domain**.

## Passo 2: aparecer no Google (1 hora)

1. Acesse o **Google Search Console** (search.google.com/search-console) e adicione o endereço do site.
2. Envie o sitemap: `seu-endereco/sitemap.xml`.
3. A partir daí, o Google começa a mostrar suas páginas. As primeiras visitas costumam chegar em semanas, e o tráfego cresce ao longo dos meses.

## Passo 3: ganhar dinheiro

- **Google AdSense:** quando o site já tiver algumas páginas e visitas, peça a aprovação em adsense.google.com. Depois de aprovado, cole o código `ca-pub-...` em `ADSENSE_CLIENT` no gerador. Os espaços de anúncio já estão reservados nas páginas.
- **Afiliados:** inclua nos textos links de bancos digitais, cursos ou contas de investimento (programas da Awin, Lomadee, Hotmart). A calculadora de juros compostos combina muito bem com isso.

## Passo 4: crescer (o que realmente traz dinheiro)

Cada calculadora nova é mais uma "porta de entrada" do Google. Boas próximas calculadoras:
rescisão trabalhista, FGTS, seguro-desemprego, adicional noturno, financiamento de imóvel/veículo, MEI (DAS), conversão de CLT para PJ, IMC, regra de três e porcentagem.

**Meta realista:** sites assim costumam render de R$ 5 a R$ 20 a cada 1.000 visitas em anúncios. Com 50 mil visitas por mês, isso dá algo entre R$ 250 e R$ 1.000 por mês. Leva meses para chegar lá e não há garantia, mas o custo é zero e o trabalho, depois de pronto, é pequeno.

---

## Aulas de matemática (Aprender)

Além das calculadoras, o site tem uma trilha de 10 aulas curtas em `aprender.html`: porcentagem, descontos, soma e multiplicação de cabeça, frações, regra de três, equações, regra do 72 e derivada. Cada aula explica um truque e gera exercícios novos a cada tentativa, corrigidos na hora com o passo a passo. Há também um desafio de 60 segundos (`desafio.html`). É tudo grátis e sem cadastro: o progresso fica salvo só no navegador de quem usa.

Para criar uma aula nova, adicione um item em `LICOES` no gerador e um gerador de exercícios com o mesmo `id` em `docs/js/licoes.js`.

## Manutenção (todo mês de janeiro)

As tabelas de INSS e Imposto de Renda mudam todo ano. Elas ficam **em um único lugar**: o topo de `docs/js/calculos.js`. Basta pedir ao Claude: *"atualize as tabelas de INSS e IR para o ano novo"*.

## Para quem for mexer no código

- `docs/`: o site publicado (HTML, CSS e JS puros, sem dependências).
- `docs/js/calculos.js`: todas as regras de cálculo e as tabelas oficiais.
- `ferramentas/gerar_paginas.py`: gera as páginas, o sitemap e o robots.txt. Para criar uma calculadora nova, basta adicionar um item em `CALCS` e rodar `python3 ferramentas/gerar_paginas.py`.
- `docs/js/licoes.js`: geradores de exercícios das aulas. `docs/js/treino.js`: tela das aulas e do desafio.
- `tests/`: testes dos cálculos e dos exercícios (`node --test tests/*.test.js`).

*Os resultados são estimativas e não substituem a orientação de um contador.*
