from pathlib import Path

def obtener_rutas():
    ROOT = Path(__file__).resolve().parents[2]
    in_file = ROOT / "PRESENTAR_EVALUACION_UTP" / "DATOS" / "DIRTY" / "sucio.csv"
    out_file = ROOT / "PRESENTAR_EVALUACION_UTP" / "DATOS" / "CLEAR" / "limpio.csv"
    return in_file, out_file
