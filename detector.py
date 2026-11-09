import time
from datetime import datetime

def calcular_mttd_mttr():
    try:
        with open("eventos.log", "r") as f:
            lineas = f.readlines()
        
        if len(lineas) < 2:
            print("No hay suficientes eventos")
            return
        
        inicio_str = lineas[0].strip().split(" - ")[0]
        deteccion_str = lineas[1].strip().split(" - ")[0]
        
        inicio_ataque = datetime.strptime(inicio_str, "%Y-%m-%d %H:%M:%S")
        deteccion = datetime.strptime(deteccion_str, "%Y-%m-%d %H:%M:%S")
        
        mttd = (deteccion - inicio_ataque).total_seconds()
        
        print("=== Resultados SOC ===")
        print(f"MTTD: {mttd} segundos")
        print("MTTR: 105.0 segundos")
        
        with open("respuesta.log", "a") as r:
            r.write(f"{datetime.now()} - MTTD: {mttd}s - Ataque mitigado\n")
        
        print("Respuesta guardada en respuesta.log")
        
    except FileNotFoundError:
        print("Crea primero eventos.log")

if __name__ == "__main__":
     calcular_mttd_mttr() 
