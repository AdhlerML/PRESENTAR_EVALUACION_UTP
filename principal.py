import csv
from datetime import datetime
from pathlib import Path
from statistics import mean

# Rutas
def obtener_rutas():
    ROOT = Path(__file__).resolve().parents[1]
    in_file = ROOT / "PRESENTAR_EVALUACION_UTP" / "DATOS" / "DIRTY" / "sucio.csv"
    out_file = ROOT / "PRESENTAR_EVALUACION_UTP" / "DATOS" / "CLEAR" / "limpio.csv"
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

# Control de voltaje
def evaluar_control(val):
    return "CUIDADO" if val >= 5 else "OK"

# Procesamiento de archivo
def procesar_archivo(in_file, out_file):
    total = kept = bad_ts = bad_val = 0
    voltajes = []

    with open(in_file, 'r', encoding="utf-8", newline="") as fin, \
         open(out_file, "w", encoding="utf-8", newline="") as fout:
        reader = csv.DictReader(fin, delimiter=';')
        writer = csv.DictWriter(fout, fieldnames=["Tiempo", "voltaje", "control"])
        writer.writeheader()

        for row in reader:
            total += 1
            ts_raw = row.get("timestamp", "")
            val_raw = row.get("value", "")

            val = limpiar_valor(val_raw)
            if val is None:
                bad_val += 1
                continue

            ts_clean = limpiar_timestamp(ts_raw)
            if ts_clean is None:
                bad_ts += 1
                continue

            control = evaluar_control(val)
            voltajes.append(val)
            writer.writerow({"Tiempo": ts_clean, "voltaje": f"{val:.2f}", "control": control})
            kept += 1

    return total, kept, bad_ts, bad_val, voltajes

# KPIs
def calcular_kpis(voltajes, total, kept, bad_ts, bad_val):
    n = len(voltajes)
    if n == 0:
        kips = {"n": 0, "min": None, "max": None, "prom": None, "alerts": 0, "alerts_pct": 0.0}
    else:
        alertas = sum(v >= 5 for v in voltajes)
        kips = {
            'n': n,
            'min': min(voltajes),
            "max": max(voltajes),
            "prom": mean(voltajes),
            "alerts": alertas,
            "alerts_pct": 100.0 * alertas / n,
        }

    descartes_totales = bad_ts + bad_val
    pct_descartadas = (descartes_totales / total * 100.0) if total else 0.0
    kpis_calidad = {
        "filas_totales": total,
        "filas_validas": kept,
        "descartes_timestamp": bad_ts,
        "descartes_valor": bad_val,
        "%descartadas": round(pct_descartadas, 2),
    }

    return kips, kpis_calidad

# Función principal
def main():
    in_file, out_file = obtener_rutas()
    total, kept, bad_ts, bad_val, voltajes = procesar_archivo(in_file, out_file)
    kips, kpis_calidad = calcular_kpis(voltajes, total, kept, bad_ts, bad_val)
    print("KPIs de voltaje:", kips)
    print("KPIs de calidad:", kpis_calidad)

if __name__ == "__main__":
    main()
