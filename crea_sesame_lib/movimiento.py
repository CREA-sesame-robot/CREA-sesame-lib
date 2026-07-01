# Import the low-level functions from the companion library
import time
import requests
from . import connection

AVAILABLE_EMOTES = [
    "rest", "swim", "dance", "wave", "point", "stand", 
    "cute", "pushup", "freaky", "bow", "worm", "shake", "shrug", 
    "dead", "crab", "idle", "stand"
]
VALID_DIRECTIONS = {"forward", "backward", "left", "right"}

def _send_go(direction: str):
    """Internal: sends the go=<direction> command directly to the robot."""
    controller = connection.get_controller()

    if controller.is_mock:
        print(f"   TX (mock): go={direction}")
        return

    url = f"{controller.base_url}/cmd"
    response = requests.get(url, params={"go": direction}, timeout=5)
    print(f"   TX: go={direction} -> {response.status_code}")
    return response


def _send_stop():
    """Internal: sends the stop=1 command directly to the robot."""
    controller = connection.get_controller()

    if controller.is_mock:
        print("   TX (mock): stop=1")
        return

    url = f"{controller.base_url}/cmd"
    response = requests.get(url, params={"stop": 1}, timeout=5)
    print(f"   TX: stop=1 -> {response.status_code}")
    return response

def _calcular_duracion(angulo: float) -> float:
    """
    Calcula la duración (en segundos, como entero) necesaria para girar
    el robot un ángulo dado, asumiendo que gira 360° en 35 segundos.
    
    angulo: ángulo deseado en grados (0-360). 0° = frente del robot.
    """
    TIEMPO_VUELTA_COMPLETA = 22
    
    # Normalizar el ángulo al rango [0, 360)
    angulo = angulo % 360
    
    duracion = (angulo / 360) * TIEMPO_VUELTA_COMPLETA
    
    return round(duracion,3)

def mover(direction: str, duration: float):
    """
    Mueve el robot en cualquier dirección por `duracion`segundos, luego se detiene.
    Direcciones: "forward", "backward", "left", "right"
    """
    direction = direction.lower()
    if direction not in VALID_DIRECTIONS:
        raise ValueError(f"Dirección invalida '{direction}'. Tiene que ser alguna entre: {VALID_DIRECTIONS}")

    _send_go(direction)
    time.sleep(duration)
    _send_stop()

def mover_adelante(duracion:float):
    main_controller = connection.get_controller()
    _send_go("forward")
    time.sleep(duracion)
    _send_stop()
def girar_derecha(duracion:float):
    #main_controller = connection.get_controller()
    _send_go("right")
    time.sleep(duracion)

    _send_stop()
def girar_izquierda(duracion:float):
    #main_controller = connection.get_controller()
    _send_go("left")
    time.sleep(duracion)
    _send_stop()
def mover_atras(duracion:float):
    main_controller = connection.get_controller()
    _send_go("backward")
    time.sleep(duracion)
    _send_stop()

def detener():
    """
    Detiene cualquier acción del robot
    """
    _send_stop()

def girar_derecha_angulo(angulo: int):
    """
    Gira a la derecha hasta estar posicionado en el ángulo enviado en el
    parámetro `angulo`. Asume que inicia mirando al ángulo 0°
    """

    tiempo = _calcular_duracion(angulo)
    print(tiempo)
    girar_derecha(tiempo)

def girar_izquierda_angulo(angulo: int):
    """
    Gira a la derecha hasta estar posicionado en el ángulo enviado en el
    parámetro `angulo`. Asume que inicia mirando al ángulo 0°
    """
    tiempo = _calcular_duracion(angulo)
    girar_izquierda(tiempo)
