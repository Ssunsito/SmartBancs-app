import json
import os

def generar_datos():
    # Asegurar que el directorio data exista dentro de tests
    directorio = "tests/data"
    os.makedirs(directorio, exist_ok=True)

    # 1. Datos para prueba de estrés (50 transacciones con montos dinámicos)
    stress_data = []
    for i in range(50):
        stress_data.append({
            "cuenta_origen_id": 1,
            "cuenta_destino_id": 2,
            "monto": round(10.0 + (i * 0.15), 2) # Montos variables: 10.0, 10.15, 10.30...
        })

    with open(f"{directorio}/stress_data.json", "w") as f:
        json.dump(stress_data, f, indent=4)

    # 2. Datos para incidente (Deadlock cruzado - 200 transacciones)
    # Alternamos direcciones para forzar la colisión en la base de datos
    incident_data = []
    for i in range(200):
        if i % 2 == 0:
            incident_data.append({"cuenta_origen_id": 1, "cuenta_destino_id": 2, "monto": 1.5})
        else:
            incident_data.append({"cuenta_origen_id": 2, "cuenta_destino_id": 1, "monto": 2.5})

    with open(f"{directorio}/incident_data.json", "w") as f:
        json.dump(incident_data, f, indent=4)

    print("[Generador] Datos de prueba creados exitosamente en 'tests/data/'")

if __name__ == "__main__":
    generar_datos()