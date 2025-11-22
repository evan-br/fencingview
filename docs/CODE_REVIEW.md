# FencingView 0.0.1 - Revisão Completa do Código

**Data**: 21 de Novembro de 2025  
**Objetivo**: Preparar a biblioteca para lançamento no PyPI  
**Versão alvo**: 0.0.1

---

## 📋 Resumo Executivo

O projeto está **estruturalmente sólido** para uma versão 0.0.1, mas apresenta **problemas críticos** que devem ser corrigidos antes do lançamento no PyPI:

- ✅ Arquitetura bem-definida (3 camadas claras)
- ✅ Padrão Generator implementado corretamente
- ✅ Tratamento básico de erros presente
- ⚠️ **CRÍTICO**: Metadata do PyPI incompleta/placeholder
- ⚠️ **CRÍTICO**: README.md vazio (obrigatório para PyPI)
- ⚠️ **CRÍTICO**: Docstrings insuficientes para classes principais
- ⚠️ **CRÍTICO**: Imports não exportados no `__init__.py`
- ⚠️ **IMPORTANTE**: Logging inadequado (apenas `print()`)
- ⚠️ **IMPORTANTE**: Tratamento de erros fragmentado
- ⚠️ **IMPORTANTE**: Falta validação de entrada em funções

---

## 🔴 Problemas Críticos

### 1. **pyproject.toml - Metadata do PyPI Incompleta**

**Localização**: `pyproject.toml`

**Problemas identificados**:
```toml
authors = [
  { name = "Seu Nome", email = "seu.email@exemplo.com" },  # ❌ Placeholder!
]

[project.urls]
"Homepage" = "https://github.com/seu-usuario/fencingview"  # ❌ Placeholder!
```

**Por que é problema**:
- PyPI rejeita pacotes com autor/email placeholder
- Falta de links importantes (Documentation, Repository, Bug Tracker)
- Falta de license e keywords para descoberta

**Recomendação**:
```toml
authors = [
  { name = "Seu Nome Real", email = "seu.email.real@dominio.com" },
]

[project.urls]
Homepage = "https://github.com/seu-usuario/fencingview"
Documentation = "https://fencingview.readthedocs.io"
Repository = "https://github.com/seu-usuario/fencingview"
"Bug Tracker" = "https://github.com/seu-usuario/fencingview/issues"

[project]
keywords = ["computer-vision", "fencing", "epee", "yolo", "mediapipe", "pose-estimation"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering :: Image Recognition",
]
```

---

### 2. **README.md - Vazio (Obrigatório)**

**Localização**: `README.md`

**Problema**: Arquivo completamente vazio. PyPI exige README com:
- Descrição do projeto
- Installation instructions
- Quick start example
- Features
- Requirements
- License

**Recomendação**: Ver seção "README Proposto" abaixo.

---

### 3. **Docstrings Insuficientes nos Módulos Core**

**Localização**: `src/fencingview/epee/`

**Problemas**:

#### `vision.py` - FencingVision
```python
class FencingVision:
    """
    Responsável exclusivamente por extrair dados brutos do frame:  # ❌ Falta docstring método __init__
    - Detectar pessoas (YOLO)
    - Extrair esqueleto/pose (MediaPipe)
    """
    def __init__(self, yolo_model_path="yolov8n.pt", conf_threshold=0.8):
        # ❌ Falta docstring! O que cada parâmetro faz?
```

#### `scouting.py` - ActionClassifier
```python
@staticmethod
def classify_pose(landmarks, bbox_height, baseline_height=None):
    # ❌ Sem docstring
    # ❌ 'landmarks' pode ser vazio? Como é o formato?
    # ❌ Qual é o tipo de retorno esperado?
```

#### `match.py` - EpeeMatch
```python
def analyze(self, show_preview=True):
    """
    Generator que processa o video frame a frame.  # ✓ Docstring OK mas poderia ser mais completa
    Yields (retorna) dados a cada frame para quem chamar.
    """
    # ❌ Falta exemplo de uso no docstring
    # ❌ Falta descrição de yields
    # ❌ Falta quais exceções podem ser levantadas
```

---

### 4. **__init__.py - Imports Não Exportados**

**Localização**: `src/fencingview/__init__.py`

**Problema atual**:
```python
# Arquivo vazio!
```

**Por que é problema**:
- Usuários precisam saber o que importar
- API não é clara
- Dificulta descoberta de recursos

**Recomendação**:
```python
"""FencingView: Computer Vision library for Fencing (Epee) Analysis"""

__version__ = "0.0.1"
__author__ = "Evandro Rissatto Pereira"
__email__ = "erissatto@gmail.com"

from .epee.match import EpeeMatch
from .epee.vision import FencingVision
from .common.geometry import calculate_distance, calculate_angle

__all__ = [
    "EpeeMatch",
    "FencingVision",
    "calculate_distance",
    "calculate_angle",
]
```

---

## 🟡 Problemas Importantes (Não-bloqueadores, mas prioritários)

### 5. **Logging Inadequado - Apenas `print()`**

**Problema**: Todo o código usa `print()` em vez de logging module

**Localização**:
- `vision.py:14`: `print(f"[FencingView] Carregando modelos...")`
- `match.py:28`: `print(f"[FencingView] Iniciando análise de: ...")`
- `test_script.py`: múltiplos `print()`

**Por que é problema**:
- Impossível controlar nível de logging (debug, info, warning, error)
- Não produz logs estruturados para produção
- Difícil desabilitar logs verbosos
- Impossível redirecionar para arquivo

**Recomendação**:
```python
import logging

logger = logging.getLogger(__name__)

# Em vision.py:
logger.info(f"Loading YOLO model from {yolo_model_path}")

# Em match.py:
logger.info(f"Starting analysis of video: {self.video_path}")
```

---

### 6. **Tratamento de Erros Fragmentado**

**Problema**: Apenas 2 `try/except` em todo o código

**Localização**:
- `vision.py:15-17`: Apenas carregamento de YOLO
- `match.py:23-26`: Apenas abertura de arquivo
- ❌ FALTA: Validação de frame vazio, landmarks corrompidos, etc.

**Cenários não tratados**:
```python
# vision.py - process_frame() - E SE:
- frame for None?
- frame tiver dimensões inválidas?
- MediaPipe falhar no processamento?
- YOLO retornar resultado vazio?

# match.py - analyze() - E SE:
- Video stream for interrompido mid-frame?
- FencingVision lançar exceção?
- Baseline height ficar inválido (negativo)?
```

**Recomendação**: Adicionar validações e tratamento apropriado.

---

### 7. **Falta de Validação de Entrada**

**Problema**: Nenhuma função valida seus inputs

**Exemplos**:
```python
# vision.py - process_frame(self, frame)
# ❌ Não valida se frame é None
# ❌ Não valida se frame tem shape válida
# ❌ Não valida conf_threshold (deve ser 0.0 a 1.0)

# scouting.py - update(self, center_x)
# ❌ Não valida se center_x é número válido
# ❌ Não valida se center_x é negativo

# match.py - __init__(self, video_path, config=None)
# ❌ Não valida se video_path existe antes de criar objeto
# ❌ Não valida config dict
```

---

### 8. **ActionClassifier - Implementação Incompleta**

**Localização**: `src/fencingview/epee/scouting.py:31-46`

**Problema**:
```python
@staticmethod
def classify_pose(landmarks, bbox_height, baseline_height=None):
    if not landmarks:
        return "desconhecido"
    
    # Aqui só tem:
    # - Comentários
    # - Placeholder para lógica
    # - Lógica SIMPLES só com altura do bbox
    
    if baseline_height and bbox_height < baseline_height * 0.88:
        return "afundo"
    
    return "en garde"  # Default
```

**Por que é problema**:
- Classificação de pose é muito simplista (apenas altura)
- Usa `calculate_angle` mas nunca chama a função
- Docstring diz "usar `geometry.py` angle calculations" mas não faz
- Landmarks passados não são usados
- Pode haver falsos positivos (ex: player se movimentando horizontalmente)

**Nota**: Isso é ESPERADO para v0.0.1, mas deve ser documentado como TODO explícito.

---

### 9. **Falta de Type Hints**

**Problema**: Zero type hints em todo o código

**Atual**:
```python
def process_frame(self, frame):  # ❌ frame é o quê? Retorna o quê?
    return players_data

def update(self, center_x):  # ❌ center_x é int? float? Retorna nada?
    self.history.append(center_x)
```

**Recomendação** (para v0.1.0 ou v0.0.2):
```python
def process_frame(self, frame: np.ndarray) -> list[dict]:
    """Extract players from frame."""
    
def update(self, center_x: float) -> None:
    """Update movement history."""
```

---

### 10. **Falta LICENSE**

**Problema**: Nenhum arquivo LICENSE no projeto

**Por que é problema**:
- Obrigatório para publicar no PyPI (classifiers exigem isso)
- Usuários não sabem permissões de uso

**Recomendação**: Criar `LICENSE` file (MIT, Apache 2.0, ou escolher outra)

---

## 🟢 Problemas Menores

### 11. **test_script.py - Hardcoded Video Path**
```python
VIDEO = "epee1.mp4"  # ❌ Deve aceitar argumento de CLI
```

### 12. **Comentários em Português + Código em Inglês**
Mistura de idiomas prejudica legibilidade para colaboradores internacionais.

### 13. **Falta de .gitignore**
```python
# Deve incluir:
*.pt (YOLO models)
__pycache__/
*.egg-info/
*.pyc
.venv/
```

### 14. **Falta de MANIFEST.in**
Para incluir arquivos não-Python no pacote.

---

## ✅ Checklist de Ações Necessárias Antes do PyPI

### **CRÍTICA - BLOQUEIA PUBLICAÇÃO**
- [ ] Atualizar `pyproject.toml` com metadata real
- [ ] Criar `README.md` com documentação completa
- [ ] Adicionar docstrings a todas as classes e métodos públicos
- [ ] Implementar `__init__.py` com `__all__` e versão
- [ ] Criar arquivo `LICENSE`

### **IMPORTANTE - RECOMENDADO**
- [ ] Implementar logging module (em vez de print)
- [ ] Adicionar validação de entrada em funções críticas
- [ ] Melhorar tratamento de exceções
- [ ] Marcar `ActionClassifier.classify_pose()` como TODO/WIP explicitamente
- [ ] Criar `.gitignore`

### **OPCIONAL - MELHORIAS FUTURAS**
- [ ] Adicionar type hints (v0.1.0)
- [ ] Criar `MANIFEST.in`
- [ ] Adicionar tests unitários (`pytest`)
- [ ] Melhorar estrutura de configuração (config.yaml)
- [ ] Adicionar exemplo de notebook Jupyter

---

## 📄 README Proposto

```markdown
# FencingView 🤺

Computer Vision library for analyzing **epee fencing matches** from video.

Combines YOLO person detection, MediaPipe pose estimation, and custom heuristics to extract:
- Player detection and tracking (left/right)
- Movement classification (advancing, retreating, stopped)
- Pose estimation (en garde, lunge)
- Keypoint landmarks (33 MediaPipe pose points)

## Features

- ⚡ **Real-time processing** via generator pattern
- 🎯 **Deterministic 2-player detection** (always left/right)
- 📊 **Frame-by-frame analysis** with absolute coordinates
- 🧠 **MediaPipe pose** extraction and transformation
- 🚀 **Modular architecture** (Vision → Scouting → Analysis)

## Requirements

- Python ≥ 3.9
- YOLO v8 model (`yolov8n.pt` included in releases)
- Video file (MP4, AVI, MOV, etc.)

## Installation

```bash
pip install fencingview
```

## Quick Start

```python
from fencingview import EpeeMatch

# Load and analyze video
match = EpeeMatch("path/to/epee_match.mp4")

# Process frame-by-frame
for frame_data in match.analyze(show_preview=True):
    players = frame_data["players"]
    
    if "A" in players and "B" in players:
        player_a = players["A"]
        print(f"Player A: {player_a['action']} - {player_a['movement']}")
        print(f"Keypoints: {len(player_a['keypoints'])} landmarks")
    
    # Press 'q' to exit
```

## Output Format

Each frame yields:
```python
{
    "frame_id": 42,
    "players": {
        "A": {
            "bbox": (x1, y1, x2, y2),                              # Bounding box
            "center": (cx, cy),                                    # Center point
        "action": "en garde" | "lunge",                          # Pose
            "movement": "advancing" | "retreating" | "stopped",      # Direction
            "keypoints": [(x1, y1), (x2, y2), ...],              # 33 landmarks
        },
        "B": { ... }  # Right player (same structure)
    }
}
```

## Architecture

- **Vision Layer** (`FencingVision`): YOLO detection + MediaPipe pose
- **Scouting Layer** (`MovementTracker`, `ActionClassifier`): Motion/action analysis
- **Match Layer** (`EpeeMatch`): Pipeline orchestration and frame generation

## Known Limitations (v0.0.1)

- ⚠️ Pose classification uses only bbox height (incomplete)
- ⚠️ Assumes exactly 2 players in frame
- ⚠️ Horizontal movement tracking only (X-axis)
- ⚠️ No multi-person re-identification across frames

## API Reference

### EpeeMatch

```python
EpeeMatch(video_path, config=None)
```

**Parameters:**
- `video_path` (str): Path to video file
- `config` (dict, optional): Configuration dict
  - `yolo_path` (str): Path to YOLO model (default: "yolov8n.pt")

**Methods:**
- `analyze(show_preview=True)`: Generator yielding frame_data dicts

## Contributing

Contributions welcome! See issues for tasks.

## License

MIT License - See LICENSE file

## Citation

If you use FencingView in research, please cite:

```bibtex
@software{fencingview2025,
    title={FencingView: Computer Vision for Epee Fencing Analysis},
    author={Evandro Rissatto Pereira},
    year={2025},
    url={https://github.com/evan-br/fencingview}
}
```

## Roadmap

- [ ] v0.1.0: Type hints, improved pose classification
- [ ] v0.2.0: Multi-video batch processing
- [ ] v0.3.0: Action classification (attacks, defenses)
- [ ] v1.0.0: Production-ready stability

```

---

## 📊 Relatório Final

| Categoria | Status | Severidade |
|-----------|--------|-----------|
| Arquitetura | ✅ Sólida | - |
| Code Quality | ⚠️ Básica | Média |
| Documentation | ❌ Criticamente incompleta | **CRÍTICA** |
| Error Handling | ⚠️ Fragmentado | Importante |
| Logging | ❌ Inadequado (apenas print) | Importante |
| PyPI Metadata | ❌ Placeholder | **CRÍTICA** |
| Type Safety | ❌ Falta type hints | Baixa |

**Veredito**: Pode ser publicado se os problemas **CRÍTICOS** forem resolvidos.

---

## 🚀 Próximas Ações Recomendadas

1. ✏️ Atualizar `pyproject.toml` com metadata real
2. 📝 Criar `README.md` usando template proposto
3. 🔧 Implementar logging module
4. ✅ Adicionar docstrings PEP 257
5. 📦 Criar `LICENSE` file
6. 🧪 Testar local: `pip install -e .`
7. ✔️ Verificar com `twine check`
8. 🌐 Publicar no TestPyPI primeiro
9. 📦 Depois publicar no PyPI oficial

---

**Nota**: Esta revisão baseada em boas práticas PyPI e PEP standards (8, 257, 440).
