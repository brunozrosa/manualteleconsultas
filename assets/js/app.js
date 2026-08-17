// assets/js/app.js

const state = {
  activeSection: 'home',
  sidebarCollapsed: false,
  darkMode: false,
  fontScale: 1.0,
  activeSteps: {},
};

const SIDEBAR_SECTIONS = {
  'INÍCIO': { icon: 'icon-home', pages: ['home'] },
  'SEÇÃO 1 — INTRODUÇÃO': { icon: 'icon-book', pages: ['sec1-apresentacao', 'sec1-estudo-predibra', 'sec1-referencial-teorico', 'sec1-objetivo-teleconsultas'] },
  'SEÇÃO 2 — OPERACIONAL': { icon: 'icon-checklist', pages: ['sec2-cuidados-eticos', 'sec2-links-necessarios', 'sec2-preparando-teleconsulta', 'sec2-durante-teleconsulta', 'sec2-pos-consulta', 'sec2-estruturacao-teleconsultas'] },
  'SEÇÃO 3 — TELECONSULTAS': { icon: 'icon-chat', pages: ['sec3-fontes-informacao', 'sec3-tele1-anamnese', 'sec3-tele2-obstaculos', 'sec3-tele3-plano', 'sec3-tele4-manutencao'] },
  'SEÇÃO 4 — PLANO ALIMENTAR': { icon: 'icon-leaf', pages: ['sec4-plano-alimentar'] },
  'REFERÊNCIAS': { icon: 'icon-book', pages: ['referencias'] },
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function slugify(text) {
  return text.toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, '').trim()
    .replace(/\s+/g, '-');
}

function svgIcon(id, extraClass) {
  const cls = extraClass ? `icon ${extraClass}` : 'icon';
  return `<svg class="${cls}" aria-hidden="true"><use href="#${id}"/></svg>`;
}

// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  initPreferences();
  renderSidebarTOC();
  handleHashRouting();

  const viewport = document.getElementById('content-viewport');
  if (viewport) viewport.addEventListener('scroll', updateReadingProgress);

  window.addEventListener('hashchange', handleHashRouting);

  MANUAL.order.forEach(pId => { state.activeSteps[pId] = 1; });
});

function initPreferences() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.body.classList.add('dark-mode');
    state.darkMode = true;
    updateThemeToggleUI();
  }
  const savedScale = localStorage.getItem('fontScale');
  if (savedScale) {
    state.fontScale = parseFloat(savedScale);
    document.documentElement.style.setProperty('--font-scale', state.fontScale);
  }
}

// ---------------------------------------------------------------------------
// Routing
// ---------------------------------------------------------------------------
function handleHashRouting() {
  const hash = window.location.hash.replace('#', '');
  if (hash && MANUAL.pages[hash]) {
    selectSection(hash, false);
  } else {
    selectSection('home', false);
  }
}

function selectSection(pId, updateHash = true) {
  const page = MANUAL.pages[pId];
  if (!page) return;

  state.activeSection = pId;

  const viewport = document.getElementById('content-viewport');
  if (viewport) {
    viewport.innerHTML = page.html;
    // Fix SVG icons on file:/// protocol by using inline sprite anchors
    viewport.querySelectorAll('svg use').forEach(useEl => {
      const href = useEl.getAttribute('href') || '';
      if (href.includes('#') && !href.startsWith('#')) {
        const id = href.split('#')[1];
        useEl.setAttribute('href', '#' + id);
      }
    });
    viewport.scrollTop = 0;
  }

  // Teleconsulta color theme
  document.body.classList.remove('tele-theme-1', 'tele-theme-2', 'tele-theme-3', 'tele-theme-4');
  if (pId === 'sec3-tele1-anamnese') document.body.classList.add('tele-theme-1');
  else if (pId === 'sec3-tele2-obstaculos') document.body.classList.add('tele-theme-2');
  else if (pId === 'sec3-tele3-plano') document.body.classList.add('tele-theme-3');
  else if (pId === 'sec3-tele4-manutencao') document.body.classList.add('tele-theme-4');
  updateNavbarTheme(pId);

  // Sidebar highlight
  document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.sidebar-nav li').forEach(el => el.classList.remove('active-sub', 'headings-expanded'));

  const activeSubItem = document.querySelector(`.sidebar-nav li[data-sub-section="${pId}"]`);
  if (activeSubItem) {
    activeSubItem.classList.add('active-sub', 'headings-expanded');
    const parentContainer = activeSubItem.closest('.menu-item-container');
    if (parentContainer) parentContainer.classList.add('expanded');
  }

  // Highlight active section parent item
  for (const [secTitle, secData] of Object.entries(SIDEBAR_SECTIONS)) {
    if (secData.pages.includes(pId)) {
      const secSlug = slugify(secTitle);
      const container = document.querySelector(`.menu-item-container[data-section="${secSlug}"]`);
      if (container) {
        const menuItem = container.querySelector('.menu-item');
        if (menuItem) menuItem.classList.add('active');
      }
    }
  }

  // Stepper init
  const telePages = ['sec3-tele1-anamnese', 'sec3-tele2-obstaculos', 'sec3-tele3-plano', 'sec3-tele4-manutencao'];
  if (telePages.includes(pId)) {
    showTeleStep(pId, state.activeSteps[pId] || 1);
  }

  updateHeaderHUD(pId);
  renderLocalTOC(pId);

  if (updateHash) window.location.hash = pId;

  let visited = JSON.parse(localStorage.getItem('visited_pages') || '{}');
  visited[pId] = true;
  localStorage.setItem('visited_pages', JSON.stringify(visited));
  updateSidebarProgress();

  clearSearch();
  setTimeout(updateReadingProgress, 100);
}

// ---------------------------------------------------------------------------
// Local TOC ("Nesta página")
// ---------------------------------------------------------------------------
function renderLocalTOC(pId) {
  const toc = document.getElementById('local-toc');
  if (!toc) return;

  const viewport = document.getElementById('content-viewport');
  if (!viewport) return;

  const telePages = ['sec3-tele1-anamnese', 'sec3-tele2-obstaculos', 'sec3-tele3-plano', 'sec3-tele4-manutencao'];
  const isTelePage = telePages.includes(pId);

  if (isTelePage) {
    const panes = viewport.querySelectorAll('.step-content-pane');
    if (panes.length === 0) {
      toc.style.display = 'none';
      return;
    }

    let tocHtml = '<div class="local-toc-inner">';
    tocHtml += '<button class="local-toc-toggle" onclick="toggleLocalTOC()" aria-expanded="true">';
    tocHtml += `${svgIcon('icon-checklist')} <span>Nesta Teleconsulta</span> ${svgIcon('icon-chevron-down','toc-chevron')}`;
    tocHtml += '</button>';
    tocHtml += '<nav class="local-toc-nav" id="local-toc-nav">';

    panes.forEach(pane => {
      const stepNum = parseInt(pane.getAttribute('data-step-content'));
      if (!stepNum) return;
      // Adiciona cabeçalho da Etapa
      tocHtml += `<a href="#" class="toc-item" onclick="selectStepAndScroll(event, ${stepNum}, null)">Etapa ${stepNum}</a>`;
      
      // Busca H3 dentro desse painel
      const h3s = pane.querySelectorAll('h3.h3-subsection[id]');
      h3s.forEach(h3 => {
        const id = h3.getAttribute('id');
        let text = h3.textContent.trim();
        // Remove os prefixos de ordenação a), b), c) redundantes no menu
        text = text.replace(/^[a-z]\)\s*/i, '');
        tocHtml += `<a href="#${id}" class="toc-item-sub" onclick="selectStepAndScroll(event, ${stepNum}, '${id}')">${text}</a>`;
      });
    });

    tocHtml += '</nav></div>';
    toc.innerHTML = tocHtml;
    toc.style.display = 'block';
  } else {
    // Collect H2 (h2-section) and H3 (h3-subsection) elements
    const h2s = viewport.querySelectorAll('h2.h2-section[id]');
    const h3s = viewport.querySelectorAll('h3.h3-subsection[id]');

    if (h2s.length === 0 && h3s.length === 0) {
      toc.style.display = 'none';
      return;
    }

    // Build TOC tree
    let tocHtml = '<div class="local-toc-inner">';
    tocHtml += '<button class="local-toc-toggle" onclick="toggleLocalTOC()" aria-expanded="true">';
    tocHtml += `${svgIcon('icon-checklist')} <span>Nesta página</span> ${svgIcon('icon-chevron-down','toc-chevron')}`;
    tocHtml += '</button>';
    tocHtml += '<nav class="local-toc-nav" id="local-toc-nav">';

    // Build a combined ordered list preserving DOM order
    const allHeadings = viewport.querySelectorAll('h2.h2-section[id], h3.h3-subsection[id]');
    allHeadings.forEach(heading => {
      const id = heading.getAttribute('id');
      const text = heading.textContent.trim();
      const isH3 = heading.classList.contains('h3-subsection');
      const indent = isH3 ? 'toc-item-sub' : 'toc-item';
      tocHtml += `<a href="#${id}" class="${indent}" onclick="scrollToAnchor(event,'${id}')">${text}</a>`;
    });

    tocHtml += '</nav></div>';
    toc.innerHTML = tocHtml;
    toc.style.display = 'block';
  }
}

function toggleLocalTOC() {
  const nav = document.getElementById('local-toc-nav');
  const btn = document.querySelector('.local-toc-toggle');
  if (!nav || !btn) return;
  const isExpanded = btn.getAttribute('aria-expanded') === 'true';
  btn.setAttribute('aria-expanded', String(!isExpanded));
  nav.style.display = isExpanded ? 'none' : 'flex';
  const chevron = btn.querySelector('.toc-chevron');
  if (chevron) chevron.style.transform = isExpanded ? 'rotate(-90deg)' : '';
}

function scrollToAnchor(event, id) {
  event.preventDefault();
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function selectStepAndScroll(event, stepNum, elementId) {
  event.preventDefault();
  showTeleStep(state.activeSection, stepNum);
  
  if (elementId) {
    const el = document.getElementById(elementId);
    if (el) {
      setTimeout(() => {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 50);
    }
  } else {
    const pane = document.querySelector(`.step-content-pane[data-step-content="${stepNum}"]`);
    if (pane) {
      setTimeout(() => {
        pane.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 50);
    }
  }
}

// ---------------------------------------------------------------------------
// Teleconsulta stepper
// ---------------------------------------------------------------------------
// Teleconsulta page navigation config
const TELE_PAGE_NAV = {
  'sec3-tele1-anamnese': { prevId: 'sec3-fontes-informacao', prevLabel: 'Fontes de Informação', nextId: 'sec3-tele2-obstaculos', nextLabel: '2ª Teleconsulta' },
  'sec3-tele2-obstaculos': { prevId: 'sec3-tele1-anamnese', prevLabel: '1ª Teleconsulta', nextId: 'sec3-tele3-plano', nextLabel: '3ª Teleconsulta' },
  'sec3-tele3-plano': { prevId: 'sec3-tele2-obstaculos', prevLabel: '2ª Teleconsulta', nextId: 'sec3-tele4-manutencao', nextLabel: '4ª Teleconsulta' },
  'sec3-tele4-manutencao': { prevId: 'sec3-tele3-plano', prevLabel: '3ª Teleconsulta', nextId: 'sec4-plano-alimentar', nextLabel: 'Plano Alimentar Base' }
};

function showTeleStep(pId, stepNum) {
  state.activeSteps[pId] = stepNum;
  const viewport = document.getElementById('content-viewport');
  if (!viewport) return;

  viewport.querySelectorAll('.step-content-pane').forEach(p => p.classList.remove('active'));
  const activePane = viewport.querySelector(`.step-content-pane[data-step-content="${stepNum}"]`);
  if (activePane) activePane.classList.add('active');

  viewport.querySelectorAll('.step-indicator').forEach(ind => {
    ind.classList.toggle('active', parseInt(ind.getAttribute('data-step')) === stepNum);
  });

  // Inject exactly 2 navigation buttons for every step
  const allPanes = viewport.querySelectorAll('.step-content-pane');
  const totalSteps = allPanes.length;
  const nav = TELE_PAGE_NAV[pId];

  // Remove any previously injected footer
  viewport.querySelectorAll('.step-nav-injected').forEach(el => el.remove());

  if (activePane && nav) {
    const footer = document.createElement('div');
    footer.className = 'step-navigation-footer content-wide step-nav-injected';

    let leftBtn, rightBtn;
    const iconPrev = `<svg class="icon rotate-180" aria-hidden="true"><use href="#icon-arrow-right"/></svg>`;
    const iconNext = `<svg class="icon" aria-hidden="true"><use href="#icon-arrow-right"/></svg>`;

    if (stepNum > 1) {
      leftBtn = `<button class="nav-btn prev-btn" onclick="showTeleStep('${pId}', ${stepNum - 1})">${iconPrev} Etapa anterior</button>`;
    } else {
      leftBtn = `<button class="nav-btn prev-btn" onclick="selectSection('${nav.prevId}')">${iconPrev} ${nav.prevLabel}</button>`;
    }

    if (stepNum < totalSteps) {
      rightBtn = `<button class="nav-btn next-btn" onclick="showTeleStep('${pId}', ${stepNum + 1})">Próxima etapa ${iconNext}</button>`;
    } else {
      rightBtn = `<button class="nav-btn next-btn" onclick="selectSection('${nav.nextId}')">${nav.nextLabel} ${iconNext}</button>`;
    }

    footer.innerHTML = leftBtn + rightBtn;
    activePane.appendChild(footer);
  }

  const stepper = viewport.querySelector('.tele-stepper');
  if (stepper) {
    stepper.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    viewport.scrollTop = 0;
  }
  updateHeaderHUD(pId);
  updateReadingProgress();
}

// ---------------------------------------------------------------------------
// Action cards
// ---------------------------------------------------------------------------
function toggleActionCard(el) {
  const card = el.closest('.action-card');
  if (!card) return;
  card.classList.toggle('checked');
  // swap icon
  const use = el.querySelector('use');
  if (use) {
    const current = use.getAttribute('href');
    use.setAttribute('href', card.classList.contains('checked')
      ? 'assets/icons/sprite.svg#icon-check-square'
      : 'assets/icons/sprite.svg#icon-square');
  }
}

// ---------------------------------------------------------------------------
// Header HUD
// ---------------------------------------------------------------------------
function updateHeaderHUD(pId, subTitleText = null) {
  const page = MANUAL.pages[pId];
  if (!page) return;
  const breadcrumbs = document.getElementById('app-breadcrumbs');
  const readTimeBadge = document.getElementById('header-read-time');
  
  const telePages = ['sec3-tele1-anamnese', 'sec3-tele2-obstaculos', 'sec3-tele3-plano', 'sec3-tele4-manutencao'];
  const isTele = telePages.includes(pId);

  if (breadcrumbs) {
    if (pId === 'home') {
      breadcrumbs.innerHTML = `<span>Início</span>`;
    } else {
      let html = `<span>${page.section}</span> ${svgIcon('icon-chevron-right')} <span>${page.title}</span>`;
      
      let subPart = '';
      if (isTele) {
        const step = state.activeSteps[pId] || 1;
        subPart = `Etapa ${step}`;
      } else if (subTitleText) {
        subPart = subTitleText;
      }
      
      if (subPart) {
        html += ` ${svgIcon('icon-chevron-right')} <span>${subPart}</span>`;
      }
      breadcrumbs.innerHTML = html;
    }
  }
  if (readTimeBadge) {
    if (pId === 'home') {
      readTimeBadge.style.display = 'none';
    } else {
      readTimeBadge.style.display = 'flex';
      readTimeBadge.innerHTML = `${svgIcon('icon-clock')} <span>${page.readingTime} min</span>`;
    }
  }
}

function updateActiveSubtopicOnScroll() {
  const pId = state.activeSection;
  const page = MANUAL.pages[pId];
  if (!page) return;

  const telePages = ['sec3-tele1-anamnese', 'sec3-tele2-obstaculos', 'sec3-tele3-plano', 'sec3-tele4-manutencao'];
  if (telePages.includes(pId)) return; // Stepper manages steps on its own

  const viewport = document.getElementById('content-viewport');
  if (!viewport) return;

  const headings = viewport.querySelectorAll('h2.h2-section[id], h3.h3-subsection[id]');
  let activeHeading = null;

  const viewportRect = viewport.getBoundingClientRect();
  // Iterate ALL headings — do not break early
  for (let heading of headings) {
    const rect = heading.getBoundingClientRect();
    const topOffset = rect.top - viewportRect.top;
    if (topOffset <= 100) {
      activeHeading = heading;
    }
  }

  if (activeHeading) {
    const text = activeHeading.textContent.trim();
    if (text) {
      updateHeaderHUD(pId, text);
      return;
    }
  }
  updateHeaderHUD(pId);
}

// ---------------------------------------------------------------------------
// Navbar and progress bar theme (cannot use CSS vars across sibling elements)
// ---------------------------------------------------------------------------
const TELE_ACCENT_COLORS = {
  'sec3-tele1-anamnese': '#0d9488',
  'sec3-tele2-obstaculos': '#2563eb',
  'sec3-tele3-plano': '#439273',
  'sec3-tele4-manutencao': '#d97706'
};
const DEFAULT_ACCENT = '#296092'; // azul PREDIBRA

function updateNavbarTheme(pId) {
  const color = TELE_ACCENT_COLORS[pId] || DEFAULT_ACCENT;
  const navbar = document.querySelector('.top-navbar');
  const progressBar = document.getElementById('reading-progress-bar');
  if (navbar) navbar.style.borderBottomColor = color;
  if (progressBar) progressBar.style.backgroundColor = color;
}

// ---------------------------------------------------------------------------
// Reading progress bar
// ---------------------------------------------------------------------------
function updateReadingProgress() {
  const viewport = document.getElementById('content-viewport');
  const bar = document.getElementById('reading-progress-bar');
  if (!viewport || !bar) return;
  const scrollable = viewport.scrollHeight - viewport.clientHeight;
  const pct = scrollable > 0 ? (viewport.scrollTop / scrollable) * 100 : 0;
  bar.style.width = `${Math.min(100, Math.max(0, pct))}%`;

  updateActiveSubtopicOnScroll();
}

// ---------------------------------------------------------------------------
// Theme + Font
// ---------------------------------------------------------------------------
function toggleTheme() {
  state.darkMode = !state.darkMode;
  document.body.classList.toggle('dark-mode', state.darkMode);
  localStorage.setItem('theme', state.darkMode ? 'dark' : 'light');
  updateThemeToggleUI();
}

function updateThemeToggleUI() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  btn.innerHTML = state.darkMode
    ? `${svgIcon('icon-sun')} Modo Claro`
    : `${svgIcon('icon-moon')} Modo Escuro`;
}

function adjustFontSize(dir) {
  state.fontScale = Math.min(1.4, Math.max(0.8, state.fontScale + dir * 0.1));
  document.documentElement.style.setProperty('--font-scale', state.fontScale);
  localStorage.setItem('fontScale', state.fontScale);
}

// ---------------------------------------------------------------------------
// Sidebar
// ---------------------------------------------------------------------------
function toggleSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  if (sidebar) {
    sidebar.classList.toggle('collapsed');
    state.sidebarCollapsed = !state.sidebarCollapsed;
  }
}

function toggleSubmenu(event, sectionSlug) {
  event.stopPropagation();
  const container = document.querySelector(`.menu-item-container[data-section="${sectionSlug}"]`);
  if (container) container.classList.toggle('expanded');
}

function getPageHeadings(pId) {
  const page = MANUAL.pages[pId];
  if (!page || !page.html) return [];

  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = page.html;

  const telePages = ['sec3-tele1-anamnese', 'sec3-tele2-obstaculos', 'sec3-tele3-plano', 'sec3-tele4-manutencao'];
  const isTele = telePages.includes(pId);

  if (isTele) {
    const panes = tempDiv.querySelectorAll('.step-content-pane');
    const steps = [];
    panes.forEach(pane => {
      const stepNum = parseInt(pane.getAttribute('data-step-content'));
      if (stepNum) {
        steps.push({
          id: `step-${stepNum}`,
          text: `Etapa ${stepNum}`,
          stepNum: stepNum
        });
      }
    });
    return steps;
  } else {
    const headings = [];
    const allHeadings = tempDiv.querySelectorAll('h2.h2-section[id], h3.h3-subsection[id]');
    allHeadings.forEach(heading => {
      const id = heading.getAttribute('id');
      const text = heading.textContent.trim();
      const isH3 = heading.classList.contains('h3-subsection');
      headings.push({
        id: id,
        text: text,
        isSub: isH3
      });
    });
    return headings;
  }
}

function renderSidebarTOC() {
  const nav = document.querySelector('.sidebar-nav');
  if (!nav) return;
  nav.innerHTML = '';

  for (const [secTitle, secData] of Object.entries(SIDEBAR_SECTIONS)) {
    const secSlug = slugify(secTitle);

    let totalTime = 0;
    secData.pages.forEach(pId => {
      if (MANUAL.pages[pId]) totalTime += MANUAL.pages[pId].readingTime || 0;
    });

    const container = document.createElement('div');
    container.className = 'menu-item-container';
    container.setAttribute('data-section', secSlug);

    // Expand SEÇÃO 1 and SEÇÃO 3 by default
    if (secTitle.includes('SEÇÃO 1') || secTitle.includes('SEÇÃO 3')) {
      container.classList.add('expanded');
    }

    const menuItem = document.createElement('div');
    menuItem.className = 'menu-item';
    menuItem.onclick = () => selectSection(secData.pages[0]);
    menuItem.innerHTML = `
      <span class="menu-title">${svgIcon(secData.icon)} ${secTitle}</span>
      ${totalTime > 0 ? `<span class="read-badge">${totalTime} min</span>` : ''}
      ${secData.pages.length > 1 || (secData.pages.length === 1 && secTitle !== 'INÍCIO') ? `<span class="toggle-submenu" onclick="toggleSubmenu(event,'${secSlug}')">${svgIcon('icon-chevron-right')}</span>` : ''}
    `;
    container.appendChild(menuItem);

    if (secData.pages.length > 1 || (secData.pages.length === 1 && secTitle !== 'INÍCIO')) {
      const submenu = document.createElement('ul');
      submenu.className = 'submenu';

      secData.pages.forEach(pId => {
        const page = MANUAL.pages[pId];
        if (!page) return;

        const li = document.createElement('li');
        li.className = 'page-menu-item-container';
        li.setAttribute('data-sub-section', pId);

        const isTele = ['sec3-tele1-anamnese','sec3-tele2-obstaculos','sec3-tele3-plano','sec3-tele4-manutencao'].includes(pId);
        
        const pageRow = document.createElement('div');
        pageRow.className = isTele ? 'page-menu-row tele-link' : 'page-menu-row';
        pageRow.onclick = e => {
          e.stopPropagation();
          if (state.activeSection === pId) {
            li.classList.toggle('headings-expanded');
          } else {
            selectSection(pId);
          }
        };

        const headings = getPageHeadings(pId);
        const hasHeadings = headings.length > 0;

        pageRow.innerHTML = `
          <span class="sub-title">${page.title}</span>
          <span class="sub-read-badge">${page.readingTime} min</span>
          ${hasHeadings ? `<span class="toggle-headings-btn">${svgIcon('icon-chevron-right')}</span>` : ''}
        `;
        li.appendChild(pageRow);

        if (hasHeadings) {
          const headingsList = document.createElement('ul');
          headingsList.className = 'page-headings-list';
          headings.forEach(heading => {
            const hLi = document.createElement('li');
            hLi.className = heading.isSub ? 'heading-item sub-heading' : 'heading-item';
            hLi.textContent = heading.text;
            hLi.onclick = e => {
              e.stopPropagation();
              const targetActive = state.activeSection === pId;
              if (!targetActive) {
                selectSection(pId);
              }
              const scrollAction = () => {
                if (isTele) {
                  showTeleStep(pId, heading.stepNum);
                } else {
                  const targetEl = document.getElementById(heading.id);
                  if (targetEl) targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
              };
              if (targetActive) {
                scrollAction();
              } else {
                setTimeout(scrollAction, 150);
              }
            };
            headingsList.appendChild(hLi);
          });
          li.appendChild(headingsList);
        }

        submenu.appendChild(li);
      });
      container.appendChild(submenu);
    }
    nav.appendChild(container);
  }
  updateSidebarProgress();
}

function updateSidebarProgress() {
  // Visited page tick indicators removed
}

// ---------------------------------------------------------------------------
// Search
// ---------------------------------------------------------------------------
function performSearch() {
  const input = document.getElementById('manual-search');
  const hud = document.getElementById('search-hud');
  const list = document.getElementById('search-results-list');
  const count = document.getElementById('search-count');
  const clearBtn = document.getElementById('search-clear-btn');
  if (!input || !hud || !list) return;

  const query = input.value.trim().toLowerCase();
  if (query.length < 2) {
    hud.style.display = 'none';
    if (clearBtn) clearBtn.style.display = 'none';
    return;
  }
  if (clearBtn) clearBtn.style.display = 'block';
  list.innerHTML = '';

  const targets = [];
  MANUAL.order.forEach(pId => {
    const page = MANUAL.pages[pId];
    if (!page) return;
    if (page.title.toLowerCase().includes(query)) {
      targets.push({ title: page.title, text: `Seção: ${page.title}`, pageId: pId, context: page.section });
    }
    const searchText = page.searchText;
    let idx = searchText.toLowerCase().indexOf(query);
    while (idx !== -1 && targets.length < 50) {
      const s = Math.max(0, idx - 60);
      const e = Math.min(searchText.length, idx + query.length + 80);
      let snippet = searchText.substring(s, e);
      if (s > 0) snippet = '...' + snippet;
      if (e < searchText.length) snippet += '...';
      targets.push({ title: page.title, text: snippet, pageId: pId, context: `${page.section} › ${page.title}` });
      idx = searchText.toLowerCase().indexOf(query, idx + 1 + query.length);
    }
  });

  if (count) count.textContent = targets.length;
  hud.style.display = 'flex';

  if (targets.length === 0) {
    list.innerHTML = '<div class="no-results-msg">Nenhum resultado encontrado.</div>';
    return;
  }

  targets.forEach(target => {
    const card = document.createElement('div');
    card.className = 'search-item-card';
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    const highlighted = target.text.replace(regex, '<mark>$1</mark>');
    card.innerHTML = `<div class="search-item-context">${target.context}</div>
      <div class="search-item-snippet">${highlighted}</div>`;
    card.onclick = () => { clearSearch(); selectSection(target.pageId); };
    list.appendChild(card);
  });
}

function clearSearch() {
  const input = document.getElementById('manual-search');
  const hud = document.getElementById('search-hud');
  const clearBtn = document.getElementById('search-clear-btn');
  if (input) input.value = '';
  if (hud) hud.style.display = 'none';
  if (clearBtn) clearBtn.style.display = 'none';
}

function shareSection() {
  const url = window.location.href;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(url).then(() => alert('Link copiado para a área de transferência!'));
  } else {
    prompt('Copie o link:', url);
  }
}

// ---------------------------------------------------------------------------
// References Popup System
// ---------------------------------------------------------------------------
let referencesMap = null;

const SUPERSCRIPT_MAP = {
  '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
  '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9'
};

function normalizeSuperscriptText(text) {
  let normalized = '';
  for (let char of text) {
    if (SUPERSCRIPT_MAP[char]) {
      normalized += SUPERSCRIPT_MAP[char];
    } else {
      normalized += char;
    }
  }
  return normalized;
}

function getReferenceText(num) {
  if (!referencesMap) {
    referencesMap = {};
    const refPage = MANUAL.pages['referencias'];
    if (refPage) {
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = refPage.html;
      const paragraphs = tempDiv.querySelectorAll('p.body-text');
      paragraphs.forEach(p => {
        const text = p.textContent.trim();
        // matches "1- " or "1 - " or "10 - " etc.
        const match = text.match(/^(\d+)\s*[-–]\s*(.*)$/);
        if (match) {
          referencesMap[parseInt(match[1])] = match[2].trim();
        }
      });
    }
  }
  return referencesMap[num] || null;
}

function showReferencePopup(text) {
  const normalized = normalizeSuperscriptText(text);
  const nums = normalized.match(/\d+/g);
  if (!nums || nums.length === 0) return;
  
  let refContentHtml = '';
  nums.forEach(numStr => {
    const num = parseInt(numStr);
    const refText = getReferenceText(num);
    if (refText) {
      refContentHtml += `<div class="ref-popup-item"><strong>[${num}]</strong> ${refText}</div>`;
    } else {
      refContentHtml += `<div class="ref-popup-item"><strong>[${num}]</strong> Referência não encontrada no manual.</div>`;
    }
  });

  let modal = document.getElementById('reference-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'reference-modal';
    modal.className = 'ref-modal-overlay';
    modal.innerHTML = `
      <div class="ref-modal-container">
        <div class="ref-modal-header">
          <h3>Referência Bibliográfica</h3>
          <button class="ref-modal-close" onclick="closeReferencePopup()">
            <svg class="icon"><use href="#icon-x"/></svg>
          </button>
        </div>
        <div class="ref-modal-body" id="ref-modal-body-content"></div>
      </div>
    `;
    document.body.appendChild(modal);
    
    // Add close on overlay click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeReferencePopup();
      }
    });
  }

  // Set the icon sprite href fix for the close button SVG
  const useEl = modal.querySelector('svg use');
  if (useEl) {
    const href = useEl.getAttribute('href') || '';
    if (href.includes('#') && !href.startsWith('#')) {
      const id = href.split('#')[1];
      useEl.setAttribute('href', '#' + id);
    }
  }

  document.getElementById('ref-modal-body-content').innerHTML = refContentHtml;
  modal.classList.add('active');
}

function closeReferencePopup() {
  const modal = document.getElementById('reference-modal');
  if (modal) {
    modal.classList.remove('active');
  }
}

// Bind to window for HTML onclick actions
window.closeReferencePopup = closeReferencePopup;

// Delegated click listener for <sup> tags
document.addEventListener('click', (e) => {
  const sup = e.target.closest('sup');
  if (sup) {
    e.preventDefault();
    e.stopPropagation();
    showReferencePopup(sup.textContent);
  }
});
