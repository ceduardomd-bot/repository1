const assert = require('node:assert');
const test = require('node:test');
const C = require('../docs/js/calculos.js');

test('INSS progressivo', () => {
  assert.strictEqual(C.calcularINSS(1621), 121.58);
  assert.strictEqual(C.calcularINSS(3000), 248.59);   // valor publicado
  assert.strictEqual(C.calcularINSS(20000), 988.08);  // teto
});

test('IRRF com redutor 2026', () => {
  assert.strictEqual(C.salarioLiquido(5000, 0).irrf, 0);          // isento até 5 mil
  const s = C.salarioLiquido(10000, 0);                           // sem redutor
  assert.strictEqual(s.irrf, C.calcularIRRF(10000, s.inss, 0));
  assert.ok(s.irrf === 1569.55);
  const t = C.salarioLiquido(6000, 0);                            // transição
  const semRedutor = (6000 - t.inss) * 0.275 - 908.73;
  assert.strictEqual(t.irrf, Math.round((semRedutor - (978.62 - 0.133145 * 6000)) * 100) / 100);
});

test('13º proporcional', () => {
  const d = C.decimoTerceiro(3000, 6, 0);
  assert.strictEqual(d.bruto, 1500);
  assert.strictEqual(d.primeira, 750);
});

test('férias com terço e abono', () => {
  const f = C.ferias(3000, 20, 10, 0);
  assert.strictEqual(f.ferias, 2000);
  assert.strictEqual(f.terco, 666.67);
  assert.strictEqual(f.abono, 1000);
});

test('horas extras e juros', () => {
  assert.strictEqual(C.horasExtras(2200, 220, 10, 0).total, 150);
  assert.strictEqual(C.jurosCompostos(1000, 0, 0.01, 12).montante, 1126.83);
});
