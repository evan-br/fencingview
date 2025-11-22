# FencingView - Próximas Etapas: Git, Build e PyPI

**Data**: 22 de Novembro de 2025  
**Versão alvo**: 0.0.1  
**Status**: Pronto para publicação

---

## 📋 Checklist Final Antes de Publicar

### Passo 0: Verificações Finais (2-3 min)

```bash
# 1. Verificar que está no diretório correto
cd c:\Users\User\Desktop\fencingview

# 2. Validar estrutura do projeto
python -c "from fencingview import EpeeMatch; print('✓ Import OK')"

# 3. Testar o demo
python examples/demo_analysis.py --no-preview --help

# 4. Verificar metadata
python -c "import fencingview; print(f'Version: {fencingview.__version__}'); print(f'Author: {fencingview.__author__}')"

# 5. Limpar builds anteriores
rmdir /s /q build & rmdir /s /q dist & for /d %i in (*.egg-info) do rmdir /s /q "%i" & for /d %i in (src\*.egg-info) do rmdir /s /q "%i"
```

---

## 🔧 Etapa 1: Preparar Repositório Git (5 min)

### 1.1 Inicializar Git (se ainda não estiver)
```bash
cd c:\Users\User\Desktop\fencingview

# Verificar se Git já está inicializado
git status

# Se não estiver, inicializar:
git init
git config user.name "Evandro Rissatto Pereira"
git config user.email "erissatto@gmail.com"
```

### 1.2 Adicionar Remoto (GitHub)
```bash
# Remover remoto antigo se existir
git remote remove origin

# Adicionar novo remoto
git remote add origin https://github.com/evan-br/fencingview.git

# Verificar
git remote -v
```

### 1.3 Criar .gitignore (já está pronto)
✅ Arquivo `.gitignore` já foi atualizado com:
- `*.pt` (modelos YOLO)
- `*.mp4`, `*.avi`, `*.mov` (vídeos)
- `dist/`, `build/`, `*.egg-info/` (builds)
- `.venv/`, `__pycache__/` (Python cache)

---

## 📦 Etapa 2: Fazer Commit e Push para GitHub (5-10 min)

### 2.1 Adicionar Todos os Arquivos
```bash
# Status atual
git status

# Adicionar arquivos (excluindo .gitignore)
git add .

# Verificar o que será commitado
git status
```

### 2.2 Fazer Commit
```bash
git commit -m "chore: organize project structure and prepare for PyPI v0.0.1

- Move docs to /docs/ directory with INDEX.md
- Move examples to /examples/ with demo_analysis.py
- Create STRUCTURE.md explaining project layout
- Translate PYPI_RELEASE_CHECKLIST.md to English
- Update .gitignore for large files
- All code reviewed and tested for PyPI release
- Ready for publication on PyPI"
```

### 2.3 Verificar Commits
```bash
git log --oneline -5
```

### 2.4 Push para GitHub (Primeira vez)
```bash
# Se for primeira vez, criar branch main
git branch -M main

# Push com novo branch
git push -u origin main

# Depois, simples push
git push
```

### 2.5 Verificar no GitHub
Abrir: https://github.com/evan-br/fencingview

---

## 🏗️ Etapa 3: Build do Pacote (2-3 min)

### 3.1 Limpar Builds Antigos
```bash
# PowerShell
rm -r build/ dist/ src/fencingview.egg-info/ -ErrorAction SilentlyContinue
```

### 3.2 Executar Build
```bash
python -m build

# Deve gerar:
# - dist/fencingview-0.0.1.tar.gz      (source distribution)
# - dist/fencingview-0.0.1-py3-none-any.whl  (wheel)
```

### 3.3 Validar Build
```bash
# Verificar conteúdo
python -m twine check dist/*

# Deve retornar: PASSED para ambos os arquivos
```

---

## ✅ Etapa 4: Publicar no PyPI (5-10 min)

### 4.1 Opção A: Com Token (RECOMENDADO)

#### Passo 1: Gerar Token no PyPI
1. Abrir: https://pypi.org/account/
2. Login com sua conta
3. Account settings → API tokens
4. Criar novo token com escopo: "Entire account"
5. Copiar o token (formato: `pypi-AgEI...`)

#### Passo 2: Configurar Credenciais
Criar arquivo `~/.pypirc`:

**Windows** (criar arquivo em `C:\Users\<seu-usuario>\.pypirc`):
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEI... (seu token aqui)

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-... (token de teste, se tiver)
```

#### Passo 3: Upload para PyPI
```bash
python -m twine upload dist/*

# Ou com autenticação inline (menos seguro):
python -m twine upload dist/* --username __token__ --password pypi-AgEI...
```

### 4.2 Opção B: TestPyPI Primeiro (RECOMENDADO PARA PRIMEIRA VEZ)

#### Passo 1: Publicar em TestPyPI
```bash
# Use testpypi do .pypirc configurado acima
python -m twine upload --repository testpypi dist/*
```

#### Passo 2: Testar Instalação
```bash
# Em um venv diferente:
python -m venv test_env
test_env\Scripts\activate
pip install -i https://test.pypi.org/simple/ fencingview==0.0.1
python -c "import fencingview; print(fencingview.__version__)"
```

#### Passo 3: Se Tudo OK, Publicar em PyPI Oficial
```bash
python -m twine upload dist/*
```

---

## 🚀 Etapa 5: Verificação Pós-Publicação (3-5 min)

### 5.1 Verificar no PyPI
Abrir: https://pypi.org/project/fencingview/

Verificar:
- ✅ Versão correta (0.0.1)
- ✅ Descrição e README renderizado
- ✅ Author correto (Evandro Rissatto Pereira)
- ✅ License (MIT)
- ✅ Links (GitHub, Documentation, etc)

### 5.2 Testar Instalação Global
```bash
# Em um novo venv
python -m venv test_install
test_install\Scripts\activate
pip install fencingview

# Testar
python -c "from fencingview import EpeeMatch; print('✓ Works!')"
```

### 5.3 Criar Release no GitHub
1. Abrir: https://github.com/evan-br/fencingview/releases
2. "Create a new release"
3. Tag: `v0.0.1`
4. Title: `FencingView v0.0.1 - Alpha Release`
5. Description:
```markdown
## v0.0.1 - Alpha Release

### Features
- YOLO v8 person detection
- MediaPipe 33-point pose estimation
- Movement tracking (advancing, retreating, stopped)
- Pose classification (en garde, lunge)
- Real-time frame-by-frame analysis

### Known Limitations
- Pose classification uses height-based heuristics
- No multi-person re-identification
- Horizontal movement tracking only

### Installation
```bash
pip install fencingview
```

### Usage
```python
from fencingview import EpeeMatch

match = EpeeMatch("video.mp4")
for frame_data in match.analyze(show_preview=True):
    print(frame_data["players"])
```

### Links
- [GitHub](https://github.com/evan-br/fencingview)
- [PyPI](https://pypi.org/project/fencingview)
- [Documentation](https://github.com/evan-br/fencingview/tree/main/docs)
- [Examples](https://github.com/evan-br/fencingview/tree/main/examples)
```

6. Publish release

---

## 📅 Timeline Estimado

| Etapa | Tempo | Status |
|-------|-------|--------|
| 0. Verificações finais | 2-3 min | 📋 |
| 1. Git setup | 5 min | 📋 |
| 2. Commit & Push | 5-10 min | 📋 |
| 3. Build | 2-3 min | 📋 |
| 4. Publicar (PyPI) | 5-10 min | 🚀 |
| 5. Verificação | 3-5 min | ✅ |
| **TOTAL** | **~30 min** | 🎉 |

---

## ⚠️ Troubleshooting

### Erro: "Repository URL not in .pypirc"
```bash
# Editar .pypirc manualmente ou usar inline:
python -m twine upload dist/* --repository pypi
```

### Erro: "Invalid authentication"
```bash
# Verificar token está correto no .pypirc
# Regenerar token se necessário
```

### Erro: "Package already exists"
- A versão 0.0.1 já existe no PyPI
- Incrementar versão em `pyproject.toml` para 0.0.2
- Fazer novo commit e rebuild

### Erro: "README rendering failed"
- Verificar README.md em https://readme.so/
- Checar formatação Markdown
- Adicionar `content-type: text/x-rst` se necessário

---

## 🎯 Comandos Rápidos (Copie e Cole)

### Tudo de uma vez (se tudo estiver OK):
```bash
cd c:\Users\User\Desktop\fencingview

# 1. Git
git add .
git commit -m "chore: prepare for PyPI v0.0.1"
git push

# 2. Build
rm -r build/ dist/ -ErrorAction SilentlyContinue
python -m build

# 3. Validar
python -m twine check dist/*

# 4. Publicar (após ter .pypirc configurado)
python -m twine upload dist/*
```

---

## ✨ Próximos Passos Após Publicação

1. **Criar Tags no GitHub**: `git tag v0.0.1 && git push --tags`
2. **Comunicar lançamento**: 
   - GitHub Discussions
   - Twitter/LinkedIn (opcional)
   - Comunidades Python
3. **Coletar feedback**: Issues e PRs
4. **Planejar v0.1.0**:
   - Type hints
   - Logging module
   - Unit tests

---

**Você está pronto para publicar! 🚀**

Próxima ação: Execute `git status` para ver o que será commitado.
