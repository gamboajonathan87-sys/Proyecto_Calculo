
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


x = sp.symbols('x')


I = (80 + x) * (4000 - 50*x)


I_expandida = sp.expand(I)
print("I(x) expandida =", I_expandida)


dI = sp.diff(I_expandida, x)
print("I'(x) =", dI)


criticos = sp.solve(dI, x)
x_opt = criticos[0]
print("Incremento óptimo x =", float(x_opt), "dólares")


precio_opt = 80 + float(x_opt)
suscriptores = int(4000 - 50*float(x_opt))
ingreso_max = float(I_expandida.subs(x, x_opt))
print("Precio mensual óptimo =", precio_opt, "dólares/mes")
print("Suscripciones activas =", suscriptores, "usuarios")
print("Ingreso mensual máximo =", ingreso_max, "dólares")

d2I = sp.diff(dI, x)
print("I''(x) =", d2I)
print("I''(0) =", float(d2I.subs(x, x_opt)))


x_vals = np.linspace(0, 80, 300)
I_func = sp.lambdify(x, I_expandida, 'numpy')
I_vals = I_func(x_vals)

plt.figure(figsize=(8, 5))
plt.plot(x_vals, I_vals, color='steelblue', linewidth=2, label='I(x) = -50x² + 320,000')
plt.scatter([float(x_opt)], [float(ingreso_max)],
            color='red', zorder=5, s=100,
            label=f'Óptimo: x=${float(x_opt):.2f}, I=${float(ingreso_max):,.2f}')
plt.title('Problema 3 — Maximización de ingresos')
plt.xlabel('Incremento de precio x (dólares)')
plt.ylabel('Ingresos I(x) (dólares)')
plt.legend()
plt.grid(True)
plt.show()