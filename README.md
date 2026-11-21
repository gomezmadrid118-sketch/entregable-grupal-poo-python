# Participantes:

- Harold Andres Galvis | Rol: Lider de grupo
- Nicolas Antonio Arboleda | Rol: Desarollador del Diagrama de clases
- Diego Alejandro Arango | Rol: Tester
- Emmanuel Gómez Madrid | Rol: Administrador del repositorio y el readme

# Resolución a las preguntas:

- `¿Por qué Vehiculo es abstracta? ¿Qué ocurre si se intenta instanciarla?` \
R//: La clase vehiculo actua como abstracta ya que es quien define atributos y metodos que se heredarán a las clases que se usaron en este ejercicio, se puede ver como una plantilla o contrato que la subclase que la heredada debe cumplir, si se intenta instanciar este marcará error, ya que el rol de una clase abstracta no supera el funcionamiento del contrato
- `¿Dónde se aplica el polimorfismo en el sistema y qué ventaja trae al agregar un nuevo tipo de vehículo?` \
R//: El polimorfismo se aplica en este caso en el metodo calcular_cobro creado por la clase abstracta padre y usado por las diferentes subclases heredadas, la ventaja que tre el uso del polimorfismo es adaptar el metodo del padre a quien lo hereda, ya que por ejemplo en este ejercicio los carros, las motos y los camiones no tienen la misma tarifa ni el mismo tope diario
- `¿Qué pasaría si placa fuera un atributo público? ¿Qué problemas aparecerían?` \
R//: Lo que ocurriría es que se podría acceder y modificar desde cualquier parte del código a cualquier placa registrada 
- - `¿Por qué recaudo_total no tiene setter?` \
R//: Porque es el dinero que ganó el parqueadero y solo debe cambiar en un momento: cuando se retira un vehículo (dentro de `retirar`). Si tuviera setter, cualquiera podría escribir `p.recaudo_total = 0` desde afuera y dañar la cuenta. Sin setter, Python lanza un `AttributeError` si alguien lo intenta (las pruebas lo comprueban). Así el dato queda protegido y es de solo lectura.

- `¿Qué diferencia hay entre _atributo y __atributo? ¿Es realmente imposible acceder al segundo?` \
R//: Con `_atributo` (un guion bajo) le dices a otros programadores "no lo toques", pero Python no lo bloquea. Con `__atributo` (dos guiones bajos) Python le cambia el nombre por dentro a `_Clase__atributo`, para que no se use por accidente. No es imposible acceder: se puede con `carro._Vehiculo__placa`. Es una protección contra descuidos, no una seguridad real.

- `¿Por qué Parqueadero no hereda de Vehiculo ni al revés? ¿Qué relación hay entre ambas clases?` \
R//: Porque la herencia se usa cuando una clase "es un tipo de" otra (un carro es un vehículo), y un parqueadero no es un vehículo ni al revés. La relación es de composición: el parqueadero "tiene" vehículos, los guarda en su diccionario y los usa, pero cada clase es independiente.

- `Si el parqueadero recibe un objeto que no es un vehículo pero tiene placa y calcular_cobro, ¿funcionaría? ¿Cómo se llama ese comportamiento?` \
R//: Sí, funcionaría, porque el parqueadero solo usa `vehiculo.placa` y `vehiculo.calcular_cobro(horas)` y no revisa de qué clase es el objeto. Eso se llama **duck typing** ("si camina y hace cuac como un pato, es un pato"). Una sola precaución: la placa tendría que venir ya en mayúsculas, porque esa limpieza la hace la clase `Vehiculo`, no el parqueadero.

- `¿Qué cambiaría si el cobro de cada vehículo viviera como un if/elif dentro de Parqueadero.retirar?` \
R//: El parqueadero tendría que conocer todos los tipos de vehículo y todas sus tarifas. Cada vez que se agregue un tipo nuevo (por ejemplo, bicicleta) habría que editar `retirar` y agregar otro `elif`, con más riesgo de errores y un método cada vez más largo. Con polimorfismo, como está ahora, solo se crea una clase nueva con su `calcular_cobro` y `Parqueadero` no se toca.