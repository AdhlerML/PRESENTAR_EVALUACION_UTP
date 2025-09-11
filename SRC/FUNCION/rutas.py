from pathlib import Path

def obtener_rutas():
    ROOT = Path(__file__).resolve().parents[2]
    
    in_file = ROOT /  "DATA" / "RAW" / "sucio.csv"
    out_file = ROOT /  "DATA" / "PROCESSED" / "Temperaturas_Procesado.csv"
    return in_file, out_file
