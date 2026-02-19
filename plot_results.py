import matplotlib.pyplot as plt
from geometry_engine import generate_naca4

# 1. Extraer los datos geométricos
# ALERÓN ORIGINAL (NACA 8412)
xu_orig, yu_orig, xl_orig, yl_orig = generate_naca4(m=0.08, p=0.4, t=0.12)

# ALERÓN OPTIMIZADO POR LA IA (Datos de tu telemetría)
xu_opt, yu_opt, xl_opt, yl_opt = generate_naca4(m=0.0862, p=0.4380, t=0.1029)

# 2. Configurar un lienzo profesional (Estilo Dark Mode)
plt.style.use('dark_background')
plt.figure(figsize=(12, 5))

# 3. Dibujar el Original (En gris y discontinuo, como un "fantasma")
plt.plot(xu_orig, yu_orig, color='gray', linestyle='--', alpha=0.8, label='Baseline (L/D: 178.14)')
plt.plot(xl_orig, yl_orig, color='gray', linestyle='--', alpha=0.8)

# 4. Dibujar el Optimizado (En un cyan brillante y relleno, para que destaque)
plt.plot(xu_opt, yu_opt, color='cyan', linewidth=2, label='AI Optimized (L/D: 186.76)')
plt.plot(xl_opt, yl_opt, color='cyan', linewidth=2)
plt.fill_between(xu_opt, yl_opt, yu_opt, color='cyan', alpha=0.2) # Relleno interior

# 5. Ajustes de telemetría visual
plt.gca().invert_yaxis() # Alerón de F1: Fuerza hacia abajo
plt.title('F1 Rear Wing: CFD Optimization Pipeline', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Chord Position (x)', fontsize=12)
plt.ylabel('Geometry (y)', fontsize=12)
plt.axis('equal') # Vital para que la proporción sea real
plt.legend(loc='upper right', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.3)

# Mostrar la obra de arte
plt.tight_layout()
plt.show()