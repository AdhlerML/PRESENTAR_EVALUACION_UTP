from datetime import datetime

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
