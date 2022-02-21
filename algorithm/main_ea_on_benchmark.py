from functools import partial

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation

from ea_on_benchmark import run_evolution, generate_population, fitness
from benchmark_functions import rosenbrock, rastrigin
import sys

# Fixing random state for reproducibility
np.random.seed(42)

# read the bench function from user
bench_name = "rosenbrock"
if len(sys.argv) == 2:
    bench_name = sys.argv[1]

if bench_name == "rosenbrock":
    # set initial limits
    x_min, x_max = -2.5, 2.5
    y_min, y_max = -1, 3
    z_min, z_max = 0, 2500
    bench = lambda x, y: rosenbrock(x, y, a=0, b=50)
    title = "Rosenbrock"

elif bench_name == "rastrigin":
    # set initial limits
    x_min, x_max = -5, 5
    y_min, y_max = -5, 5
    z_min, z_max = 0, 100
    bench = rastrigin
    title = "Rastrigin"
else:
    print("Only 'rosenbrock' and 'rastigrin' are allowed.")
    quit()

# create ranges of x and y
x = np.arange(x_min, x_max, 0.1)
y = np.arange(y_min, y_max, 0.1)
x, y = np.meshgrid(x, y)

# load the landscape
z = bench(x, y)

# Attaching 3D axis to the figure
fig = plt.figure(figsize=(8, 8))
# FIXME: change title if different function is used
fig.suptitle(f"{title} Benchmark")

# plot the 2d plane
# ax2d = fig.add_subplot(1, 2, 1)
# ax2d.imshow(z, cmap=cm.coolwarm, origin='lower')

# plot the 3d plane
ax3d = fig.add_subplot(1, 1, 1, projection='3d')
ax3d.set_xlim3d(x_min, x_max)
ax3d.set_ylim3d(y_min, y_max)
ax3d.set_zlim3d(z_min, z_max)
ax3d.view_init(elev=90, azim=0)

# plot the fitness function
surf = ax3d.plot_surface(x, y, z, cmap=cm.coolwarm, alpha=0.3, linewidth=0, antialiased=False)

fig.colorbar(surf, shrink=0.5, aspect=5)

fitness_limit = bench(0, 0)

population, generations, history = run_evolution(
    populate_func=partial(
        generate_population, size=15, rand_range=x_max
    ),
    fitness_func=partial(
        fitness, benchmark_func=rosenbrock
    ),
    fitness_limit=fitness_limit,
    generation_limit=1000,
)
print(population)
history.reverse()
history = history[int(len(history) / 2):]

# for i, genome in enumerate(population):
#     x_pos, y_pos = genome
#     if not (x_pos < x_min or x_pos > x_max):
#         if not (y_pos < y_min or y_pos > y_max):
#             ax3d.scatter3D(x_pos, y_pos, zorder=2)


def update(frame_number):
    if frame_number >= len(history):
        return
    ax3d.clear()

    # ax3d.plot_surface(x, y, z, cmap=cm.coolwarm, alpha=0.3, linewidth=0, antialiased=False)

    for j, genome in enumerate(history[frame_number]):
        x_pos, y_pos = genome
        if not (x_pos < x_min or x_pos > x_max):
            if not (y_pos < y_min or y_pos > y_max):
                ax3d.scatter3D(x_pos, y_pos, zorder=2)

    ax3d.plot_surface(x, y, z, cmap=cm.coolwarm, alpha=0.3, linewidth=0, antialiased=False)


# show the animation and run the simulation using swarm.update
animation = FuncAnimation(fig, update, interval=1)
plt.show()
