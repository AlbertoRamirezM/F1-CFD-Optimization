import aerosandbox as asb
from neuralfoil import get_aero_from_airfoil

def run_virtual_wind_tunnel(m, p, t, angle_of_attack, speed_kmh):
    """
    Simula el flujo de aire sobre el perfil y devuelve el Downforce y el Drag.
    """
    # 1. Crear el nombre del perfil basándonos en tus variables paramétricas
    # Ej: m=0.08, p=0.4, t=0.12 -> "naca8412"
    m_digit = int(m * 100)
    p_digit = int(p * 10)
    t_digits = int(t * 100)
    naca_name = f"naca{m_digit}{p_digit}{t_digits:02d}"
    
    # Cargar el perfil geométrico en el motor
    airfoil = asb.Airfoil(naca_name)
    
    # 2. Física pura (Condiciones de carrera de F1)
    velocity_ms = speed_kmh / 3.6 # Convertir a metros por segundo
    chord = 0.35 # Cuerda del alerón trasero en metros (35 cm)
    kinematic_viscosity = 1.48e-5 # Viscosidad del aire a 15ºC
    
    # El Número de Reynolds: Fundamental en aerodinámica (relación fuerzas inerciales vs viscosas)
    reynolds_number = (velocity_ms * chord) / kinematic_viscosity

    # print(f"--- TÚNEL DE VIENTO ACTIVADO ---")
    # print(f"Perfil: {naca_name.upper()} | Velocidad: {speed_kmh} km/h | Reynolds: {reynolds_number:.2e}")
    # print(f"Calculando ecuaciones de flujo turbulento (Neural Surrogate)...")

    # 3. Lanzar la simulación
    aero_data = get_aero_from_airfoil(
        airfoil=airfoil,
        alpha=angle_of_attack,
        Re=reynolds_number
    )
    
    # Extraer los datos (En la F1 el Lift es negativo para pegar el coche al suelo, 
    # pero aquí medimos el valor absoluto como "Downforce Coeff")
    cl = aero_data['CL'][0] # Coeficiente de Sustentación (Lift)
    cd = aero_data['CD'][0] # Coeficiente de Resistencia (Drag)
    efficiency = cl / cd    # L/D Ratio (La Meca de la aerodinámica)

    return cl, cd, efficiency

# --- PRUEBA EN PISTA ---
if __name__ == "__main__":
    # Vamos a probar nuestro alerón "agresivo" del script anterior
    # m=0.08, p=0.4, t=0.12 a 5 grados de ángulo de ataque y 300 km/h (Final de recta)
    
    C_L, C_D, L_D = run_virtual_wind_tunnel(
        m=0.08, 
        p=0.4, 
        t=0.12, 
        angle_of_attack=5.0, 
        speed_kmh=300
    )

    print("\n--- RESULTADOS DE TELEMETRÍA ---")
    print(f"Coef. Carga Aerodinámica (CL): {C_L:.4f}")
    print(f"Coef. Resistencia (CD) : {C_D:.4f}")
    print(f"Eficiencia (CL/CD)     : {L_D:.2f}")
    if L_D > 50:
        print("Veredicto: Excelente. Tienes un misil para las rectas.")
    else:
        print("Veredicto: Genera carga, pero penaliza el motor por exceso de Drag.")