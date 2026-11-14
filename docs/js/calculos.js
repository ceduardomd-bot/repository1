/*
 * Regras de cálculo e tabelas oficiais.
 * ATUALIZE ESTE BLOCO TODO ANO (janeiro), conferindo no gov.br / Receita Federal.
 */
(function (global) {
  var TABELAS = {
    ano: 2026,
    salarioMinimo: 1621.0,
    // INSS empregado: alíquota progressiva por faixa (Portaria Interministerial MPS/MF 2026)
    inss: [
      { ate: 1621.0, aliquota: 0.075, deducao: 0 },
      { ate: 2902.84, aliquota: 0.09, deducao: 24.32 },
      { ate: 4354.27, aliquota: 0.12, deducao: 111.41 },
      { ate: 8475.55, aliquota: 0.14, deducao: 198.5 } // teto
    ],
    // IRRF mensal: base × alíquota − dedução
    irrf: [
      { ate: 2428.8, aliquota: 0, deducao: 0 },
      { ate: 2826.65, aliquota: 0.075, deducao: 182.16 },
      { ate: 3751.05, aliquota: 0.15, deducao: 394.16 },
      { ate: 4664.68, aliquota: 0.225, deducao: 675.49 },
      { ate: Infinity, aliquota: 0.275, deducao: 908.73 }
    ],
    deducaoDependente: 189.59,
    descontoSimplificado: 607.2,
    // Redutor da Lei 15.270/2025 (vigente desde 01/01/2026)
    redutor: { isentoAte: 5000.0, transicaoAte: 7350.0, a: 978.62, b: 0.133145 }
  };

  function arred(v) {
    return Math.round(v * 100 + 1e-7) / 100;
  }

  function calcularINSS(base) {
    // Fórmula oficial: salário × alíquota da faixa − parcela a deduzir
    var faixas = TABELAS.inss, teto = faixas[faixas.length - 1].ate;
    var b = Math.min(Math.max(0, base), teto);
    for (var i = 0; i < faixas.length; i++) {
      if (b <= faixas[i].ate) return arred(b * faixas[i].aliquota - faixas[i].deducao);
    }
    return 0;
  }

  // rendimentoBruto: usado para o redutor; base: rendimento − INSS − deduções
  function calcularIRRF(rendimentoBruto, inss, dependentes) {
    var deducoesLegais = inss + (dependentes || 0) * TABELAS.deducaoDependente;
    var deducao = Math.max(deducoesLegais, TABELAS.descontoSimplificado);
    var base = Math.max(0, rendimentoBruto - deducao);
    var imposto = 0;
    for (var i = 0; i < TABELAS.irrf.length; i++) {
      var f = TABELAS.irrf[i];
      if (base <= f.ate) { imposto = base * f.aliquota - f.deducao; break; }
    }
    imposto = Math.max(0, imposto);
    var r = TABELAS.redutor, reducao = 0;
    if (rendimentoBruto <= r.isentoAte) reducao = imposto;
    else if (rendimentoBruto <= r.transicaoAte) reducao = Math.max(0, r.a - r.b * rendimentoBruto);
    return arred(Math.max(0, imposto - reducao));
  }

  function salarioLiquido(bruto, dependentes, outrosDescontos) {
    var inss = calcularINSS(bruto);
    var irrf = calcularIRRF(bruto, inss, dependentes);
    var outros = outrosDescontos || 0;
    return { bruto: arred(bruto), inss: inss, irrf: irrf, outros: arred(outros), liquido: arred(bruto - inss - irrf - outros) };
  }

  // meses: meses trabalhados no ano (mês com 15+ dias conta como mês cheio)
  function decimoTerceiro(salario, meses, dependentes) {
    var bruto = arred(salario / 12 * Math.min(12, Math.max(0, meses)));
    var primeira = arred(bruto / 2);
    var inss = calcularINSS(bruto);
    var irrf = calcularIRRF(bruto, inss, dependentes);
    var segunda = arred(bruto - primeira - inss - irrf);
    return { bruto: bruto, primeira: primeira, inss: inss, irrf: irrf, segunda: segunda, liquido: arred(primeira + segunda) };
  }

  // diasVendidos: abono pecuniário (até 10 dias), isento de INSS e IR
  function ferias(salario, diasFerias, diasVendidos, dependentes) {
    var diario = salario / 30;
    var valorFerias = arred(diario * diasFerias);
    var terco = arred(valorFerias / 3);
    var abono = arred(diario * (diasVendidos || 0));
    var tercoAbono = arred(abono / 3);
    var tributavel = valorFerias + terco;
    var inss = calcularINSS(tributavel);
    var irrf = calcularIRRF(tributavel, inss, dependentes);
    var bruto = arred(tributavel + abono + tercoAbono);
    return { ferias: valorFerias, terco: terco, abono: abono, tercoAbono: tercoAbono, bruto: bruto, inss: inss, irrf: irrf, liquido: arred(bruto - inss - irrf) };
  }

  function horasExtras(salario, jornadaMensal, horas50, horas100) {
    var valorHora = salario / jornadaMensal;
    var v50 = arred(valorHora * 1.5 * (horas50 || 0));
    var v100 = arred(valorHora * 2 * (horas100 || 0));
    return { valorHora: arred(valorHora), valor50: v50, valor100: v100, total: arred(v50 + v100) };
  }

  // taxa ao mês (decimal). Aportes no fim de cada mês.
  function jurosCompostos(inicial, aporteMensal, taxaMensal, meses) {
    var montante = inicial, investido = inicial;
    for (var i = 0; i < meses; i++) {
      montante = montante * (1 + taxaMensal) + aporteMensal;
      investido += aporteMensal;
    }
    return { investido: arred(investido), juros: arred(montante - investido), montante: arred(montante) };
  }

  function taxaAnualParaMensal(taxaAnual) {
    return Math.pow(1 + taxaAnual, 1 / 12) - 1;
  }

  var api = {
    TABELAS: TABELAS, calcularINSS: calcularINSS, calcularIRRF: calcularIRRF,
    salarioLiquido: salarioLiquido, decimoTerceiro: decimoTerceiro, ferias: ferias,
    horasExtras: horasExtras, jurosCompostos: jurosCompostos, taxaAnualParaMensal: taxaAnualParaMensal
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else global.Calc = api;
})(this);
