from crea_sesame_lib import connection, emotes, motion, caras
import time
def main():
    connection.conectar_robot()
    #motion.mover("forward", 3)
    #motion.mover("backward", 3)
    #motion.mover("right", 3)
    #motion.mover("left", 3)
    #emotes.hacer_emote("wave")
    #emotes.hacer_emote("swim")
    caras.cambiar_cara("angry")
    time.sleep(3)
    caras.cambiar_cara("sad")
    time.sleep(3)
    caras.cambiar_cara("happy")


#emotes.mostrar_emotes_disponibles()   


main()