# BlockSmith — Learning to Build in Minecraft with scikit-learn

An end-to-end, portfolio-ready project where a Python agent connects to a local Minecraft server and **learns** (via behavior cloning) to place blocks and assemble basic structures (walls, pillars, hollow cubes).

- **Game I/O:** Spigot server + RaspberryJuice plugin + `mcpi` Python API
- **Learning:** `scikit-learn` `MLPClassifier` trained on synthetic demonstrations of target shapes
- **Deploy:** Run the learned policy to build in-game near the player

---

## Demo (TL;DR)

```bash
# 0) Start your Spigot 1.12.x server with RaspberryJuice plugin (see Setup)
# 1) Install deps
python -m venv .venv && source .venv/bin/activate   # use .venv\Scripts\activate on Windows
pip install -r requirements.txt

# 2) Train the model (saves blocksmith_mlp.joblib)
python -m blocksmith.train

# 3) Launch Minecraft (Java), join your local Spigot world (player should be in-world)
# 4) Deploy the learned policy (watch it build near you)
python -m blocksmith.deploy
```

---

## Setup (Minecraft I/O)

1. **Install Spigot 1.12.x** and create a server folder.
2. **Install RaspberryJuice**: Place the plugin `.jar` in the server's `plugins/` directory.
3. Start the server once; RaspberryJuice opens a socket on `localhost:4711` by default.
4. In your Python environment: `pip install mcpi` (it’s listed in `requirements.txt`).

> *Note:* RaspberryJuice targets the classic mcpi API and remains a simple, reliable way to drive single-player style builds from Python for portfolio projects.

---

## Project Structure

```
blocksmith/
  README.md
  LICENSE
  .gitignore
  requirements.txt
  pyproject.toml
  Makefile
  blocksmith/
    __init__.py
    io_minecraft.py
    blueprints.py
    dataset.py
    train.py
    policy.py
    deploy.py
  notebooks/
    README.md
```

---

## How it works

- **Blueprints** define target shapes on a 16×16 grid layer (e.g., perimeter wall, hollow cube, pillar).
- **Dataset** generator simulates an “expert” that fills target cells in a simple order, producing supervision pairs:  
  **state** = concat(`current_grid`, `target_grid`) → 512 features; **action** = next cell index (0..255).
- **Training** uses `MLPClassifier` to predict next-cell actions (masked during inference to valid cells).
- **Deploy** translates chosen cells to `(x, y, z)` offsets next to your player and places blocks via `mcpi`.

---

## Commands

```bash
# Train and save model
make train

# Run the policy to build near your player
make deploy

# Clean artifacts
make clean
```

---

## Extending

- Add new shapes in `blocksmith/blueprints.py`.
- Scale to 3D layers: add a height dimension and train on (layered) targets.
- Track metrics: success rate, time-to-completion, block accuracy.
- Record a short demo video for your README/GitHub profile.

---

## License

This project is released under the MIT License (see `LICENSE`).

---

## Acknowledgements / Related
- Minecraft Pi (mcpi) API and RaspberryJuice for Python control of Java Edition servers.
- scikit-learn for the MLP implementation.
- Inspiration from behavior cloning baselines in game environments.
