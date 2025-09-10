import csv
from datetime import datetime
from pathlib import Path #importo el comando path (busca el lugar del codigo)
from statistics import mean

#crear mis variables de rutas para ingreso de archivo y salida de archivo
ROOT=Path(__file__).resolve().parents[1]#busca el lugar donde esta guardado el codigo
#/USUARIO/Sesion4
IN_FILE=ROOT/"PRESENTAR_EVALUACION_UTP"/"DATOS"/"DIRTY"/"sucio.csv" #ruta de ingreso
OUT_FILE=ROOT/"PRESENTAR_EVALUACION_UTP"/"DATOS"/"CLEAR"/"limpio.csv" #ruta de salida

#apertura de archivos
with open(IN_FILE,'r',encoding="utf-8", newline="") as fin, \
    open(OUT_FILE, "w", encoding="utf-8", newline="") as fout:
    reader=csv.DictReader(fin,delimiter=';')
    writer=csv.DictWriter(fout,fieldnames=["Tiempo","voltaje","control"])
    writer.writeheader()
#leer linea por lineal y seleccionar en crudo raw 
    total = kept = 0
    bad_ts = bad_val = 0
    voltajes=[]
    for row in reader:
        total+=1
        ts_raw  = (row.get("timestamp") or "").strip() #toma todos los valores de la columna timestamp
        val_raw = (row.get("value") or "").strip() #toma todos los valores de la columna value
#limpiar datos
        val_raw = val_raw.replace(",", ".")
        val_low = val_raw.lower() #empezar a eliminar valores no existentes
        if val_low in {"", "na", "n/a", "nan", "null", "none", "error"}:
            bad_ts += 1
            continue #salta el comando
        try:
            val = float(val_raw)
        except ValueError:
            bad_ts += 1
            continue  # saltar fila si no es número
#limpieza de datos de tiempo 
        ts_clean = None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S"):
            try:
                dt = datetime.strptime(ts_raw, fmt)
                ts_clean = dt.strftime("%Y-%m-%dT%H:%M:%S")
                break
            except ValueError:
                pass
#milisegundo (opcional)
        if ts_clean is None and "T" in ts_raw and len(ts_raw) >= 19:
            try:
                dt = datetime.strptime(ts_raw[:19], "%Y-%m-%dT%H:%M:%S")
                ts_clean = dt.strftime("%Y-%m-%dT%H:%M:%S")
            except ValueError:
                ts_clean = None

        if ts_clean is None:
            bad_ts += 1
            continue  # saltar fila si no pudimos interpretar la fecha
        
#sistema de control de voltaje - si V>= a 5 V entonces lanza una alerta
        if val >= 5:
            control = "CUIDADO"
        else:
            control = "OK"
        voltajes.append(val)    
#grabar datos en writer
        writer.writerow({"Tiempo": ts_clean, "voltaje": f"{val:.2f}", "control":control})
        kept += 1 #sume 1 kept, en nuestro caso cambia de fila
        
#KPIs
n=len(voltajes)
if n==0:
    kips={"n": 0, "min": None, "max": None, "prom": None, "alerts": 0, "alerts_pct": 0.0} # por facilidad usaremos diccionarios
else:
    alertas=sum(v >= 5 for v in voltajes) #estructuras repetitivas simples
    kips={
        'n': n,
        'min': min(voltajes),
        "max": max(voltajes),
        "prom":mean(voltajes),
        "alerts": alertas,
        "alerts_pct": 100.0 * alertas / n,
    }

descartes_totales = bad_ts + bad_val            # equivale a (total - kept) con esta lógica
pct_descartadas = (descartes_totales / total * 100.0) if total else 0.0
kpis_calidad = {
    "filas_totales": total,
    "filas_validas": kept,
    "descartes_timestamp": bad_ts,
    "descartes_valor": bad_val,
    "%descartadas": round(pct_descartadas, 2),
}

#salida de pantalla y verificacion de KPIS
print(kips)
print(kpis_calidad)