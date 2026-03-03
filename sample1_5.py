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
"""ここから上はsample1_2"""

offset_hat_y = [-0.8, -0.8, 0.6, 0.6]

def plot_line(ax, a, b, label=None, color='black', alpha=1.):#ラインを引く関数
    if label is None:
        label = f'$y = {a}x + {b}$' if a != 1 else f'$y = x + {b}$'#ラベルをつけてる。みてのとおり
    x = np.array([xmin, xmax]) #直線を引くためのX座標を準備。直線を描くには「両端の2点」だけあれば十分
    return ax.plot(x, a * x + b, color, ls='-', label=label, alpha=alpha)

def plot_hat_y(ax, D, a, b, offset_hat_y, marker='*', show_text=True): #予測値（直線上の点）を打つ関数
    A = []
    for i, row in enumerate(D):
        x = D[i,0]
        hat_y = a * x + b
        A.append(ax.scatter(x, hat_y, marker=marker, color=colormap[i]))
        if show_text:
            A.append(ax.text(x, hat_y + offset_hat_y[i], f'$(x_{i+1}, \\hat{{y}}_{i+1})$', ha='center'))
    return A

fig, ax = init_graph()
plot_data(ax, D, offset_y)
plot_line(ax, 1, 1)
plot_hat_y(ax, D, 1, 1, offset_hat_y)
plt.legend(loc='upper left')
plt.show()

offset_epsilon = [-0.3, -0.3, 0.3, 0.3]

def plot_error(plt, ax, D, a, b, offset_epsilon=None):
    A = []
    for i, row in enumerate(D):
        x, y = row
        y_hat = a * x + b
        ymin = min(y, y_hat)
        ymax = max(y, y_hat)
        A.append(plt.vlines([x], ymin, ymax, linestyles='dashed', color=colormap[i], alpha=0.5))
        if offset_epsilon is not None:
            A.append(ax.text(x + offset_epsilon[i], (ymin + ymax) / 2, f'$\epsilon_{i+1}$', ha='center', va='center'))
    return A

fig, ax = init_graph()
plot_data(ax, D, offset_y)
plot_line(ax, 1, 1)
plot_hat_y(ax, D, 1, 1, offset_hat_y)
plot_error(plt, ax, D, 1, 1, offset_epsilon)
plt.legend(loc='upper left')
plt.show()

def generate_parameter(L = 1000, xwidth=10, ymin=0, ymax=10):
    A = np.random.rand(L)
    B = np.random.rand(L) * (ymax - ymin) + ymin
    for i, b in np.ndenumerate(B):
        amax = (ymax - b) / xwidth
        amin = (ymin - b) / xwidth
        A[i] = np.random.rand() * (amax - amin) + amin
    return np.column_stack((A, B))

K = 5
np.random.seed(seed=5)
P = generate_parameter(100)

fig, ax = init_graph(grid=False)
plot_data(ax, D)

best = (None, None, None, None)
artists = []
for i in range(len(P)+K):
    # Update the best parameter if necessary.
    if i < len(P):
        a, b = P[i][0], P[i][1]
        msr = ((D[:,1] - a * D[:,0] - b) ** 2).mean()
        if best[0] is None or msr < best[1]:
            best = (i, msr, a, b)

    artist = []
    msg_current = ''

    # Draw the current best line.
    artist += plot_line(ax, best[2], best[3], color='tab:red')
    msg_best = "(Current best: $a$ = {0[2]:.2f}, $b$ = {0[3]:.1f}: MSR = ${0[1]:.2f}$)".format(best)
    
    # Draw recent lines.
    for k in range(K):
        j = i-k
        if j < 0 or len(P) <= j:
            continue
        
        if j != best[0]:
            a, b = P[j][0], P[j][1]
            artist += plot_line(ax, a, b, color='black', alpha=1.0 / (k+1))
        
        if k == 0:
            artist += plot_hat_y(ax, D, a, b, offset_hat_y, show_text=False)
            artist += plot_error(plt, ax, D, a, b)        
            msg_current = f"$a$ = {a:.2f}, $b$ = {b:.1f}: MSR = ${msr:.2f}$"
            
    artist.append(ax.text(5, 0.6, msg_current + '\n' + msg_best, color='tab:red', ha='center'))
    artists.append(artist)

ani = matplotlib.animation.ArtistAnimation(fig, artists, interval=100, repeat=False)
html = ani.to_jshtml()
plt.close(fig)
HTML(html)

def msr(a, b, D):
    xm = np.mean(D[:,0])
    ym = np.mean(D[:,1])
    x2m = np.mean(D[:,0] ** 2)
    y2m = np.mean(D[:,1] ** 2)
    xym = np.mean(D[:,0] * D[:,1])
    return x2m * (a ** 2) + b ** 2 + 2 * xm * a * b - 2 * xym * a - 2 * ym * b + y2m

N = 1000
A, B = np.meshgrid(np.linspace(-10, 10, N), np.linspace(-10, 10, N))
J = msr(A, B, D)

fig, ax = plt.subplots(dpi=100)
ax.set_aspect('equal')
ax.set_xlabel('$a$')
ax.set_ylabel('$b$')

# Draw a heat map on a logarithmic scale of MSR.
mesh = ax.pcolormesh(A, B, J, norm=matplotlib.colors.LogNorm(vmin=J.min(), vmax=J.max()), shading='auto')
cbar = fig.colorbar(mesh)
cbar.set_label('$\hat{L}_{\mathcal{D}}(a,b)$')

# Draw a contour map (clip loss values not to draw lines in smaller area)
ax.contour(
    A, B, np.clip(J, 1e-3, None), vmin=1, colors='tab:red', linewidths=0.5, linestyles='dashed',
    norm=matplotlib.colors.LogNorm(vmin=J.min(), vmax=J.max()))

def draw_means(ax, D):
    xm = np.mean(D[:,0])
    ym = np.mean(D[:,1])
    plt.vlines([xm], xmin, xmax, "black", linestyles='dashed', label=r"$\bar{x}$")
    plt.hlines([ym], ymin, ymax, "black", linestyles='dotted', label=r"$\bar{y}$")
    
def draw_regions(ax, D):
    xm = np.mean(D[:,0])
    ym = np.mean(D[:,1])
    ax.add_patch(
         matplotlib.patches.Rectangle((0, 0), xm, ym, facecolor='red', alpha=0.1, fill=True))
    ax.add_patch(
         matplotlib.patches.Rectangle((xm, ym), 10-xm, 10-ym, facecolor='red', alpha=0.1, fill=True))
    ax.add_patch(
         matplotlib.patches.Rectangle((0, ym), xm, ym, facecolor='blue', alpha=0.1, fill=True))
    ax.add_patch(
         matplotlib.patches.Rectangle((xm, 0), 10-xm, ym, facecolor='blue', alpha=0.1, fill=True))

fig, ax = init_graph()
plot_data(ax, D)
draw_means(ax, D)
draw_regions(ax, D)
plt.legend(loc='upper left')
plt.show()
##あまりにもフロントエンドっぽいことが多いので　しっかりと数式から理解する方法に変える。フロントエンドを学ぶ意味はない。インデックスの意味さえ分かればよい