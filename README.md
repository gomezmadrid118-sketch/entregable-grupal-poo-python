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
- `¿Por qué recaudo_total no tiene setter?` \
R//:
- `¿Qué diferencia hay entre _atributo y __atributo ? ¿Es realmente imposible acceder al segundo?` \
R//:
- `¿Por qué Parqueadero no hereda de Vehiculo ni al revés? ¿Qué relación hay entre ambas clases?` \
R//:
- `Si el parqueadero recibe un objeto que no es un vehículo pero tiene placa y calcular_cobro , ¿funcionaría? ¿Cómo se llama ese comportamiento?` \
R//:
- `¿Qué cambiaría si el cobro de cada vehículo viviera como un if/elif dentro de Parqueadero.retirar ?` \
R//: