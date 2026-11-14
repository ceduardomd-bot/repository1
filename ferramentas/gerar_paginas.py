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

def adsense_head():
    if not ADSENSE_CLIENT: return ""
    return f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'

def anuncio():
    return '<div class="anuncio">Espaço para anúncio</div>' if not ADSENSE_CLIENT else \
        f'<ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script>'

def pagina(arq, titulo, desc, corpo, scripts=""):
    nav = "".join(f'<a href="{c["arq"]}">{c["nome"]}</a>' for c in CALCS[:3])
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
        f"<h1>Calculadoras grátis e atualizadas para 2026</h1><p class='sub'>Contas trabalhistas e financeiras feitas em segundos, com as tabelas oficiais de INSS e Imposto de Renda.</p><div class='grade'>{grade}</div>{anuncio()}"), encoding="utf-8")

    (RAIZ / "privacidade.html").write_text(pagina("privacidade.html", "Política de Privacidade | Calcula Fácil", "Política de privacidade do Calcula Fácil.",
        """<h1>Política de Privacidade</h1><div class="card">
<p>Os valores digitados nas calculadoras são processados apenas no seu navegador e não são enviados nem armazenados por nós.</p>
<p>Este site pode exibir anúncios do Google AdSense. O Google e seus parceiros usam cookies para exibir anúncios com base em visitas anteriores a este e a outros sites. Você pode desativar a publicidade personalizada em <a href="https://adssettings.google.com">Configurações de anúncios do Google</a>.</p>
<p>Em conformidade com a LGPD (Lei 13.709/2018), você pode entrar em contato para tirar dúvidas sobre o tratamento de dados.</p></div>"""), encoding="utf-8")

    hoje = datetime.date.today().isoformat()
    urls = [""] + [c["arq"] for c in CALCS]
    (RAIZ / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE_URL}/{u}</loc><lastmod>{hoje}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print("Páginas geradas em", RAIZ)

if __name__ == "__main__":
    gerar()
