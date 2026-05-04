from abc import ABC, abstractmethod
from datetime import datetime

### logs 

def reguistrar_log(mensaje):
    with open("sistema_reservas.log", "a") as log_file:
        log_file.write(f"{datetime.now()}: {mensaje}\n")

        ##### clases abtractas

class Entidad(ABC):   # clase abstracta
    def __init__(self, id):
        self._id = id            # crea el ID 
        self._fecha_creacion = datetime.now()  # crea la fecha 

    @abstractmethod
    def mostrar_info(self):
        pass

    def get_id(self):
        return self._id
    
    ### Excepciones personalizadas para manejo de errores en el sistema ###

class sistemaError(Exception):pass
class ReservaError(sistemaError):pass
class ClienteError(sistemaError):pass
class ServicioError(sistemaError):pass

     ## clases abstractas y concretas para el sistema de reservas de servicios###

class Cliente(Entidad):      # CLASE CLIENTE
    def __init__(self, id, nombre, email):
        super().__init__(id)
        self.set_nombre(nombre)
        self.set_email(email)

    def set_nombre(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = nombre

    def set_email(self, email):
        if "@" not in email:
            raise ValueError("Email inválido")
        self._email = email

    def get_nombre(self):
        return self._nombre

    def get_email(self):
        return self._email

    def mostrar_info(self):
        return f"Cliente: {self._nombre} | Email: {self._email}"



class Servicio(Entidad):             # CLASE ABSTRACTA SERVICIO
    def __init__(self, id, nombre, tarifa_base):
        super().__init__(id)
        self._nombre = nombre
        self._tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def descripcion(self):
        pass
    
    # Servicios polimorfismo

class Sala(Servicio):
    def calcular_costo(self, duracion): # Se define el valor del costo con la duracion 
        return self._tarifa_base * duracion # Multiplica la tarifa base por el tiempo usado

    def descripcion(self):  # Método que describe el tipo de servicio
        return "Alquiler de sala"  # Retorna una descripción del servicio


class Equipo(Servicio):  # Clase Equipo que también hereda de Servicio
    def calcular_costo(self, duracion): # Método para calcular el costo del equipo
        return self._tarifa_base * duracion # Calcula costo igual que Sala (tarifa * tiempo)
 
    def descripcion(self):  # Método que describe el servicio
        return "Alquiler de equipo" # Devuelve el tipo de servicio


class Asesoria(Servicio):  # Clase Asesoria que hereda de Servicio
    def calcular_costo(self, duracion):  # Método para calcular el costo de la asesoría
        return (self._tarifa_base * duracion) * 1.2 # Calcula el costo y le aplica un recargo del 20% (multiplica por 1.2)

    def descripcion(self):
        return "Servicio de asesoría" # Retorna el nombre del servicio
    
    ### Clase Reserva que maneja las reservas de servicios ###


class Reserva:
    def __init__(self, cliente, servicio, duracion_horas):
        if duracion_horas <= 0:

            raise ValueError("La duración debe ser mayor a cero")
        
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = "Pendiente"  # Estado inicial de la reserva
        self._fecha_reserva = datetime.now()  # Fecha de creación de la reserva
        self._costo_base = servicio.calcular_costo(duracion_horas) # Calcula el costo base usando el método del servicio
        self.calcular_costo_total() # Calcula el costo total al crear la reserva
    def calcular_costo_total(self):
        return self._servicio.calcular_costo(self._duracion_horas) # Calcula el costo total usando el método del servicio
    
    def confirmar_reserva(self):
        if self._estado != "Pendiente":
            raise ValueError("Solo se pueden confirmar reservas pendientes")
        self._estado = "Confirmada"  # Cambia el estado a confirmada
        print(f"Reserva confirmada para {self._cliente.get_nombre()} - Costo Total: ${self.calcular_costo_total():.2f}")    


  
    def cancelar_reserva(self):
        if self._estado != "Confirmada":
            raise ValueError("Solo se pueden cancelar reservas confirmadas")
        self._estado = "Cancelada"  # Cambia el estado a cancelada
        print(f"Reserva cancelada para {self._cliente.get_nombre()}")  # Imprime mensaje de cancelación
  
    def procesar(self):
        if self._estado != "Confirmada":
            raise ValueError("Solo se pueden procesar reservas confirmadas")
        self._estado = "Procesada"  # Cambia el estado a procesada
        print(f"Reserva procesada para {self._cliente.get_nombre()} - Servicio: {self._servicio.descripcion()}")  # Imprime mensaje de procesamiento
        
    def mostrar_info(self):
        return (f"Reserva para {self._cliente.get_nombre()} | Servicio: {self._servicio.descripcion()} | "
                f"Duración: {self._duracion_horas} horas | Costo Total: ${self.calcular_costo_total():.2f} | "
                f"Estado: {self._estado}")
    
    ## Clase principal del sistema de reservas ###

    class app:
        def __init__(self):
            self._clientes = {}  # Diccionario para almacenar clientes por ID
            self._servicios = {}  # Diccionario para almacenar servicios por ID
            self._reservas = []  # Lista para almacenar reservas

        def agregar_cliente(self, id, nombre, email): ### Método para agregar un cliente al sistema
            if id in self._clientes:                  ### Verifica si el ID del cliente ya existe en el sistema
                raise ClienteError("El cliente con este ID ya existe")   ## Si el ID ya existe, lanza una excepción personalizada ClienteError
            cliente = Cliente(id, nombre, email)#### Crea una nueva instancia de Cliente con los datos proporcionados
            self._clientes[id] = cliente  ### Agrega el cliente al diccionario de clientes usando su ID como clave
            reguistrar_log(f"Cliente agregado: {cliente.mostrar_info()}")  # Log de cliente agregado

        def agregar_servicio(self, id, nombre, tarifa_base, tipo): ### Método para agregar un servicio al sistema
            if id in self._servicios:   ### Verifica si el ID del servicio ya existe en el sistema
                raise ServicioError("El servicio con este ID ya existe") ### Si el ID ya existe, lanza una excepción personalizada ServicioError
            if tipo == "Sala":  ### Dependiendo del tipo de servicio, crea una instancia de la clase correspondiente (Sala, Equipo o Asesoria)
                servicio = Sala(id, nombre, tarifa_base)  ### Si el tipo es "Sala", crea una instancia de la clase Sala
            elif tipo == "Equipo": ### Si el tipo es "Equipo", crea una instancia de la clase Equipo
                servicio = Equipo(id, nombre, tarifa_base)  ### Si el tipo es "Asesoria", crea una instancia de la clase Asesoria
            elif tipo == "Asesoria": ### Si el tipo es "Asesoria", crea una instancia de la clase Asesoria
                servicio = Asesoria(id, nombre, tarifa_base)  ### Si el tipo de servicio no coincide con ninguno de los casos anteriores, lanza una excepción indicando que el tipo de servicio es inválido
            else:
                raise ValueError("Tipo de servicio inválido")    ### Si el tipo de servicio no coincide con ninguno de los casos anteriores, lanza una excepción indicando que el tipo de servicio es inválido
            self._servicios[id] = servicio  ####    Agrega el servicio al diccionario de servicios usando su ID como clave
            reguistrar_log(f"Servicio agregado: {servicio.descripcion()} - Tarifa Base: ${tarifa_base:.2f}")  # Log de servicio agregado

            self . reservas = []  # Lista para almacenar reservas
            self.crear_widgets(self)  # Método para crear la interfaz gráfica 

        ### Método para crear la interfaz gráfica (Tkinter o PyQt5) ###
        
        def crear_windegets(self):
            pass  # Aquí se implementaría la creación de la interfaz gráfica usando Tkinter o PyQt5

        # cliente
        tk.label (self.root, text="ID Cliente:").grid(row=0, column=0)
        self.nombre_cliente_entry = tk.Entry(self.root)
        self.nombre_cliente_entry.grid(row=0, column=1)

        tk.label(self.root, text="Email Cliente:").grid(row=1, column=0)
        self.email_cliente_entry = tk.Entry(self.root)
        self.email_cliente_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Agregar Cliente", command=self.agregar_cliente).grid(row=2, column=0, columnspan=2)

        # servicio
        tk.Label(self.root, text="ID Servicio:").grid(row=3, column=0)
        self.id_servicio_entry = tk.StringVar(self.root)
        self.id_servicio_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Nombre Servicio:").grid(row=4, column=0)
        self.nombre_servicio_entry = tk.Entry(self.root)
        self.nombre_servicio_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Tarifa Base:").grid(row=5, column=0)
        self.tarifa_base_entry = tk.Entry(self.root)
        self.tarifa_base_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Tipo Servicio:").grid(row=6, column=0)
        self.tipo_servicio_entry = tk.Entry(self.root)
        self.tipo_servicio_entry.grid(row=6, column=1)

        tk.Button(self.root, text="Agregar Servicio", command=self.agregar_servicio).grid(row=7, column=0, columnspan=2)

        # reserva
