import time
import requests
from . import connection

AVAILABLE_FACES = [
    "happy", "sad", "angry", "surprised", "sleepy", 
    "love", "excited", "confused"
]

def mostrar_caras_disponibles():
    """
    Imprime en consola todas las caras que el robot acepta.
    Cambia la cara del robot llamando `cambiar_cara()`
    """
    print(f'Los emotes disponibles son:')
    for face in AVAILABLE_FACES:
        print(face)


def listar_caras_disponibles()-> list:
    """
    Devuelve la lista completa de caras disponibles para el robot
    """
    return AVAILABLE_FACES

def cambiar_cara(tipo_cara):
    """Hace que el Robot realice el emote de `tipo_cara`.
    Para ver la listas de emotes disponibles llamar a `enumerar_emotes_disponibles()`"""
    main_controller = connection.get_controller()
    cara_actual = tipo_cara.lower()
    if cara_actual not in AVAILABLE_FACES:
        raise ValueError(f"Cara invalida '{cara_actual}'. Para ver las caras disponibles, ejecute la función caras.mostrar_caras_disponibles() ")

    main_controller.send_command(command="idle",face=cara_actual)
    #sleep pequeño para que si se envian varios 
    # emotes al tiempo, se alcancen a hacer
    time.sleep(0.5)