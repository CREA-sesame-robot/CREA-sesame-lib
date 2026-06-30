# Import the low-level functions from the companion library
from sesame_companion import SesameRobotController
import subprocess
import re

class SesameCommander:
    def __init__(self, robot_ip: str = None, mock: bool = False):
        if mock:
            self.controller = SesameRobotController("mock")
        else:
            ip = robot_ip or self.get_robot_ip()
            print(f"[INFO] Connecting to robot at {ip}")
            self.controller = SesameRobotController(ip)

    def get_robot_ip(timeout: float = 5.0) -> str:
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

        # First match is typically the DNS server, second is the resolved redirect IP
        robot_ip = addresses[1]
        print (f'Addresses completo: {addresses}')
        print (f'Supuesto Robot IP {robot_ip}')
        return robot_ip

    def point_move_stop(self, direction: float, distance: float):
        """Point to a direction, move a distance, then stop — one call."""
        # set_direction(self.robot, direction)
        # move(self.robot, distance)
        # stop(self.robot)
        pass