from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):   # clase abstracta
    def __init__(self, id):
        self._id = id            # crea el ID 
        self._fecha_creacion = datetime.now()  # crea la fecha 

    @abstractmethod
    def mostrar_info(self):
        pass

    def get_id(self):
        return self._id



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
        return "Servicio de asesoría" # Retorna el nombre del serviciogi


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
    

        

