# Manual Interativo de Teleconsultas em Nutrição — PREDIBRA

Aplicação web interativa desenvolvida para orientar nutricionistas na condução das teleconsultas do **Estudo PREDIBRA** (Prevenção e Tratamento da Obesidade no Brasil / FSP-USP), baseada nas diretrizes do *Guia Alimentar para a População Brasileira*.

---

## 📌 Sobre o Projeto

O **Manual de Teleconsultas** é um guia operacional e metodológico completo em formato de aplicação web (SPA — *Single Page Application*), projetado para oferecer navegação rápida, fluida e intuitiva durante os atendimentos nutricionais remotos.

O manual estrutura o percurso assistencial em **4 teleconsultas individualizadas**, abordando:
1. **1ª Teleconsulta**: Acolhimento, diagnóstico do consumo de alimentos ultraprocessados e primeiras pactuações de metas.
2. **2ª Teleconsulta**: Avaliação do cumprimento de metas, enfrentamento de obstáculos e investigação do consumo de alimentos *in natura* e minimamente processados.
3. **3ª Teleconsulta**: Apresentação, validação e ajuste conjunto do Plano Alimentar qualitativo personalizado.
4. **4ª Teleconsulta**: Avaliação da rotina com o plano alimentar, estratégias de sustentabilidade dos hábitos e orientação para autonomia e autocuidado apoiado.

---

## 🚀 Funcionalidades da Aplicação

- 📖 **Navegação Modular SPA**: Troca instantânea de seções e etapas sem recarregar a página, mantendo o histórico de rota via hash (`#sec3-tele1-anamnese`).
- 🧭 **Stepper Dinâmico nas Teleconsultas**: Cada teleconsulta conta com um painel de etapas com fluxo sequencial de navegação (anterior/próximo) e barras de progresso.
- 💡 **Pop-up de Referências Bibliográficas**: Todos os números de citações sobrescritas (`<sup>`) abrem um modal instantâneo com o texto completo da referência e links sem interromper a leitura.
- 🔍 **Busca Local em Tempo Real**: Campo de pesquisa com varredura completa de todas as seções e destaque visual (`<mark>`) dos termos pesquisados.
- 🏷️ **Breadcrumbs Inteligentes com Scroll Spy**: A barra superior atualiza dinamicamente a localização do usuário conforme a rolagem do texto e a etapa ativa.
- 🎨 **Cores Temáticas por Teleconsulta**: Cada teleconsulta possui sua cor de destaque (Teal, Azul, Verde e Âmbar), refletida na barra superior, nos indicadores de leitura e no sumário lateral.
- 🌓 **Modo Escuro / Claro**: Suporte a tema escuro de alto contraste com persistência automática da preferência no `localStorage`.
- 🔠 **Ajuste de Tipografia**: Controle de escala de fonte (A- / A+) para maior acessibilidade visual.
- 📱 **Design Responsivo & Sem Dependências**: Funciona perfeitamente em desktops, notebooks, tablets e smartphones sem necessidade de frameworks pesados ou servidores backend.

---

## 📂 Estrutura de Diretórios

```plaintext
Manual_Teleconsultas/
├── index.html                  # Estrutura principal da aplicação (SPA Shell)
├── README.md                   # Documentação do repositório
├── .gitignore                  # Arquivos e pastas ignorados pelo Git
│
├── assets/
│   ├── css/
│   │   └── main.css            # Design system, tipografia, temas claro/escuro e layout
│   ├── js/
│   │   ├── app.js              # Lógica da aplicação, roteamento, HUD, busca e interações
│   │   └── registry.js         # Registro central de páginas e metadados
│   ├── images/                 # Fluxogramas, resumos gráficos e prints de plataformas
│   │   ├── Figura 1_Fluxograma.jpeg
│   │   ├── Figura 2_Resumo_1_Teleconsulta.jpeg
│   │   ├── Figura 3_Resumo_2_Teleconsulta.jpeg
│   │   ├── Figura 4_Resumo_3_Teleconsulta.jpeg
│   │   ├── Figura 5_Resumo_4_Teleconsulta.jpeg
│   │   ├── Parte_1_Plano-Alimentar.png ... Parte_7_Plano-Alimentar.png
│   │   └── modules/            # Ilustrações dos módulos do aplicativo Feijão no Prato
│   └── logos/                  # Logotipos do estudo PREDIBRA e plataformas de apoio
│
└── content/                    # Conteúdo modularizado em arquivos JavaScript
    ├── home.js                         # Página inicial
    ├── sec1-apresentacao.js            # Seção 1 - Apresentação
    ├── sec1-estudo-predibra.js         # Seção 1 - O Estudo PREDIBRA
    ├── sec1-referencial-teorico.js     # Seção 1 - Referencial Teórico
    ├── sec1-objetivo-teleconsultas.js  # Seção 1 - Objetivos
    ├── sec2-cuidados-eticos.js         # Seção 2 - Cuidados Éticos
    ├── sec2-links-necessarios.js       # Seção 2 - Links e Plataformas
    ├── sec2-preparando-teleconsulta.js # Seção 2 - Pré-consulta
    ├── sec2-durante-teleconsulta.js    # Seção 2 - Durante o Atendimento
    ├── sec2-pos-consulta.js            # Seção 2 - Pós-consulta
    ├── sec2-estruturacao-teleconsultas.js # Seção 2 - Estrutura Geral
    ├── sec3-fontes-informacao.js       # Seção 3 - Fontes de Informação
    ├── sec3-tele1-anamnese.js          # Seção 3 - 1ª Teleconsulta
    ├── sec3-tele2-obstaculos.js        # Seção 3 - 2ª Teleconsulta
    ├── sec3-tele3-plano.js             # Seção 3 - 3ª Teleconsulta
    ├── sec3-tele4-manutencao.js        # Seção 3 - 4ª Teleconsulta
    ├── sec4-plano-alimentar.js         # Seção 4 - Plano Alimentar Base
    └── referencias.js                  # Referências Bibliográficas
```

---

## 🛠️ Tecnologias Utilizadas

- **HTML5**: Estrutura semântica com SVG Icon Sprite embutido (independente de rede externa).
- **CSS3 Puro**: Design System com CSS Custom Properties (variáveis), Grid, Flexbox e animações fluidas.
- **JavaScript Moderno (ES6+)**: Vanilla JS sem bibliotecas externas, utilizando eventos delegados e manipulação eficiente do DOM.
- **Google Fonts**: Tipografia *Outfit* (títulos) e *Inter* (corpo de texto).

---

## 💻 Como Executar

Por ser uma aplicação web estática (*client-side*), **não é necessária instalação de dependências nem compilação de código**.

### Opção 1: Abrir diretamente no navegador
Basta dar dois cliques no arquivo `index.html` ou arrastá-lo para qualquer navegador web moderno (Chrome, Edge, Firefox, Safari).

### Opção 2: Servidor estático local (recomendado)
Caso prefira rodar com um servidor local:

```bash
# Com Python 3:
python -m http.server 8000

# Com Node.js (npx serve):
npx serve .

# Com a extensão 'Live Server' no VS Code:
# Clique com o botão direito em index.html e selecione "Open with Live Server"
```

Acesse: `http://localhost:8000`

---

## 📄 Licença e Créditos

Desenvolvido para o **Estudo PREDIBRA** — *Prevenção e Tratamento da Obesidade no Brasil*  
**Faculdade de Saúde Pública da Universidade de São Paulo (FSP-USP)**
