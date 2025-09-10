from PROCESOS.rutas import obtener_rutas
from PROCESOS.archivo import procesar_archivo
from PROCESOS.kpis import calcular_kpis

def main():
    in_file, out_file = obtener_rutas()
    total, kept, bad_ts, bad_val, voltajes = procesar_archivo(in_file, out_file)
    kips, kpis_calidad = calcular_kpis(voltajes, total, kept, bad_ts, bad_val)
    print("KPIs de voltaje:", kips)
    print("KPIs de calidad:", kpis_calidad)

if __name__ == "__main__":
    main()
