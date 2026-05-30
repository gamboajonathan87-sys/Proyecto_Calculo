import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np
import sympy as sp

app = dash.Dash(__name__)
app.title = "Cálculo I — Proyecto Final"

AZUL = "#1e3a5f"
ACENTO = "#e74c3c"
FONDO = "#f4f6f9"
CARD = "#ffffff"

def card(children):
    return html.Div(style={"backgroundColor": CARD, "borderRadius": "12px", "padding": "24px",
                            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)", "marginBottom": "20px"}, children=children)

def resultado_badge(label, valor):
    return html.Div(style={"display": "inline-block", "backgroundColor": AZUL, "color": "white",
                            "borderRadius": "8px", "padding": "10px 18px", "margin": "6px",
                            "textAlign": "center"}, children=[
        html.Div(label, style={"fontSize": "0.75rem", "opacity": "0.8"}),
        html.Div(valor, style={"fontSize": "1.2rem", "fontWeight": "bold"}),
    ])

app.layout = html.Div(style={"fontFamily": "Segoe UI, sans-serif", "backgroundColor": FONDO, "minHeight": "100vh"}, children=[
    html.Div(style={"backgroundColor": AZUL, "padding": "30px", "textAlign": "center",
                    "boxShadow": "0 4px 12px rgba(0,0,0,0.3)"}, children=[
        html.H1("Proyecto Final — Cálculo I", style={"color": "white", "margin": 0, "fontSize": "2.2rem"}),
        html.P("Jonathan Gamoa - Gabriel Puac - Ander Lucas", style={"color": "#aac4e0", "margin": "8px 0 0 0"}),
        html.P("Universidad Mariano Gálvez de Guatemala", style={"color": "#7aafd4", "margin": "4px 0 0 0", "fontSize": "0.9rem"}),
    ]),
    html.Div(style={"maxWidth": "1100px", "margin": "30px auto", "padding": "0 20px"}, children=[
        dcc.Tabs(id="tabs", value="p1", children=[
            dcc.Tab(label="🥫 Problema 1 — Lata cilíndrica", value="p1"),
            dcc.Tab(label="🔌 Problema 2 — Tendido de cable", value="p2"),
            dcc.Tab(label="💰 Problema 3 — Maximización", value="p3"),
            dcc.Tab(label="📄 Código fuente", value="codigo"),
        ]),
        html.Div(id="contenido-tab"),
    ])
])

def tab_p1():
    r_sym = sp.symbols('r', positive=True)
    C_sym = 2 * sp.pi * r_sym**2 + 710 / r_sym
    dC = sp.diff(C_sym, r_sym)
    r_opt = float(sp.solve(dC, r_sym)[0])
    h_opt = 355 / (np.pi * r_opt**2)
    costo_min = float(C_sym.subs(r_sym, r_opt))
    r_vals = np.linspace(0.5, 8, 300)
    C_vals = 2*np.pi*r_vals**2 + 710/r_vals
    frames = []
    for i in range(0, 300, 4):
        frames.append(go.Frame(data=[
            go.Scatter(x=r_vals, y=C_vals, mode='lines', name='C(r)', line=dict(color='steelblue', width=3)),
            go.Scatter(x=[r_vals[i]], y=[C_vals[i]], mode='markers', marker=dict(color=ACENTO, size=14), name='Recorrido'),
            go.Scatter(x=[r_opt], y=[costo_min], mode='markers+text', text=[f'Óptimo r={r_opt:.2f}'],
                       textposition='top right', marker=dict(color='green', size=12, symbol='star'), name='Mínimo'),
        ], name=str(i)))
    fig = go.Figure(data=[
        go.Scatter(x=r_vals, y=C_vals, mode='lines', name='C(r)', line=dict(color='steelblue', width=3)),
        go.Scatter(x=[r_vals[0]], y=[C_vals[0]], mode='markers', marker=dict(color=ACENTO, size=14), name='Recorrido'),
        go.Scatter(x=[r_opt], y=[costo_min], mode='markers+text', text=[f'Óptimo r={r_opt:.2f}'],
                   textposition='top right', marker=dict(color='green', size=12, symbol='star'), name='Mínimo'),
    ], frames=frames)
    fig.update_layout(title="C(r) = 2πr² + 710/r — Costo de la lata (animado)",
        xaxis_title="Radio r (cm)", yaxis_title="Costo C(r) (cm²)",
        plot_bgcolor=FONDO, paper_bgcolor=CARD,
        updatemenus=[dict(type="buttons", showactive=False, y=1.15, x=0.1, buttons=[
            dict(label="▶ Animar", method="animate", args=[None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]),
            dict(label="⏹ Parar", method="animate", args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}]),
        ])])
    return html.Div([
        card([html.H3("🥫 Problema 1 — Diseño óptimo de una lata cilíndrica", style={"color": AZUL}),
              html.P("Una empresa produce latas de aluminio con volumen fijo de 355 ml. Se buscan las dimensiones que minimicen el costo de material."),
              html.B("Función objetivo: "), html.Code("C(r) = 2πr² + 710/r"),
              html.Br(), html.B("Derivada: "), html.Code("C'(r) = 4πr − 710/r²"),
              html.Br(), html.B("Punto crítico: "), html.Code("C'(r) = 0  →  r = ∛(355/2π)"),]),
        card([html.P("▶ Presiona Animar para ver el punto recorriendo la curva hasta el mínimo.", style={"color": "#555"}),
              dcc.Graph(figure=fig)]),
        card([html.H4("Resultados", style={"color": AZUL, "marginTop": 0}),
              html.Div([resultado_badge("Radio óptimo", f"{r_opt:.4f} cm"),
                        resultado_badge("Altura óptima", f"{h_opt:.4f} cm"),
                        resultado_badge("Costo mínimo", f"{costo_min:.4f} cm²"),
                        resultado_badge("Relación h/r", f"{h_opt/r_opt:.4f}"),]),
              html.P("✅ C''(r_opt) > 0 → es un mínimo confirmado.", style={"color": "green", "marginTop": "16px"}),
              html.P("📌 La lata óptima tiene altura ≈ 2× el radio, minimizando el material usado."),]),
    ])

def tab_p2():
    x_sym = sp.symbols('x')
    C_sym = 1500*x_sym + 3000*sp.sqrt(16 + (6 - x_sym)**2)
    dC = sp.diff(C_sym, x_sym)
    x_opt = float(sp.solve(dC, x_sym)[0])
    dist_agua = float(sp.sqrt(16 + (6 - x_opt)**2))
    costo_min = float(C_sym.subs(x_sym, x_opt))
    x_vals = np.linspace(0, 6, 300)
    C_vals = 1500*x_vals + 3000*np.sqrt(16 + (6 - x_vals)**2)
    frames = []
    for i in range(0, 300, 4):
        frames.append(go.Frame(data=[
            go.Scatter(x=x_vals, y=C_vals, mode='lines', name='C(x)', line=dict(color='steelblue', width=3)),
            go.Scatter(x=[x_vals[i]], y=[C_vals[i]], mode='markers', marker=dict(color=ACENTO, size=14), name='Recorrido'),
            go.Scatter(x=[x_opt], y=[costo_min], mode='markers+text', text=[f'Óptimo x={x_opt:.2f}'],
                       textposition='top right', marker=dict(color='green', size=12, symbol='star'), name='Mínimo'),
        ], name=str(i)))
    fig = go.Figure(data=[
        go.Scatter(x=x_vals, y=C_vals, mode='lines', name='C(x)', line=dict(color='steelblue', width=3)),
        go.Scatter(x=[x_vals[0]], y=[C_vals[0]], mode='markers', marker=dict(color=ACENTO, size=14), name='Recorrido'),
        go.Scatter(x=[x_opt], y=[costo_min], mode='markers+text', text=[f'Óptimo x={x_opt:.2f}'],
                   textposition='top right', marker=dict(color='green', size=12, symbol='star'), name='Mínimo'),
    ], frames=frames)
    fig.update_layout(title="C(x) = 1500x + 3000√(16+(6-x)²) — Costo del cable (animado)",
        xaxis_title="Distancia por tierra x (km)", yaxis_title="Costo C(x) ($)",
        plot_bgcolor=FONDO, paper_bgcolor=CARD,
        updatemenus=[dict(type="buttons", showactive=False, y=1.15, x=0.1, buttons=[
            dict(label="▶ Animar", method="animate", args=[None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]),
            dict(label="⏹ Parar", method="animate", args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}]),
        ])])
    return html.Div([
        card([html.H3("🔌 Problema 2 — Tendido de cable tierra-isla", style={"color": AZUL}),
              html.P("Conectar tierra firme con una isla a 4 km de la costa. Cable submarino: $3,000/km. Cable terrestre: $1,500/km. Costa disponible: 6 km."),
              html.B("Función objetivo: "), html.Code("C(x) = 1500x + 3000·√(16 + (6−x)²)"),
              html.Br(), html.B("Restricción: "), html.Code("0 ≤ x ≤ 6"),]),
        card([html.P("▶ Presiona Animar para ver cómo varía el costo al cambiar x.", style={"color": "#555"}),
              dcc.Graph(figure=fig)]),
        card([html.H4("Resultados", style={"color": AZUL, "marginTop": 0}),
              html.Div([resultado_badge("Distancia por tierra", f"{x_opt:.4f} km"),
                        resultado_badge("Distancia bajo agua", f"{dist_agua:.4f} km"),
                        resultado_badge("Costo mínimo", f"${costo_min:,.2f}"),
                        resultado_badge("Costo en x=0", "$21,633.31"),
                        resultado_badge("Costo en x=6", "$21,000.00"),]),
              html.P("✅ C''(x_opt) > 0 → es un mínimo confirmado.", style={"color": "green", "marginTop": "16px"}),
              html.P("📌 Tender 3.69 km por tierra y 4.62 km bajo el agua es la combinación más económica."),]),
    ])

def tab_p3():
    x_sym = sp.symbols('x')
    I_sym = sp.expand((80 + x_sym) * (4000 - 50*x_sym))
    dI = sp.diff(I_sym, x_sym)
    x_opt = float(sp.solve(dI, x_sym)[0])
    precio_opt = 80 + x_opt
    suscriptores = int(4000 - 50*x_opt)
    ingreso_max = float(I_sym.subs(x_sym, x_opt))

    x_vals = np.linspace(0, 80, 300)
    I_func = sp.lambdify(x_sym, I_sym, 'numpy')
    I_vals = I_func(x_vals)

    frames = []
    for i in range(0, 300, 4):
        frames.append(go.Frame(data=[
            go.Scatter(x=x_vals, y=I_vals, mode='lines', name='I(x)',
                       line=dict(color='steelblue', width=3)),
            go.Scatter(x=[x_vals[i]], y=[I_vals[i]], mode='markers',
                       marker=dict(color=ACENTO, size=14), name='Recorrido'),
            go.Scatter(x=[x_opt], y=[ingreso_max], mode='markers+text',
                       text=[f'Máximo x=${x_opt:.0f}'], textposition='top right',
                       marker=dict(color='green', size=12, symbol='star'), name='Máximo'),
        ], name=str(i)))

    fig = go.Figure(data=[
        go.Scatter(x=x_vals, y=I_vals, mode='lines', name='I(x)',
                   line=dict(color='steelblue', width=3)),
        go.Scatter(x=[x_vals[0]], y=[I_vals[0]], mode='markers',
                   marker=dict(color=ACENTO, size=14), name='Recorrido'),
        go.Scatter(x=[x_opt], y=[ingreso_max], mode='markers+text',
                   text=[f'Máximo x=${x_opt:.0f}'], textposition='top right',
                   marker=dict(color='green', size=12, symbol='star'), name='Máximo'),
    ], frames=frames)

    fig.update_layout(
        title="I(x) = -50x² + 320,000 — Ingresos (animado)",
        xaxis_title="Incremento de precio x ($)",
        yaxis_title="Ingresos I(x) ($)",
        plot_bgcolor=FONDO, paper_bgcolor=CARD,
        updatemenus=[dict(type="buttons", showactive=False, y=1.15, x=0.1, buttons=[
            dict(label="▶ Animar", method="animate",
                 args=[None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]),
            dict(label="⏹ Parar", method="animate",
                 args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}]),
        ])])

    return html.Div([
        card([
            html.H3("💰 Problema 3 — Maximización de ingresos", style={"color": AZUL}),
            html.P("Una startup cobra $80/mes con 4,000 suscriptores. Por cada $1 de aumento pierde 50 suscriptores."),
            html.B("Función objetivo: "), html.Code("I(x) = (80 + x)(4,000 − 50x)"),
            html.Br(), html.B("Expandida: "), html.Code("I(x) = −50x² + 320,000"),
            html.Br(), html.B("Derivada: "), html.Code("I'(x) = −100x"),
            html.Br(), html.B("Punto crítico: "), html.Code("x = 0"),
        ]),
        card([
            html.P("▶ Presiona Animar para visualizar la función de ingresos.", style={"color": "#555"}),
            dcc.Graph(figure=fig),
        ]),
        card([
            html.H4("Resultados", style={"color": AZUL, "marginTop": 0}),
            html.Div([
                resultado_badge("Incremento óptimo", f"${x_opt:.2f}"),
                resultado_badge("Precio óptimo", f"${precio_opt:.2f}/mes"),
                resultado_badge("Suscriptores activos", f"{suscriptores:,}"),
                resultado_badge("Ingreso máximo", f"${ingreso_max:,.2f}"),
            ]),
            html.P("✅ I''(0) = -100 < 0 → es un máximo confirmado.", style={"color": "green", "marginTop": "16px"}),
            html.P("📌 No conviene subir el precio. Con la tasa de deserción actual de 50 suscriptores por cada $1, el precio óptimo se mantiene en $80/mes con 4,000 suscriptores activos e ingresos de $320,000."),
        ]),
    ])

def tab_codigo():
    def bloque(titulo, archivo):
        try:
            codigo = open(archivo, encoding="utf-8").read()
        except:
            codigo = "Archivo no encontrado."
        return card([html.H4(titulo, style={"color": AZUL, "marginTop": 0}),
                     html.Pre(codigo, style={"backgroundColor": "#1e1e1e", "color": "#d4d4d4",
                                              "padding": "16px", "borderRadius": "8px",
                                              "overflowX": "auto", "fontSize": "0.85rem"}),])
    return html.Div([
        html.H3("📄 Código fuente de los 3 problemas", style={"color": AZUL}),
        bloque("problema1.py — Lata cilíndrica", "problema1.py"),
        bloque("problema2.py — Tendido de cable", "problema2.py"),
        bloque("problema3.py — Maximización de ingresos", "problema3.py"),
    ])

@app.callback(Output("contenido-tab", "children"), Input("tabs", "value"))
def render_tab(tab):
    if tab == "p1": return tab_p1()
    if tab == "p2": return tab_p2()
    if tab == "p3": return tab_p3()
    if tab == "codigo": return tab_codigo()

if __name__ == "__main__":
    app.run(debug=True)