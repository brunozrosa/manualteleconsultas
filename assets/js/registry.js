// assets/js/registry.js
window.MANUAL = {
  pages: {},
  order: [
    'home',
    'sec1-apresentacao',
    'sec1-estudo-predibra',
    'sec1-referencial-teorico',
    'sec1-objetivo-teleconsultas',
    'sec2-cuidados-eticos',
    'sec2-links-necessarios',
    'sec2-preparando-teleconsulta',
    'sec2-durante-teleconsulta',
    'sec2-pos-consulta',
    'sec2-estruturacao-teleconsultas',
    'sec3-fontes-informacao',
    'sec3-tele1-anamnese',
    'sec3-tele2-obstaculos',
    'sec3-tele3-plano',
    'sec3-tele4-manutencao',
    'sec4-plano-alimentar',
    'referencias'
  ],
  registerPage: function(id, data) {
    this.pages[id] = data;
  }
};
