"""Interfaz web para escribir la orden (prompt) y enviarla a la cadena.

    ros2 run laya_ordenes interfaz_ordenes --ros-args -p puerto_web:=8090

Luego, desde la PC de CADA integrante (misma red del laboratorio), abrir:

    http://IP_DEL_JETSON:8090        (ej. http://172.51.1.18:8090)

Qué hace con cada orden escrita:
  1. Llama al servicio /interpretar_orden (Pregunta 1). NO habla con LAYA directo.
  2. Si permitido=False -> la rechaza ANTES de encolar y muestra la causa.
  3. Si permitido=True y la casilla "Encolar" está marcada -> envía el goal a la
     acción del broker (/pick_place) con la PRIORIDAD que decidió el modelo.
  4. Muestra en vivo la cola del broker (/arm/queue_state) y el avance de cada pedido.

No publica nada al brazo: el worker del broker sigue siendo el único publicador.
Evidencia: CSV en evidencias/interfaz/ordenes_interfaz.csv y el tópico
/interfaz/ordenes (std_msgs/String con JSON) para grabarlo con ros2 bag.
"""
import csv
import datetime
import json
import os
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String

try:
    from .cadena import ClienteCadena, Seguimiento
except ImportError:  # ejecutado como script: python3 interfaz_ordenes.py
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from cadena import ClienteCadena, Seguimiento


class InterfazOrdenes(Node):
    def __init__(self):
        super().__init__('interfaz_ordenes')
        self.declare_parameter('host', '0.0.0.0')
        self.declare_parameter('puerto_web', 8090)
        self.declare_parameter('accion_broker', '/logistica/pick_place')
        self.declare_parameter('topico_cola', '')
        self.declare_parameter('zona', 'deposito')
        self.declare_parameter('timeout_decision_s', 5.0)
        self.declare_parameter('registro_csv', os.path.expanduser(
            '~/logistica/evidencias/interfaz/ordenes_interfaz.csv'))

        self.zona = str(self.get_parameter('zona').value)
        self.timeout_decision = float(self.get_parameter('timeout_decision_s').value)
        self.csv = str(self.get_parameter('registro_csv').value)
        if self.csv:
            os.makedirs(os.path.dirname(os.path.abspath(self.csv)), exist_ok=True)
        self.lock = threading.Lock()
        self.ordenes = {}          # id -> dict listo para JSON
        self.orden_ids = []        # orden de llegada
        self.registrados = set()
        self.pub = self.create_publisher(String, '/interfaz/ordenes', 10)
        self.cadena = ClienteCadena(self, str(self.get_parameter('accion_broker').value),
                                    al_actualizar=self._actualizar,
                                    topico_cola=str(self.get_parameter('topico_cola').value))

    # --------------------------------------------------------- estado
    def _actualizar(self, seg):
        d = seg.como_dict()
        with self.lock:
            if seg.id not in self.ordenes:
                self.orden_ids.append(seg.id)
            self.ordenes[seg.id] = d
            del self.orden_ids[:-60]
            terminado = seg.terminado.is_set() and seg.id not in self.registrados
            if terminado:
                self.registrados.add(seg.id)
        if terminado:
            self._registrar(d)

    def _registrar(self, d):
        dec = d.get('decision') or {}
        fila = {
            'fecha': datetime.datetime.now().isoformat(timespec='milliseconds'),
            'id': d['id'], 'cliente': d['cliente'], 'frase': d['frase'],
            'accion': dec.get('accion', ''), 'objeto': dec.get('objeto', ''),
            'color': dec.get('color', ''), 'prioridad': dec.get('prioridad', ''),
            'permitido': dec.get('permitido', ''), 'degradada': dec.get('degradada', ''),
            'fuente': dec.get('fuente', ''), 'motivo': dec.get('motivo', ''),
            'ms_decision': dec.get('ms_decision', ''), 'estado_final': d['estado'],
            'mensaje': d['mensaje'], 'exito': d['exito'],
            'wait_time_s': d['wait_time_s'], 'exec_time_s': d['exec_time_s'],
            't_envio': d['t_envio'], 't_aceptado': d['t_aceptado'],
            't_salida_cola': d['t_salida_cola'], 't_inicio_mov': d['t_inicio_mov'],
            't_fin': d['t_fin'], 'physical_verified': d.get('physical_verified'),
            'position_error_mm': d.get('position_error_mm'),
            'etapas_broker': json.dumps(d.get('etapas', []), ensure_ascii=False),
            'feedback': json.dumps(d['feedback'], ensure_ascii=False),
        }
        msg = String()
        msg.data = json.dumps(fila, ensure_ascii=False, default=str)
        self.pub.publish(msg)
        if not self.csv:
            return
        try:
            with self.lock:
                nuevo = not os.path.exists(self.csv) or os.path.getsize(self.csv) == 0
                with open(self.csv, 'a', newline='', encoding='utf-8') as f:
                    w = csv.DictWriter(f, fieldnames=list(fila))
                    if nuevo:
                        w.writeheader()
                    w.writerow(fila)
        except OSError as exc:
            self.get_logger().warn(f'No pude escribir {self.csv}: {exc}')

    def estado(self):
        with self.lock:
            ordenes = [self.ordenes[i] for i in reversed(self.orden_ids)]
        cli_b = self.cadena.cli_broker
        return {
            'interprete': self.cadena.cli_interprete.service_is_ready(),
            'broker': bool(cli_b is not None and cli_b.server_is_ready()),
            'pickplace_disponible': cli_b is not None,
            'cola': self.cadena.estado_cola,
            'ordenes': ordenes,
            'ahora': time.time(),
        }

    # --------------------------------------------------------- orden
    def procesar(self, cliente, frase, encolar):
        cliente = (cliente or 'web').strip()[:40] or 'web'
        frase = (frase or '').strip()[:300]
        if not frase:
            return 400, {'ok': False, 'error': 'Escribe una orden.'}
        try:
            decision, ms = self.cadena.interpretar(frase, self.timeout_decision)
        except Exception as exc:
            self.get_logger().warn(f'[{cliente}] sin decisión: {exc}')
            return 503, {'ok': False, 'error': f'Sin decisión: {exc}'}
        self.get_logger().info(
            f'[{cliente}] "{frase}" -> {decision["accion"]}/{decision["objeto"]}/'
            f'{decision["color"]} prio={decision["prioridad"]} '
            f'permitido={decision["permitido"]} fuente={decision.get("fuente")} ({ms:.0f} ms)')
        decision['ms_decision'] = round(ms, 1)
        if encolar or not decision['permitido']:
            seg = self.cadena.enviar_al_broker(decision, cliente, frase, self.zona)
            if seg.estado == 'rechazada_antes_de_encolar':
                self.get_logger().warn(f'[{cliente}] RECHAZADA antes de encolar: {seg.mensaje}')
        else:  # permitida, pero el usuario solo quería ver la decisión
            seg = Seguimiento(uuid.uuid4().hex[:8], cliente, frase, decision)
            seg.estado, seg.mensaje, seg.t_fin = 'solo_interpretada', 'no se encoló', time.time()
            seg.terminado.set()
            self._actualizar(seg)
        return 200, {'ok': True, 'decision': decision, 'ms_decision': round(ms, 1)}


PAGINA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>JetCobot · Órdenes</title>
<style>
:root{--bg:#f4f5f7;--card:#fff;--ink:#1d2330;--mute:#667085;--line:#e3e6eb;
--acc:#0b6bcb;--ok:#127a3d;--okbg:#e6f4ec;--bad:#b42318;--badbg:#fdecea;--warn:#8a5a00;--warnbg:#fff4dc}
*{box-sizing:border-box}body{margin:0;font:15px/1.45 system-ui,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--ink)}
header{background:#14213d;color:#fff;padding:14px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header h1{font-size:18px;margin:0;font-weight:650}.pill{font-size:12px;padding:3px 9px;border-radius:99px;background:#2b3a5c}
.pill.on{background:#1f7a45}.pill.off{background:#9b2c2c}
main{max-width:1100px;margin:0 auto;padding:18px;display:grid;grid-template-columns:1.1fr .9fr;gap:16px}
@media(max-width:820px){main{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
h2{font-size:15px;margin:0 0 10px}label{font-size:13px;color:var(--mute);display:block;margin:8px 0 4px}
input[type=text],textarea{width:100%;padding:10px;border:1px solid var(--line);border-radius:8px;font:inherit}
textarea{min-height:84px;resize:vertical}
.fila{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:10px}
button{background:var(--acc);color:#fff;border:0;border-radius:8px;padding:10px 18px;font:inherit;font-weight:600;cursor:pointer}
button:disabled{opacity:.5;cursor:wait}.chips button{background:#eef3fb;color:#0b4d93;font-weight:500;padding:6px 10px;font-size:13px}
.res{margin-top:12px;padding:12px;border-radius:10px;display:none}.res.ok{background:var(--okbg)}.res.bad{background:var(--badbg)}
.kv{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}.kv div{background:#ffffffaa;border-radius:6px;padding:6px}
.kv b{display:block;font-size:11px;color:var(--mute);font-weight:500}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:6px 4px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--mute);font-weight:500}.b{font-size:12px;padding:2px 7px;border-radius:99px;white-space:nowrap}
.b.completada{background:var(--okbg);color:var(--ok)}.b.fallida,.b.error,.b.rechazada_antes_de_encolar,.b.rechazada_por_broker{background:var(--badbg);color:var(--bad)}
.b.en_cola,.b.enviado,.b.ejecutando,.b.sin_broker,.b.solo_interpretada{background:var(--warnbg);color:var(--warn)}
.cola li{margin:4px 0}.muted{color:var(--mute);font-size:13px}
</style></head><body>
<header><h1>JetCobot · Órdenes en lenguaje natural</h1>
<span id="pi" class="pill">intérprete…</span><span id="pb" class="pill">broker…</span></header>
<main>
<section class="card">
  <h2>Nueva orden</h2>
  <label for="cli">Integrante (client_id)</label>
  <input id="cli" type="text" placeholder="ej. sebastian">
  <label for="fr">Orden (prompt)</label>
  <textarea id="fr" placeholder="ej. recoge el cubo rojo urgente"></textarea>
  <div class="fila chips">
    <button type="button" data-f="recoge el cubo rojo urgente">cubo rojo urgente</button>
    <button type="button" data-f="toma el cubo azul cuando puedas">cubo azul sin prisa</button>
    <button type="button" data-f="recoge la pelota morada">objeto inexistente</button>
    <button type="button" data-f="golpea el cubo verde">orden no permitida</button>
  </div>
  <div class="fila">
    <label style="margin:0;color:var(--ink)"><input id="enc" type="checkbox" checked> Encolar en el broker si está permitida</label>
    <button id="env" style="margin-left:auto">Enviar orden</button>
  </div>
  <div id="res" class="res"></div>
  <p class="muted">Ctrl+Enter también envía. La prioridad NO se escribe a mano: la decide el modelo.</p>
</section>
<section class="card">
  <h2>Cola del broker</h2>
  <div id="cola" class="muted">Sin datos de /arm/queue_state todavía.</div>
</section>
<section class="card" style="grid-column:1/-1">
  <h2>Pedidos recientes (todos los integrantes)</h2>
  <div style="overflow-x:auto"><table><thead><tr><th>Hora</th><th>Integrante</th><th>Orden</th><th>Decisión</th><th>Prio</th><th>Estado</th><th>Detalle</th></tr></thead>
  <tbody id="tb"></tbody></table></div>
</section>
</main>
<script>
const $=s=>document.querySelector(s);
try{$('#cli').value=localStorage.getItem('cli')||''}catch(e){}
document.querySelectorAll('[data-f]').forEach(b=>b.onclick=()=>{$('#fr').value=b.dataset.f;$('#fr').focus()});
$('#fr').addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey))enviar()});
$('#env').onclick=enviar;
function td(t){const c=document.createElement('td');c.textContent=t==null?'':t;return c}
async function enviar(){
  const cliente=$('#cli').value.trim()||'web',frase=$('#fr').value.trim();if(!frase)return;
  try{localStorage.setItem('cli',cliente)}catch(e){}
  $('#env').disabled=true;const r=$('#res');r.style.display='block';r.className='res';r.textContent='Interpretando…';
  try{
    const resp=await fetch('/api/orden',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({cliente,frase,encolar:$('#enc').checked})});
    const j=await resp.json();
    if(!j.ok){r.className='res bad';r.textContent=j.error;return}
    const d=j.decision;r.className='res '+(d.permitido?'ok':'bad');r.innerHTML='';
    const h=document.createElement('div');h.style.fontWeight='600';
    h.textContent=(d.permitido?'PERMITIDA':'RECHAZADA antes de encolar')+' · '+(d.fuente||'')+(d.degradada?' (degradada)':'')+' · '+j.ms_decision+' ms';
    r.appendChild(h);const kv=document.createElement('div');kv.className='kv';
    [['acción',d.accion],['objeto',d.objeto],['color',d.color],['prioridad',d.prioridad]].forEach(([k,v])=>{
      const x=document.createElement('div');const b=document.createElement('b');b.textContent=k;x.appendChild(b);x.append(String(v));kv.appendChild(x)});
    r.appendChild(kv);const m=document.createElement('div');m.className='muted';m.style.marginTop='6px';m.textContent='Motivo: '+(d.motivo||'');r.appendChild(m);
    $('#fr').value='';
  }catch(e){r.className='res bad';r.textContent='Error de red: '+e}
  finally{$('#env').disabled=false;refrescar()}
}
async function refrescar(){
  try{
    const j=await (await fetch('/api/estado')).json();
    $('#pi').className='pill '+(j.interprete?'on':'off');$('#pi').textContent='intérprete '+(j.interprete?'listo':'no disponible');
    $('#pb').className='pill '+(j.broker?'on':'off');$('#pb').textContent=j.pickplace_disponible?('broker '+(j.broker?'listo':'no disponible')):'sin acción PickPlace';
    const c=j.cola,box=$('#cola');
    if(c){box.innerHTML='';const p=document.createElement('div');
      p.textContent='Ejecutando: '+(c.ejecutando||'—')+(c.ejecutando?' ('+c.ejecutando_s+' s)':'')+' · En cola: '+c.longitud+' · aceptados '+c.aceptados+' / rechazados '+c.rechazados+' / completados '+c.completados;
      box.appendChild(p);const ul=document.createElement('ol');ul.className='cola';
      c.clientes.forEach((cl,i)=>{const li=document.createElement('li');li.textContent=cl+' · prio '+c.prioridades[i]+' · espera '+c.espera_s[i]+' s';ul.appendChild(li)});
      box.appendChild(ul)}
    const tb=$('#tb');tb.innerHTML='';
    j.ordenes.forEach(o=>{const tr=document.createElement('tr');const d=o.decision||{};
      const hora=new Date(((o.t_creado||o.t_envio||j.ahora))*1000).toLocaleTimeString();
      tr.appendChild(td(hora));tr.appendChild(td(o.cliente));tr.appendChild(td(o.frase));
      tr.appendChild(td([d.accion,d.objeto,d.color].join(' / ')));tr.appendChild(td(d.prioridad));
      const e=document.createElement('td');const s=document.createElement('span');s.className='b '+o.estado;s.textContent=o.estado.replaceAll('_',' ');e.appendChild(s);tr.appendChild(e);
      let det=o.mensaje||'';if(o.posicion_cola>0)det='posición '+o.posicion_cola+' · '+det;
      if(o.wait_time_s!=null)det+=' · espera '+o.wait_time_s.toFixed(2)+' s, ejec '+o.exec_time_s.toFixed(2)+' s';
      tr.appendChild(td(det));tb.appendChild(tr)});
  }catch(e){}
}
setInterval(refrescar,1000);refrescar();
</script></body></html>"""


def crear_handler(nodo):
    class Handler(BaseHTTPRequestHandler):
        def _json(self, codigo, datos):
            cuerpo = json.dumps(datos, ensure_ascii=False, default=str).encode('utf-8')
            self.send_response(codigo)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)

        def do_GET(self):
            if self.path in ('/', '/index.html'):
                cuerpo = PAGINA.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(cuerpo)))
                self.end_headers()
                self.wfile.write(cuerpo)
            elif self.path.startswith('/api/estado'):
                self._json(200, nodo.estado())
            else:
                self._json(404, {'ok': False, 'error': 'no existe'})

        def do_POST(self):
            if not self.path.startswith('/api/orden'):
                return self._json(404, {'ok': False, 'error': 'no existe'})
            try:
                largo = min(int(self.headers.get('Content-Length', 0)), 10000)
                datos = json.loads(self.rfile.read(largo).decode('utf-8') or '{}')
            except (ValueError, UnicodeDecodeError):
                return self._json(400, {'ok': False, 'error': 'JSON inválido'})
            codigo, resp = nodo.procesar(datos.get('cliente'), datos.get('frase'),
                                         bool(datos.get('encolar', True)))
            self._json(codigo, resp)

        def log_message(self, *args):  # silencia el log HTTP por petición
            pass
    return Handler


def main(args=None):
    rclpy.init(args=args)
    nodo = InterfazOrdenes()
    exe = MultiThreadedExecutor(num_threads=6)
    exe.add_node(nodo)
    hilo = threading.Thread(target=exe.spin, daemon=True)
    hilo.start()
    host = str(nodo.get_parameter('host').value)
    puerto = int(nodo.get_parameter('puerto_web').value)
    servidor = ThreadingHTTPServer((host, puerto), crear_handler(nodo))
    servidor.daemon_threads = True
    nodo.get_logger().info(
        f'Interfaz lista: abre http://<IP_JETSON>:{puerto} desde cada PC '
        f'(local: http://127.0.0.1:{puerto}). Ctrl+C para salir.')
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        servidor.server_close()
        exe.shutdown()
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
