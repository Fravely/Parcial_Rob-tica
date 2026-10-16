#!/usr/bin/env python3
"""Evalua conjunto etiquetado de 50 frases por /interpretar_orden.
No crea ground truth ni declara exactitud sin datos. Corridas calma y carga por separado.
"""
import argparse,csv,statistics,time
from pathlib import Path
import rclpy
from rclpy.node import Node
from laya_ordenes_interfaces.srv import InterpretarOrden
from laya_ordenes.logic import clasificar_respaldo

def tasa(valores):
    return round(100*sum(valores)/len(valores),2) if valores else None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--entrada',required=True)
    ap.add_argument('--salida',required=True);ap.add_argument('--timeout',type=float,default=7.0)
    ap.add_argument('--objetos',nargs='+',default=['cubo','botella','pelota','caja'])
    ap.add_argument('--colores',nargs='+',default=['rojo','azul','verde','amarillo'])
    a=ap.parse_args()
    with open(a.entrada,encoding='utf-8',newline='') as f:frases=list(csv.DictReader(f))
    if len(frases)!=50:raise SystemExit(f'El docente debe entregar exactamente 50 frases; hay {len(frases)}')
    rclpy.init();nodo=Node('evaluador_laya_50');cli=nodo.create_client(InterpretarOrden,'/interpretar_orden')
    if not cli.wait_for_service(timeout_sec=10):raise SystemExit('No aparece /interpretar_orden')
    columnas=['frase','accion_esperada','objeto_esperado','color_esperado','prioridad_esperada','permitido_esperado']
    nuevos=['accion_laya','objeto_laya','color_laya','prioridad_laya','permitido_laya','fuente','degradada',
            'latencia_total_ms','latencia_http_ms','inferencia_ms','resto_http_ms',
            'accion_respaldo','objeto_respaldo','color_respaldo','prioridad_respaldo','permitido_respaldo',
            'acierto_laya','acierto_respaldo']
    salida=Path(a.salida);salida.parent.mkdir(parents=True,exist_ok=True)
    vs=[];aciertos_l=[];aciertos_r=[]
    with open(salida,'w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=columnas+nuevos);wr.writeheader()
        for row in frases:
            frase=row['frase'];t0=time.perf_counter();rq=InterpretarOrden.Request();rq.frase=frase
            fut=cli.call_async(rq);rclpy.spin_until_future_complete(nodo,fut,timeout_sec=a.timeout)
            if not fut.done() or fut.result() is None:
                raise SystemExit('Servicio no respondio: revisar /interpretar_orden y timeout')
            d=fut.result();ms=(time.perf_counter()-t0)*1000;vs.append(ms)
            respaldo=clasificar_respaldo(frase,a.objetos,a.colores)
            esperado=[row['accion_esperada'],row['objeto_esperado'],row['color_esperado'],row['permitido_esperado'].strip().lower()]
            # No comparar exactitud de prioridad sin criterio de tolerancia docente.
            ready=all(x for x in esperado)
            correct_l=ready and [d.accion,d.objeto,d.color,str(d.permitido).lower()]==esperado
            correct_r=ready and [respaldo['accion'],respaldo['objeto'],respaldo['color'],str(respaldo['permitido']).lower()]==esperado
            aciertos_l.append(correct_l if ready and not d.degradada else None)
            aciertos_r.append(correct_r if ready else None)
            wr.writerow({**{k:row.get(k,'') for k in columnas},'accion_laya':d.accion,'objeto_laya':d.objeto,
                'color_laya':d.color,'prioridad_laya':d.prioridad,'permitido_laya':d.permitido,
                'fuente':d.fuente,'degradada':d.degradada,'latencia_total_ms':round(ms,3),
                'latencia_http_ms':d.latencia_http_ms,'inferencia_ms':d.inferencia_ms,
                'resto_http_ms':d.resto_http_ms,'accion_respaldo':respaldo['accion'],
                'objeto_respaldo':respaldo['objeto'],'color_respaldo':respaldo['color'],
                'prioridad_respaldo':respaldo['prioridad'],'permitido_respaldo':respaldo['permitido'],
                'acierto_laya':correct_l if ready and not d.degradada else '',
                'acierto_respaldo':correct_r if ready else ''})
    print('CSV:',salida)
    print('Latencia total mediana ms:',round(statistics.median(vs),2))
    print('Latencia total p95 ms:',round(sorted(vs)[int((len(vs)-1)*.95)],2))
    al=[v for v in aciertos_l if v is not None]
    ar=[v for v in aciertos_r if v is not None]
    print('Exactitud LAYA real sobre',len(al),'frases etiquetadas/no degradadas:',tasa(al))
    print('Exactitud respaldo sobre',len(ar),'frases etiquetadas:',tasa(ar))
    if len(al)<50:print('ADVERTENCIA: falta medir 50 inferencias LAYA REALES; no atribuir respaldo a LAYA')
    nodo.destroy_node();rclpy.shutdown()
if __name__=='__main__':main()
