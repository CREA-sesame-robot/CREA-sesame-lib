import time
import requests
from . import connection

AVAILABLE_EMOTES = [
    "rest", "swim", "dance", "wave", "point", "stand", 
    "cute", "pushup", "freaky", "bow", "worm", "shake", "shrug", 
    "dead", "crab", "idle", "stand"
]

def mostrar_emotes_disponibles():
    """
    Imprime en consola todos los emotes que el robot acepta.
    Realiza los emotes llamando `hacer_emote()`
    """
    print(f'Los emotes disponibles son:')
    for emote in AVAILABLE_EMOTES:
        print(emote)

def hacer_emote(tipo_emote):
    """Hace que el Robot realice el emote de `tipo_emote`.
    Para ver la listas de emotes disponibles llamar a `mostrar_emotes_disponibles()`"""
    main_controller = connection.get_controller()
    emote_actual = tipo_emote.lower()
    if emote_actual not in AVAILABLE_EMOTES:
        raise ValueError(f"Emote invalido '{emote_actual}'. Para ver emotes disponibles, ejecute la función emotes.enumerar_emotes_disponibles() ")

    main_controller.send_command(emote_actual)
    #sleep pequeño para que si se envian varios 
    # emotes al tiempo, se alcancen a hacer
    time.sleep(1)