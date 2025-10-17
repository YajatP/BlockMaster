import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from blocksmith.blueprints import hollow_box_3d, grid2d_perimeter, to_3d_from_2d
from blocksmith.planner import plan_build
from blocksmith.actions import execute
from blocksmith.world import GridWorld, MCWorld
from blocksmith.io_minecraft import MCClient
from blocksmith.metrics import voxel_iou, precision_recall

st.set_page_config(page_title="BlockSmith Dashboard", layout="wide")
st.sidebar.title("BlockSmith v2")
mode = st.sidebar.selectbox("Mode", ["Dry (GridWorld)", "Real (Minecraft)"])
shape = st.sidebar.selectbox("Shape", ["hollow_box", "perimeter2d"])
w_dim = st.sidebar.slider("Width (w)", 2, 32, 8)
d_dim = st.sidebar.slider("Depth (d)", 2, 32, 8)
h_dim = st.sidebar.slider("Height (h)", 2, 32, 4)
reach = st.sidebar.slider("Reach (Manhattan)", 1, 6, 4)
block_id = st.sidebar.number_input("Block ID", min_value=1, max_value=155, value=1, step=1)

st.title("🧱 BlockSmith Dashboard")
st.caption("Plan, simulate, and (optionally) deploy builds to a running Minecraft world.")

def render_grid(ax, arr, title):
    proj = arr.max(axis=2).astype(int)
    ax.imshow(proj.T, origin="lower", interpolation="nearest")
    ax.set_title(title); ax.set_xticks([]); ax.set_yticks([])

col1, col2 = st.columns(2)

if shape == "hollow_box":
    target = hollow_box_3d(w_dim, d_dim, h_dim)
else:
    target = to_3d_from_2d(grid2d_perimeter(w_dim), 1)

origin = (2, 1, 2)

with col1:
    st.subheader("Target (projection)")
    fig, ax = plt.subplots()
    render_grid(ax, target, "Target")
    st.pyplot(fig)

plan = plan_build(origin, target, block_id=block_id)
st.info(f"Planned actions: {len(plan.actions)}")

run_dry = st.button("Plan & Simulate (Dry)")

if run_dry or mode.startswith("Dry"):
    world = GridWorld(w_dim + 20, d_dim + 20, max(h_dim + 5, 5), start=(1,1,1), floor_y=0)
    for x in range(world.w):
        for z in range(world.d):
            world.set_block(x, 0, z, 1)
    execute(world, agent_y=origin[1], actions=plan.actions, reach=reach)
    built = np.zeros_like(target)
    x0,y0,z0 = origin
    for x in range(w_dim):
        for z in range(d_dim):
            for y in range(h_dim):
                built[x, z, y] = 1 if world.get_block(x0+x, y0+y, z0+z) != 0 else 0
    iou = voxel_iou(target, built)
    p, r = precision_recall(target, built)

    with col2:
        st.subheader("Built (projection)")
        fig2, ax2 = plt.subplots()
        render_grid(ax2, built, f"Built • IoU={iou:.3f}, P={p:.3f}, R={r:.3f}")
        st.pyplot(fig2)

if mode.startswith("Real"):
    st.warning("Real mode requires a running Spigot server with RaspberryJuice and the player in-world.")
    if st.button("Deploy to Minecraft (Run)"):
        try:
            mc = MCClient()
            world = MCWorld(mc)
            execute(world, agent_y=origin[1], actions=plan.actions, reach=reach)
            st.success("Deployment commands sent to Minecraft.")
        except Exception as e:
            st.error(f"Failed to deploy: {e}")
