from sesame_companion import *
import subprocess
import re

#Singleton para poder reducir la dependencia a la clase de sesame_companion
_controller: SesameRobotController | None = None

def obtener_ip_robot(timeout: float = 5.0) -> str:
    """
    Discovers the robot's IP address by running nslookup.
    """
    try:
        result = subprocess.run(
            ["nslookup", "www.msftconnecttest.com"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("No se pudo conectar al robot. Revisa que estes conectado al WIFI de tu robot :)")
    except FileNotFoundError:
        raise RuntimeError("el comando nslookup no pudo ser realizado")

    if result.returncode != 0:
        raise RuntimeError(f"nslookup falló de una manera inesperada: {result.stderr.strip()}")

    # Parse the "Address:" lines, skip the DNS server's own address (first one)
    addresses = re.findall(r"Address:\s*([\d.]+)", result.stdout)

    if len(addresses) < 2:
        raise RuntimeError(
            f"No se pudo encontrar la dirección IP del robot:\n{result.stdout}"
        )

    # Addresses tiene 2 direcciones, una de DNS y la otra la real. Deberían ser la misma
    robot_ip = addresses[1]
    #print (f'Addresses completo: {addresses}')
    print("¡Conexión con el robot exitosa! B-)")
    print (f'Dirección del robot: {robot_ip}')
    return robot_ip

def conectar_robot(robot_ip: str = None, mock: bool = False) -> None:
    """
    IMPORTANTE llamar antes de intentar mandar comandos al robot.
    Conecta al robot y guarda el Controller
    """
    global _controller

    if mock:
        _controller = SesameRobotController("mock")
        print("[INFO] Connected in MOCK mode")
        return

    ip = robot_ip or obtener_ip_robot()
    _controller = SesameRobotController(ip)
    print("[INFO]¡Conexión con el robot exitosa! B-)")
    print (f'[INFO]Dirección del robot: {ip}')


def get_controller() -> SesameRobotController:
    """Función auxiliar para obtener el controller en otros modulos."""
    if _controller is None:
        raise RuntimeError(
            "El Robot no está conectado. Por favor ejecute conectar_robot() antes de cualquier otra cosa"
        )
    return _controller