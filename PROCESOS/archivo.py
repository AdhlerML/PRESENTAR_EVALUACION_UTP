import csv
from .limpieza import limpiar_valor, limpiar_timestamp
from .control import evaluar_control

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
