#!/usr/bin/env python3
"""Marcar las regiones de la camara sobre una imagen, SIN mover el brazo.

Usa una imagen tomada DESDE la pose de escaneo. No importa ROS ni arm_broker a
proposito: asi corre en cualquier laptop con OpenCV y escritorio, aunque no tenga
ROS 2 instalado (en JupyterLab no hay ventanas y cv.selectROI no funciona).

    python3 herramientas/marcar_regiones_item2.py \
        --imagen escaneo.png \
        --config plantillas/item2_montaje.json \
        --salida plantillas/item2_calibrado.json

El archivo de entrada NO se modifica. Si deposito_grados trae una pose por color,
pide tambien una region de deposito por color.
"""
import argparse
import json
from pathlib import Path

COLORES = ('amarillo', 'azul', 'verde', 'rojo')


def solapan(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return max(ax, bx) < min(ax + aw, bx + bw) and max(ay, by) < min(ay + ah, by + bh)


def main():
    import cv2 as cv
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', default='plantillas/item2_montaje.json')
    p.add_argument('--imagen', required=True, help='PNG tomada con el brazo en escaneo')
    p.add_argument('--salida', default='plantillas/item2_calibrado.json')
    a = p.parse_args()

    c = json.loads(Path(a.config).read_text(encoding='utf-8'))
    frame = cv.imread(a.imagen)
    if frame is None:
        raise SystemExit('no se pudo leer la imagen ' + a.imagen)
    alto, ancho = frame.shape[:2]
    c['alto_imagen'], c['ancho_imagen'] = int(alto), int(ancho)

    por_color = isinstance(c.get('deposito_grados'), dict)
    nombres = list(COLORES) + (['deposito_' + x for x in COLORES] if por_color else ['deposito'])

    print(f'Imagen {ancho}x{alto}. La camara debe quedar EXACTAMENTE asi durante todo el ensayo.')
    print('Selecciona un rectangulo por posicion; ENTER acepta, C cancela.')
    print('Ajusta la region al lugar de agarre: no incluyas las posiciones vecinas.')
    regiones = {}
    try:
        for nombre in nombres:
            r = tuple(int(v) for v in cv.selectROI('Posicion: ' + nombre, frame, False))
            cv.destroyAllWindows()
            if min(r[2:]) <= 0:
                raise SystemExit('seleccion cancelada: no se guardo nada')
            for otro, caja in regiones.items():
                if solapan(r, caja):
                    raise SystemExit(f'la region {nombre} se solapa con {otro}: repite el marcado')
            regiones[nombre] = list(r)
    finally:
        cv.destroyAllWindows()

    c['regiones'] = regiones
    # El montaje sigue SIN validar: falta comprobar el modelo, la aproximacion y la pinza.
    c['montaje_validado'] = False
    salida = Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Guardado: ' + str(salida))
    print('Falta: previsualizar los planes y, solo entonces, poner montaje_validado en true.')


if __name__ == '__main__':
    main()
