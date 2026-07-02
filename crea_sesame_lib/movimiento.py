# crea_sesame_lib/movimiento.py
import time
import requests
import msvcrt
from . import connection

AVAILABLE_EMOTES = [
    "rest", "swim", "dance", "wave", "point", "stand", 
    "cute", "pushup", "freaky", "bow", "worm", "shake", "shrug", 
    "dead", "crab", "idle", "stand"
]
VALID_DIRECTIONS = {"forward", "backward", "left", "right"}


# Funciones internas para enviar requests HTTP y el thread de detener todo
def _send_go(direction: str):
    """Envía el comando go=<direction> al robot."""
    controller = connection.get_controller()
    if controller.is_mock:
        print(f"   TX (mock): go={direction}")
        return
    url = f"{controller.base_url}/cmd"
    response = requests.get(url, params={"go": direction}, timeout=5)
    print(f"   TX: go={direction} -> {response.status_code}")
    return response


def _send_stop():
    """Envía el comando stop=1 al robot."""
    controller = connection.get_controller()
    if controller.is_mock:
        print("   TX (mock): stop=1")
        return
    url = f"{controller.base_url}/cmd"
    response = requests.get(url, params={"stop": 1}, timeout=5)
    print(f"   TX: stop=1 -> {response.status_code}")
    return response

def _esperar_interruptible(duracion: float):
    """
    Espera `duracion` segundos en el hilo principal, revisando cada 50ms
    si se presionó ESPACIO o si el stop_event ya fue activado.
    Esto permite detectar el espacio SIN necesitar hilos secundarios ni admin.
    """
    stop_event = connection.get_stop_event()
    deadline = time.time() + duracion

    while time.time() < deadline:
        if stop_event.is_set():
            return
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key == " ":
                print("\n[INFO] Espacio presionado — deteniendo robot")
                stop_event.set()
                _send_stop()
                return
        time.sleep(0.05)

def _mover_base(direction: str, duracion: float, label: str):
    """Lógica común para todas las funciones de movimiento."""
    stop_event = connection.get_stop_event()

    if stop_event.is_set():
        print(f"[INFO] {label} por {duracion}s ignorado")
        return

    _send_go(direction)
    _esperar_interruptible(duracion)

    if not stop_event.is_set():
        _send_stop()


 
# Movimientos básicos


def mover(direction: str, duracion: float):
    """
    Mueve el robot en cualquier dirección por `duracion` segundos, luego se detiene.
    Direcciones: "forward", "backward", "left", "right".
    Presiona ESPACIO en cualquier momento para detener el robot.

    Ejemplo:
        mover("forward", 5)
    Esto mueve el robot hacia adelante por 5 segundos.
    """
    direction = direction.lower()
    if direction not in VALID_DIRECTIONS:
        raise ValueError(f"Dirección inválida '{direction}'. Debe ser una de: {VALID_DIRECTIONS}")
    _mover_base(direction, duracion, f"mover({direction})")



def mover_adelante(duracion: float):
    """
    Mueve el robot hacia adelante por `duracion` segundos, luego se detiene.
    Presiona ESPACIO en cualquier momento para detener el robot.

    Ejemplo:
        mover_adelante(3)
    Esto mueve el robot adelante por 3 segundos
    """
    _mover_base("forward", duracion, "mover_adelante")


def mover_atras(duracion: float):
    """
    Mueve el robot hacia atrás por `duracion` segundos, luego se detiene.
    Presiona ESPACIO en cualquier momento para detener el robot.

    Ejemplo:
        mover_atras(3)
    Esto mueve el robot hacia atrás por 3 segundos
    """
    _mover_base("backward", duracion, "mover_atras")


def girar_derecha(duracion: float):
    """
    Gira el robot hacia la derecha por `duracion` segundos, luego se detiene.
    Presiona ESPACIO en cualquier momento para detener el robot.

    Ejemplo:
        girar_derecha(3)
    Esto gira el robot hacia la derecha por 3 segundos
    """
    _mover_base("right", duracion, "girar_derecha")


def girar_izquierda(duracion: float):
    """
    Gira el robot hacia la izquierda por `duracion` segundos, luego se detiene.
    Presiona ESPACIO en cualquier momento para detener el robot.

    Ejemplo:
        girar_izquierda(3)
    Esto gira el robot a la izquierda por 3 segundos
    """
    _mover_base("left", duracion, "girar_izquierda")


def detener():
    """
    Detiene cualquier acción del robot inmediatamente.
    """
    connection.get_stop_event().set()
    _send_stop()


# TODO: funciones para hacer movimientos de angulo

def _calcular_duracion(angulo: float) -> float:
    """
    Calcula la duración en segundos para girar el robot un ángulo dado.
    Asume que el robot gira 360° en 22 segundos.
    """
    TIEMPO_VUELTA_COMPLETA = 22
    angulo = angulo % 360
    return round((angulo / 360) * TIEMPO_VUELTA_COMPLETA, 3)


def girar_derecha_angulo(angulo: int):
    """
    Gira el robot a la derecha el número de grados indicado.
    Asume que inicia mirando al ángulo 0°.

    Ejemplo:
        girar_derecha_angulo(90)
    """
    girar_derecha(_calcular_duracion(angulo))


def girar_izquierda_angulo(angulo: int):
    """
    Gira el robot a la izquierda el número de grados indicado.
    Asume que inicia mirando al ángulo 0°.

    Ejemplo:
        girar_izquierda_angulo(180)
    """
    girar_izquierda(_calcular_duracion(angulo))


# TODO: secuencias de comandos, probar más exhaustivo

def secuencia_movimiento(steps: list):
    """
    Ejecuta una lista de tuplas (direccion, duracion) en orden.
    Presiona ESPACIO en cualquier momento para detener el robot y abortar toda la secuencia.

    Ejemplo:
        secuencia_movimiento([
            ("forward", 2),
            ("left", 1),
            ("forward", 3),
        ])
    """
    connection._reset_stop()
    print(f"[INFO] Ejecutando secuencia de {len(steps)} pasos. Presiona ESPACIO para abortar.")

    for direction, duration in steps:
        mover(direction, duration)

    if not connection.get_stop_event().is_set():
        print("[INFO] Secuencia completa.")
    
    connection._reset_stop()