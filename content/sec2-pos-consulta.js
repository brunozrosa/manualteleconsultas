// content/sec2-pos-consulta.js
MANUAL.registerPage('sec2-pos-consulta', {
  section: 'SEÇÃO 2 — ORIENTAÇÕES OPERACIONAIS',
  title: 'Pós Consulta',
  readingTime: 1,
  prevId: 'sec2-durante-teleconsulta',
  nextId: 'sec2-estruturacao-teleconsultas',
  searchText: "Pós Consulta Faça o registro das informações coletadas na teleconsulta que ainda não tenham sido registradas (no formulário da teleconsulta); Envie por e-mail os combinados pactuados na teleconsulta e materiais de apoio, quando oportuno; Certifique-se de que todos os campos do formulário foram preenchidos corretamente, marque o formulário como completo, salve e envie.",
  html: `<div class="page-hero" id="page-top">
  <div class="page-hero-inner">
    <span class="section-badge">SEÇÃO 2 — ORIENTAÇÕES OPERACIONAIS</span>
    <div class="page-hero-title-row">
      <div class="page-hero-icon"><svg class="icon" aria-hidden="true"><use href="#icon-check"/></svg></div>
      <h1 class="h1-page">Pós Consulta</h1>
    </div>
    <div class="page-hero-meta">
      <svg class="icon" aria-hidden="true"><use href="#icon-clock"/></svg> <span>1 min de leitura</span>
    </div>
  </div>
</div>
<div class="local-toc" id="local-toc" aria-label="Nesta página"></div>
<div class="steps-grid">
  <div class="step-card">
    <div class="step-card-num">1</div>
    <div class="step-card-content">
      <strong>Registrar Informações Coletadas:</strong> Faça o registro das informações coletadas na teleconsulta que ainda não tenham sido registradas (no formulário da teleconsulta).
    </div>
    <div class="step-card-icon-right">
      <svg class="icon" aria-hidden="true"><use href="#icon-clipboard"/></svg>
    </div>
  </div>

  <div class="step-card">
    <div class="step-card-num">2</div>
    <div class="step-card-content">
      <strong>Enviar Combinados por E-mail:</strong> Envie por e-mail os combinados pactuados na teleconsulta e materiais de apoio, quando oportuno.
    </div>
    <div class="step-card-icon-right">
      <svg class="icon" aria-hidden="true"><use href="#icon-chat"/></svg>
    </div>
  </div>

  <div class="step-card">
    <div class="step-card-num">3</div>
    <div class="step-card-content">
      <strong>Finalizar Formulário:</strong> Certifique-se de que todos os campos do formulário foram preenchidos corretamente, marque o formulário como completo, salve e envie.
    </div>
    <div class="step-card-icon-right">
      <svg class="icon" aria-hidden="true"><use href="#icon-check"/></svg>
    </div>
  </div>
</div>
<div class="page-nav-footer content-wide">
<button class="nav-btn" onclick="selectSection('sec2-durante-teleconsulta')">
  <svg class="icon rotate-180" aria-hidden="true"><use href="#icon-arrow-right"/></svg> Ir para Durante a Teleconsulta
</button>
<button class="nav-btn next-btn" onclick="selectSection('sec2-estruturacao-teleconsultas')">
  Ir para Estruturação das Teleconsultas <svg class="icon" aria-hidden="true"><use href="#icon-arrow-right"/></svg>
</button>
</div>`
});
