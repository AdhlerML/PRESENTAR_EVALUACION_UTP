from statistics import mean

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
