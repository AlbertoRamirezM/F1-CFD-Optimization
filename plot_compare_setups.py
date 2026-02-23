import matplotlib.pyplot as plt
from geometry_engine import generate_naca4

# 1. Generar los perfiles de los extremos del Frente de Pareto
# MONZA (Low Drag)
xu_mz, yu_mz, xl_mz, yl_mz = generate_naca4(m=0.03, p=0.3, t=0.10)

# MÓNACO (High Downforce)
xu_mc, yu_mc, xl_mc, yl_mc = generate_naca4(m=0.08, p=0.4, t=0.10)

# 2. Configurar el lienzo (Modo Oscuro AWS F1)
plt.style.use('dark_background')
plt.figure(figsize=(14, 6))

# INVERTIR EJE Y: Los aviones vuelan hacia arriba, los F1 se pegan al suelo
plt.gca().invert_yaxis()

# 3. Dibujar Setup de Monza (Velocidad Punta)
plt.plot(xu_mz, yu_mz, color='#00ffcc', linewidth=2, label='Spec MONZA (Low Drag - V. Max)')
plt.plot(xl_mz, yl_mz, color='#00ffcc', linewidth=2)
plt.fill_between(xu_mz, yl_mz, yu_mz, color='#00ffcc', alpha=0.4)

# 4. Dibujar Setup de Mónaco (Máxima Carga)
plt.plot(xu_mc, yu_mc, color='#ff00ff', linewidth=2, label='Spec MÓNACO (High Downforce)')
plt.plot(xl_mc, yl_mc, color='#ff00ff', linewidth=2)
plt.fill_between(xu_mc, yl_mc, yu_mc, color='#ff00ff', alpha=0.4)

# 5. Formato profesional
plt.title('F1 Telemetry: Setup Comparison (Monza vs Monaco)', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Posición de la cuerda (x)', fontsize=12)
plt.ylabel('Geometría invertida para Downforce (y)', fontsize=12)
plt.axis('equal') # Vital para ver la proporción real
plt.legend(loc='upper right', fontsize=12, facecolor='black', edgecolor='white')
plt.grid(True, linestyle=':', alpha=0.3)

plt.tight_layout()
plt.show()