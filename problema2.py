
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


x = sp.symbols('x', positive=True)


C = 1500*x + 3000*sp.sqrt(16 + (6 - x)**2)


dC = sp.diff(C, x)
print("C'(x) =", dC)


criticos = sp.solve(dC, x)
x_opt = criticos[0]
print("Distancia óptima por tierra x =", round(float(x_opt), 4), "km")


dist_agua = sp.sqrt(16 + (6 - x_opt)**2)
print("Distancia bajo el agua =", round(float(dist_agua), 4), "km")


costo_min = C.subs(x, x_opt)
print("Costo mínimo =", round(float(costo_min), 2), "dólares")


print("Costo en x=0:", round(float(C.subs(x, 0)), 2))
print("Costo en x=6:", round(float(C.subs(x, 6)), 2))


d2C = sp.diff(dC, x)
print("C''(x_opt) =", round(float(d2C.subs(x, x_opt)), 4), "→ es mínimo si > 0")

# esta seccion es la grafica del problema
x_vals = np.linspace(0, 6, 300)
C_func = sp.lambdify(x, C, 'numpy')
C_vals = C_func(x_vals)

plt.figure(figsize=(8, 5))
plt.plot(x_vals, C_vals, color='steelblue', linewidth=2, label='C(x)')
plt.scatter([float(x_opt)], [float(costo_min)],
            color='red', zorder=5, s=100, label=f'Óptimo: x={float(x_opt):.2f} km')
plt.title('Problema 2 — Costo del tendido de cable')
plt.xlabel('Distancia por tierra x (km)')
plt.ylabel('Costo C(x) (dólares)')
plt.legend()
plt.grid(True)
plt.show()