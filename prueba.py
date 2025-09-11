import csv
from datetime import datetime
from pathlib import Path
from statistics import mean

# Rutas
def obtener_rutas():
    ROOT = Path(__file__).resolve().parents[0]
    

    
    in_file = ROOT /  "DATA" / "RAW" / "sucio.csv"
    out_file = ROOT /  "DATA" / "PROCESSED" / "limpio.csv"
    return in_file, out_file

# Limpieza de valor
def limpiar_valor(val_raw):
    val_raw = val_raw.replace(",", ".").strip().lower()
    if val_raw in {"", "na", "n/a", "nan", "null", "none", "error"}:
        return None
    try:
        return float(val_raw)
    except ValueError:
        return None

# Limpieza de timestamp
def limpiar_timestamp(ts_raw):
    ts_raw = ts_raw.strip()
    formatos = ["%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S"]
    for fmt in formatos:
        try:
            dt = datetime.strptime(ts_raw, fmt)
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    if "T" in ts_raw and len(ts_raw) >= 19:
        try:
            dt = datetime.strptime(ts_raw[:19], "%Y-%m-%dT%H:%M:%S")
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None
    return None



# Evaluar alerta
def evaluar_alerta(temp):
    return "ALERTA" if temp > 40 else "OK"

# Procesamiento

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

# KPIs

def calcular_kpis(filas_totales, filas_validas, descartes_ts, descartes_valor, temps):
    n = len(temps)
    temp_min = min(temps) if temps else None
    temp_max = max(temps) if temps else None
    temp_prom = mean(temps) if temps else None
    alertas = sum(t > 40 for t in temps)
    
    kpis_calidad = {
        "filas_totales": filas_totales,
        "filas_validas": filas_validas,
        "descartes_timestamp": descartes_ts,
        "descartes_valor": descartes_valor,
    }
    
    kpis_temp = {
        "n": n,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "temp_prom": round(temp_prom, 2) if temp_prom else None,
        "alertas": alertas,
    }
    
    return kpis_calidad, kpis_temp

def main():
    in_file, out_file = obtener_rutas()
    filas_totales, filas_validas, descartes_ts, descartes_valor, temps = procesar_archivo(in_file, out_file)
    kips_temp, kpis_calidad = calcular_kpis(filas_totales, filas_validas, descartes_ts, descartes_valor, temps)
    print("KPIs de temperatura:", kips_temp)
    print("KPIs de calidad:", kpis_calidad)

if __name__ == "__main__":
    main()
