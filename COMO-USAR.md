# Como usar

Arquivos deste pacote:

```
github-profile/
├── .github/
│   └── workflows/
│       └── main.yml           → Automação do GitHub Actions (atualiza stats e Pac-Man)
├── assets/
│   └── banner.svg             → Template base do banner (com marcadores dinâmicos)
├── scripts/
│   └── generate_stats.py      → Script que consulta a API do GitHub e compila o banner
├── output/
│   ├── banner.svg             → Banner final gerado/atualizado pelo bot
│   ├── banner.png             → Versão estática (fallback / redes sociais)
│   ├── avatar.jpg             → Foto usada no banner e na prévia
│   ├── pacman-contribution-graph.svg       → Gráfico Pac-Man (tema claro)
│   └── pacman-contribution-graph-dark.svg  → Gráfico Pac-Man (tema escuro)
├── README.md                  → README do perfil (já personalizado)
├── preview.html               → Prévia local (abra no navegador)
└── COMO-USAR.md               → Este guia
```

## 1. Publicar no GitHub

O GitHub só exibe um README no perfil se o repositório tiver **exatamente o mesmo nome
do usuário**. Para você: repositório **`AlyssonCx4`**.

1. Crie um repositório **público** chamado `AlyssonCx4`.
2. Envie todos os arquivos deste projeto para a branch `main`:
   - `.github/` (para ativar o GitHub Actions)
   - `assets/`
   - `scripts/`
   - `output/`
   - `README.md`
3. **Ative a permissão de escrita para o GitHub Actions**:
   - No repositório no GitHub, acesse **Settings** → **Actions** → **General**.
   - Em **Workflow permissions**, selecione **Read and write permissions** e clique em **Save**.
   - Isso permite que o workflow faça commit automático dos gráficos e banners atualizados.
4. (Opcional) **Secret para commits privados**:
   - Por padrão, o GitHub Actions conta suas contribuições públicas. Se quiser incluir contribuições de repositórios privados, gere um Personal Access Token (classic) com o escopo `read:user` e adicione em **Settings** → **Secrets and variables** → **Actions** com o nome `PROFILE_STATS_TOKEN`.
5. Abra `https://github.com/AlyssonCx4` — o README aparece na aba **Overview** e as ações rodarão a cada 6 horas automaticamente!

## 2. Dados já preenchidos

| Campo | Valor usado |
| :--- | :--- |
| Nome | Alysson Morais |
| Usuário | `AlyssonCx4` |
| Local | Caxias–MA · Brasil |
| E-mail | `allisoncx4@gmail.com` |
| LinkedIn | `linkedin.com/in/alysson-morais-20038436b` |
| Status | Disponível para projetos |
| Atualização do banner | `2026-11-10` |

Para mudar qualquer texto, edite direto:

- **Banner:** `output/banner.svg` (procure pelo texto, ex.: `Caxias–MA`)
- **README:** `README.md`
- **Prévia:** `preview.html`

O LinkedIn já está ativo no README, no painel de links do banner e na prévia.

## 3. Pré-visualizar

- **Banner sozinho:** abra `output/banner.svg` ou `output/banner.png` no navegador.
- **README completo:** abra `preview.html` no navegador.
  - O botão **tema claro / escuro** simula os dois temas do GitHub.
  - Os cards de estatística aparecem como placeholder porque dependem do seu usuário real.

Também é possível visualizar no próprio GitHub: crie um branch, suba os arquivos e abra o
README antes de mergear.

## 4. Trocar a foto

A foto fica **embutida no SVG em base64** (o GitHub bloqueia imagens externas dentro de SVG
carregado como `<img>`, então não dá para usar `<image href="avatar.jpg">`).

A foto já está aplicada (`output/avatar.jpg`). Para trocar por outra, rode na pasta do projeto:

```bash
convert sua-foto.jpg -resize 460x460^ -gravity center -extent 460x460 output/avatar.jpg
python3 - <<'PY'
import base64, re
from pathlib import Path

b64 = base64.b64encode(Path('output/avatar.jpg').read_bytes()).decode()
svg = Path('output/banner.svg').read_text()
svg = re.sub(r'href="data:image/jpeg;base64,[^"]+"',
             f'href="data:image/jpeg;base64,{b64}"', svg, count=1)
Path('output/banner.svg').write_text(svg)
PY
rsvg-convert -w 1200 -h 660 output/banner.svg -o output/banner.png
```

O enquadramento é `xMidYMid slice` (centralizado). Se o rosto ficar cortado, ajuste o
`preserveAspectRatio` do bloco `<!-- avatar -->`.

## 5. Personalizar o visual

Cores principais do banner:

| Uso | Cor |
| :--- | :--- |
| Fundo | `#0B0F14` → `#131A22` |
| Azul (front / destaque) | `#58A6FF` |
| Roxo (IA / automação) | `#BC8CFF` |
| Verde (status / back-end) | `#3FB950` / `#7EE787` |
| Ciano (dados) | `#56D4DD` |
| Texto | `#E6EDF3` / `#C9D1D9` |
| Texto suave | `#8B949E` / `#6E7681` |

Detalhes:

- **Animações** (cursor piscando, status pulsando, fluxo entre os nós) usam SVG/SMIL e
  funcionam dentro de `<img>` no GitHub. Para desligar, remova as tags `<animate>`.
- **Fontes** usam a pilha monoespaçada do sistema (`ui-monospace`, `SFMono-Regular`,
  `Consolas`…), então não precisa instalar nada.

## 6. Observações

- O GitHub faz **cache das imagens**. Se alterar o SVG e não ver mudança, espere alguns
  minutos ou acrescente `?v=2` no `src` do README.
- Os cards de estatística usam serviços públicos:
  - `github-readme-stats.vercel.app`
  - `github-readme-activity-graph.vercel.app`
  - `img.shields.io`

  Se algum ficar fora do ar, o README continua funcionando — só o card não carrega.
- `banner.png` serve como fallback para lugares que não renderizam SVG.
- O perfil tem **0 repositórios públicos** hoje; por isso o README fala em projetos
  “em breve”. Quando publicar os primeiros, vale fixá-los no perfil.

## Checklist final

- [x] Dados pessoais substituídos
- [x] Foto aplicada
- [x] LinkedIn ativo
- [x] Banner com foto, nome, usuário e cidade
- [x] README com o stack nas 4 áreas
- [ ] Criar o repositório público `AlyssonCx4`
- [ ] Enviar `README.md` + pasta `output/`
- [ ] Prévia conferida em tema claro e escuro
