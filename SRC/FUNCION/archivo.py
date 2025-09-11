import csv
from .limpieza import limpiar_valor, limpiar_timestamp
from .control import evaluar_alerta

def procesar_archivo(in_file, out_file):
    
    filas_totales = filas_validas = descartes_ts = descartes_valor = 0
    temps = []

    with open(in_file, 'r', encoding='utf-8', newline='') as fin, \
     open(out_file, 'w', encoding='utf-8', newline='') as fout:
         
        reader = csv.DictReader(fin, delimiter=';')
        writer = csv.DictWriter(fout, fieldnames=["Timestamp", "Voltaje", "Temp_C", "Alertas"])
        writer.writeheader()

        for row in reader:
                filas_totales += 1
                val_raw = row.get("value", "")
                ts_raw = row.get("timestamp", "")

                val = limpiar_valor(val_raw)
                if val is None:
                    descartes_valor += 1
                    continue

                ts_clean = limpiar_timestamp(ts_raw)
                if ts_clean is None:
                    descartes_ts += 1
                    continue

                temp = round(18 * val - 64, 2)
                alerta = evaluar_alerta(temp)
                temps.append(temp)

                writer.writerow({
                    "Timestamp": ts_clean,
                    "Voltaje": f"{val:.2f}",
                    "Temp_C": f"{temp:.2f}",
                    "Alertas": alerta
        })
        filas_validas += 1
    return filas_totales, filas_validas, descartes_ts, descartes_valor, temps
