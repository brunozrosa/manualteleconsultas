"""
Quality checks on the generated content files.
"""
import re, os

errors = []
warnings = []

def check_file(fpath, page_id):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Check for hero header
    if 'page-hero' not in content:
        errors.append(f'{page_id}: missing page-hero')
    
    # 2. Check for local-toc div
    if 'local-toc' not in content:
        errors.append(f'{page_id}: missing local-toc')
    
    # 3. Check for h1-page class (page title)
    if 'h1-page' not in content:
        errors.append(f'{page_id}: missing h1-page title')
    
    # 4. Check for body-text paragraphs
    body_texts = content.count('body-text')
    if body_texts == 0:
        warnings.append(f'{page_id}: no body-text paragraphs')
    
    # 5. Check for content-prose or content-wide
    if 'content-prose' not in content and 'content-wide' not in content:
        warnings.append(f'{page_id}: no content-prose or content-wide wrapper')
    
    # 6. Check for page-nav-footer (bottom nav)
    if 'page-nav-footer' not in content:
        errors.append(f'{page_id}: missing page-nav-footer')
    
    # 7. For teleconsulta pages, check stepper
    tele_pages = ['sec3-tele1-anamnese', 'sec3-tele2-obstaculos', 'sec3-tele3-plano', 'sec3-tele4-manutencao']
    if page_id in tele_pages:
        if 'tele-stepper' not in content:
            errors.append(f'{page_id}: missing tele-stepper')
        if 'step-content-pane' not in content:
            errors.append(f'{page_id}: missing step-content-pane')
        if 'pre-info-grid' not in content:
            warnings.append(f'{page_id}: no pre-info-grid (may be OK if page has no H4 before first H3)')
    
    # 8. Check h2-section headings are anchored
    h2s = re.findall(r'h2-section[^>]*id="([^"]+)"', content)
    
    print(f'  {page_id}: body-text={body_texts}, h2s={len(h2s)}')

content_dir = 'content'
for fname in sorted(os.listdir(content_dir)):
    if fname.endswith('.js'):
        page_id = fname.replace('.js', '')
        # Only check pages in PAGE_ORDER
        known_pages = [
            'sec1-apresentacao', 'sec1-estudo-predibra', 'sec1-referencial-teorico',
            'sec1-objetivo-teleconsultas', 'sec2-cuidados-eticos', 'sec2-links-necessarios',
            'sec2-preparando-teleconsulta', 'sec2-durante-teleconsulta', 'sec2-pos-consulta',
            'sec2-estruturacao-teleconsultas', 'sec3-fontes-informacao',
            'sec3-tele1-anamnese', 'sec3-tele2-obstaculos', 'sec3-tele3-plano',
            'sec3-tele4-manutencao', 'sec4-plano-alimentar', 'referencias',
        ]
        if page_id in known_pages:
            check_file(os.path.join(content_dir, fname), page_id)

print(f'\nErrors ({len(errors)}):')
for e in errors:
    print(' ERROR:', e)
print(f'\nWarnings ({len(warnings)}):')
for w in warnings:
    print(' WARN:', w)
