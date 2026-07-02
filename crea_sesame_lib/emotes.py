# crea_sesame_lib/emotes.py
import time
import msvcrt
from . import connection

AVAILABLE_EMOTES = [
    "rest", "swim", "dance", "wave", "point", "stand", 
    "cute", "pushup", "freaky", "bow", "worm", "shake", "shrug", 
    "dead", "crab", "idle", "stand"
]


def mostrar_emotes_disponibles():
    """
    Imprime en consola todos los emotes que el robot acepta.
    Realiza los emotes llamando hacer_emote()
    """
    print("Los emotes disponibles son:")
    for emote in AVAILABLE_EMOTES:
        print(emote)


def hacer_emote(tipo_emote: str):
    """
    Hace que el robot realice el emote indicado.
    Se ignora si se presionó ESPACIO previamente.
    Para ver la lista de emotes disponibles, llama a mostrar_emotes_disponibles()

    Ejemplo:
        hacer_emote("wave")
    """
    stop_event = connection.get_stop_event()

    # Check for spacebar before doing anything
    if msvcrt.kbhit():
        key = msvcrt.getwch()
        if key == " ":
            print("\n[INFO] Deteniendo robot")
            stop_event.set()

    if stop_event.is_set():
        print(f"[INFO] emote '{tipo_emote}' ignorado")
        return

    emote_actual = tipo_emote.lower()
    if emote_actual not in AVAILABLE_EMOTES:
        raise ValueError(
            f"Emote inválido '{emote_actual}'. "
            f"Para ver emotes disponibles, ejecute emotes.mostrar_emotes_disponibles()"
        )

    main_controller = connection.get_controller()
    main_controller.send_command(emote_actual)

    # Small wait so back-to-back emotes don't overlap,
    # but still interruptible by spacebar
    deadline = time.time() + 1.0
    while time.time() < deadline:
        if stop_event.is_set():
            return
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key == " ":
                print("\n[INFO] Deteniendo robot")
                stop_event.set()
                return
        time.sleep(0.05)