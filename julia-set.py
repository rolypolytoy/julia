#Sorry for the lack of documentation!
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.widgets import Slider
import tkinter as tk
from numba import jit

plt.switch_backend('TkAgg')

@jit(nopython=True)
def julia_calculation(z_real, z_imag, c_real, c_imag, max_iter):
    output = np.zeros_like(z_real, dtype=np.int32)
    for i in range(z_real.shape[0]):
        for j in range(z_real.shape[1]):
            zr = z_real[i, j]
            zi = z_imag[i, j]
            for n in range(max_iter):
                zr2 = zr * zr
                zi2 = zi * zi
                if zr2 + zi2 > 4.0:
                    output[i, j] = n
                    break
                zi = 2 * zr * zi + c_imag
                zr = zr2 - zi2 + c_real
            else:
                output[i, j] = max_iter
    return output

def compute_julia(h, w, c_real, c_imag, max_iter):
    y = np.linspace(-1.5, 1.5, h)
    x = np.linspace(-1.5, 1.5, w)
    z_real, z_imag = np.meshgrid(x, y)
    return julia_calculation(z_real, z_imag, c_real, c_imag, max_iter)

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

fig_width = screen_width/100
fig_height = screen_height/100

h = int(min(600, min(screen_height, screen_width)))
w = int(min(600, min(screen_height, screen_width)))
c_real_init = -0.7
c_imag_init = 0.27
max_iter = 50

fig = plt.figure(figsize=(fig_width, fig_height))
fig.patch.set_facecolor('black')

ax = fig.add_subplot(111)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0.1)

colors = [(0, 0, 0), (0, 0, 0.5), (0, 0, 1), (0, 0.5, 1),
          (0, 1, 1), (0.5, 1, 0.5), (1, 1, 0), (1, 0.5, 0), (1, 0, 0)]
cmap = LinearSegmentedColormap.from_list('julia', colors, N=max_iter)

julia = compute_julia(h, w, c_real_init, c_imag_init, max_iter)
img = ax.imshow(julia, cmap=cmap, extent=[-1.5, 1.5, -1.5, 1.5],
                interpolation='nearest', aspect='equal')
plt.axis('off')

slider_width = 0.4
slider_height = 0.03
slider_x = 0.5 - slider_width/2
slider_y1 = 0.05
slider_y2 = 0.01

ax_c_real = plt.axes([slider_x, slider_y1, slider_width, slider_height])
ax_c_imag = plt.axes([slider_x, slider_y2, slider_width, slider_height])

ax_c_real.set_facecolor('lightgray')
ax_c_imag.set_facecolor('lightgray')

slider_c_real = Slider(ax_c_real, 'Real', -2.0, 1.0, valinit=c_real_init, color='darkblue')
slider_c_imag = Slider(ax_c_imag, 'Imaginary', -1.0, 1.0, valinit=c_imag_init, color='darkred')

for slider in [slider_c_real, slider_c_imag]:
    slider.label.set_color('white')
    slider.valtext.set_color('white')
    slider.track.set_color('gray')

def update(val):
    c_real = slider_c_real.val
    c_imag = slider_c_imag.val
    
    julia = compute_julia(h, w, c_real, c_imag, max_iter)
    img.set_data(julia)
    fig.canvas.draw_idle()

slider_c_real.on_changed(update)
slider_c_imag.on_changed(update)

def maximize_window():
    manager = plt.get_current_fig_manager()
    if hasattr(manager, 'window'):
        if hasattr(manager.window, 'showMaximized'):
            manager.window.showMaximized()
        elif hasattr(manager.window, 'maximize'):
            manager.window.maximize()
    elif hasattr(manager, 'resize'):
        if hasattr(manager.window, 'maxsize'):
            manager.resize(*manager.window.maxsize())

maximize_window()
plt.show()
