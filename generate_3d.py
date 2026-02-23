import numpy as np
from stl import mesh
from geometry_engine import generate_naca4

def export_wing_to_stl(m, p, t, span, filename):
    print(f"Generando modelo 3D: NACA {int(m*100)}{int(p*10)}{int(t*100):02d}...")
    
    # 1. Obtener coordenadas del perfil 2D
    xu, yu, xl, yl = generate_naca4(m, p, t)
    
    # Envolver el ala 
    x_2d = np.concatenate([xu, xl[::-1]])
    y_2d = np.concatenate([yu, yl[::-1]])
    
    # 2. Generar Vértices 3D (Raíz del ala en Z=0, Punta en Z=span)
    num_pts = len(x_2d)
    vertices = np.zeros((num_pts * 2, 3))
    
    for i in range(num_pts):
        vertices[i] = [x_2d[i], y_2d[i], 0.0]            # Lado izquierdo (chasis)
        vertices[i+num_pts] = [x_2d[i], y_2d[i], span]   # Lado derecho (exterior)
        
    # 3. Tejer la malla 3D (Crear triángulos conectando los vértices)
    faces = []
    for i in range(num_pts - 1):
        # Dos triángulos por cada cuadrícula para crear la "piel" de fibra de carbono
        faces.append([i, i+1, i+num_pts])
        faces.append([i+1, i+1+num_pts, i+num_pts])
        
    # 4. Compilar y guardar el archivo STL
    wing_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            wing_mesh.vectors[i][j] = vertices[f[j],:]
            
    wing_mesh.save(filename)
    print(f"¡Guardado con éxito como '{filename}'!")

if __name__ == "__main__":
    print("INICIANDO LÍNEA DE ENSAMBLAJE VIRTUAL...")
    
    # Fabricamos el ala de Monza (Baja Carga - NACA 3310 de tu telemetría)
    # Le damos un "span" (envergadura) de 1.0 metros
    export_wing_to_stl(0.03, 0.3, 0.10, span=1.0, filename="F1_RearWing_Monza.stl")
    
    # Fabricamos el ala de Mónaco (Alta Carga - NACA 8410 de tu telemetría)
    export_wing_to_stl(0.08, 0.4, 0.10, span=1.0, filename="F1_RearWing_Monaco.stl")
    
    print("Fabricación completada. Revisa la carpeta de tu proyecto.")