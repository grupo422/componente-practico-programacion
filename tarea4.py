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