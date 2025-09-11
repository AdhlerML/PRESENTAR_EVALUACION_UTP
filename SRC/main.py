from FUNCION.rutas import obtener_rutas
from FUNCION.archivo import procesar_archivo
from FUNCION.kpis import calcular_kpis

def main():
    in_file, out_file = obtener_rutas()
    filas_totales, filas_validas, descartes_ts, descartes_valor, temps = procesar_archivo(in_file, out_file)
    kips_temp, kpis_calidad = calcular_kpis(filas_totales, filas_validas, descartes_ts, descartes_valor, temps)
    print("KPIs de temperatura:", kips_temp)
    print("KPIs de calidad:", kpis_calidad)

if __name__ == "__main__":
    main()