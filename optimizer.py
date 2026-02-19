import numpy as np
from scipy.optimize import differential_evolution
from aero_solver import run_virtual_wind_tunnel

# 1. DEFINIR EL OBJETIVO 
def objective_function(x):
    # x es el "ADN" de nuestro alerón: [Camber, Posición, Espesor]
    m, p, t = x[0], x[1], x[2]
    
    try:
        # Metemos el ala en el túnel de viento a 300 km/h y 5º de ataque
        cl, cd, efficiency = run_virtual_wind_tunnel(m, p, t, angle_of_attack=5.0, speed_kmh=300)
        
        # Penalización: Si el ala genera sustentación hacia arriba, la descartamos
        if cl < 0:
            return 10000 
            
        # El algoritmo busca el número MÁS PEQUEÑO. 
        # Como queremos MAXIMIZAR la eficiencia, le pasamos la eficiencia en NEGATIVO.
        return -efficiency 
    except:
        # Si las matemáticas fallan al generar una forma imposible, matamos esa mutación
        return 10000

if __name__ == "__main__":
    print("Iniciando IA de Optimización Evolutiva CFD...")
    
    # 2. LAS REGLAS DE LA FIA (Nuestros límites / Bounds)
    # Camber (m): 0% a 9% | Posición (p): 20% a 50% | Espesor (t): 10% a 15%
    bounds = [(0.0, 0.09), (0.2, 0.5), (0.10, 0.15)]
    
    # 3. LANZAR LA EVOLUCIÓN
    print("Mutando geometrías y buscando el alerón perfecto... (Esto puede tardar unos segundos)")
    
    # differential_evolution es un algoritmo genético hiper-robusto
    result = differential_evolution(
        func=objective_function, 
        bounds=bounds, 
        maxiter=15,  # 15 generaciones máximas
        popsize=5,   # 5 individuos (alerones) por generación
        disp=True    # Que nos muestre por pantalla cómo va mejorando
    )
    
    # 4. RESULTADOS DE CAMPEONATO
    best_m, best_p, best_t = result.x
    print("\n ¡OPTIMIZACIÓN COMPLETADA! ")
    print(f"Mejor perfil encontrado: NACA {int(best_m*100)}{int(best_p*10)}{int(best_t*100):02d}")
    print(f"Eficiencia Máxima Alcanzada (L/D): {-result.fun:.2f}")
    print(f"ADN Exacto: m={best_m:.4f}, p={best_p:.4f}, t={best_t:.4f}")