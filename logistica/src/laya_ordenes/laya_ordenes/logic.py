"""Lógica pura: preguntas tipadas para LAYA y clasificador degradado seguro.

Sin importaciones de ROS: se puede probar en un equipo sin JetCobot.
"""
import math
import re
import unicodedata


ACCIONES = {
    'recoger': 'Agarrar, recoger, tomar o levantar un objeto de la mesa con la pinza.',
    'colocar': 'Depositar, dejar, colocar o trasladar un objeto a una zona indicada.',
    'detener': 'Parar o cancelar el trabajo del robot.',
    'peligrosa': 'Golpear, lanzar, romper, forzar el brazo o ignorar normas de seguridad.',
    'otra': 'No hay una orden reconocible de manipulación de objetos.'
}
COLORES_BASE = ['rojo', 'azul', 'verde', 'amarillo']
PROHIBIDAS = re.compile(
    r'\b(golpe\w*|romp\w*|lanz\w*|arroj\w*|desactiv\w*|'
    r'forz\w*|dan\w*|aplast\w*|salt\w*\s+seguridad)\b'
)
# Una orden negativa no equivale a una autorización para mover el brazo.
NEGADA = re.compile(
    r'\bno\s+(?:quiero\s+que\s+|debes\s+|vayas\s+a\s+)?'
    r'(?:recoj\w*|agarr\w*|tom\w*|levant\w*|coloc\w*|deposit\w*|mov\w*)\b'
)


def normalizar(texto):
    texto = unicodedata.normalize('NFKD', texto.casefold())
    return ''.join(c for c in texto if not unicodedata.combining(c))


def contiene_etiqueta(texto_norm, etiqueta):
    """Busca palabras completas, sin admitir cubo dentro de 'cubosidad'."""
    etiqueta = normalizar(etiqueta)
    return bool(re.search(r'(?<!\w)' + re.escape(etiqueta) + r's?(?!\w)', texto_norm))


def limpiar_catalogo(items):
    resultado = []
    for x in items:
        x = normalizar(str(x).strip())
        if x and x not in ('otro', 'ninguno') and x not in resultado:
            resultado.append(x)
    return resultado


def preguntas(objetos, colores):
    objs = {o: f'Objeto físico disponible sobre la mesa: {o}.' for o in objetos}
    objs.update({'otro': 'Se pide otro objeto fuera del inventario.',
                 'ninguno': 'No se indica ningún objeto.'})
    cols = {c: f'El objeto solicitado es de color {c}.' for c in colores}
    cols.update({'otro': 'Se pide un color distinto de los configurados.',
                 'ninguno': 'No se especifica el color.'})
    return {
        'accion': {'type': 'choice', 'instructions': '¿Qué acción pide el operador?',
                   'criteria': ACCIONES},
        'objeto': {'type': 'choice', 'instructions': '¿Qué objeto menciona?', 'criteria': objs},
        'color': {'type': 'choice', 'instructions': '¿Qué color menciona?', 'criteria': cols},
        'prioridad': {
            'type': 'score', 'instructions': 'Nivel de urgencia de la orden, de bajo a alto.',
            'criteria': ['sin urgencia', 'baja', 'normal', 'alta', 'emergente']
        },
        'autorizacion': {
            'type': 'noul',
            'instructions': '¿La instrucción autoriza manipular sin dañar objetos, personas o el brazo y sin violar la seguridad?',
            'criteria': {
                'false': 'La orden no autoriza una manipulación segura o pide daño, fuerza o conducta prohibida.',
                'true': 'La orden autoriza una manipulación inocua de un objeto de la mesa.'
            }
        }
    }


def politica_local(frase, accion, objeto, color, objetos, colores):
    """Regla de bloqueo local, aun cuando el modelo vote sí."""
    texto = normalizar(frase)
    if PROHIBIDAS.search(texto) or NEGADA.search(texto):
        return False, 'orden negativa o potencialmente peligrosa'
    if accion not in ('recoger', 'colocar'):
        return False, 'acción no ejecutable por este puente'
    if objeto not in objetos:
        return False, 'objeto desconocido o no disponible en el inventario'
    if color not in colores:
        return False, 'color no configurado'
    # Una clasificación inferida nunca debe introducir un objeto/color que no se pidió.
    if not contiene_etiqueta(texto, objeto) or not contiene_etiqueta(texto, color):
        return False, 'objeto o color no consta explícitamente en la frase'
    return True, 'orden autorizable; falta validación física antes del movimiento'


def clasificar_respaldo(frase, objetos, colores):
    texto = normalizar(frase)
    if PROHIBIDAS.search(texto):
        accion = 'peligrosa'
    elif re.search(r'\b(deteng\w*|deten\w*|par\w*|cancel\w*)\b', texto):
        accion = 'detener'
    elif re.search(r'\b(recoj\w*|recog\w*|agarr\w*|tom\w*|levant\w*)\b', texto):
        accion = 'recoger'
    elif re.search(r'\b(coloc\w*|deposit\w*|dej\w*|traslad\w*|mov\w*)\b', texto):
        accion = 'colocar'
    else:
        accion = 'otra'
    objeto = next((o for o in objetos if contiene_etiqueta(texto, o)), 'ninguno')
    color = next((c for c in colores if contiene_etiqueta(texto, c)), 'ninguno')
    prio = 180 if re.search(r'\b(urgente|inmediatamente|ahora|rapido)\b', texto) else (
        20 if 'sin prisa' in texto or 'cuando puedas' in texto else 80)
    ok, motivo = politica_local(frase, accion, objeto, color, objetos, colores)
    return dict(accion=accion, objeto=objeto, color=color, prioridad=prio,
                permitido=ok, motivo=motivo)


def _eleccion(answers, campo, opciones, confianza_minima):
    answer = answers[campo]
    if answer.get('type') != 'choice':
        raise ValueError(f'{campo}: respuesta no es choice')
    eleccion = answer.get('choice')
    if eleccion not in opciones:
        raise ValueError(f'{campo}: elección desconocida {eleccion!r}')
    probabilidades = answer.get('probabilities', {})
    conf = answer.get('answer_confidence', probabilidades.get(eleccion))
    if conf is not None and (not isinstance(conf, (int, float)) or
                             not math.isfinite(conf) or conf < confianza_minima):
        raise ValueError(f'{campo}: confianza insuficiente')
    return eleccion


def analizar_laya(respuesta, frase, objetos, colores, confianza_minima=0.50):
    answers = respuesta['answers']
    accion = _eleccion(answers, 'accion', ACCIONES, confianza_minima)
    objeto = _eleccion(answers, 'objeto', set(objetos) | {'otro', 'ninguno'}, confianza_minima)
    color = _eleccion(answers, 'color', set(colores) | {'otro', 'ninguno'}, confianza_minima)
    p = answers['prioridad']
    if p.get('type') != 'score':
        raise ValueError('prioridad: respuesta no es score')
    score = float(p['score'])
    if not math.isfinite(score):
        raise ValueError('prioridad no finita')
    prioridad = max(0, min(255, int(round(score * 50))))
    autorizacion = answers['autorizacion']
    if autorizacion.get('type') != 'noul':
        raise ValueError('autorizacion: respuesta no es noul')
    prob_si = float(autorizacion['noul'])
    if not math.isfinite(prob_si) or not 0 <= prob_si <= 1:
        raise ValueError('autorizacion fuera de 0..1')
    permitido_local, motivo = politica_local(frase, accion, objeto, color, objetos, colores)
    permitido = prob_si >= 0.60 and permitido_local
    if prob_si < 0.60:
        motivo = f'LAYA no autoriza (probabilidad sí={prob_si:.2f})'
    return dict(accion=accion, objeto=objeto, color=color, prioridad=prioridad,
                permitido=permitido, motivo=motivo)


def inferencia_header(cabeceras):
    """Devuelve la medición del servidor, o -1 si no existe (no inventa cifras)."""
    raw = cabeceras.get('X-Inference-Time-Ms')
    if raw is None:
        timing = cabeceras.get('Server-Timing', '')
        m = re.search(r'(?:^|,)\s*inference\s*;\s*dur\s*=\s*([0-9.]+)', timing, re.I)
        raw = m.group(1) if m else None
    try:
        valor = float(raw)
        return valor if math.isfinite(valor) and valor >= 0 else -1.0
    except (ValueError, TypeError):
        return -1.0
