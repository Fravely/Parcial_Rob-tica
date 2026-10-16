#!/usr/bin/env python3
"""Exporta Bag ROS2 SQLite (.db3) de /arm/queue_state y /joint_states.
Ejemplo: python3 herramientas/exportar_csv.py evidencias/fifo_bag --salida evidencias/fifo_csv
Se ejecuta con source /opt/ros/humble/setup.bash + source install/setup.bash.
"""
import argparse,csv,json,sqlite3
from pathlib import Path
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

def exportar(bag, salida):
    bag=Path(bag); salida=Path(salida)
    if not bag.exists(): raise RuntimeError('No existe bag: '+str(bag))
    bases=sorted(bag.glob('*.db3')) if bag.is_dir() else [bag]
    if not bases or any(p.suffix!='.db3' for p in bases):
        raise RuntimeError('Solo bag sqlite3 .db3. Si es MCAP, vuelve a grabar con -s sqlite3.')
    salida.mkdir(parents=True, exist_ok=True)
    qrows=[]; jrows=[]
    for base in bases:
        con=sqlite3.connect(str(base))
        topicmap={i:(nm,ty) for i,nm,ty in con.execute('SELECT id,name,type FROM topics')}
        for topic_id,data,t_ns in con.execute('SELECT topic_id,data,timestamp FROM messages ORDER BY timestamp'):
            meta=topicmap.get(topic_id)
            if meta is None: continue
            nombre,tipo=meta
            if nombre not in ('/arm/queue_state','/joint_states'): continue
            msg=deserialize_message(bytes(data),get_message(tipo))
            if nombre=='/arm/queue_state':
                qrows.append({'t_ns':t_ns,'executing_client':msg.executing_client,
                    'executing_goal_id':msg.executing_goal_id,'executing_elapsed_s':msg.executing_elapsed_s,
                    'queue_length':msg.queue_length,
                    'queued_goal_ids':json.dumps(list(msg.queued_goal_ids)),
                    'queued_clients':json.dumps(list(msg.queued_clients)),
                    'queued_priorities':json.dumps(list(msg.queued_priorities)),
                    'queued_wait_s':json.dumps(list(msg.queued_wait_s)),
                    'total_accepted':msg.total_accepted,'total_rejected':msg.total_rejected,
                    'total_completed':msg.total_completed})
            else:
                jrows.append({'t_ns':t_ns,'names':json.dumps(list(msg.name)),
                              'position':json.dumps(list(msg.position))})
        con.close()
    for name,rows,fields in [
        ('queue_state.csv',qrows,['t_ns','executing_client','executing_goal_id','executing_elapsed_s',
            'queue_length','queued_goal_ids','queued_clients','queued_priorities','queued_wait_s',
            'total_accepted','total_rejected','total_completed']),
        ('joint_states.csv',jrows,['t_ns','names','position'])]:
        with open(salida/name,'w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=fields)
            writer.writeheader();writer.writerows(sorted(rows,key=lambda x:x['t_ns']))
    print(f'EXPORTADO {len(qrows)} queue_state y {len(jrows)} joint_states a {salida}')
    if not qrows: print('AVISO: no hay muestras de cola; revisa el bag y la interfaz')
    if not jrows: print('AVISO: NO hubo joint_states; en modo seguro esto es normal')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('bag');ap.add_argument('--salida',required=True)
    a=ap.parse_args();exportar(a.bag,a.salida)
