/*
 * Geradores de exercícios das aulas de matemática.
 * Cada gerador devolve { pergunta, resposta (número), passos (lista de textos) }.
 * O último passo sempre termina mostrando a resposta.
 */
(function (global) {
  function int(r, a, b) { return a + Math.floor(r() * (b - a + 1)); }
  function pick(r, lista) { return lista[Math.floor(r() * lista.length)]; }
  function arred(v) { return Math.round(v * 100) / 100; }

  // Número no padrão brasileiro: inteiro sem casas, senão duas casas com vírgula
  function fmt(v) {
    if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v));
    return v.toFixed(2).replace('.', ',');
  }
  function rs(v) { return 'R$ ' + fmt(v); }

  function passosPct(p, base) {
    var d = arred(base / 10);
    switch (p) {
      case 1: return ['1% é dividir por 100: ' + base + ' ÷ 100 = ' + fmt(base / 100)];
      case 5: return ['10% de ' + base + ' é ' + fmt(d), '5% é a metade disso: ' + fmt(d) + ' ÷ 2 = ' + fmt(d / 2)];
      case 10: return ['10% é dividir por 10: ' + base + ' ÷ 10 = ' + fmt(d)];
      case 15: return ['10% de ' + base + ' é ' + fmt(d), '5% é a metade: ' + fmt(d / 2), 'Some os dois: ' + fmt(d) + ' + ' + fmt(d / 2) + ' = ' + fmt(d * 1.5)];
      case 20: return ['10% de ' + base + ' é ' + fmt(d), '20% é o dobro: ' + fmt(d) + ' × 2 = ' + fmt(d * 2)];
      case 25: return ['25% é um quarto: ' + base + ' ÷ 4 = ' + fmt(base / 4)];
      case 30: return ['10% de ' + base + ' é ' + fmt(d), '30% é o triplo: ' + fmt(d) + ' × 3 = ' + fmt(d * 3)];
      default: return ['50% é a metade: ' + base + ' ÷ 2 = ' + fmt(base / 2)];
    }
  }

  var SUP = { 1: '', 2: '²', 3: '³' };
  function termo(c, e) { return (c === 1 ? '' : c) + 'x' + SUP[e]; }

  var GERADORES = {
    porcentagem: function (r) {
      var p = pick(r, [1, 5, 10, 15, 20, 25, 30, 50]);
      var base = p === 1 ? int(r, 1, 9) * 100 : int(r, 2, 40) * 20;
      return { pergunta: 'Quanto é ' + p + '% de ' + base + '?', resposta: arred(base * p / 100), passos: passosPct(p, base) };
    },

    desconto: function (r) {
      var p = pick(r, [5, 10, 15, 20, 25, 30, 50]), preco = int(r, 1, 20) * 20;
      var valor = arred(preco * p / 100), sobe = r() < 0.4;
      var fim = sobe ? preco + valor : preco - valor;
      var passos = passosPct(p, preco);
      passos.push(sobe ? 'Some ao preço: ' + preco + ' + ' + fmt(valor) + ' = ' + rs(fim)
                       : 'Tire do preço: ' + preco + ' − ' + fmt(valor) + ' = ' + rs(fim));
      return {
        pergunta: sobe ? 'Uma conta de ' + rs(preco) + ' sobe ' + p + '%. Qual é o novo valor?'
                       : 'Um produto de ' + rs(preco) + ' está com ' + p + '% de desconto. Quanto você paga?',
        resposta: fim, passos: passos
      };
    },

    soma: function (r) {
      var b = pick(r, [18, 19, 28, 29, 38, 39, 48, 49, 98, 99]);
      var redondo = Math.ceil(b / 10) * 10, dif = redondo - b;
      if (r() < 0.5) {
        var a = int(r, 15, 85);
        return {
          pergunta: 'Quanto é ' + a + ' + ' + b + '?', resposta: a + b,
          passos: ['Arredonde ' + b + ' para ' + redondo + ': ' + a + ' + ' + redondo + ' = ' + (a + redondo),
                   'Você somou ' + dif + ' a mais, então tire: ' + (a + redondo) + ' − ' + dif + ' = ' + (a + b)]
        };
      }
      var m = b + int(r, 6, 70);
      return {
        pergunta: 'Quanto é ' + m + ' − ' + b + '?', resposta: m - b,
        passos: ['Arredonde ' + b + ' para ' + redondo + ': ' + m + ' − ' + redondo + ' = ' + (m - redondo),
                 'Você tirou ' + dif + ' a mais, então devolva: ' + (m - redondo) + ' + ' + dif + ' = ' + (m - b)]
      };
    },

    vezes: function (r) {
      var m = pick(r, [5, 9, 11]), n = int(r, 12, 98), dez = n * 10;
      var passos = m === 5 ? ['Multiplique por 10: ' + n + ' × 10 = ' + dez, '5 é metade de 10, então divida por 2: ' + dez + ' ÷ 2 = ' + (n * 5)]
        : m === 9 ? ['Multiplique por 10: ' + n + ' × 10 = ' + dez, '9 é 10 menos 1, então tire um ' + n + ': ' + dez + ' − ' + n + ' = ' + (n * 9)]
        : ['Multiplique por 10: ' + n + ' × 10 = ' + dez, '11 é 10 mais 1, então some um ' + n + ': ' + dez + ' + ' + n + ' = ' + (n * 11)];
      return { pergunta: 'Quanto é ' + n + ' × ' + m + '?', resposta: n * m, passos: passos };
    },

    quebrar: function (r) {
      var a = int(r, 3, 9), n;
      do { n = int(r, 13, 99); } while (n % 10 === 0);
      var d = Math.floor(n / 10) * 10, u = n % 10;
      return {
        pergunta: 'Quanto é ' + a + ' × ' + n + '?', resposta: a * n,
        passos: ['Quebre ' + n + ' em ' + d + ' + ' + u, a + ' × ' + d + ' = ' + (a * d), a + ' × ' + u + ' = ' + (a * u),
                 'Some as duas partes: ' + (a * d) + ' + ' + (a * u) + ' = ' + (a * n)]
      };
    },

    fracoes: function (r) {
      var f = pick(r, [[1, 2], [1, 3], [2, 3], [1, 4], [3, 4], [1, 5], [2, 5], [3, 5], [4, 5], [3, 8], [5, 8], [3, 10], [7, 10]]);
      var base = f[1] * int(r, 2, 25), q = base / f[1];
      var passos = ['Divida pelo número de baixo: ' + base + ' ÷ ' + f[1] + ' = ' + q];
      if (f[0] > 1) passos.push('Multiplique pelo número de cima: ' + q + ' × ' + f[0] + ' = ' + (q * f[0]));
      return { pergunta: 'Quanto é ' + f[0] + '/' + f[1] + ' de ' + base + '?', resposta: q * f[0], passos: passos };
    },

    regra3: function (r) {
      var item = pick(r, ['kg de carne', 'litros de gasolina', 'pacotes de café', 'camisetas', 'ingressos']);
      var u = pick(r, [2, 2.5, 3, 4, 5, 6, 7.5, 8, 12, 15]), q1 = int(r, 2, 9), q2;
      do { q2 = int(r, 2, 12); } while (q2 === q1);
      var total = arred(u * q1), resp = arred(u * q2);
      return {
        pergunta: 'Se ' + q1 + ' ' + item + ' custam ' + rs(total) + ', quanto custam ' + q2 + ' ' + item + '?', resposta: resp,
        passos: ['Descubra o preço de 1: ' + rs(total) + ' ÷ ' + q1 + ' = ' + rs(u),
                 'Multiplique pela quantidade que você quer: ' + q2 + ' × ' + rs(u) + ' = ' + rs(resp)]
      };
    },

    equacao: function (r) {
      var a = int(r, 2, 9), x = int(r, 1, 12), b = int(r, 1, 20), mais = r() < 0.5;
      var c = mais ? a * x + b : a * x - b;
      return {
        pergunta: 'Quanto vale x em ' + a + 'x ' + (mais ? '+' : '−') + ' ' + b + ' = ' + c + '?', resposta: x,
        passos: [(mais ? 'Tire ' + b + ' dos dois lados: ' : 'Some ' + b + ' nos dois lados: ') + a + 'x = ' + (a * x),
                 'Divida os dois lados por ' + a + ': x = ' + x]
      };
    },

    juros: function (r) {
      var taxa = pick(r, [1, 2, 3, 4, 6, 8, 9, 12]), ano = r() < 0.5;
      var per = ano ? 'ano' : 'mês', pl = ano ? 'anos' : 'meses';
      return {
        pergunta: 'Pela regra do 72: um valor que rende ' + taxa + '% ao ' + per + ' dobra em cerca de quantos ' + pl + '?',
        resposta: 72 / taxa,
        passos: ['Divida 72 pela taxa: 72 ÷ ' + taxa + ' = ' + (72 / taxa) + ' ' + pl]
      };
    },

    derivada: function (r) {
      var a = int(r, 1, 6), n = pick(r, [2, 3]), k = int(r, 1, 3), c = a * n;
      var resp = c * Math.pow(k, n - 1);
      return {
        pergunta: 'Se f(x) = ' + termo(a, n) + ', quanto vale a derivada f′(' + k + ')?', resposta: resp,
        passos: ['O expoente desce multiplicando e diminui 1: f′(x) = ' + termo(c, n - 1),
                 n === 2 ? 'Troque x por ' + k + ': ' + c + ' × ' + k + ' = ' + resp
                         : 'Troque x por ' + k + ': ' + c + ' × ' + k + '² = ' + c + ' × ' + (k * k) + ' = ' + resp]
      };
    }
  };

  // Aulas que entram no desafio de 60 segundos (só conta de cabeça)
  var DESAFIO = ['porcentagem', 'soma', 'vezes', 'quebrar', 'fracoes'];

  function gerar(id, r) { return GERADORES[id](r || Math.random); }

  // Aceita "12,5", "12.5", "R$ 1.250,00", "15%"
  function conferir(esperado, texto) {
    var t = String(texto).replace(/[^0-9,.\-−]/g, '').replace('−', '-');
    if (t.indexOf(',') >= 0) t = t.replace(/\./g, '').replace(',', '.');
    var n = parseFloat(t);
    return !isNaN(n) && Math.abs(n - esperado) < 0.005;
  }

  // Sequência de dias seguidos. Datas no formato AAAA-MM-DD (dia local).
  function ontem(dia) {
    var p = dia.split('-'), d = new Date(+p[0], +p[1] - 1, +p[2] - 1);
    return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  }
  function proximaOfensiva(of, hoje) {
    if (!of || !of.dia) return { dia: hoje, n: 1 };
    if (of.dia === hoje) return of;
    return { dia: hoje, n: of.dia === ontem(hoje) ? of.n + 1 : 1 };
  }
  function ofensivaAtual(of, hoje) {
    return of && (of.dia === hoje || of.dia === ontem(hoje)) ? of.n : 0;
  }

  var api = {
    GERADORES: GERADORES, DESAFIO: DESAFIO, gerar: gerar, conferir: conferir, fmt: fmt,
    proximaOfensiva: proximaOfensiva, ofensivaAtual: ofensivaAtual
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else global.Treino = api;
})(this);
