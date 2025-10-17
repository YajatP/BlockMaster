# BlockSmith v2 — Hierarchical Builder + Dashboard + CI

**What’s inside**
- Movement & A* pathfinding, reachability-aware placement
- Hierarchical macros (hollow box) + micro actions
- 3D blueprints; metrics (IoU / Precision / Recall)
- CLI, tests (pytest), mypy, ruff, GitHub Actions, Docker
- **Streamlit Dashboard** for planning, simulating, and real deployment

---

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev,dash]'

# run checks
pytest -q
mypy blocksmith
ruff check .
```

### Run the dashboard
```bash
make dashboard
# or
streamlit run dashboard/app.py
```

### Deploy to real Minecraft
- Start Spigot 1.12.x with the RaspberryJuice plugin; join the world with the Minecraft client.
- Then in another terminal:
```bash
python -m blocksmith.deploy --real --shape hollow_box --w 8 --d 8 --h 4
```

### CLI examples
```bash
blocksmith plan --shape hollow_box --w 8 --d 8 --h 4
blocksmith simulate --shape hollow_box --w 8 --d 8 --h 4
```

---

## Repo Layout
```
blocksmith_v2_all/
  README.md
  LICENSE
  .gitignore
  pyproject.toml
  requirements.txt
  mypy.ini
  ruff.toml
  Makefile
  Dockerfile
  compose.yml
  .github/workflows/ci.yml
  blocksmith/
    __init__.py
    io_minecraft.py
    world.py
    nav.py
    actions.py
    planner.py
    blueprints.py
    metrics.py
    dataset.py
    policy.py
    train.py
    deploy.py
    cli.py
  dashboard/
    app.py
  tests/
    test_blueprints.py
    test_nav.py
    test_metrics.py
    test_actions.py
    test_policy_mask.py
```

---

## Notes
- Planner builds bottom-up for micro placements; hollow box uses macro edges for speed.
- Dashboard includes top-down projections and IoU/precision/recall on dry runs.
- Real mode requires mcpi + RaspberryJuice. Tests use a mock GridWorld; no Minecraft needed.
