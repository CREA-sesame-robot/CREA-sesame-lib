from crea_sesame_lib import connection, emotes, caras
from crea_sesame_lib import movimiento
import time
def main():
   connection.conectar_robot()
   #motion.mover("right", 9)
   #motion.girar_derecha(9)
   
   movimiento.mover("left", 9)
   #caras.cambiar_cara("sad")
   emotes.hacer_emote("swim")
   time.sleep(5)
   emotes.hacer_emote("stand")
   movimiento.mover("right", 3)
   time.sleep(1)
   #movimiento.girar_derecha_angulo(90)

def sec():
   connection.conectar_robot()
   """for l in caras.listar_caras_disponibles():
      caras.cambiar_cara(l)
      time.sleep(0.1)
   #caras.cambiar_cara("happy")
   emotes.hacer_emote("dance")"""
   movimiento.mover_atras(5)
   movimiento.mover("left", 3)
   movimiento.mover_adelante(5)
   movimiento.mover("right", 3)
   emotes.hacer_emote("wave")
""" connection.conectar_robot()
    motion.mover("forward", 5)
    #motion.mover("backward", 3)
    motion.mover("right", 3)
    #motion.mover("left", 3)
    emotes.hacer_emote("wave")
    time.sleep(6)
    #emotes.hacer_emote("swim")
    caras.cambiar_cara("angry")
    time.sleep(5)
    caras.cambiar_cara("sad")
    time.sleep(3)
    caras.cambiar_cara("happy")"""
#emotes.mostrar_emotes_disponibles()   


main()
#sec()