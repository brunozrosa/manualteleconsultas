// content/home.js
MANUAL.registerPage('home', {
  section: 'INÍCIO',
  title: 'Início',
  readingTime: 0,
  prevId: null,
  nextId: 'sec1-apresentacao',
  searchText: "MANUAL PARA TELECONSULTAS EM NUTRIÇÃO BASEADO NO GUIA ALIMENTAR PARA A POPULAÇÃO BRASILEIRA Universidade de São Paulo Faculdade de Saúde Pública Projeto de pesquisa Eficácia de uma intervenção digital de promoção da dieta brasileira na prevenção de doenças o ensaio clínico PREDIBRA Núcleo de Pesquisas Epidemiológicas em Nutrição e Saúde NUPENS São Paulo 2026 Introdução Orientações Operacionais Teleconsultas",
  html: `<div class="home-page-container">
  <header class="home-hero">
    <h1 class="home-title">MANUAL PARA TELECONSULTAS EM NUTRIÇÃO</h1>
    <h2 class="home-subtitle">BASEADO NO GUIA ALIMENTAR PARA A POPULAÇÃO BRASILEIRA</h2>
    
    <div class="home-meta-info">
      <p class="home-institution">Universidade de São Paulo</p>
      <p class="home-faculty">Faculdade de Saúde Pública</p>
      <p class="home-project">Projeto de pesquisa “Eficácia de uma intervenção digital de promoção da dieta brasileira na prevenção de doenças: o ensaio clínico PREDIBRA”</p>
      <p class="home-center">Núcleo de Pesquisas Epidemiológicas em Nutrição e Saúde - NUPENS</p>
      <p class="home-location">São Paulo, 2026</p>
    </div>
  </header>
  
  <div class="home-divider"></div>
  
  <section class="home-summary-section">
    <h3 class="home-section-title">Sumário do Manual</h3>
    <div class="home-summary-grid">
      <div class="home-summary-card" onclick="selectSection('sec1-apresentacao')">
        <div class="card-icon">
          <svg class="icon"><use href="#icon-book"/></svg>
        </div>
        <h4>Introdução</h4>
        <p>Apresenta a contextualização do projeto PREDIBRA, seus objetivos e os referenciais teóricos que orientam o cuidado em saúde e o cuidado nutricional.</p>
        <span class="card-action">Acessar Seção <svg class="icon"><use href="#icon-arrow-right"/></svg></span>
      </div>
      <div class="home-summary-card" onclick="selectSection('sec2-cuidados-eticos')">
        <div class="card-icon">
          <svg class="icon"><use href="#icon-checklist"/></svg>
        </div>
        <h4>Orientações Operacionais</h4>
        <p>Reúne orientações práticas e cuidados éticos para a realização de teleconsultas, englobando a preparação, a condução e o pós-consulta.</p>
        <span class="card-action">Acessar Seção <svg class="icon"><use href="#icon-arrow-right"/></svg></span>
      </div>
      <div class="home-summary-card" onclick="selectSection('sec3-fontes-informacao')">
        <div class="card-icon">
          <svg class="icon"><use href="#icon-chat"/></svg>
        </div>
        <h4>Teleconsultas</h4>
        <p>Detalhamento prático de cada uma das quatro teleconsultas de nutrição estruturadas, focando no Guia Alimentar para a População Brasileira.</p>
        <span class="card-action">Acessar Seção <svg class="icon"><use href="#icon-arrow-right"/></svg></span>
      </div>
      <div class="home-summary-card" onclick="selectSection('sec4-plano-alimentar')">
        <div class="card-icon">
          <svg class="icon"><use href="#icon-leaf"/></svg>
        </div>
        <h4>Plano Alimentar Base</h4>
        <p>Apresenta o plano alimentar de referência com foco na dieta tradicional brasileira recomendada pelo Guia.</p>
        <span class="card-action">Acessar Seção <svg class="icon"><use href="#icon-arrow-right"/></svg></span>
      </div>
    </div>
  </section>
  
  <div class="page-nav-footer content-wide">
    <div></div>
    <button class="nav-btn next-btn" onclick="selectSection('sec1-apresentacao')">
      Ir para Apresentação <svg class="icon" aria-hidden="true"><use href="#icon-arrow-right"/></svg>
    </button>
  </div>
</div>`
});
