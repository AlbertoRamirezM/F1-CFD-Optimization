import numpy as np
import matplotlib.pyplot as plt

def generate_naca4(m, p, t, c=1.0, num_points=100):
    """
    Genera las coordenadas (x, y) de un perfil NACA de 4 dígitos.
    m: Camber máximo (en % de la cuerda, ej: 0.08 para mucho downforce)
    p: Posición del camber máximo (en décimas de la cuerda, ej: 0.4)
    t: Espesor máximo (en % de la cuerda, ej: 0.12)
    c: Longitud de la cuerda (por defecto 1.0)
    """
    # 1. Distribuir puntos a lo largo de la cuerda (más densidad en los bordes para precisión CFD)
    beta = np.linspace(0, np.pi, num_points)
    x = c * (0.5 * (1 - np.cos(beta))) # Distribución de coseno (agrupa puntos en leading/trailing edges)

    # 2. Ecuación de espesor (Thickness distribution)
    yt = 5 * t * c * (0.2969 * np.sqrt(x/c) - 0.1260 * (x/c) - 
                      0.3516 * (x/c)**2 + 0.2843 * (x/c)**3 - 0.1015 * (x/c)**4)

    # 3. Ecuación de la línea de curvatura media (Camber line)
    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)

    if p > 0:
        # Parte delantera del ala
        front = x <= p * c
        yc[front] = m * (x[front] / p**2) * (2 * p - x[front] / c)
        dyc_dx[front] = (2 * m / p**2) * (p - x[front] / c)

        # Parte trasera del ala
        back = x > p * c
        yc[back] = m * ((c - x[back]) / (1 - p)**2) * (1 + x[back] / c - 2 * p)
        dyc_dx[back] = (2 * m / (1 - p)**2) * (p - x[back] / c)

    # 4. Calcular el ángulo de la superficie
    theta = np.arctan(dyc_dx)

    # 5. Calcular coordenadas de la superficie superior (Upper) e inferior (Lower)
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    return xu, yu, xl, yl

# --- ZONA DE PRUEBAS (Tu túnel de viento inicial) ---
if __name__ == "__main__":
    # Vamos a generar un perfil muy agresivo, típico de alerón trasero de alta carga (ej. NACA 8412)
    # m = 0.08 (Camber alto), p = 0.4 (Posición), t = 0.12 (Espesor)
    
    xu, yu, xl, yl = generate_naca4(m=0.08, p=0.4, t=0.12)

    # Visualización profesional
    plt.figure(figsize=(10, 4))
    plt.plot(xu, yu, 'b-', label='Extradós (Upper)')
    plt.plot(xl, yl, 'r-', label='Intradós (Lower)')
    plt.plot(xu, (yu+yl)/2, 'k--', label='Camber Line', alpha=0.5) # Línea media
    
    # Invertir el eje Y para que parezca un alerón trasero de F1 (que genera fuerza hacia ABAJO, no hacia arriba como un avión)
    plt.gca().invert_yaxis() 

    plt.title('F1 Rear Wing Baseline Profile (NACA 8412 Invertido)')
    plt.xlabel('Posición en la Cuerda (x)')
    plt.ylabel('Geometría (y)')
    plt.axis('equal') # Vital para no deformar la imagen
    plt.legend()
    plt.grid(True, linestyle=':')
    plt.show()