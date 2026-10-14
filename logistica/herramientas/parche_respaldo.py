#!/usr/bin/env python3
"""OPCIONAL (recomendado antes del examen): corrige 5 fallas del clasificador de respaldo
y de la política local en src/laya_ordenes/laya_ordenes/logic.py.

Fallas encontradas en evidencias/pregunta1/practica_calma.csv:
  1. "fuerza el brazo para recoger…" pasaba como PERMITIDA (regex 'forz' no cubre 'fuerza').
  2. "para" (preposición) se leía como DETENER  ("…brazo para recoger…").
  3. "mueve…" / "pon…" quedaban como acción 'otra' ('mov' no cubre 'mueve').
  4. "no coloques…" no se reconocía ('coloc' no cubre 'coloq').
  5. Colores en femenino (roja, amarilla) no se reconocían -> 10 errores de color.

En las 50 frases de práctica: respaldo 4 campos 30/50 -> 44/50, permitido 40/50 -> 50/50,
0 falsos permitidos (antes y después). OJO: medido sobre el MISMO conjunto con que se
diseñó el parche; validen con las 50 frases del docente.

Uso:
  cd ~/logistica            # o la carpeta del workspace que usen
  python3 herramientas/parche_respaldo.py src/laya_ordenes/laya_ordenes/logic.py
  python3 -m unittest discover -s tests -v
  colcon build --symlink-install --packages-select laya_ordenes

Deja una copia del original en logic.py.antes_parche. Para deshacer:
  mv src/laya_ordenes/laya_ordenes/logic.py.antes_parche src/laya_ordenes/laya_ordenes/logic.py
"""
import shutil
import sys

CAMBIOS = [
    (r"r'forz\w*|dan\w*|aplast\w*|salt\w*\s+seguridad)\b'",
     r"r'forz\w*|fuerz\w*|dan\w*|aplast\w*|salt\w*\s+seguridad)\b'"),
    (r"r'(?:recoj\w*|agarr\w*|tom\w*|levant\w*|coloc\w*|deposit\w*|mov\w*)\b'",
     r"r'(?:recoj\w*|agarr\w*|tom\w*|levant\w*|coloc\w*|coloq\w*|deposit\w*|mov\w*|muev\w*)\b'"),
    ('''    etiqueta = normalizar(etiqueta)
    return bool(re.search(r'(?<!\\w)' + re.escape(etiqueta) + r's?(?!\\w)', texto_norm))''',
     '''    etiqueta = normalizar(etiqueta)
    base = re.escape(etiqueta)
    if etiqueta in COLORES_BASE and etiqueta.endswith('o'):  # rojo/roja, amarillo/amarilla
        base = re.escape(etiqueta[:-1]) + '[oa]'
    return bool(re.search(r'(?<!\\w)' + base + r's?(?!\\w)', texto_norm))'''),
    (r"r'\b(deteng\w*|deten\w*|par\w*|cancel\w*)\b'",
     r"r'\b(deteng\w*|deten\w*|parar|pare\w*|cancel\w*)\b|^\s*para\b'"),
    (r"r'\b(coloc\w*|deposit\w*|dej\w*|traslad\w*|mov\w*)\b'",
     r"r'\b(coloc\w*|coloq\w*|deposit\w*|dej\w*|traslad\w*|mov\w*|muev\w*|pon|pone\w*)\b'"),
]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ruta = sys.argv[1]
    texto = open(ruta, encoding='utf-8').read()
    if 'fuerz\\w*' in texto:
        sys.exit('El parche ya parece aplicado (encontré "fuerz"). No hago nada.')
    for viejo, nuevo in CAMBIOS:
        if viejo not in texto:
            sys.exit('No encontré este fragmento (¿logic.py distinto?):\n' + viejo[:90])
        texto = texto.replace(viejo, nuevo)
    shutil.copy2(ruta, ruta + '.antes_parche')
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(texto)
    print(f'Parche aplicado a {ruta} (copia: {ruta}.antes_parche)')


if __name__ == '__main__':
    main()
