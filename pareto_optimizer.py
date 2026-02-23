import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from aero_solver import run_virtual_wind_tunnel

def get_objective(peso_downforce):
    """
    peso_downforce = 0.0 -> Solo nos importa el Drag (Monza)
    peso_downforce = 1.0 -> Solo nos importa el Downforce (Mónaco)
    """
    def objective_function(x):
        m, p, t = x[0], x[1], x[2]
        try:
            cl, cd, _ = run_virtual_wind_tunnel(m, p, t, angle_of_attack=5.0, speed_kmh=300)
            
            # Filtro de seguridad
            if cl < 0 or cd <= 0:
                return 10000
            
            # Normalizamos los valores para que la IA los entienda igual
            # Multiplicamos el Drag por 100 porque suele ser un número muy pequeño comparado con el Lift
            penalizacion_drag = cd * 100
            recompensa_lift = cl
            
            # Calculamos la puntuación (queremos minimizar este número)
            # A mayor peso_downforce, más nos importa maximizar CL (minimizar -CL)
            puntuacion = (1 - peso_downforce) * penalizacion_drag + peso_downforce * (-recompensa_lift)
            return puntuacion
        except:
            return 10000
            
    return objective_function

if __name__ == "__main__":
    print("Iniciando Simulador de Estrategia: Frente de Pareto (Monza vs Mónaco)")
    bounds = [(0.0, 0.09), (0.2, 0.5), (0.10, 0.15)]
    
    # Vamos a simular 5 setups diferentes
    pesos = [0.01, 0.04, 0.1, 0.3, 0.9]
    circuitos = [
        "Monza (Low Drag)", 
        "Spa (Med-Low)", 
        "Silverstone (Balanced)", 
        "Suzuka (Med-High)", 
        "Mónaco (High Downforce)"
    ]
    
    resultados_cl = []
    resultados_cd = []
    
    # ---------------------------------------------------------
    # BUCLE DE OPTIMIZACIÓN DEL CAMPEONATO
    # ---------------------------------------------------------
    for i, w in enumerate(pesos):
        print(f"\n Optimizando Setup para {circuitos[i]}...")
        
        # Generamos la IA con la mentalidad del circuito actual
        obj_func = get_objective(peso_downforce=w)
        
        # Lanzamos la evolución (bajamos maxiter a 10 para que no tarde demasiado)
        result = differential_evolution(obj_func, bounds, maxiter=10, popsize=5)
        
        # Extraemos el ADN ganador
        best_m, best_p, best_t = result.x
        
        # Medimos sus valores reales en el túnel de viento
        cl, cd, _ = run_virtual_wind_tunnel(best_m, best_p, best_t, angle_of_attack=5.0, speed_kmh=300)
        
        resultados_cl.append(cl)
        resultados_cd.append(cd)
        
        print(f"Completado -> CL (Agarre): {cl:.4f} | CD (Freno): {cd:.4f}")
        print(f"   ADN: NACA {int(best_m*100)}{int(best_p*10)}{int(best_t*100):02d}")

    # ---------------------------------------------------------
    # TELEMETRÍA VISUAL (El gráfico definitivo)
    # ---------------------------------------------------------
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    
    # Dibujamos la curva que une a todos los alerones (El Frente de Pareto)
    plt.plot(resultados_cd, resultados_cl, color='cyan', linestyle='-', linewidth=2, marker='o', markersize=8)
    
    # Ponemos las etiquetas de los circuitos en cada punto
    for i, txt in enumerate(circuitos):
        plt.annotate(txt, (resultados_cd[i], resultados_cl[i]), 
                     textcoords="offset points", xytext=(15,-5), ha='left', color='white', fontsize=10)

    plt.title('Frente de Pareto Aerodinámico (Downforce vs Drag)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Coeficiente de Resistencia al Avance (CD) -> Menor es mejor', fontsize=12)
    plt.ylabel('Coeficiente de Sustentación Invertida (CL) -> Mayor es mejor', fontsize=12)
    
    # Relleno inferior para darle aspecto de software profesional
    plt.fill_between(resultados_cd, resultados_cl, min(resultados_cl)-0.1, color='cyan', alpha=0.1)
    
    plt.grid(True, linestyle=':', alpha=0.3)
    plt.tight_layout()
    plt.show()