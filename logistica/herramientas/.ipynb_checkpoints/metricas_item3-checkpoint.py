#!/usr/bin/env python3
"""Resumen RB2 ítem 3 con CSV REALES de 4 clientes.
No calcula mediciones inventadas. Jain de 1/(1+espera media) por cliente,
no de objetivos idénticos completados: esa métrica sería trivial si cada cliente completó N.
"""
import argparse,csv,glob,statistics,math
from collections import defaultdict
from pathlib import Path

def percentil(v,p=.95):
    if not v:return None
    a=sorted(v); posicion=(len(a)-1)*p;lo=int(posicion);hi=min(lo+1,len(a)-1)
    return a[lo]+(a[hi]-a[lo])*(posicion-lo)
def resumen(patron):
    archivos=sorted(glob.glob(patron))
    if not archivos: raise ValueError('No se encontraron CSV: '+patron)
    filas=[]
    for p in archivos:
        with open(p,encoding='utf-8',newline='') as f: filas += list(csv.DictReader(f))
    buenos=[f for f in filas if f['estado']=='OK' and f['espera_s']!='']
    por=defaultdict(list)
    for f in buenos:por[f['cliente']].append(float(f['espera_s']))
    ws=[w for ls in por.values() for w in ls]
    scores=[1/(1+statistics.mean(w)) for w in por.values()]
    jain=(sum(scores)**2)/(len(scores)*sum(x*x for x in scores)) if scores else None
    tfin=[float(f['t_fin_unix']) for f in filas if f.get('t_fin_unix')]
    from datetime import datetime
    tinicio=[]
    for f in filas:
        try:tinicio.append(datetime.fromisoformat(f['fecha_envio']).timestamp())
        except ValueError:pass
    duracion=(max(tfin)-min(tinicio)) if tinicio and tfin else None
    throughput=(len(buenos)/duracion) if duracion and duracion>0 else None
    return dict(archivos=archivos,total=len(filas),ok=len(buenos),rechazados=sum(f['estado']=='RECHAZADO' for f in filas),
                mediana_s=statistics.median(ws) if ws else None,p95_s=percentil(ws),
                max_s=max(ws) if ws else None,jain_espera=jain,throughput_goals_s=throughput,
                clientes={k:{'n':len(v),'mediana_s':statistics.median(v),'p95_s':percentil(v),
                             'media_s':statistics.mean(v)} for k,v in sorted(por.items())})
def fmt(x):return 'N/D' if x is None else f'{x:.4f}'
def imprimir(nombre,s):
    print(f'\n### {nombre}: {len(s["archivos"])} CSV, {s["total"]} pedidos, OK={s["ok"]}, rechazados={s["rechazados"]}')
    for k in ('mediana_s','p95_s','max_s','jain_espera','throughput_goals_s'):
        print(f'{k:24s}: {fmt(s[k])}')
    for cli,v in s['clientes'].items():
        print(f'  {cli}: n={v["n"]} espera mediana={fmt(v["mediana_s"])} p95={fmt(v["p95_s"])}')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--fifo',required=True,help='glob, entre comillas');ap.add_argument('--prioridad',required=True)
    a=ap.parse_args()
    imprimir('FIFO',resumen(a.fifo));imprimir('PRIORIDAD',resumen(a.prioridad))
    print('\nAtencion: los resultados son de ejecucion REAL solo si broker.publicar_joint_states=true y el driver actuó.')
    print('Jain definido en el docstring, no equivale a tasa de agarres correctos.')
