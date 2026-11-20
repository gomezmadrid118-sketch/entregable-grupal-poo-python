# Integrantes:
# 1. Nombre: Harold Andres Galvis Rivas | Rol: Lider de grupo
# 2. Nombre: Emmanuel Gómez Madrid | Rol: Administrador del repositorio en GitHud
# 3. Nombre: NIcolas Antonia Arboleda Soto | Rol: Desarollador del Diagrama de clases
# 4. Nombre: Diego | Rol: Tester

from abc import ABC, abstractmethod
from datetime import datetime
from math import ceil
import re


class Vehiculo(ABC):
    """Superclase abstracta de todos los vehículos."""

    def __init__(self, placa, propietario):
        self.__placa = ""
        self.placa = placa
        self.propietario = propietario

    @property
    def placa(self):
        return self.__placa

    @placa.setter
    def placa(self, valor):
        valor = str(valor).strip().upper()
        if not re.fullmatch(r"[A-Z]{3}\d{2}[A-Z0-9]", valor):
            raise ValueError(
                "Placa inválida. Debe tener 3 letras, 2 dígitos y 1 letra o dígito."
            )
        self.__placa = valor

    @staticmethod
    def horas_a_cobrar(minutos):
        """Redondea hacia arriba y cobra mínimo una hora."""
        if minutos < 0:
            raise ValueError("Los minutos no pueden ser negativos.")
        return max(1, ceil(minutos / 60))

    @staticmethod
    def cobro_con_tope(horas, tarifa, tope):
        """Cobra cada bloque de 24 horas al tope y las horas restantes por tarifa."""
        bloques, restantes = divmod(horas, 24)
        return bloques * tope + min(restantes * tarifa, tope)

    @abstractmethod
    def calcular_cobro(self, horas):
        """Cada subclase define su regla de cobro."""
        raise NotImplementedError

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(placa='{self.placa}', "
            f"propietario='{self.propietario}')"
        )


class Carro(Vehiculo):
    TARIFA_HORA = 4000
    TOPE_DIARIO = 30000

    def calcular_cobro(self, horas):
        return self.cobro_con_tope(horas, self.TARIFA_HORA, self.TOPE_DIARIO)


class Moto(Vehiculo):
    TARIFA_HORA = 2000
    TOPE_DIARIO = 12000

    def calcular_cobro(self, horas):
        return self.cobro_con_tope(horas, self.TARIFA_HORA, self.TOPE_DIARIO)


class Camion(Vehiculo):
    TARIFA_HORA = 8000
    RECARGO_INGRESO = 5000

    def calcular_cobro(self, horas):
        return horas * self.TARIFA_HORA + self.RECARGO_INGRESO


class Parqueadero:
    def __init__(self, nombre, capacidad):
        if not isinstance(capacidad, int) or capacidad < 1:
            raise ValueError("La capacidad debe ser un entero mayor que cero.")
        self.nombre = nombre
        self.__capacidad = capacidad
        self.__vehiculos = {}  # placa: (vehículo, hora de ingreso)
        self.__recaudo = 0

    @property
    def cupos_disponibles(self):
        return self.__capacidad - len(self.__vehiculos)

    @property
    def recaudo_total(self):
        return self.__recaudo

    @property
    def vehiculos_dentro(self):
        return [datos[0] for datos in self.__vehiculos.values()]

    def ingresar(self, vehiculo, ingreso=None):
        ingreso = ingreso or datetime.now()

        if vehiculo.placa in self.__vehiculos:
            raise ValueError(f"La placa {vehiculo.placa} ya está dentro.")
        if self.cupos_disponibles <= 0:
            raise RuntimeError("El parqueadero está lleno.")

        self.__vehiculos[vehiculo.placa] = (vehiculo, ingreso)

    def retirar(self, placa, salida=None):
        salida = salida or datetime.now()
        placa = str(placa).strip().upper()

        if placa not in self.__vehiculos:
            raise KeyError(f"La placa {placa} no está en el parqueadero.")

        vehiculo, ingreso = self.__vehiculos[placa]
        if salida < ingreso:
            raise ValueError("La salida no puede ser anterior a la entrada.")

        minutos = ceil((salida - ingreso).total_seconds() / 60)
        horas = Vehiculo.horas_a_cobrar(minutos)
        cobro = vehiculo.calcular_cobro(horas)

        del self.__vehiculos[placa]
        self.__recaudo += cobro
        return cobro


# -------------------- PRUEBAS DE ACEPTACIÓN --------------------

def lanza(excepcion, funcion, *args):
    try:
        funcion(*args)
    except excepcion:
        return True
    return False


if __name__ == "__main__":
    base = datetime(2026, 11, 20, 8, 0)

    # Encapsulamiento y validación de placa
    carro = Carro("abc123", "Ana")
    assert carro.placa == "ABC123"
    assert lanza(ValueError, Carro, "12", "X")
    assert lanza(ValueError, Moto, "ABCD12", "X")

    # Abstracción
    assert lanza(TypeError, Vehiculo, "ABC123", "X")

    # Tiempo a cobrar
    assert Vehiculo.horas_a_cobrar(0) == 1
    assert Vehiculo.horas_a_cobrar(60) == 1
    assert Vehiculo.horas_a_cobrar(61) == 2

    # Polimorfismo: cobro según el tipo de vehículo
    assert Moto("AAA11A", "X").calcular_cobro(3) == 6000
    assert Moto("AAA11A", "X").calcular_cobro(8) == 12000
    assert Moto("AAA11A", "X").calcular_cobro(24) == 12000
    assert carro.calcular_cobro(4) == 16000
    assert carro.calcular_cobro(30) == 54000
    assert Camion("TRK789", "X").calcular_cobro(2) == 21000
    assert Camion("TRK789", "X").calcular_cobro(30) == 245000

    # Flujo completo del parqueadero
    p = Parqueadero("Central", 3)
    moto = Moto("XYZ45A", "Luis")
    camion = Camion("TRK789", "Marta")

    p.ingresar(carro, base)
    p.ingresar(moto, base)
    p.ingresar(camion, base)
    assert p.cupos_disponibles == 0
    assert len(p.vehiculos_dentro) == 3

    assert lanza(RuntimeError, p.ingresar, Carro("QWE111", "Pedro"), base)
    assert lanza(ValueError, p.ingresar, carro, base)

    assert p.retirar("abc123", datetime(2026, 11, 20, 11, 10)) == 16000
    assert p.retirar("XYZ45A", datetime(2026, 11, 20, 13, 0)) == 10000
    assert lanza(
        ValueError, p.retirar, "TRK789", datetime(2026, 11, 20, 7, 0)
    )
    assert len(p.vehiculos_dentro) == 1
    assert p.retirar("TRK789", datetime(2026, 11, 20, 10, 0)) == 21000

    assert lanza(KeyError, p.retirar, "ZZZ999")
    assert p.recaudo_total == 47000
    assert p.cupos_disponibles == 3

    # Encapsulamiento del parqueadero
    assert lanza(AttributeError, setattr, p, "recaudo_total", 0)
    assert lanza(AttributeError, setattr, p, "cupos_disponibles", 99)

    print("Todas las pruebas pasaron")
