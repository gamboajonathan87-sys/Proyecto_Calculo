
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


r = sp.symbols('r', positive=True)


C = 2 * sp.pi * r**2 + 710 / r


dC = sp.diff(C, r)
print("C'(r) =", dC)


criticos = sp.solve(dC, r)
r_opt = criticos[0]
print("Radio óptimo r =", round(float(r_opt), 4), "cm")


h_opt = 355 / (sp.pi * r_opt**2)
print("Altura óptima h =", round(float(h_opt), 4), "cm")


costo_min = C.subs(r, r_opt)
print("Costo mínimo =", round(float(costo_min), 4), "cm²")


d2C = sp.diff(dC, r)
print("C''(r_opt) =", round(float(d2C.subs(r, r_opt)), 4), "→ es mínimo si > 0")

# esta seccion es la grafica del problema
r_vals = np.linspace(0.5, 8, 300)
C_func = sp.lambdify(r, C, 'numpy')
C_vals = C_func(r_vals)

plt.figure(figsize=(8, 5))
plt.plot(r_vals, C_vals, color='steelblue', linewidth=2, label='C(r)')
plt.scatter([float(r_opt)], [float(costo_min)],
            color='red', zorder=5, s=100, label=f'Óptimo: r={float(r_opt):.2f} cm')
plt.title('Problema 1 — Costo de la lata cilíndrica')
plt.xlabel('Radio r (cm)')
plt.ylabel('Costo C(r) (cm²)')
plt.legend()
plt.grid(True)
plt.show()