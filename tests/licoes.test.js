const assert = require('node:assert');
const test = require('node:test');
const T = require('../docs/js/licoes.js');

// Gerador pseudoaleatório fixo, para os testes serem repetíveis
function semente(s) {
  return () => { s = (s * 1664525 + 1013904223) % 4294967296; return s / 4294967296; };
}

test('todo exercício tem resposta válida e o último passo chega nela', () => {
  for (const id of Object.keys(T.GERADORES)) {
    const r = semente(id.length * 7919);
    for (let i = 0; i < 500; i++) {
      const e = T.gerar(id, r);
      assert.ok(Number.isFinite(e.resposta) && e.resposta >= 0, `${id}: resposta ${e.resposta}`);
      assert.strictEqual(Math.round(e.resposta * 100) / 100, e.resposta, `${id}: mais de 2 casas em ${e.pergunta}`);
      assert.ok(e.passos.length >= 1 && e.pergunta.endsWith('?'), id);
      assert.ok(e.passos[e.passos.length - 1].includes(T.fmt(e.resposta)), `${id}: "${e.passos.join(' | ')}" não chega em ${e.resposta}`);
      assert.ok(T.conferir(e.resposta, T.fmt(e.resposta)), `${id}: resposta formatada não confere`);
    }
  }
});

test('desafio só usa aulas que existem', () => {
  for (const id of T.DESAFIO) assert.ok(T.GERADORES[id], id);
});

test('exemplos conferidos à mão', () => {
  const fixo = v => () => v;
  assert.deepStrictEqual(T.gerar('derivada', fixo(0.5)), {   // a=4, n=3, k=2
    pergunta: 'Se f(x) = 4x³, quanto vale a derivada f′(2)?', resposta: 48,
    passos: ['O expoente desce multiplicando e diminui 1: f′(x) = 12x²', 'Troque x por 2: 12 × 2² = 12 × 4 = 48']
  });
  const p = T.gerar('porcentagem', fixo(0.4));               // 15% de 340
  assert.strictEqual(p.pergunta, 'Quanto é 15% de 340?');
  assert.strictEqual(p.resposta, 51);
});

test('conferir aceita os formatos que as pessoas digitam', () => {
  assert.ok(T.conferir(12.5, '12,5'));
  assert.ok(T.conferir(12.5, '12.50'));
  assert.ok(T.conferir(1250, 'R$ 1.250,00'));
  assert.ok(T.conferir(15, '15%'));
  assert.ok(!T.conferir(15, '16'));
  assert.ok(!T.conferir(15, ''));
  assert.ok(!T.conferir(15, 'abc'));
});

test('sequência de dias', () => {
  assert.deepStrictEqual(T.proximaOfensiva(undefined, '2026-03-01'), { dia: '2026-03-01', n: 1 });
  assert.deepStrictEqual(T.proximaOfensiva({ dia: '2026-02-28', n: 4 }, '2026-03-01'), { dia: '2026-03-01', n: 5 });
  assert.deepStrictEqual(T.proximaOfensiva({ dia: '2026-03-01', n: 5 }, '2026-03-01'), { dia: '2026-03-01', n: 5 });
  assert.deepStrictEqual(T.proximaOfensiva({ dia: '2026-02-20', n: 9 }, '2026-03-01'), { dia: '2026-03-01', n: 1 });
  assert.strictEqual(T.ofensivaAtual({ dia: '2025-12-31', n: 3 }, '2026-01-01'), 3);
  assert.strictEqual(T.ofensivaAtual({ dia: '2025-12-30', n: 3 }, '2026-01-01'), 0);
});
