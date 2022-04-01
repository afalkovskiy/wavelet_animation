# plot animated rotation of Ricker wavelet, AF, Apr 2022
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import hilbert, chirp
import math

pi = math.pi

def ricker(f, length=0.512, dt=0.001):
    t = np.linspace(-length/2, (length-dt)/2, length/dt)
    y = (1.-2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    return t, y

fig, ax = plt.subplots()

f = 25
inc = 1
flag = 0
t, y = ricker (f)
z= hilbert(y) #form the analytical signal
inst_amplitude = np.abs(z) #envelope extraction
plt.plot(t, inst_amplitude, color='orange', alpha=0.7, label="envelope")
plt.plot(t, -1*inst_amplitude, color='orange', alpha=0.7)

line, = ax.plot(t, y, label="wavelet")

txt1 = 'Frequency ' + str(f) + 'Hz'
label = ax.text(0.2, 0.7, txt1, ha='right', va='top', fontsize=16)

def init():  # only required for blitting to give a clean slate.
    line.set_ydata([np.nan] * len(t))
    z= hilbert(y) #form the analytical signal
    inst_amplitude = np.abs(z) #envelope extraction
    plt.plot(t, inst_amplitude, color='orange', alpha=0.7, label="envelope")
    plt.plot(t, -1*inst_amplitude, color='orange', alpha=0.7)
    txt1 = ''
    label.set_text(txt1)
    return line, label

def animate(i):
    global f
    global inc
    global flag

    x1, y1 = ricker(f)
    z= hilbert(y1) #form the analytical signal
    phase_deg = i*10%360
    phase = phase_deg * pi/180
    y_rot = math.cos(phase)*z.real - math.sin(phase)*z.imag
    y1 = 0 * y_rot
    ax.fill_between(t, y1, y_rot, where=y_rot >= y1,
                    facecolor='lightblue', interpolate=True)

    line.set_xdata(x1)
    line.set_ydata(y_rot)

    txt1 = 'Phase ' + str(round(phase_deg, 1)) + u'\N{DEGREE SIGN}'
    label.set_text(txt1)

    return line, label

ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=100, blit=False, save_count=36)

plt.title('Ricker wavelet ' + str(f) + 'Hz: phase rotation')
plt.xlabel('time (s)')
plt.ylabel('amplitude')
plt.xlim((-0.21, 0.21))
plt.ylim(-1.1, 1.1)

plt.grid()
plt.legend()

# writergif = animation.PillowWriter(fps=6)
# ani.save('Ricker_Phase_anim3.gif', writer=writergif)

plt.show()
