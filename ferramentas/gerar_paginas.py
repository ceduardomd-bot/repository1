"""Gera as páginas HTML do site. Rode: python3 ferramentas/gerar_paginas.py"""
import pathlib, datetime

SITE_NOME = "Calcula Fácil"
SITE_URL = "https://SEU-USUARIO.github.io/repository1"  # troque quando tiver domínio
ADSENSE_CLIENT = ""  # ex.: "ca-pub-1234567890123456" (deixe vazio até ser aprovado)
RAIZ = pathlib.Path(__file__).resolve().parent.parent / "docs"

CALCS = [
  dict(arq="salario-liquido.html", nome="Salário Líquido",
    titulo="Calculadora de Salário Líquido 2026 (com INSS e IR atualizados)",
    desc="Descubra quanto você recebe de verdade. Calcule o salário líquido 2026 com descontos de INSS, Imposto de Renda e a nova isenção até R$ 5 mil.",
    campos=[("bruto","Salário bruto (R$)","3000"),("dep","Nº de dependentes","0"),("outros","Outros descontos (R$)","0")],
    js="""var r=Calc.salarioLiquido(num('bruto'),num('dep'),num('outros'));
mostrar([['Salário bruto',r.bruto],['(−) INSS',r.inss],['(−) Imposto de Renda',r.irrf],['(−) Outros descontos',r.outros],['Salário líquido',r.liquido,1]]);""",
    texto="""<h2>Como o salário líquido é calculado</h2>
<p>O salário líquido é o valor que cai na sua conta. Ele é o salário bruto menos os descontos obrigatórios: <strong>INSS</strong> e <strong>Imposto de Renda Retido na Fonte (IRRF)</strong>, além de outros descontos como vale-transporte, plano de saúde ou pensão.</p>
<h2>Isenção do Imposto de Renda até R$ 5.000 em 2026</h2>
<p>Desde janeiro de 2026 (Lei 15.270/2025), quem recebe até R$ 5.000 por mês não tem imposto retido na fonte. Entre R$ 5.000,01 e R$ 7.350 o desconto é reduzido gradualmente. Acima disso, vale a tabela normal.</p>
<h2>Perguntas frequentes</h2>
<p><strong>O INSS é calculado sobre o salário todo?</strong> Não. As alíquotas de 7,5% a 14% são progressivas e há um teto: o desconto máximo em 2026 é de R$ 988,08.</p>
<p><strong>Dependentes reduzem o imposto?</strong> Sim. Cada dependente abate R$ 189,59 da base de cálculo do IR.</p>"""),
  dict(arq="decimo-terceiro.html", nome="13º Salário",
    titulo="Calculadora de 13º Salário 2026: 1ª e 2ª parcela",
    desc="Calcule o valor do seu 13º salário 2026, integral ou proporcional, com o valor exato da primeira e da segunda parcela já com descontos.",
    campos=[("sal","Salário bruto (R$)","3000"),("meses","Meses trabalhados no ano","12"),("dep","Nº de dependentes","0")],
    js="""var r=Calc.decimoTerceiro(num('sal'),num('meses'),num('dep'));
mostrar([['13º bruto',r.bruto],['1ª parcela (até 30/nov)',r.primeira],['(−) INSS',r.inss],['(−) Imposto de Renda',r.irrf],['2ª parcela (até 20/dez)',r.segunda],['Total líquido',r.liquido,1]]);""",
    texto="""<h2>Como funciona o 13º salário</h2>
<p>O 13º é pago em duas parcelas. A <strong>primeira</strong>, até 30 de novembro, é metade do valor bruto, sem descontos. A <strong>segunda</strong>, até 20 de dezembro, é o restante já com INSS e Imposto de Renda descontados.</p>
<h2>13º proporcional</h2>
<p>Quem não trabalhou o ano todo recebe 1/12 do salário por mês trabalhado. O mês com 15 dias ou mais de trabalho conta como mês inteiro.</p>
<p class="aviso">Horas extras, adicional noturno e comissões habituais entram na média do 13º. Some essas médias ao salário para um valor mais preciso.</p>"""),
  dict(arq="ferias.html", nome="Férias",
    titulo="Calculadora de Férias 2026 com 1/3 e abono pecuniário",
    desc="Calcule o valor das suas férias com o terço constitucional, a opção de vender 10 dias (abono) e os descontos de INSS e IR de 2026.",
    campos=[("sal","Salário bruto (R$)","3000"),("dias","Dias de férias","30"),("vend","Dias vendidos (abono, até 10)","0"),("dep","Nº de dependentes","0")],
    js="""var v=Math.min(10,num('vend'));var r=Calc.ferias(num('sal'),num('dias'),v,num('dep'));
mostrar([['Férias',r.ferias],['1/3 de férias',r.terco],['Abono pecuniário',r.abono],['1/3 do abono',r.tercoAbono],['(−) INSS',r.inss],['(−) Imposto de Renda',r.irrf],['Total líquido',r.liquido,1]]);""",
    texto="""<h2>Como as férias são calculadas</h2>
<p>Você recebe o salário dos dias de descanso mais <strong>1/3 a mais</strong> (terço constitucional). INSS e Imposto de Renda incidem sobre férias + 1/3.</p>
<h2>Vender 10 dias de férias compensa?</h2>
<p>O abono pecuniário permite vender até 1/3 das férias (10 dias, em férias de 30). Esse valor e o seu terço <strong>não têm desconto de INSS nem de IR</strong>, por isso costuma render um bom dinheiro extra.</p>
<p class="aviso">Para 30 dias de direito: se vender 10, preencha 20 em "Dias de férias" e 10 em "Dias vendidos".</p>"""),
  dict(arq="horas-extras.html", nome="Horas Extras",
    titulo="Calculadora de Horas Extras 50% e 100%",
    desc="Saiba quanto vale sua hora extra. Calcule horas extras de 50% e 100% (domingos e feriados) a partir do seu salário e da sua jornada.",
    campos=[("sal","Salário bruto (R$)","3000"),("jor","Jornada mensal (horas)","220"),("h50","Horas extras 50%","10"),("h100","Horas extras 100%","0")],
    js="""var r=Calc.horasExtras(num('sal'),num('jor')||220,num('h50'),num('h100'));
mostrar([['Valor da sua hora normal',r.valorHora],['Horas extras 50%',r.valor50],['Horas extras 100%',r.valor100],['Total de horas extras',r.total,1]]);""",
    texto="""<h2>Como calcular a hora extra</h2>
<p>Divida o salário pela jornada mensal (220 horas para quem trabalha 44h por semana, 200 para 40h, 180 para 36h). A hora extra em dia útil vale no mínimo <strong>50% a mais</strong>. Em domingos e feriados geralmente vale <strong>100% a mais</strong>.</p>
<p class="aviso">Quem faz horas extras com frequência também tem direito ao reflexo no DSR (descanso semanal remunerado), que não está incluído aqui. Confira também a convenção coletiva da sua categoria, que pode prever percentuais maiores.</p>"""),
  dict(arq="juros-compostos.html", nome="Juros Compostos",
    titulo="Calculadora de Juros Compostos com aportes mensais",
    desc="Simule quanto seu dinheiro rende com juros compostos e aportes mensais. Veja o total investido, os juros ganhos e o valor final.",
    campos=[("ini","Valor inicial (R$)","1000"),("ap","Aporte mensal (R$)","200"),("taxa","Taxa de juros ao ano (%)","10"),("anos","Período (anos)","10")],
    js="""var r=Calc.jurosCompostos(num('ini'),num('ap'),Calc.taxaAnualParaMensal(num('taxa')/100),Math.round(num('anos')*12));
mostrar([['Total investido',r.investido],['Juros ganhos',r.juros],['Valor final',r.montante,1]]);""",
    texto="""<h2>O que são juros compostos</h2>
<p>São "juros sobre juros": o rendimento de cada mês passa a render também nos meses seguintes. Por isso, quanto mais tempo o dinheiro fica aplicado, mais rápido ele cresce.</p>
<h2>Que taxa usar?</h2>
<p>Use a taxa anual do investimento que você está avaliando (por exemplo, um percentual do CDI ou da Selic). A calculadora converte para taxa mensal equivalente. O resultado não desconta Imposto de Renda nem inflação.</p>"""),
]

# Aulas de matemática. O "id" liga a aula ao gerador de exercícios em docs/js/licoes.js.
LICOES = [
  dict(id="porcentagem", nome="Porcentagem de cabeça",
    titulo="Como calcular porcentagem de cabeça (com treino grátis)",
    desc="Aprenda a calcular qualquer porcentagem de cabeça a partir de 10%, 5% e 1%, e treine com exercícios corrigidos na hora.",
    texto="""<p>Toda porcentagem sai de três contas fáceis:</p>
<ul><li><strong>10%</strong>: divida por 10 (ande a vírgula uma casa). 10% de 240 é 24.</li>
<li><strong>5%</strong>: é a metade dos 10%. 5% de 240 é 12.</li>
<li><strong>1%</strong>: divida por 100. 1% de 240 é 2,40.</li></ul>
<p>O resto é montar: 15% é 10% + 5% (24 + 12 = 36). 20% é o dobro dos 10%. 25% é um quarto, e 50% é a metade.</p>"""),
  dict(id="desconto", nome="Descontos e aumentos",
    titulo="Como calcular desconto e aumento de cabeça",
    desc="Descubra na hora quanto fica um preço com desconto ou um reajuste em porcentagem, sem calculadora. Com exercícios corrigidos.",
    texto="""<p>São dois passos: ache a porcentagem do preço e depois <strong>tire</strong> (desconto) ou <strong>some</strong> (aumento).</p>
<p>Exemplo: R$ 80 com 15% de desconto. 10% de 80 é 8, 5% é 4, então 15% é 12. Você paga 80 − 12 = <strong>R$ 68</strong>.</p>
<p class="aviso">Cuidado com uma pegadinha: subir 10% e depois descer 10% não volta ao mesmo valor, porque a segunda conta é feita sobre um preço diferente.</p>"""),
  dict(id="soma", nome="Somar e subtrair arredondando",
    titulo="Como somar e subtrair de cabeça arredondando os números",
    desc="O truque de arredondar e compensar para somar e subtrair de cabeça em segundos. Explicação curta e treino corrigido na hora.",
    texto="""<p>Números terminados em 8 ou 9 atrapalham. Troque por um número redondo e depois <strong>acerte a diferença</strong>.</p>
<p>47 + 39: faça 47 + 40 = 87. Você somou 1 a mais, então tire 1: <strong>86</strong>.</p>
<p>83 − 28: faça 83 − 30 = 53. Você tirou 2 a mais, então devolva 2: <strong>55</strong>.</p>"""),
  dict(id="vezes", nome="Multiplicar por 5, 9 e 11",
    titulo="Como multiplicar por 5, 9 e 11 de cabeça",
    desc="Três atalhos para multiplicar qualquer número por 5, 9 ou 11 de cabeça, sempre começando por vezes 10. Com treino grátis.",
    texto="""<p>Os três atalhos começam do mesmo jeito: <strong>multiplique por 10</strong>, que é só colocar um zero.</p>
<ul><li><strong>× 5</strong>: 5 é metade de 10. 46 × 5: 460 ÷ 2 = 230.</li>
<li><strong>× 9</strong>: 9 é 10 menos 1. 46 × 9: 460 − 46 = 414.</li>
<li><strong>× 11</strong>: 11 é 10 mais 1. 46 × 11: 460 + 46 = 506.</li></ul>"""),
  dict(id="quebrar", nome="Multiplicar quebrando o número",
    titulo="Como multiplicar números grandes de cabeça",
    desc="Aprenda a multiplicar números de dois algarismos de cabeça quebrando em dezenas e unidades. Explicação e exercícios corrigidos.",
    texto="""<p>Ninguém precisa decorar 7 × 46. Quebre o número maior em <strong>dezenas e unidades</strong>, multiplique cada parte e some.</p>
<p>7 × 46: quebre 46 em 40 + 6. 7 × 40 = 280 e 7 × 6 = 42. Some: 280 + 42 = <strong>322</strong>.</p>
<p>Comece sempre pela parte maior: se precisar só de uma ideia do valor, ela já diz quase tudo.</p>"""),
  dict(id="fracoes", nome="Frações de um valor",
    titulo="Como calcular a fração de um número (3/4 de 240, por exemplo)",
    desc="Calcule frações de qualquer valor em dois passos: divida pelo número de baixo e multiplique pelo de cima. Com treino grátis.",
    texto="""<p>Fração de um valor se resolve em dois passos: <strong>divida pelo número de baixo</strong> e <strong>multiplique pelo de cima</strong>.</p>
<p>3/4 de 240: 240 ÷ 4 = 60, e 60 × 3 = <strong>180</strong>.</p>
<p>O número de baixo diz em quantas partes iguais o valor foi dividido. O de cima diz quantas dessas partes você quer.</p>"""),
  dict(id="regra3", nome="Regra de três",
    titulo="Regra de três simples: como fazer de cabeça",
    desc="Resolva regra de três sem montar tabela: descubra o valor de 1 unidade e multiplique. Explicação e exercícios do dia a dia.",
    texto="""<p>Esqueça a tabela com o X. Na maioria das contas do dia a dia basta <strong>achar o valor de 1</strong> e multiplicar.</p>
<p>Se 4 kg custam R$ 30, 1 kg custa 30 ÷ 4 = R$ 7,50. Então 6 kg custam 6 × 7,50 = <strong>R$ 45</strong>.</p>
<p class="aviso">Isso vale quando as duas coisas crescem juntas (mais quilos, mais dinheiro). Quando uma sobe e a outra desce, como pedreiros e dias de obra, a conta é outra.</p>"""),
  dict(id="equacao", nome="Equações: achando o x",
    titulo="Equação do 1º grau: como achar o x passo a passo",
    desc="Aprenda a resolver equações do primeiro grau desfazendo as contas na ordem certa. Explicação simples e exercícios corrigidos.",
    texto="""<p>Uma equação é uma balança: o que você fizer de um lado, faça do outro. Para achar o x, <strong>desfaça as contas de trás para frente</strong>.</p>
<p>3x + 7 = 22. Primeiro tire 7 dos dois lados: 3x = 15. Depois divida os dois lados por 3: <strong>x = 5</strong>.</p>
<p>Confira trocando o x pelo resultado: 3 × 5 + 7 = 22. Fechou.</p>"""),
  dict(id="juros", nome="Juros: a regra do 72", rel=("juros-compostos.html", "Simule o valor exato na calculadora de juros compostos"),
    titulo="Regra do 72: em quanto tempo seu dinheiro dobra",
    desc="Use a regra do 72 para estimar de cabeça em quanto tempo um investimento (ou uma dívida) dobra com juros compostos.",
    texto="""<p>Com juros compostos, divida <strong>72 pela taxa</strong> e você tem, aproximadamente, o tempo para o valor dobrar.</p>
<p>Rendendo 6% ao ano, o dinheiro dobra em cerca de 72 ÷ 6 = <strong>12 anos</strong>. Uma dívida de cartão a 12% ao mês dobra em cerca de 6 meses.</p>
<p class="aviso">É uma estimativa: funciona bem para taxas entre 2% e 12% e perde precisão fora disso.</p>"""),
  dict(id="derivada", nome="Cálculo sem medo: derivada",
    titulo="Derivada sem medo: a regra da potência explicada",
    desc="Entenda o que é derivada e aprenda a regra da potência, a primeira ferramenta do Cálculo, com exercícios corrigidos na hora.",
    texto="""<p>A derivada mede <strong>a velocidade com que uma coisa muda</strong>. Se f(x) é a distância percorrida, a derivada f′(x) é a velocidade naquele instante.</p>
<p>Para potências existe um atalho, a regra da potência: <strong>o expoente desce multiplicando e diminui 1</strong>.</p>
<p>f(x) = 3x² vira f′(x) = 6x. No ponto x = 2, a derivada vale 6 × 2 = <strong>12</strong>: ali a função está crescendo 12 unidades para cada unidade de x.</p>"""),
]
for i, l in enumerate(LICOES):
    l["arq"] = f"aula-{l['id']}.html"
    l["dia"] = i + 1

def adsense_head():
    if not ADSENSE_CLIENT: return ""
    return f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'

def anuncio():
    return '<div class="anuncio">Espaço para anúncio</div>' if not ADSENSE_CLIENT else \
        f'<ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script>'

def pagina(arq, titulo, desc, corpo, scripts=""):
    nav = '<a href="aprender.html">Aprender matemática</a>' + "".join(f'<a href="{c["arq"]}">{c["nome"]}</a>' for c in CALCS[:3])
    return f"""<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE_URL}/{'' if arq=='index.html' else arq}">
<meta property="og:title" content="{titulo}"><meta property="og:description" content="{desc}">
<link rel="stylesheet" href="css/style.css">
{adsense_head()}
</head><body>
<header class="topo"><div class="wrap"><a class="logo" href="index.html">Calcula<span>Fácil</span></a><nav>{nav}</nav></div></header>
<main class="wrap">
{corpo}
</main>
<footer><div class="wrap">© {datetime.date.today().year} {SITE_NOME}. Valores com base nas tabelas oficiais de 2026. Resultados são estimativas e não substituem a orientação de um contador. · <a href="privacidade.html">Privacidade</a></div></footer>
{scripts}
</body></html>
"""

SCRIPTS_TREINO = '<script src="js/licoes.js"></script><script src="js/treino.js"></script>'

def gerar_aulas():
    for i, l in enumerate(LICOES):
        prox = LICOES[i + 1] if i + 1 < len(LICOES) else None
        rel = f'<p><a href="{l["rel"][0]}">{l["rel"][1]}</a></p>' if l.get("rel") else ""
        depois = f'<a href="{prox["arq"]}">Próxima aula: {prox["nome"]}</a>' if prox else '<a href="desafio.html">Teste tudo no desafio de 60 segundos</a>'
        corpo = f"""<p class="migalha"><a href="aprender.html">Aprender matemática</a> · Aula {l['dia']} de {len(LICOES)}</p>
<h1>{l['titulo']}</h1>
<p class="sub">{l['desc']}</p>
<article class="card"><h2>A ideia em 1 minuto</h2>{l['texto']}{rel}</article>
<div class="card" id="treino" data-licao="{l['id']}" data-proxima="{prox['arq'] if prox else ''}">
<h2>Agora é a sua vez</h2>
<div class="barra"><i id="barra"></i></div><p class="aviso" id="progresso"></p>
<p class="pergunta" id="pergunta">Ative o JavaScript do navegador para ver os exercícios.</p>
<form id="resp"><label>Sua resposta<input id="entrada" inputmode="decimal" autocomplete="off"></label><button id="botao">Conferir</button></form>
<div id="fb" aria-live="polite"></div>
</div>
{anuncio()}
<p>{depois} · <a href="aprender.html">Ver todas as aulas</a></p>"""
        (RAIZ / l["arq"]).write_text(pagina(l["arq"], l["titulo"], l["desc"], corpo, SCRIPTS_TREINO), encoding="utf-8")

    itens = "".join(f'<li><a href="{l["arq"]}" data-id="{l["id"]}"><span>Aula {l["dia"]}</span><strong>{l["nome"]}</strong><em>5 min</em></a></li>' for l in LICOES)
    (RAIZ / "aprender.html").write_text(pagina("aprender.html", "Aprenda matemática de cabeça: aulas grátis com treino",
        "Aulas curtas e grátis de matemática: porcentagem, conta de cabeça, frações, regra de três, equações, juros e derivadas, com exercícios corrigidos na hora.",
        f"""<h1>Aprenda a fazer conta de cabeça</h1>
<p class="sub">{len(LICOES)} aulas de 5 minutos, grátis e sem cadastro. Cada aula explica um truque e depois você treina com exercícios novos a cada tentativa, corrigidos na hora com o passo a passo.</p>
<p class="aviso" id="resumo">Seu progresso fica salvo neste navegador.</p>
<ol class="trilha" id="trilha">{itens}</ol>
<a class="chamada" href="desafio.html"><strong>Desafio de 60 segundos</strong>Quantas contas de cabeça você acerta em um minuto? Tente bater o seu recorde.</a>
{anuncio()}""", SCRIPTS_TREINO), encoding="utf-8")

    (RAIZ / "desafio.html").write_text(pagina("desafio.html", "Desafio de 60 segundos: teste sua conta de cabeça",
        "Jogo grátis de cálculo mental: quantas contas de porcentagem, soma, multiplicação e frações você acerta em 60 segundos?",
        f"""<h1>Desafio de 60 segundos</h1>
<p class="sub">Porcentagem, soma, multiplicação e frações misturadas. Responda o máximo que conseguir em um minuto.</p>
<div class="card" id="desafio">
<p class="placar" id="d-placar">60 s · 0 acertos</p>
<p class="pergunta" id="d-pergunta"></p>
<form id="d-resp" class="oculto"><label>Sua resposta<input id="d-entrada" inputmode="decimal" autocomplete="off"></label><button>Responder</button></form>
<div id="d-fb" aria-live="polite"></div>
<button type="button" id="d-comecar">Começar</button>
</div>
{anuncio()}
<p>Errou algum tipo de conta? <a href="aprender.html">Veja o truque na aula correspondente</a>.</p>""", SCRIPTS_TREINO), encoding="utf-8")


def gerar():
    for c in CALCS:
        campos = "\n".join(f'<label>{rot}<input id="{i}" inputmode="decimal" value="{v}"></label>' for i, rot, v in c["campos"])
        outros = "".join(f'<a href="{o["arq"]}"><strong>{o["nome"]}</strong>{o["desc"][:80]}…</a>' for o in CALCS if o is not c)
        corpo = f"""<h1>{c['titulo']}</h1>
<p class="sub">{c['desc']}</p>
<div class="card"><form id="f">{campos}<button>Calcular</button></form></div>
<div id="caixa-resultado" class="card oculto"><table id="resultado"></table></div>
{anuncio()}
<article class="card">{c['texto']}</article>
<h2>Outras calculadoras</h2><div class="grade">{outros}</div>"""
        js = f"""<script src="js/calculos.js"></script><script src="js/ui.js"></script>
<script>document.getElementById('f').addEventListener('submit',function(e){{e.preventDefault();{c['js']}}});</script>"""
        (RAIZ / c["arq"]).write_text(pagina(c["arq"], c["titulo"], c["desc"], corpo, js), encoding="utf-8")

    grade = "".join(f'<a href="{c["arq"]}"><strong>{c["nome"]}</strong>{c["desc"][:90]}…</a>' for c in CALCS)
    (RAIZ / "index.html").write_text(pagina("index.html", "Calcula Fácil: calculadoras trabalhistas e financeiras 2026",
        "Calculadoras grátis e atualizadas para 2026: salário líquido, 13º, férias, horas extras e juros compostos.",
        f"<h1>Calculadoras grátis e atualizadas para 2026</h1><p class='sub'>Contas trabalhistas e financeiras feitas em segundos, com as tabelas oficiais de INSS e Imposto de Renda.</p><div class='grade'>{grade}</div><a class='chamada' href='aprender.html'><strong>Novo: aprenda a fazer conta de cabeça</strong>{len(LICOES)} aulas curtas e grátis, com exercícios corrigidos na hora e um desafio de 60 segundos.</a>{anuncio()}"), encoding="utf-8")
    gerar_aulas()

    (RAIZ / "privacidade.html").write_text(pagina("privacidade.html", "Política de Privacidade | Calcula Fácil", "Política de privacidade do Calcula Fácil.",
        """<h1>Política de Privacidade</h1><div class="card">
<p>Os valores digitados nas calculadoras são processados apenas no seu navegador e não são enviados nem armazenados por nós.</p>
<p>Este site pode exibir anúncios do Google AdSense. O Google e seus parceiros usam cookies para exibir anúncios com base em visitas anteriores a este e a outros sites. Você pode desativar a publicidade personalizada em <a href="https://adssettings.google.com">Configurações de anúncios do Google</a>.</p>
<p>Em conformidade com a LGPD (Lei 13.709/2018), você pode entrar em contato para tirar dúvidas sobre o tratamento de dados.</p></div>"""), encoding="utf-8")

    hoje = datetime.date.today().isoformat()
    urls = [""] + [c["arq"] for c in CALCS] + ["aprender.html", "desafio.html"] + [l["arq"] for l in LICOES]
    (RAIZ / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE_URL}/{u}</loc><lastmod>{hoje}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print("Páginas geradas em", RAIZ)

if __name__ == "__main__":
    gerar()
