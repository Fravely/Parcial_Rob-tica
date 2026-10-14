#!/usr/bin/env python3
"""
grabar_y_transcribir.py

Pregunta 3 - etapa de voz:
1) Inicia grabación con arecord.
2) El usuario presiona ENTER para detenerla.
3) Envía el .wav a Google AI Studio / Gemini.
4) Imprime y guarda la transcripción.
5) Usa GEMINI_API_KEY desde variable de entorno (NO hardcodeada).

Requisitos:
  sudo apt install alsa-utils
  python3 -m pip install -U google-genai

Uso:
  export GEMINI_API_KEY="TU_CLAVE"
  python3 grabar_y_transcribir.py

Opciones:
  python3 grabar_y_transcribir.py --salida orden_01.wav
  python3 grabar_y_transcribir.py --timeout 8
"""

import argparse
import multiprocessing as mp
import os
import subprocess
import sys
import time
from pathlib import Path


def grabar_wav(ruta: Path, dispositivo: str | None = None) -> None:
    """Graba con ALSA/arecord hasta que el usuario presione ENTER."""
    cmd = [
        "arecord",
        "-q",
        "-f", "S16_LE",   # PCM 16-bit
        "-r", "16000",     # 16 kHz, suficiente para voz
        "-c", "1",         # mono
        "-t", "wav",
    ]
    if dispositivo:
        cmd += ["-D", dispositivo]
    cmd.append(str(ruta))

    print("\n🎙️  GRABACIÓN LISTA")
    print("Habla ahora.")
    print("Presiona ENTER cuando termines de hablar.\n")

    try:
        proceso = subprocess.Popen(cmd)
    except FileNotFoundError:
        sys.exit(
            "ERROR: no encuentro 'arecord'. Instálalo con:\n"
            "  sudo apt install alsa-utils"
        )

    try:
        input()
    except KeyboardInterrupt:
        pass
    finally:
        # SIGINT permite que arecord cierre correctamente el archivo WAV.
        proceso.send_signal(2)
        try:
            proceso.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proceso.terminate()
            proceso.wait(timeout=2)

    if not ruta.exists() or ruta.stat().st_size < 100:
        sys.exit(f"ERROR: no se generó correctamente {ruta}")

    print(f"✅ Audio guardado: {ruta} ({ruta.stat().st_size / 1024:.1f} KB)")


def _trabajo_gemini(ruta_audio: str, cola: mp.Queue) -> None:
    """Proceso separado para poder aplicar un timeout duro."""
    try:
        from google import genai

        # genai.Client() toma GEMINI_API_KEY del entorno.
        cliente = genai.Client()

        audio = cliente.files.upload(file=ruta_audio)

        # API oficial de transcripción de Gemini.
        respuesta = cliente.interactions.create(
            model="gemini-3.5-transcribe",
            input=[
                {
                    "type": "audio",
                    "uri": audio.uri,
                    "mime_type": audio.mime_type,
                }
            ],
            generation_config={
                "transcription_config": {
                    "language_codes": ["es"],
                    "custom_vocabulary": [
                        "JetCobot",
                        "lata",
                        "cubo",
                        "bloque",
                        "rojo",
                        "azul",
                        "verde",
                        "amarillo",
                    ],
                }
            },
        )

        texto = (respuesta.output_text or "").strip()
        cola.put(("ok", texto))
    except Exception as exc:
        cola.put(("error", f"{type(exc).__name__}: {exc}"))


def transcribir_con_timeout(ruta: Path, timeout_s: float) -> tuple[str, float]:
    """Transcribe con Google; si excede timeout_s, mata el proceso y vuelve."""
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError(
            "No existe GEMINI_API_KEY en esta terminal.\n"
            "Configúrala con:\n"
            '  export GEMINI_API_KEY="TU_CLAVE"'
        )

    cola: mp.Queue = mp.Queue()
    proceso = mp.Process(target=_trabajo_gemini, args=(str(ruta), cola))
    inicio = time.perf_counter()
    proceso.start()
    proceso.join(timeout_s)
    latencia = time.perf_counter() - inicio

    if proceso.is_alive():
        proceso.terminate()
        proceso.join(2)
        raise TimeoutError(
            f"Google no respondió dentro del límite de {timeout_s:.1f} s."
        )

    if cola.empty():
        raise RuntimeError("Google terminó sin devolver una respuesta.")

    estado, contenido = cola.get()
    if estado != "ok":
        raise RuntimeError(contenido)

    if not contenido:
        raise RuntimeError("Google devolvió una transcripción vacía.")

    return contenido, latencia


def guardar_transcripcion(ruta_audio: Path, texto: str, latencia_s: float) -> Path:
    ruta_txt = ruta_audio.with_suffix(".txt")
    ruta_txt.write_text(
        f"audio={ruta_audio.name}\n"
        f"transcripcion={texto}\n"
        f"latencia_transcripcion_s={latencia_s:.3f}\n",
        encoding="utf-8",
    )
    return ruta_txt


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Graba voz, la envía a Google AI Studio y obtiene texto."
    )
    parser.add_argument(
        "--salida",
        default="orden_voz.wav",
        help="archivo WAV de salida (default: orden_voz.wav)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=8.0,
        help="tiempo máximo de espera de Google en segundos (default: 8)",
    )
    parser.add_argument(
        "--dispositivo",
        default=None,
        help="dispositivo ALSA opcional, ej. hw:1,0",
    )
    args = parser.parse_args()

    ruta = Path(args.salida).expanduser().resolve()
    ruta.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 64)
    print("P3 · VOZ → GOOGLE AI STUDIO → TEXTO")
    print("=" * 64)

    grabar_wav(ruta, args.dispositivo)

    print("\n☁️  Enviando audio a Google AI Studio...")
    try:
        texto, latencia = transcribir_con_timeout(ruta, args.timeout)
    except TimeoutError as exc:
        print(f"\n⚠️  TIMEOUT: {exc}")
        print("Para la P3, aquí debe activarse el modo texto por teclado.")
        texto = input("⌨️  Orden por teclado > ").strip()
        latencia = args.timeout
        if not texto:
            print("No se ingresó una orden.")
            return 2
    except Exception as exc:
        print(f"\n⚠️  Falló la transcripción: {exc}")
        print("Modo degradado: escribe la orden por teclado.")
        texto = input("⌨️  Orden por teclado > ").strip()
        latencia = 0.0
        if not texto:
            print("No se ingresó una orden.")
            return 2

    ruta_txt = guardar_transcripcion(ruta, texto, latencia)

    print("\n" + "=" * 64)
    print("TRANSCRIPCIÓN")
    print("=" * 64)
    print(texto)
    print(f"\nLatencia: {latencia:.3f} s")
    print(f"Evidencia: {ruta_txt}")
    print("\nSIGUIENTE ETAPA DE LA P3:")
    print("Enviar este texto al servicio ROS 2 /interpretar_orden de la P1.")
    return 0


if __name__ == "__main__":
    # Necesario para multiprocessing de forma portable.
    mp.freeze_support()
    raise SystemExit(main())
