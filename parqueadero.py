
from abc import ABC, abstractmethod  #"ABC", ABSTRACTMETHOD sirve para crear una clase "molde" que no puede usar sola. 
from datetime import datetime  #sirve para manejar fechas y horas 
from math import ceil # ceil redondea hacia arriba 
import re #"re" permite validar si una cadena de texto cumple con un patrón específico


class Vehiculo(ABC):                #molde de los vehiculos 
    """Superclase abstracta de todos los vehículos."""

    def __init__(self, placa, propietario):   #constructor 
        self.__placa = ""     #creacion de placa privada
        self.placa = placa    #validador
        self.propietario = propietario 

    @property #permite leer un dato privado como si fuera un dato normal 
    def placa(self):
        return self.__placa 

    @placa.setter  #guardar la placa con validacion, se ejecuta cada vez que alguien asigna una placa quita los espacios y la pone en mayusculas revisa que tenga 3 letras y 2 numeros si no cumple lanza un error
    def placa(self, valor):
        valor = str(valor).strip().upper()
        if not re.fullmatch(r"[A-Z]{3}\d{2}[A-Z0-9]", valor):
            raise ValueError(
                "Placa inválida. Debe tener 3 letras, 2 dígitos y 1 letra o dígito."
            )
        self.__placa = valor

    @staticmethod # es una funcion que no necesita un vehiculo para funcionar si los minutos son negativos da error, redondea hacia arriba y cobra minimo una hora (61m =2hrs)
    def horas_a_cobrar(minutos):
        """Redondea hacia arriba y cobra mínimo una hora."""
        if minutos < 0:
            raise ValueError("Los minutos no pueden ser negativos.")
        return max(1, ceil(minutos / 60))

    @staticmethod # separa los dias completos de las horas que sobran cada dia completo cuesta el tope, las horas sobrantes cuestan (horaxtarifa)pero nunca mas que el tope
    def cobro_con_tope(horas, tarifa, tope):
        """Cobra cada bloque de 24 horas al tope y las horas restantes por tarifa."""
        bloques, restantes = divmod(horas, 24)
        return bloques * tope + min(restantes * tarifa, tope)

    @abstractmethod #obliga ah cada hijo (carro,moto,camion) a escribir su propio : calcular_cobro.
    def calcular_cobro(self, horas):
        """Cada subclase define su regla de cobro."""
        raise NotImplementedError

    def __repr__(self): #define como se ve el vehiculo al imprimirlo 
        return (
            f"{self.__class__.__name__}(placa='{self.placa}', "
            f"propietario='{self.propietario}')"
        )


class Carro(Vehiculo): #hereda todo de vehiculo tiene su tarifa y su tope como atributos de clase(vale para todas sus carros),($4.000hr):(tope:$30.0000) = cobro_con_tope 
    TARIFA_HORA = 4000
    TOPE_DIARIO = 30000

    def calcular_cobro(self, horas):
        return self.cobro_con_tope(horas, self.TARIFA_HORA, self.TOPE_DIARIO)


class Moto(Vehiculo): #hereda todo de vehiculo tiene su tarifa y su tope como atributos de clase(vale para todas sus motos),($2.000hr):(tope:$12.0000) = cobro_con_tope 
    TARIFA_HORA = 2000
    TOPE_DIARIO = 12000

    def calcular_cobro(self, horas):
        return self.cobro_con_tope(horas, self.TARIFA_HORA, self.TOPE_DIARIO)


class Camion(Vehiculo): #no tiene tope diario cobra($8000hr) + (fijo:$5000) por entrar 
    TARIFA_HORA = 8000
    RECARGO_INGRESO = 5000

    def calcular_cobro(self, horas):
        return horas * self.TARIFA_HORA + self.RECARGO_INGRESO


class Parqueadero: # recibe el nombre y capacidad con la condicion de capacidad >0 guarda areas privadas (capacidad,diccionario,recaudo) 
    def __init__(self, nombre, capacidad):
        if not isinstance(capacidad, int) or capacidad < 1:
            raise ValueError("La capacidad debe ser un entero mayor que cero.")
        self.nombre = nombre
        self.__capacidad = capacidad
        self.__vehiculos = {}  # placa: (vehículo, hora de ingreso)
        self.__recaudo = 0

    @property #capacidad menos los vehiculos que hayan adentro 
    def cupos_disponibles(self):
        return self.__capacidad - len(self.__vehiculos)

    @property #el dinero ganado hasta ahora.
    def recaudo_total(self):
        return self.__recaudo

    @property #la lista de los vehiculos qu estan adentro solo se pueden leer nadie puede cambiarlos desde afuera
    def vehiculos_dentro(self):
        return [datos[0] for datos in self.__vehiculos.values()]

    def ingresar(self, vehiculo, ingreso=None):  #si no das hora usa la hora actual., da error si la placa ya esta dentro o si no hay cupos si toda esta bien lo guardara junto con su hora de ingreso 
        ingreso = ingreso or datetime.now()

        if vehiculo.placa in self.__vehiculos:
            raise ValueError(f"La placa {vehiculo.placa} ya está dentro.")
        if self.cupos_disponibles <= 0:
            raise RuntimeError("El parqueadero está lleno.")

        self.__vehiculos[vehiculo.placa] = (vehiculo, ingreso)

    def retirar(self, placa, salida=None): #limpia la placa , da error si la placa no esta en el parqueadero y da error si la salida es antes que la entrada 
        salida = salida or datetime.now()
        placa = str(placa).strip().upper()

        if placa not in self.__vehiculos:
            raise KeyError(f"La placa {placa} no está en el parqueadero.")

        vehiculo, ingreso = self.__vehiculos[placa]
        if salida < ingreso:
            raise ValueError("La salida no puede ser anterior a la entrada.")

#calcula los minutos entre entrada y salida y los pasa a horas a cobrar. cada vehiculo calcula su cobro con su propia regla , lo saca del parqueadero suma el cobro al recaudo y lo devuelve 

        minutos = ceil((salida - ingreso).total_seconds() / 60)
        horas = Vehiculo.horas_a_cobrar(minutos)
        cobro = vehiculo.calcular_cobro(horas)

        del self.__vehiculos[placa]
        self.__recaudo += cobro
        return cobro


# -------------------- PRUEBAS DE ACEPTACIÓN --------------------

def lanza(excepcion, funcion, *args):  #ejecuta una funcion y mira si salio el error esperado, Devuelve : True si el error salio y : False si no ; sirve para comprobar que el codigo falla cuando debe fallar    
    try:
        funcion(*args)
    except excepcion:
        return True
    return False


if __name__ == "__main__":   #significa que las prueban solo corren si ejecutas este archivo directamente.  
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
