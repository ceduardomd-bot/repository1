// Tela das aulas, da trilha e do desafio de 60 segundos. O progresso fica só no navegador.
(function () {
  var CHAVE = 'cf_treino', META = 8;

  function ler() { try { return JSON.parse(localStorage.getItem(CHAVE)) || {}; } catch (e) { return {}; } }
  function gravar(s) { try { localStorage.setItem(CHAVE, JSON.stringify(s)); } catch (e) {} }
  function hoje() {
    var d = new Date();
    return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  }
  function el(id) { return document.getElementById(id); }
  function novo(tag, texto, classe) {
    var e = document.createElement(tag);
    if (texto) e.textContent = texto;
    if (classe) e.className = classe;
    return e;
  }
  function marcarDia(s) { s.ofensiva = Treino.proximaOfensiva(s.ofensiva, hoje()); }

  // ---------- Aula ----------
  var caixa = el('treino');
  if (caixa) (function () {
    var id = caixa.getAttribute('data-licao'), proxima = caixa.getAttribute('data-proxima');
    var s = ler(), atual = null, esperando = true;
    s.acertos = s.acertos || {}; s.feitas = s.feitas || {};
    var entrada = el('entrada'), botao = el('botao'), fb = el('fb');

    function progresso() {
      var n = Math.min(s.acertos[id] || 0, META);
      el('barra').style.width = (n / META * 100) + '%';
      el('progresso').textContent = s.feitas[id] ? 'Aula concluída. Continue praticando o quanto quiser.'
        : n + ' de ' + META + ' acertos para concluir a aula';
    }
    function pergunta() {
      atual = Treino.gerar(id);
      el('pergunta').textContent = atual.pergunta;
      entrada.value = ''; entrada.disabled = false; fb.textContent = ''; fb.className = '';
      botao.textContent = 'Conferir'; esperando = true; entrada.focus();
    }
    function corrigir() {
      if (!entrada.value.trim()) return;
      var certo = Treino.conferir(atual.resposta, entrada.value);
      fb.textContent = ''; fb.className = 'fb ' + (certo ? 'ok' : 'erro');
      fb.appendChild(novo('strong', certo ? 'Certo!' : 'Ainda não. A resposta é ' + Treino.fmt(atual.resposta) + '.'));
      var ol = novo('ol');
      atual.passos.forEach(function (p) { ol.appendChild(novo('li', p)); });
      fb.appendChild(ol);
      if (certo) {
        s.acertos[id] = (s.acertos[id] || 0) + 1; marcarDia(s);
        if (s.acertos[id] >= META && !s.feitas[id]) {
          s.feitas[id] = true;
          var fim = novo('p', 'Você concluiu esta aula. ');
          var a = novo('a', proxima ? 'Ir para a próxima aula' : 'Voltar para a trilha');
          a.href = proxima || 'aprender.html'; fim.appendChild(a); fb.appendChild(fim);
        }
        gravar(s);
      }
      progresso();
      entrada.disabled = true; botao.textContent = 'Próxima pergunta'; esperando = false; botao.focus();
    }
    el('resp').addEventListener('submit', function (e) { e.preventDefault(); if (esperando) corrigir(); else pergunta(); });
    progresso(); pergunta(); entrada.blur();
  })();

  // ---------- Trilha ----------
  var trilha = el('trilha');
  if (trilha) (function () {
    var s = ler(), feitas = s.feitas || {}, total = 0, n = 0;
    Array.prototype.forEach.call(trilha.querySelectorAll('a[data-id]'), function (a) {
      total++;
      if (feitas[a.getAttribute('data-id')]) { n++; a.classList.add('feita'); a.querySelector('em').textContent = 'Concluída'; }
    });
    var dias = Treino.ofensivaAtual(s.ofensiva, hoje());
    el('resumo').textContent = n + ' de ' + total + ' aulas concluídas · ' +
      (dias ? dias + (dias > 1 ? ' dias seguidos' : ' dia seguido') + ' de treino' : 'faça uma aula hoje para começar sua sequência') +
      (s.recorde ? ' · recorde no desafio: ' + s.recorde : '');
  })();

  // ---------- Desafio de 60 segundos ----------
  var jogo = el('desafio');
  if (jogo) (function () {
    var atual, pontos, resto, relogio;
    var entrada = el('d-entrada'), form = el('d-resp'), fb = el('d-fb');

    function pergunta() {
      var ids = Treino.DESAFIO;
      atual = Treino.gerar(ids[Math.floor(Math.random() * ids.length)]);
      el('d-pergunta').textContent = atual.pergunta; entrada.value = ''; entrada.focus();
    }
    function placar() { el('d-placar').textContent = resto + ' s · ' + pontos + (pontos === 1 ? ' acerto' : ' acertos'); }
    function fim() {
      clearInterval(relogio); form.classList.add('oculto'); el('d-pergunta').textContent = '';
      var s = ler(), novoRecorde = pontos > (s.recorde || 0);
      if (novoRecorde) s.recorde = pontos;
      if (pontos > 0) marcarDia(s);
      gravar(s);
      fb.className = 'fb ok';
      fb.textContent = 'Tempo esgotado: ' + pontos + (pontos === 1 ? ' acerto' : ' acertos') + '. ' +
        (novoRecorde && pontos > 0 ? 'Novo recorde!' : 'Seu recorde é ' + (s.recorde || 0) + '.');
      el('d-comecar').textContent = 'Jogar de novo'; el('d-comecar').classList.remove('oculto'); el('d-comecar').focus();
    }
    el('d-comecar').addEventListener('click', function () {
      pontos = 0; resto = 60; fb.textContent = ''; fb.className = '';
      this.classList.add('oculto'); form.classList.remove('oculto'); placar(); pergunta();
      relogio = setInterval(function () { resto--; placar(); if (resto <= 0) fim(); }, 1000);
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!entrada.value.trim() || resto <= 0) return;
      var certo = Treino.conferir(atual.resposta, entrada.value);
      if (certo) pontos++;
      fb.className = 'fb ' + (certo ? 'ok' : 'erro');
      fb.textContent = certo ? 'Certo!' : atual.pergunta.replace('Quanto é ', '').replace('?', '') + ' = ' + Treino.fmt(atual.resposta);
      placar(); pergunta();
    });
  })();
})();
