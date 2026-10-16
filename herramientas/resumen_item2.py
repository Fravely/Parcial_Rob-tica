#!/usr/bin/env python3
"""Tabla de DIEZ intentos reales. La revision humana contrasta el resultado con el video.

    python3 herramientas/resumen_item2.py evidencias/pregunta2/intentos.csv --ultimos 10 \
        --crear-revision evidencias/pregunta2/revision_video.csv     # 1) crea la plantilla
    # 2) completar objeto_correcto (si/no), zona_correcta (si/no) y evidencia (minuto del video)
    python3 herramientas/resumen_item2.py evidencias/pregunta2/intentos.csv --ultimos 10 \
        --revision evidencias/pregunta2/revision_video.csv           # 3) tabla definitiva

--ultimos 10 toma los diez ultimos intentos del CSV (si hubo ensayos antes de la demostracion).
"""
import argparse
import csv
from pathlib import Path

def resumir(archivo, revision=None, ultimos=0):
    with open(archivo, encoding='utf-8', newline='') as f:
        filas=list(csv.DictReader(f))
    if ultimos:
        filas=filas[-ultimos:]
    if len(filas)!=10 or len({f['goal_id'] for f in filas})!=10:
        raise ValueError('se requieren exactamente diez intentos distintos, incluidos fallos')
    revisiones={}
    if revision:
        with open(revision, encoding='utf-8', newline='') as f:
            for r in csv.DictReader(f):
                if r['goal_id'] in revisiones: raise ValueError('revision duplicada')
                revisiones[r['goal_id']]=r
        if set(revisiones)!={r['goal_id'] for r in filas}:
            raise ValueError('la revision debe cubrir exactamente los mismos diez intentos')
    salida=[]
    for i,r in enumerate(filas,1):
        v=revisiones.get(r['goal_id'])
        if v:
            if v['objeto_correcto'] not in ('si','no') or v['zona_correcta'] not in ('si','no') or not v['evidencia']:
                raise ValueError('completar si/no y evidencia en cada revision')
            exito=v['objeto_correcto']=='si' and v['zona_correcta']=='si'
        else:
            exito=r['physical_verified']=='True'
        error=r['position_error_mm']
        # Una entrega exitosa sin lectura articular tiene metrica pendiente, nunca cero.
        error=error if exito and error and float(error)>=0 else ''
        agarre=r.get('error_agarre_mm','')
        agarre=agarre if agarre and float(agarre)>=0 else ''
        salida.append(dict(intento=i,goal_id=r['goal_id'],cliente=r.get('cliente',''),
            accion=r.get('accion',''),color=r['color'],zona=r['zona'],
            fuente=r['fuente'],degradada=r['degradada'],exito=exito,
            error_fk_deposito_mm=error,error_fk_agarre_mm=agarre,
            criterio='video_revisado' if v else 'vision_automatica_provisional',
            resultado_ejecucion=r['success'],observacion=r['message']))
    return salida

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv');p.add_argument('--revision');p.add_argument('--crear-revision')
    p.add_argument('--salida',default='evidencias/pregunta2/tabla_10_intentos.csv')
    p.add_argument('--ultimos',type=int,default=0,help='usar solo los N ultimos intentos del CSV')
    a=p.parse_args()
    filas=resumir(a.csv,a.revision,a.ultimos)
    if a.crear_revision:
        with open(a.crear_revision,'w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=['goal_id','objeto_correcto','zona_correcta','evidencia'])
            w.writeheader()
            w.writerows({'goal_id':r['goal_id']} for r in filas)
        print('Completar la revision con el video y volver a ejecutar con --revision.')
    salida=Path(a.salida);salida.parent.mkdir(parents=True,exist_ok=True)
    with salida.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(filas[0]));w.writeheader();w.writerows(filas)
    exitos=sum(r['exito'] for r in filas)
    print(f'Exito: {exitos}/10 = {exitos*10:.0f}%')
    if not a.revision: print('PROVISIONAL: criterio visual; revisar objeto y zona en el video.')
    if any(r['fuente']!='LAYA' or r['degradada']=='True' for r in filas):
        print('Incluye respaldo: NO demuestra prioridad proveniente de LAYA para todo el ensayo.')
    if any(r['exito'] and not r['error_fk_deposito_mm'] for r in filas):
        print('Hay exitos sin error FK medido: metrica pendiente.')
    print(salida)

if __name__=='__main__':
    main()
