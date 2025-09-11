from statistics import mean

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
        "temp_min en C": temp_min,
        "temp_max en C": temp_max,
        "temp_prom en C": round(temp_prom, 2) if temp_prom else None,
        "alertas": alertas,
    }
    
    return kpis_calidad, kpis_temp
