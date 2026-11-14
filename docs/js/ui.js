// Funções de tela compartilhadas pelas páginas
function brl(v){return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});}
function num(id){var v=String(document.getElementById(id).value).replace(/\./g,'').replace(',','.');var n=parseFloat(v);return isNaN(n)?0:n;}
function mostrar(linhas){
  var t=document.getElementById('resultado');
  t.innerHTML=linhas.map(function(l){return '<tr'+(l[2]?' class="total"':'')+'><td>'+l[0]+'</td><td>'+brl(l[1])+'</td></tr>';}).join('');
  document.getElementById('caixa-resultado').classList.remove('oculto');
  document.getElementById('caixa-resultado').scrollIntoView({behavior:'smooth',block:'nearest'});
}
