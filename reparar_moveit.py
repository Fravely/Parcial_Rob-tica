#!/usr/bin/env python3
"""Crea config/moveit_local.yaml a partir del move_group en ejecucion.

Uso (con scripts/moveit.sh ya abierto en otra terminal):
    source scripts/entorno.sh && python3 reparar_moveit.py

Solo consulta parametros y escribe archivos dentro de este proyecto.
No importa pymycobot, no abre el puerto serie y no envia movimientos.
Limites del fabricante:
https://www.yahboom.net/study/JetCobot/14909/
"""
import ast
import copy
import datetime
import json
import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

LIMITES_YAHBOOM_GRADOS = [168.0, 135.0, 150.0, 145.0, 165.0, 180.0]



def aplanar(diccionario, prefijo=""):
    resultado = {}
    for clave, valor in diccionario.items():
        nombre = prefijo + clave
        if isinstance(valor, dict):
            resultado.update(aplanar(valor, nombre + "."))
        else:
            resultado[nombre] = valor
    return resultado


def leer_constantes_broker(archivo):
    valores = {}
    for nodo in ast.parse(Path(archivo).read_text(encoding="utf-8")).body:
        if isinstance(nodo, ast.Assign):
            for destino in nodo.targets:
                if isinstance(destino, ast.Name) and destino.id in ("JOINT_NAMES", "JOINT_LIMITS"):
                    valores[destino.id] = ast.literal_eval(nodo.value)
    nombres = valores["JOINT_NAMES"]
    limites = valores["JOINT_LIMITS"]
    if nombres != [f"{i}_Joint" for i in range(1, 7)] or len(limites) != 6:
        raise ValueError("Las articulaciones del broker no corresponden al modelo esperado.")
    return nombres, limites


def preparar_parametros(parametros, nombres, limites_broker, poses):
    originales = aplanar(copy.deepcopy(parametros))
    # El dump incluye parametros sin inicializar (null/NaN); no son overrides validos.
    p = {k: v for k, v in originales.items()
         if v is not None and not (isinstance(v, float) and not math.isfinite(v))
         and v != []}
    modelo = ET.fromstring(p["robot_description"])
    cambios = []
    for nombre, limites, maximo_grados in zip(nombres, limites_broker, LIMITES_YAHBOOM_GRADOS):
        lo, hi = map(float, limites)
        if not all(math.isfinite(v) for v in (lo, hi)) or lo >= hi:
            raise ValueError("Limites invalidos en el broker: " + nombre)
        maximo = math.radians(maximo_grados)
        lo, hi = max(lo, -maximo), min(hi, maximo)
        if lo >= hi:
            raise ValueError("Sin rango comun entre broker y fabricante: " + nombre)
        encontrados = [j for j in modelo.findall("joint") if j.get("name") == nombre]
        if len(encontrados) != 1 or encontrados[0].get("type") != "revolute":
            raise ValueError("Articulacion ausente o de otro tipo: " + nombre)
        joint = encontrados[0]
        limite = joint.find("limit")
        if limite is None:
            raise ValueError("Articulacion sin limites URDF: " + nombre)
        limite.set("lower", repr(lo))
        limite.set("upper", repr(hi))
        # Si hay limites suaves, se conservan y tambien restringen las poses.
        suave = joint.find("safety_controller")
        lo_efectivo, hi_efectivo = lo, hi
        if suave is not None:
            lo_efectivo = max(lo, float(suave.get("soft_lower_limit", lo)))
            hi_efectivo = min(hi, float(suave.get("soft_upper_limit", hi)))
        indice = nombres.index(nombre)
        for etiqueta, pose in poses.items():
            if len(pose) != 6:
                raise ValueError("Pose incompleta: " + etiqueta)
            q = math.radians(float(pose[indice]))
            if not math.isfinite(q) or not lo_efectivo <= q <= hi_efectivo:
                raise ValueError(f"Pose {etiqueta}: {nombre} fuera de los limites efectivos.")
        prefijo = "robot_description_planning.joint_limits." + nombre + "."
        p[prefijo + "has_position_limits"] = True
        p[prefijo + "min_position"] = lo
        p[prefijo + "max_position"] = hi
        cambios.append((nombre, math.degrees(lo), math.degrees(hi)))
    p["robot_description"] = ET.tostring(modelo, encoding="unicode")
    p["allow_trajectory_execution"] = False
    return p, cambios


def main():
    # PyYAML ya forma parte de la instalacion ROS del Jetson.
    import yaml
    proyecto = Path(__file__).resolve().parent
    nombres, limites = leer_constantes_broker(
        proyecto / "src/arm_broker/arm_broker/broker.py")
    c = json.loads((proyecto / "config/poses.json").read_text(encoding="utf-8"))
    # Las cuatro poses de recogida viven en posiciones_recogida (cuatro lugares fijos).
    poses = {nombre: lugar["grados"] for nombre, lugar in c["posiciones_recogida"].items()}
    poses.update(deposito=c["deposito_grados"], escaneo=c["escaneo_grados"], home=c["home_grados"])

    print("Leyendo el MoveIt abierto; no se envia ningun movimiento.", flush=True)
    salida = subprocess.check_output(
        ["ros2", "param", "dump", "/move_group"], text=True, timeout=30)
    documento = yaml.safe_load(salida)
    candidatos = [v["ros__parameters"] for v in documento.values()
                  if isinstance(v, dict) and "ros__parameters" in v]
    if len(candidatos) != 1:
        raise ValueError("No se obtuvo una unica configuracion de /move_group.")
    parametros, cambios = preparar_parametros(candidatos[0], nombres, limites, poses)
    nuevo_yaml = yaml.safe_dump({"/move_group": {"ros__parameters": parametros}},
                               sort_keys=False, allow_unicode=True)
    # Comprobar que el YAML guardado conserva valores y tipos antes de instalarlo.
    if yaml.safe_load(nuevo_yaml)["/move_group"]["ros__parameters"] != parametros:
        raise ValueError("No se pudo serializar la configuracion de MoveIt.")

    config = proyecto / "config"
    respaldo = config / ("respaldo_moveit_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    respaldo.mkdir()
    (respaldo / "parametros_originales.yaml").write_text(salida, encoding="utf-8")
    destino = config / "moveit_local.yaml"
    if destino.exists():
        (respaldo / "moveit_local_anterior.yaml").write_bytes(destino.read_bytes())
    temporal = config / "moveit_local.yaml.tmp"
    temporal.write_text(nuevo_yaml, encoding="utf-8", newline="\n")
    temporal.replace(destino)

    print("\nLIMITES LOCALES EN GRADOS (fabricante intersectado con broker):")
    for nombre, lo, hi in cambios:
        print(f"  {nombre}: {lo:.2f} a {hi:.2f}")
    print("\nCONFIGURACION LOCAL LISTA")
    print("Respaldo:", respaldo)
    print("Archivo:", destino)
    print("Deten TU MoveIt y TU broker con Ctrl+C.")
    print("Reinicia MoveIt con: bash scripts/moveit.sh  (ahora carga config/moveit_local.yaml)")
    print("Reinicia el broker en otra terminal con: bash scripts/broker.sh")
    print("No necesitas recompilar. Los archivos de /opt/ros permanecen intactos.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.SubprocessError, ET.ParseError) as exc:
        raise SystemExit("No se aplico la configuracion completa: " + str(exc))
