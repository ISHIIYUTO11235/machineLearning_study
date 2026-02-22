import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches
import matplotlib.colors
import matplotlib.animation
from IPython.display import HTML
import japanize_matplotlib

D = np.array([[1, 3], [3, 6], [6, 5], [8, 7]])

colormap = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange'] #データのプロttpの設定
offset_y = [0.5, 0.5, -0.5, -0.5]
xmin, xmax = 0, 10
ymin, ymax = 0, 10

def init_graph(dpi=100, grid=True):#グラフ初期化
    fig, ax = plt.subplots(dpi=dpi, figsize=(6, 6))
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    if grid:
        ax.grid()
    return fig, ax

def plot_data(ax, D, offset_y=None, marker='o'): #データをじっさいにプロットする
    A = []
    for i, row in enumerate(D):
        A.append(ax.scatter(D[i,0], D[i,1], marker=marker, color=colormap[i]))
        if offset_y is not None:
            A.append(ax.text(D[i,0], D[i,1] + offset_y[i], f'$(x_{i+1}, y_{i+1})$', ha='center'))
    return A

fig, ax = init_graph()
plot_data(ax, D, offset_y)
plt.show()
