import os
import json
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text):
    nfkd = unicodedata.normalize('NFKD', text)
    ascii_text = ''.join(c for c in nfkd if not unicodedata.combining(c))
    lower = ascii_text.lower()
    slug = re.sub(r'[^a-z0-9\s]+', '', lower).strip()
    slug = re.sub(r'\s+', '-', slug)
    return slug or 'item'


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def format_runs_to_html(runs):
    parts = []
    for run in runs:
        txt = run.get('text', '')
        if not txt:
            continue
        txt_e = esc(txt)
        if run.get('bold'):
            txt_e = f'<strong>{txt_e}</strong>'
        if run.get('italic'):
            txt_e = f'<em>{txt_e}</em>'
        parts.append(txt_e)
    return ''.join(parts)


# ---------------------------------------------------------------------------
# Page / Section Definitions
# ---------------------------------------------------------------------------

PAGE_METADATA = {
    'home': {
        'section': 'INÍCIO',
        'title': 'Início',
        'icon': 'icon-home',
        'prevId': None,
        'nextId': 'sec1-apresentacao',
    },
    'sec1-apresentacao': {
        'section': 'SEÇÃO 1 — INTRODUÇÃO',
        'title': 'Apresentação',
        'icon': 'icon-book',
        'prevId': 'home',
        'nextId': 'sec1-estudo-predibra',
    },
    'sec1-estudo-predibra': {
        'section': 'SEÇÃO 1 — INTRODUÇÃO',
        'title': 'Estudo PREDIBRA',
        'icon': 'icon-activity',
        'prevId': 'sec1-apresentacao',
        'nextId': 'sec1-referencial-teorico',
    },
    'sec1-referencial-teorico': {
        'section': 'SEÇÃO 1 — INTRODUÇÃO',
        'title': 'Referencial Teórico',
        'icon': 'icon-book',
        'prevId': 'sec1-estudo-predibra',
        'nextId': 'sec1-objetivo-teleconsultas',
    },
    'sec1-objetivo-teleconsultas': {
        'section': 'SEÇÃO 1 — INTRODUÇÃO',
        'title': 'Objetivo das Teleconsultas',
        'icon': 'icon-target',
        'prevId': 'sec1-referencial-teorico',
        'nextId': 'sec2-cuidados-eticos',
    },
    'sec2-cuidados-eticos': {
        'section': 'SEÇÃO 2 — ORIENTAÇÕES OPERACIONAIS',
        'title': 'Cuidados Éticos',
        'icon': 'icon-shield',
        'prevId': 'sec1-objetivo-teleconsultas',
        'nextId': 'sec2-links-necessarios',
    },
    'sec2-links-necessarios': {
        'section': 'SEÇÃO 2 — ORIENTAÇÕES OPERACIONAIS',
        'title': 'Links Necessários',
        'icon': 'icon-link',
        'prevId': 'sec2-cuidados-eticos',
        'nextId': 'sec2-preparando-teleconsulta',
    },
    'sec2-preparando-teleconsulta': {
        'section': 'SEÇÃO 2 — ORIENTAÇÕES OPERACIONAIS',
        'title': 'Preparando-se para a Teleconsulta',
        'icon': 'icon-checklist',
        'prevId': 'sec2-links-necessarios',
        'nextId': 'sec2-durante-teleconsulta',
    },
    'sec2-durante-teleconsulta': {
        'section': 'SEÇÃO 2 — ORIENTAÇÕES OPERACIONAIS',
        'title': 'Durante a Teleconsulta',
        'icon': 'icon-chat',
        'prevId': 'sec2-preparando-teleconsulta',
        'nextId': 'sec2-pos-consulta',
    },
    'sec2-pos-consulta': {
        'section': 'SEÇÃO 2 — ORIENTAÇÕES OPERACIONAIS',
        'title': 'Pós Consulta',
        'icon': 'icon-check',
        'prevId': 'sec2-durante-teleconsulta',
        'nextId': 'sec2-estruturacao-teleconsultas',
    },
    'sec2-estruturacao-teleconsultas': {
        'section': 'SEÇÃO 2 — ORIENTAÇÕES OPERACIONAIS',
        'title': 'Estruturação das Teleconsultas',
        'icon': 'icon-checklist',
        'prevId': 'sec2-pos-consulta',
        'nextId': 'sec3-fontes-informacao',
    },
    'sec3-fontes-informacao': {
        'section': 'SEÇÃO 3 — AS QUATRO TELECONSULTAS',
        'title': 'Fontes de Informação',
        'icon': 'icon-search',
        'prevId': 'sec2-estruturacao-teleconsultas',
        'nextId': 'sec3-tele1-anamnese',
    },
    'sec3-tele1-anamnese': {
        'section': 'SEÇÃO 3 — AS QUATRO TELECONSULTAS',
        'title': '1ª Teleconsulta',
        'icon': 'icon-clipboard',
        'prevId': 'sec3-fontes-informacao',
        'nextId': 'sec3-tele2-obstaculos',
    },
    'sec3-tele2-obstaculos': {
        'section': 'SEÇÃO 3 — AS QUATRO TELECONSULTAS',
        'title': '2ª Teleconsulta',
        'icon': 'icon-target',
        'prevId': 'sec3-tele1-anamnese',
        'nextId': 'sec3-tele3-plano',
    },
    'sec3-tele3-plano': {
        'section': 'SEÇÃO 3 — AS QUATRO TELECONSULTAS',
        'title': '3ª Teleconsulta',
        'icon': 'icon-food',
        'prevId': 'sec3-tele2-obstaculos',
        'nextId': 'sec3-tele4-manutencao',
    },
    'sec3-tele4-manutencao': {
        'section': 'SEÇÃO 3 — AS QUATRO TELECONSULTAS',
        'title': '4ª Teleconsulta',
        'icon': 'icon-maintenance',
        'prevId': 'sec3-tele3-plano',
        'nextId': 'sec4-plano-alimentar',
    },
    'sec4-plano-alimentar': {
        'section': 'SEÇÃO 4 — PLANO ALIMENTAR BASE',
        'title': 'Plano Alimentar Base',
        'icon': 'icon-leaf',
        'prevId': 'sec3-tele4-manutencao',
        'nextId': 'referencias',
    },
    'referencias': {
        'section': 'REFERÊNCIAS',
        'title': 'Referências Bibliográficas',
        'icon': 'icon-book',
        'prevId': 'sec4-plano-alimentar',
        'nextId': None,
    },
}

PAGE_ORDER = [
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
    'referencias',
]

IS_TELECONSULTA = {
    'sec3-tele1-anamnese',
    'sec3-tele2-obstaculos',
    'sec3-tele3-plano',
    'sec3-tele4-manutencao',
}

# Sidebar grouping: section label -> list of page ids
SIDEBAR_SECTIONS = {
    'INÍCIO': {
        'icon': 'icon-home',
        'pages': ['home'],
    },
    'SEÇÃO 1 — INTRODUÇÃO': {
        'icon': 'icon-book',
        'pages': ['sec1-apresentacao', 'sec1-estudo-predibra', 'sec1-referencial-teorico', 'sec1-objetivo-teleconsultas'],
    },
    'SEÇÃO 2 — OPERACIONAL': {
        'icon': 'icon-checklist',
        'pages': ['sec2-cuidados-eticos', 'sec2-links-necessarios', 'sec2-preparando-teleconsulta',
                  'sec2-durante-teleconsulta', 'sec2-pos-consulta', 'sec2-estruturacao-teleconsultas'],
    },
    'SEÇÃO 3 — TELECONSULTAS': {
        'icon': 'icon-chat',
        'pages': ['sec3-fontes-informacao', 'sec3-tele1-anamnese', 'sec3-tele2-obstaculos',
                  'sec3-tele3-plano', 'sec3-tele4-manutencao'],
    },
    'SEÇÃO 4 — PLANO ALIMENTAR': {
        'icon': 'icon-leaf',
        'pages': ['sec4-plano-alimentar'],
    },
    'REFERÊNCIAS': {
        'icon': 'icon-book',
        'pages': ['referencias'],
    },
}

# ---------------------------------------------------------------------------
# Page routing: assign each element to a page_id based on H1/H2 headings
# ---------------------------------------------------------------------------

def get_page_id_for_heading(text, level, current_page_id):
    t = text.strip().lower()

    if level == 1:
        # H1 signals a new top-level section; we stay in current page
        # unless it's a standalone section
        if 'referências' in t or 'referencias' in t:
            return 'referencias'
        return current_page_id

    if level == 2:
        if 'apresentação' in t or 'apresentacao' in t:
            return 'sec1-apresentacao'
        if 'estudo predibra' in t:
            return 'sec1-estudo-predibra'
        if 'referencial teórico' in t or 'referencial teorico' in t:
            return 'sec1-referencial-teorico'
        if 'objetivo' in t and 'teleconsult' in t:
            return 'sec1-objetivo-teleconsultas'
        if 'cuidados éticos' in t or 'cuidados eticos' in t:
            return 'sec2-cuidados-eticos'
        if 'links necessários' in t or 'links necessarios' in t:
            return 'sec2-links-necessarios'
        if 'preparando' in t and 'teleconsult' in t:
            return 'sec2-preparando-teleconsulta'
        if 'durante a teleconsult' in t:
            return 'sec2-durante-teleconsulta'
        if 'pós consulta' in t or 'pos consulta' in t:
            return 'sec2-pos-consulta'
        if 'estruturação' in t or 'estruturacao' in t:
            return 'sec2-estruturacao-teleconsultas'
        if 'fontes de informação' in t or 'fontes de informacao' in t:
            return 'sec3-fontes-informacao'
        if '1ª teleconsulta' in t or '1a teleconsulta' in t:
            return 'sec3-tele1-anamnese'
        if '2ª teleconsulta' in t or '2a teleconsulta' in t:
            return 'sec3-tele2-obstaculos'
        if '3ª teleconsulta' in t or '3a teleconsulta' in t:
            return 'sec3-tele3-plano'
        if '4ª teleconsulta' in t or '4a teleconsulta' in t:
            return 'sec3-tele4-manutencao'
        if 'plano alimentar base' in t:
            return 'sec4-plano-alimentar'
        # H2 "vamos começar?" → maps to sec2-cuidados-eticos (opening of sec2)
        if 'vamos come' in t:
            return 'sec2-cuidados-eticos'
        if '4 - ocorrências' in t or 'ocorrencias' in t:
            return 'sec2-durante-teleconsulta'

    return current_page_id

# ---------------------------------------------------------------------------
# Reading time & search text
# ---------------------------------------------------------------------------

def calculate_reading_time(elements):
    words = 0
    for el in elements:
        if el['type'] in ('paragraph', 'heading'):
            words += len(el.get('text', '').split())
        elif el['type'] == 'table':
            for row in el.get('data', []):
                for cell in row:
                    words += len(cell.split())
    return max(1, round(words / 200))


def compile_search_text(elements):
    parts = []
    for el in elements:
        if el['type'] in ('paragraph', 'heading'):
            parts.append(el.get('text', ''))
        elif el['type'] == 'table':
            for row in el.get('data', []):
                parts.append(' '.join(row))
    full = ' '.join(parts)
    return full.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').replace('\r', '')

# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def svg_icon(icon_id, extra_class=''):
    cls = f'icon {extra_class}'.strip()
    return f'<svg class="{cls}" aria-hidden="true"><use href="assets/icons/sprite.svg#{icon_id}"/></svg>'


def render_table_to_html(table_el):
    data = table_el.get('data', [])
    if not data:
        return ''
    rows_html = []
    for r_idx, row in enumerate(data):
        is_header = r_idx == 0
        tag = 'th' if is_header else 'td'
        cells = []
        col_idx = 0
        while col_idx < len(row):
            cell_text = row[col_idx].strip()
            colspan = 1
            while col_idx + colspan < len(row) and row[col_idx + colspan].strip() == cell_text:
                colspan += 1
            cspan = f' colspan="{colspan}"' if colspan > 1 else ''
            cell_html = cell_text.replace('\n', '<br>')
            cells.append(f'<{tag}{cspan}>{cell_html}</{tag}>')
            col_idx += colspan
        rows_html.append(f'<tr>{"".join(cells)}</tr>')
    return f'''<div class="content-wide table-responsive">
<table class="manual-table">{"".join(rows_html)}</table>
</div>'''


def render_paragraph_to_html(el, in_card=False):
    """Convert a paragraph element to HTML, detecting special types."""
    runs = el.get('runs', [])
    text = el.get('text', '')
    formatted = format_runs_to_html(runs) if runs else esc(text)
    text_lower = text.lower().strip()

    # --- Alert boxes ---
    if text_lower.startswith('importante:'):
        content = re.sub(r'^importante:\s*', '', formatted, flags=re.IGNORECASE)
        return f'''<div class="content-prose alert-box alert-importante">
  {svg_icon('icon-info','alert-icon')}
  <div class="alert-content"><strong>Importante:</strong> {content}</div>
</div>'''

    if text_lower.startswith('atenção:') or text_lower.startswith('atencao:'):
        content = re.sub(r'^aten[çc]ao:\s*', '', formatted, flags=re.IGNORECASE)
        return f'''<div class="content-prose alert-box alert-atencao">
  {svg_icon('icon-alert','alert-icon')}
  <div class="alert-content"><strong>Atenção:</strong> {content}</div>
</div>'''

    if text_lower.startswith('dica:'):
        content = re.sub(r'^dica:\s*', '', formatted, flags=re.IGNORECASE)
        return f'''<div class="content-prose alert-box alert-dica">
  {svg_icon('icon-lightbulb','alert-icon')}
  <div class="alert-content"><strong>Dica:</strong> {content}</div>
</div>'''

    # --- Speech boxes ---
    speech_prefixes = {
        'explique:': ('icon-chat', 'Fala sugerida', 'speech-box'),
        'pergunte:': ('icon-question', 'Sugestão de pergunta', 'speech-box speech-question'),
        'exemplo de explicação:': ('icon-lightbulb', 'Exemplo de explicação', 'speech-box speech-example'),
        'exemplo de explicacao:': ('icon-lightbulb', 'Exemplo de explicação', 'speech-box speech-example'),
        'exemplo:': ('icon-lightbulb', 'Exemplo', 'speech-box speech-example'),
    }
    for prefix_key, (icon_id, label, cls) in speech_prefixes.items():
        if text_lower.startswith(prefix_key):
            content = formatted[len(prefix_key):].strip()
            return f'''<div class="content-prose {cls}">
  <div class="speech-header">
    <span class="speech-label">{svg_icon(icon_id)} {label}</span>
  </div>
  <div class="speech-content"><em>{content}</em></div>
</div>'''

    # --- Figure caption ---
    if text_lower.startswith('figura ') or text_lower.startswith('quadro '):
        return f'<p class="content-prose figure-label">{svg_icon("icon-search")} {formatted}</p>'

    # --- Action card items (numbered/lettered lists in teleconsulta context) ---
    if in_card:
        list_match = re.match(r'^(\d+[\s\-\)]+|[a-h]\)\s+)', text_lower)
        if list_match:
            prefix = list_match.group(0)
            content = formatted[len(prefix):].strip()
            clean_prefix = prefix.strip(' -)')
            return f'''<div class="action-card">
  <div class="action-checkbox" onclick="toggleActionCard(this)">{svg_icon('icon-square')}</div>
  <div class="action-content">
    <span class="action-num">{clean_prefix}</span>
    <span class="action-text">{content}</span>
  </div>
</div>'''

    return f'<p class="body-text">{formatted}</p>'

# ---------------------------------------------------------------------------
# Anchor generation
# ---------------------------------------------------------------------------
_anchor_counts = {}

def make_anchor(page_id, text):
    base = f"{page_id}-{slugify(text)}"
    n = _anchor_counts.get(base, 0)
    _anchor_counts[base] = n + 1
    return base if n == 0 else f"{base}-{n}"

# ---------------------------------------------------------------------------
# Main page renderer
# ---------------------------------------------------------------------------

def render_page_elements_to_html(page_id, elements):
    global _anchor_counts
    _anchor_counts = {}

    meta = PAGE_METADATA[page_id]
    is_tele = page_id in IS_TELECONSULTA
    html = []

    if page_id == 'home':
        home_html = """<div class="home-page-container">
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
          <svg class="icon"><use href="assets/icons/sprite.svg#icon-book"/></svg>
        </div>
        <h4>Introdução</h4>
        <p>Apresenta a contextualização do projeto PREDIBRA, seus objetivos e os referenciais teóricos que orientam o cuidado em saúde e o cuidado nutricional.</p>
        <span class="card-action">Acessar Seção <svg class="icon"><use href="assets/icons/sprite.svg#icon-arrow-right"/></svg></span>
      </div>
      <div class="home-summary-card" onclick="selectSection('sec2-cuidados-eticos')">
        <div class="card-icon">
          <svg class="icon"><use href="assets/icons/sprite.svg#icon-checklist"/></svg>
        </div>
        <h4>Orientações Operacionais</h4>
        <p>Reúne orientações práticas e cuidados éticos para a realização de teleconsultas, englobando a preparação, a condução e o pós-consulta.</p>
        <span class="card-action">Acessar Seção <svg class="icon"><use href="assets/icons/sprite.svg#icon-arrow-right"/></svg></span>
      </div>
      <div class="home-summary-card" onclick="selectSection('sec3-fontes-informacao')">
        <div class="card-icon">
          <svg class="icon"><use href="assets/icons/sprite.svg#icon-chat"/></svg>
        </div>
        <h4>Teleconsultas</h4>
        <p>Detalhamento prático de cada uma das quatro teleconsultas de nutrição estruturadas, focando no Guia Alimentar para a População Brasileira.</p>
        <span class="card-action">Acessar Seção <svg class="icon"><use href="assets/icons/sprite.svg#icon-arrow-right"/></svg></span>
      </div>
    </div>
  </section>
</div>"""
        html.append(home_html)
    else:
        # ---- Hero Header ----
    section_badge = meta['section']
    page_title = meta['title']
    page_icon = meta.get('icon', 'icon-book')
    reading_time = calculate_reading_time(elements)

    hero_html = f'''<div class="page-hero" id="page-top">
  <div class="page-hero-inner">
    <span class="section-badge">{section_badge}</span>
    <div class="page-hero-title-row">
      <div class="page-hero-icon">{svg_icon(page_icon)}</div>
      <h1 class="h1-page">{page_title}</h1>
    </div>
    <div class="page-hero-meta">
      {svg_icon('icon-clock')} <span>{reading_time} min de leitura</span>
    </div>
  </div>
</div>'''
    html.append(hero_html)

    # ---- Local TOC placeholder (populated by JS) ----
    html.append('<div class="local-toc" id="local-toc" aria-label="Nesta página"></div>')

    # ---- Content ----
    if is_tele:
        html.extend(_render_tele_page(page_id, elements, meta))
    else:
        html.extend(_render_standard_page(page_id, elements, meta))

    # ---- Bottom navigation ----
    prev_id = meta.get('prevId')
    next_id = meta.get('nextId')
    nav_parts = ['<div class="page-nav-footer content-wide">']
    if prev_id and prev_id in PAGE_METADATA:
        prev_title = PAGE_METADATA[prev_id]['title']
        nav_parts.append(f'''<button class="nav-btn" onclick="selectSection('{prev_id}')">
  {svg_icon('icon-arrow-right','rotate-180')} {prev_title}
</button>''')
    else:
        nav_parts.append('<div></div>')

    if next_id and next_id in PAGE_METADATA:
        next_title = PAGE_METADATA[next_id]['title']
        nav_parts.append(f'''<button class="nav-btn next-btn" onclick="selectSection('{next_id}')">
  {next_title} {svg_icon('icon-arrow-right')}
</button>''')
    else:
        nav_parts.append('<div></div>')
    nav_parts.append('</div>')
    html.append('\n'.join(nav_parts))

    return '\n'.join(html)


def _render_standard_page(page_id, elements, meta):
    """Render a non-teleconsulta page with H3/H4/H5/H6 hierarchy."""
    html = []
    # We'll collect runs of H5 elements into card grids
    card_buffer = []  # accumulates (h5_el, [content_elements])
    current_card_content = []
    in_card_group = False

    def flush_cards():
        nonlocal in_card_group
        if not card_buffer:
            return []
        out = ['<div class="content-wide card-grid">']
        for (h5_el, card_elems) in card_buffer:
            card_title = esc(h5_el.get('text', ''))
            out.append('<div class="content-card">')
            out.append(f'<div class="h4-label card-title">{card_title}</div>')
            out.append('<div class="card-body">')
            for cel in card_elems:
                if cel['type'] == 'paragraph':
                    out.append(render_paragraph_to_html(cel, in_card=False))
                elif cel['type'] == 'heading':
                    level = cel['level']
                    if level == 6:
                        out.append(f'<p class="h5-caption">{esc(cel["text"])}</p>')
                    else:
                        out.append(f'<p class="body-text"><strong>{esc(cel["text"])}</strong></p>')
                elif cel['type'] == 'table':
                    out.append(render_table_to_html(cel))
            out.append('</div></div>')
        out.append('</div>')
        card_buffer.clear()
        in_card_group = False
        return out

    i = 0
    while i < len(elements):
        el = elements[i]
        etype = el['type']

        if etype == 'heading':
            level = el['level']
            text = el.get('text', '')

            # Skip the H1/H2 that titles the page itself
            if level <= 2:
                title_text = meta['title'].lower()
                if text.lower().strip() in title_text or title_text in text.lower().strip():
                    i += 1
                    continue
                # For H2 sub-pages heading appearing in content: treat as section
                if level == 2:
                    html.extend(flush_cards())
                    anchor = make_anchor(page_id, text)
                    html.append(f'<h2 class="h2-section content-prose" id="{anchor}">{esc(text)}</h2>')
                    i += 1
                    continue
                i += 1
                continue

            if level == 3:
                html.extend(flush_cards())
                anchor = make_anchor(page_id, text)
                html.append(f'<h2 class="h2-section content-prose" id="{anchor}">{esc(text)}</h2>')

            elif level == 4:
                html.extend(flush_cards())
                anchor = make_anchor(page_id, text)
                html.append(f'<h3 class="h3-subsection content-prose" id="{anchor}">{esc(text)}</h3>')

            elif level == 5:
                # Start of a new card — collect its content
                if card_buffer:
                    # finalize previous card's content
                    card_buffer[-1] = (card_buffer[-1][0], current_card_content[:])
                current_card_content = []
                card_buffer.append((el, current_card_content))
                in_card_group = True

            elif level == 6:
                if in_card_group and card_buffer:
                    current_card_content.append(el)
                else:
                    html.append(f'<p class="h5-caption content-prose">{esc(text)}</p>')

        elif etype == 'paragraph':
            if in_card_group and card_buffer:
                current_card_content.append(el)
            else:
                html.extend(flush_cards())
                html.append(render_paragraph_to_html(el, in_card=False))

        elif etype == 'table':
            html.extend(flush_cards())
            html.append(render_table_to_html(el))

        i += 1

    html.extend(flush_cards())
    return html


def _render_tele_page(page_id, elements, meta):
    """Render a teleconsulta page: hero info cards + stepper by H3 etapa."""
    html = []

    # --- Pre-consulta block: collect H4s before first H3 "Etapa" ---
    pre_info = []   # H4 elements like Pré-consulta, Objetivo, Resumo
    pre_content = []  # paragraph content for those H4s
    steps = []   # list of {title, anchor, h4s: [{title, anchor, elements}]}
    current_step = None
    current_h4 = None

    i = 0
    pre_phase = True  # before first H3 "Etapa"

    while i < len(elements):
        el = elements[i]
        etype = el['type']
        level = el.get('level', 0)
        text = el.get('text', '')

        if etype == 'heading':
            if level <= 2:
                i += 1
                continue

            if level == 3:
                # H3 = Etapa N — start a new step
                pre_phase = False
                current_h4 = None
                anchor = make_anchor(page_id, text)
                current_step = {'title': text, 'anchor': anchor, 'h4s': []}
                steps.append(current_step)

            elif level == 4:
                anchor = make_anchor(page_id, text)
                if pre_phase:
                    new_h4 = {'title': text, 'anchor': anchor, 'elements': []}
                    pre_info.append(new_h4)
                    current_h4 = new_h4
                else:
                    if current_step is None:
                        current_step = {'title': 'Introdução', 'anchor': make_anchor(page_id, 'intro'), 'h4s': []}
                        steps.append(current_step)
                    # Create new h4 and append it immediately (don't double-append)
                    current_h4 = {'title': text, 'anchor': anchor, 'elements': []}
                    current_step['h4s'].append(current_h4)

            elif level == 5:
                # H5 inside tele = card group item — attach to current h4
                card_el = {'_is_h5': True, 'title': text, 'elements': []}
                if current_h4 is not None:
                    current_h4['elements'].append({'_card': card_el})
                elif pre_phase and pre_info:
                    pre_info[-1]['elements'].append({'_card': card_el})

            elif level == 6:
                card_el_ref = None
                if current_h4 and current_h4['elements'] and isinstance(current_h4['elements'][-1], dict) and '_card' in current_h4['elements'][-1]:
                    card_el_ref = current_h4['elements'][-1]['_card']
                if card_el_ref:
                    card_el_ref['elements'].append({'type': 'heading', 'level': 6, 'text': text})
                elif current_h4 is not None:
                    current_h4['elements'].append(el)
                elif pre_phase and pre_info:
                    pre_info[-1]['elements'].append(el)

        elif etype == 'paragraph':
            if pre_phase and pre_info:
                # attach to last pre_info h4
                pre_info[-1]['elements'].append(el)
            elif pre_phase:
                pre_content.append(el)
            elif current_h4 is not None:
                # check if last element is a card to add to it
                if current_h4['elements'] and isinstance(current_h4['elements'][-1], dict) and '_card' in current_h4['elements'][-1]:
                    current_h4['elements'][-1]['_card']['elements'].append(el)
                else:
                    current_h4['elements'].append(el)
            elif current_step is not None:
                current_step.setdefault('intro_elements', []).append(el)

        elif etype == 'table':
            if current_h4 is not None:
                current_h4['elements'].append(el)
            elif pre_phase and pre_info:
                pre_info[-1]['elements'].append(el)

        i += 1

    # --- Render pre-info cards ---
    if pre_info or pre_content:
        html.append('<div class="content-wide pre-info-grid">')
        for pi in pre_info:
            anchor = pi['anchor']
            title = esc(pi['title'])
            # Pick an icon based on title keywords
            pi_icon = 'icon-info'
            tl = pi['title'].lower()
            if 'pré' in tl or 'pre' in tl:
                pi_icon = 'icon-checklist'
            elif 'objetivo' in tl:
                pi_icon = 'icon-target'
            elif 'resumo' in tl:
                pi_icon = 'icon-clipboard'
            html.append(f'<div class="pre-info-card" id="{anchor}">')
            html.append(f'<div class="pre-info-card-header">{svg_icon(pi_icon)}<span class="h4-label">{title}</span></div>')
            html.append('<div class="pre-info-card-body">')
            for cel in pi['elements']:
                if isinstance(cel, dict) and '_card' in cel:
                    pass  # cards within pre-info rendered inline
                elif cel['type'] == 'paragraph':
                    html.append(render_paragraph_to_html(cel, in_card=False))
                elif cel['type'] == 'table':
                    html.append(render_table_to_html(cel))
                elif cel['type'] == 'heading' and cel['level'] == 6:
                    html.append(f'<p class="h5-caption">{esc(cel["text"])}</p>')
            html.append('</div></div>')
        for para in pre_content:
            html.append(render_paragraph_to_html(para))
        html.append('</div>')

    # --- Stepper header ---
    if steps:
        html.append('<div class="tele-stepper content-wide">')
        for idx, step in enumerate(steps):
            active_class = 'active' if idx == 0 else ''
            step_num = idx + 1
            html.append(f'''<div class="step-indicator {active_class}" data-step="{step_num}" onclick="showTeleStep('{page_id}', {step_num})">
  <div class="step-circle">{step_num}</div>
  <div class="step-label">
    <div class="step-title">{esc(step["title"])}</div>
  </div>
</div>''')
            if idx < len(steps) - 1:
                html.append('<div class="step-line"></div>')
        html.append('</div>')

    # --- Step content panes ---
    for idx, step in enumerate(steps):
        active_class = 'active' if idx == 0 else ''
        step_num = idx + 1
        html.append(f'<div class="step-content-pane {active_class}" data-step-content="{step_num}">')

        # intro elements of the step (paragraphs before first H4)
        for el in step.get('intro_elements', []):
            html.append(render_paragraph_to_html(el))

        # H4 subsections
        for h4 in step.get('h4s', []):
            anchor = h4['anchor']
            h4_title = esc(h4['title'])
            html.append(f'<h3 class="h3-subsection content-prose" id="{anchor}">{h4_title}</h3>')

            # collect cards
            card_items = []
            non_card_items = []
            for cel in h4['elements']:
                if isinstance(cel, dict) and '_card' in cel:
                    card_items.append(cel['_card'])
                else:
                    non_card_items.append(cel)

            # render non-card elements
            for cel in non_card_items:
                if cel['type'] == 'paragraph':
                    html.append(render_paragraph_to_html(cel, in_card=True))
                elif cel['type'] == 'table':
                    html.append(render_table_to_html(cel))
                elif cel['type'] == 'heading' and cel['level'] == 6:
                    html.append(f'<p class="h5-caption content-prose">{esc(cel["text"])}</p>')

            # render card grid
            if card_items:
                html.append('<div class="content-wide card-grid">')
                for card in card_items:
                    card_title_text = esc(card.get('title', ''))
                    html.append('<div class="content-card">')
                    html.append(f'<div class="h4-label card-title">{card_title_text}</div>')
                    html.append('<div class="card-body">')
                    for ce in card.get('elements', []):
                        if ce['type'] == 'paragraph':
                            html.append(render_paragraph_to_html(ce, in_card=False))
                        elif ce['type'] == 'heading' and ce['level'] == 6:
                            html.append(f'<p class="h5-caption">{esc(ce["text"])}</p>')
                        elif ce['type'] == 'table':
                            html.append(render_table_to_html(ce))
                    html.append('</div></div>')
                html.append('</div>')

        # Step navigation buttons
        html.append('<div class="step-navigation-footer content-wide">')
        if idx > 0:
            html.append(f'<button class="nav-btn prev-btn" onclick="showTeleStep(\'{page_id}\', {step_num - 1})">{svg_icon("icon-arrow-right","rotate-180")} Etapa anterior</button>')
        else:
            html.append('<div></div>')
        if idx < len(steps) - 1:
            html.append(f'<button class="nav-btn next-btn" onclick="showTeleStep(\'{page_id}\', {step_num + 1})">Próxima etapa {svg_icon("icon-arrow-right")}</button>')
        else:
            next_id = meta.get('nextId')
            if next_id:
                next_title = PAGE_METADATA[next_id]['title']
                html.append(f'<button class="nav-btn next-btn next-tele-btn" onclick="selectSection(\'{next_id}\')">Ir para {next_title} {svg_icon("icon-arrow-right")}</button>')
            else:
                html.append('<div></div>')
        html.append('</div>')
        html.append('</div>')  # end step-content-pane

    return html

# ---------------------------------------------------------------------------
# Build everything
# ---------------------------------------------------------------------------

def build_structure():
    os.makedirs(os.path.join('assets', 'css'), exist_ok=True)
    os.makedirs(os.path.join('assets', 'js'), exist_ok=True)
    os.makedirs(os.path.join('assets', 'icons'), exist_ok=True)
    os.makedirs('content', exist_ok=True)

    with open('manual_extracted_structure.json', 'r', encoding='utf-8') as f:
        elements = json.load(f)

    # ---- Partition elements into pages ----
    pages_content = {pid: [] for pid in PAGE_ORDER}
    current_page_id = PAGE_ORDER[0]

    for el in elements:
        if el['type'] == 'heading':
            current_page_id = get_page_id_for_heading(el['text'], el['level'], current_page_id)
        if current_page_id in pages_content:
            pages_content[current_page_id].append(el)

    print('Partitioned elements:')
    for pid in PAGE_ORDER:
        print(f'  {pid}: {len(pages_content[pid])} elements')

    # ---- Generate content JS files ----
    for pid in PAGE_ORDER:
        meta = PAGE_METADATA[pid]
        p_elems = pages_content[pid]
        if pid == 'home':
            reading_time = 0
            search_text = "MANUAL PARA TELECONSULTAS EM NUTRIÇÃO BASEADO NO GUIA ALIMENTAR PARA A POPULAÇÃO BRASILEIRA Universidade de São Paulo Faculdade de Saúde Pública Projeto de pesquisa Eficácia de uma intervenção digital de promoção da dieta brasileira na prevenção de doenças o ensaio clínico PREDIBRA Núcleo de Pesquisas Epidemiológicas em Nutrição e Saúde NUPENS São Paulo 2026 Introdução Orientações Operacionais Teleconsultas"
        else:
            reading_time = calculate_reading_time(p_elems)
            search_text = compile_search_text(p_elems)
        html_content = render_page_elements_to_html(pid, p_elems)
        html_escaped = html_content.replace('`', '\\`').replace('${', '\\${')

        js_content = f"""// content/{pid}.js
MANUAL.registerPage('{pid}', {{
  section: '{meta['section']}',
  title: '{meta['title']}',
  readingTime: {reading_time},
  prevId: {f"'{meta['prevId']}'" if meta.get('prevId') else 'null'},
  nextId: {f"'{meta['nextId']}'" if meta.get('nextId') else 'null'},
  searchText: "{search_text}",
  html: `{html_escaped}`
}});
"""
        fpath = os.path.join('content', f'{pid}.js')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f'Generated {fpath}')

    # ---- registry.js ----
    order_str = ',\n    '.join(f"'{p}'" for p in PAGE_ORDER)
    registry_js = f"""// assets/js/registry.js
window.MANUAL = {{
  pages: {{}},
  order: [
    {order_str}
  ],
  registerPage: function(id, data) {{
    this.pages[id] = data;
  }}
}};
"""
    with open(os.path.join('assets', 'js', 'registry.js'), 'w', encoding='utf-8') as f:
        f.write(registry_js)
    print('Generated assets/js/registry.js')

    # ---- Build sidebar sections JS literal ----
    sidebar_sections_js = _build_sidebar_sections_js()

    # ---- app.js ----
    app_js = _build_app_js(sidebar_sections_js)
    with open(os.path.join('assets', 'js', 'app.js'), 'w', encoding='utf-8') as f:
        f.write(app_js)
    print('Generated assets/js/app.js')

    # ---- main.css (read from existing) ----
    css_path = os.path.join('assets', 'css', 'main.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            styles_content = f.read()
        styles_content = styles_content.replace('body.dark-mode {', 'body.dark-mode, body.dark {')
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(styles_content)
    print('Preserved assets/css/main.css')

    # ---- index.html ----
    scripts_tags = ['<script src="assets/js/registry.js"></script>']
    for pid in PAGE_ORDER:
        scripts_tags.append(f'<script src="content/{pid}.js"></script>')
    scripts_tags.append('<script src="assets/js/app.js"></script>')
    scripts_markup = '\n    '.join(scripts_tags)

    index_html = _build_index_html(scripts_markup)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print('Generated index.html')


def _build_sidebar_sections_js():
    """Build the JS object literal for sidebar sections."""
    lines = ['const SIDEBAR_SECTIONS = {']
    for sec_title, sec_data in SIDEBAR_SECTIONS.items():
        icon = sec_data['icon']
        pages = sec_data['pages']
        pages_str = ', '.join(f"'{p}'" for p in pages)
        safe_title = sec_title.replace("'", "\\'")
        lines.append(f"  '{safe_title}': {{ icon: '{icon}', pages: [{pages_str}] }},")
    lines.append('};')
    return '\n'.join(lines)


def _build_app_js(sidebar_sections_js):
    return r"""// assets/js/app.js

const state = {
  activeSection: 'home',
  sidebarCollapsed: false,
  darkMode: false,
  fontScale: 1.0,
  activeSteps: {},
};

""" + sidebar_sections_js + r"""

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
  return `<svg class="${cls}" aria-hidden="true"><use href="assets/icons/sprite.svg#${id}"/></svg>`;
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
    viewport.scrollTop = 0;
  }

  // Teleconsulta color theme
  document.body.classList.remove('tele-theme-1', 'tele-theme-2', 'tele-theme-3', 'tele-theme-4');
  if (pId === 'sec3-tele1-anamnese') document.body.classList.add('tele-theme-1');
  else if (pId === 'sec3-tele2-obstaculos') document.body.classList.add('tele-theme-2');
  else if (pId === 'sec3-tele3-plano') document.body.classList.add('tele-theme-3');
  else if (pId === 'sec3-tele4-manutencao') document.body.classList.add('tele-theme-4');

  // Sidebar highlight
  document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.sidebar-nav li').forEach(el => el.classList.remove('active-sub'));

  const activeSubItem = document.querySelector(`.sidebar-nav li[data-sub-section="${pId}"]`);
  if (activeSubItem) {
    activeSubItem.classList.add('active-sub');
    const parentContainer = activeSubItem.closest('.menu-item-container');
    if (parentContainer) parentContainer.classList.add('expanded');
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

// ---------------------------------------------------------------------------
// Teleconsulta stepper
// ---------------------------------------------------------------------------
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

  viewport.scrollTop = 0;
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
function updateHeaderHUD(pId) {
  const page = MANUAL.pages[pId];
  if (!page) return;
  const breadcrumbs = document.getElementById('app-breadcrumbs');
  const readTimeBadge = document.getElementById('header-read-time');
  if (breadcrumbs) {
    if (pId === 'home') {
      breadcrumbs.innerHTML = `<span>Início</span>`;
    } else {
      breadcrumbs.innerHTML = `<span>${page.section}</span> ${svgIcon('icon-chevron-right')} <span>${page.title}</span>`;
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
      ${secData.pages.length > 1 ? `<span class="toggle-submenu" onclick="toggleSubmenu(event,'${secSlug}')">${svgIcon('icon-chevron-right')}</span>` : ''}
    `;
    container.appendChild(menuItem);

    if (secData.pages.length > 1) {
      const submenu = document.createElement('ul');
      submenu.className = 'submenu';

      secData.pages.forEach(pId => {
        const page = MANUAL.pages[pId];
        if (!page) return;
        const li = document.createElement('li');
        li.setAttribute('data-sub-section', pId);
        li.onclick = e => { e.stopPropagation(); selectSection(pId); };

        const isTele = ['sec3-tele1-anamnese','sec3-tele2-obstaculos','sec3-tele3-plano','sec3-tele4-manutencao'].includes(pId);
        if (isTele) li.className = 'tele-link';

        li.innerHTML = `
          <span class="sub-title">${page.title}</span>
          <span class="sub-read-badge">${page.readingTime} min</span>
          <span class="check-progress-icon" style="margin-left:6px;display:none;">${svgIcon('icon-check')}</span>
        `;
        submenu.appendChild(li);
      });
      container.appendChild(submenu);
    }
    nav.appendChild(container);
  }
  updateSidebarProgress();
}

function updateSidebarProgress() {
  const visited = JSON.parse(localStorage.getItem('visited_pages') || '{}');
  document.querySelectorAll('.sidebar-nav li').forEach(li => {
    const pId = li.getAttribute('data-sub-section');
    const icon = li.querySelector('.check-progress-icon');
    if (icon) icon.style.display = visited[pId] ? 'inline' : 'none';
  });
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
"""


def _build_index_html(scripts_markup):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manual de Teleconsultas — PREDIBRA</title>
    <meta name="description" content="Manual para teleconsultas em nutrição baseado no Guia Alimentar para a População Brasileira — Estudo PREDIBRA / USP">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/main.css">
</head>
<body>

<!-- SVG Icon Sprite (inline, no network required) -->
<div id="svg-sprite-container" style="display:none" aria-hidden="true">
  <!-- sprite loaded via JS to avoid file:// issues with <use href="..."> on some browsers -->
</div>

<div class="app-container">
    <!-- Sidebar Navigation -->
    <aside class="sidebar" id="app-sidebar">
        <div class="sidebar-brand" onclick="selectSection('home')" style="cursor: pointer;">
            <div class="brand-logo">
                <span class="brand-logo-icon">
                    <svg class="icon icon-lg" aria-hidden="true"><use href="assets/icons/sprite.svg#icon-leaf"/></svg>
                </span>
                <span class="logo-text">PREDIBRA</span>
            </div>
            <div class="brand-subtext">Nutrição Baseada no Guia Alimentar</div>
        </div>

        <!-- Search -->
        <div class="search-box-container">
            <div class="search-input-wrapper">
                <svg class="icon search-input-icon" aria-hidden="true"><use href="assets/icons/sprite.svg#icon-search"/></svg>
                <input type="text" id="manual-search" placeholder="Buscar no manual..." oninput="performSearch()">
                <button id="search-clear-btn" onclick="clearSearch()" style="display:none;" aria-label="Limpar busca">
                    <svg class="icon"><use href="assets/icons/sprite.svg#icon-x"/></svg>
                </button>
            </div>
        </div>

        <!-- Table of Contents -->
        <div class="toc-scroll-area">
            <div class="toc-header">CONTEÚDO DO MANUAL</div>
            <nav class="sidebar-nav">
                <!-- Populated by app.js -->
            </nav>
        </div>

        <!-- Sidebar Controls -->
        <div class="sidebar-controls">
            <button class="control-btn" id="theme-toggle" onclick="toggleTheme()" title="Alternar Modo Escuro/Claro">
                <svg class="icon"><use href="assets/icons/sprite.svg#icon-moon"/></svg> Modo Escuro
            </button>
            <div class="font-size-adjuster">
                <span class="control-label">Texto:</span>
                <button class="font-btn" onclick="adjustFontSize(-1)" title="Diminuir texto">A-</button>
                <button class="font-btn" onclick="adjustFontSize(1)" title="Aumentar texto">A+</button>
            </div>
        </div>
    </aside>

    <!-- Main Content Area -->
    <div class="main-layout">
        <header class="top-navbar">
            <div class="navbar-left">
                <button class="sidebar-toggle-btn" onclick="toggleSidebar()" title="Recolher/Expandir menu" aria-label="Toggle menu">
                    <svg class="icon"><use href="assets/icons/sprite.svg#icon-menu"/></svg>
                </button>
                <div class="breadcrumbs" id="app-breadcrumbs">
                    <!-- Populated by app.js -->
                </div>
            </div>
            <div class="navbar-right">
                <div class="section-stats-badge" id="header-read-time">
                    <svg class="icon"><use href="assets/icons/sprite.svg#icon-clock"/></svg>
                    <span>— min</span>
                </div>
                <div class="print-share-controls">
                    <button class="nav-action-btn" onclick="shareSection()" title="Copiar link para esta seção">
                        <svg class="icon"><use href="assets/icons/sprite.svg#icon-share"/></svg> Compartilhar
                    </button>
                </div>
            </div>
        </header>

        <!-- Reading progress bar -->
        <div class="progress-bar-container">
            <div class="progress-bar-fill" id="reading-progress-bar"></div>
        </div>

        <!-- Search Results HUD -->
        <div class="search-results-overlay" id="search-hud" style="display:none;">
            <div class="hud-header">
                <span class="hud-title">
                    <svg class="icon"><use href="assets/icons/sprite.svg#icon-search"/></svg>
                    Resultados da busca (<span id="search-count">0</span>)
                </span>
                <button class="hud-close-btn" onclick="clearSearch()">
                    <svg class="icon"><use href="assets/icons/sprite.svg#icon-x"/></svg> Fechar
                </button>
            </div>
            <div class="hud-results-list" id="search-results-list"></div>
        </div>

        <!-- Primary Content Viewport -->
        <main class="content-viewport" id="content-viewport">
            <!-- Content loaded dynamically -->
        </main>
    </div>
</div>

<!-- Scripts -->
{scripts_markup}
</body>
</html>
"""


if __name__ == '__main__':
    build_structure()
