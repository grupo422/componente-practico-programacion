import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
from datetime import datetime

### logs 

def registrar_log(mensaje):
    with open("sistema_reservas.log", "a") as log_file:
        log_file.write(f"{datetime.now()}: {mensaje}\n")

    

class Entidad(ABC):   # clase abstracta
    def _init_(self, id):
        self._id = id            # crea el ID 
        self._fecha_creacion = datetime.now() # crea la fecha

    @abstractmethod
    def mostrar_info(self):
        pass

    def get_id(self):
        return self._id


### Excepciones personalizadas para manejo de errores en el sistema ###
### Se definen para controlar errores específicos del sistema ###
class sistemaError(Exception):pass
class ReservaError(sistemaError):pass
class ClienteError(sistemaError):pass
class ServicioError(sistemaError):pass


## clases abstractas y concretas para el sistema de reservas de servicios###
class Cliente(Entidad): # clase cliente

    def _init_(self, id, nombre, email):
        super()._init_(id)
        self.set_nombre(nombre)
        self.set_email(email)

    def set_nombre(self, nombre):
        # Validación del nombre (no vacío)
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = nombre

    def set_email(self, email):
        # Validación básica de email
        if "@" not in email or "." not in email:
            raise ValueError("Email inválido")
        self._email = email

    def get_nombre(self):
        return self._nombre

    def get_email(self):
        return self._email

    def mostrar_info(self):
        return f"Cliente: {self._nombre} | Email: {self._email}"


class Servicio(Entidad): # CLASE ABSTRACTA SERVICIO

    def _init_(self, id, nombre, tarifa_base):
        super()._init_(id)
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

    def descripcion(self): # Método que describe el tipo de servicio
        return "Alquiler de sala" # Retorna una descripción del servicio


class Equipo(Servicio): # Clase Equipo que también hereda de Servicio
    def calcular_costo(self, duracion): # Método para calcular el costo del equipo
        return self._tarifa_base * duracion # Calcula costo igual que Sala (tarifa * tiempo)

    def descripcion(self): # Método que describe el servicio
        return "Alquiler de equipo" # Devuelve el tipo de servicio


class Asesoria(Servicio): # Clase Asesoria que hereda de Servicio
    def calcular_costo(self, duracion): # Método para calcular el costo de la asesoría
        return (self._tarifa_base * duracion) * 1.2 # Calcula el costo y le aplica un recargo del 20% (multiplica por 1.2)

    def descripcion(self):
        return "Servicio de asesoría" # Retorna el nombre del servicio


### Clase Reserva que maneja las reservas de servicios ###
class Reserva:

    def _init_(self, cliente, servicio, duracion_horas):
        if duracion_horas <= 0:
            raise ValueError("La duración debe ser mayor a cero")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = "Pendiente" # Estado inicial de la reserva
        self._fecha_reserva = datetime.now() # Fecha de creación de la reserva

        self._costo_base = servicio.calcular_costo(duracion_horas) # Calcula el costo base usando el método del servicio

    def calcular_costo_total(self, impuesto=0, descuento=0):
        # Método sobrecargado (permite agregar impuestos o descuentos)
        costo = self._servicio.calcular_costo(self._duracion_horas)
        
        return costo

    def confirmar_reserva(self):
        try:
            if self._estado != "Pendiente":
                raise ValueError("Solo se pueden confirmar reservas pendientes")

            self._estado = "Confirmada" # Cambia el estado a confirmada
            registrar_log("Reserva confirmada")

            print(f"Reserva confirmada para {self._cliente.get_nombre()}")

        except Exception as e:
            registrar_log(f"Error al confirmar reserva: {e}")

    def cancelar_reserva(self):
        try:
            if self._estado != "Confirmada":
                raise ValueError("Solo se pueden cancelar reservas confirmadas")

            self._estado = "Cancelada" # Cambia el estado a cancelada
            print(f"Reserva cancelada para {self._cliente.get_nombre()}")

        except Exception as e:
            registrar_log(f"Error al cancelar reserva: {e}")

    def procesar(self):
        try:
            if self._estado != "Confirmada":
                raise ValueError("Solo se pueden procesar reservas confirmadas")

            self._estado = "Procesada" # Cambia el estado a procesada
            print(f"Reserva procesada para {self._cliente.get_nombre()} - Servicio: {self._servicio.descripcion()}")

        except Exception as e:
            registrar_log(f"Error al procesar reserva: {e}")

    def mostrar_info(self):
        return (f"Reserva para {self._cliente.get_nombre()} | Servicio: {self._servicio.descripcion()} | "
                f"Duración: {self._duracion_horas} horas | Costo Total: ${self.calcular_costo_total():.2f} | "
                f"Estado: {self._estado}")


## Clase principal del sistema de reservas ###
class app:

    def _init_(self):
        self._clientes = {} # Diccionario para almacenar clientes por ID
        self._servicios = {} # Diccionario para almacenar servicios por ID
        self._reservas = [] # Lista para almacenar reservas

    def agregar_cliente(self, id, nombre, email): # Método para agregar un cliente al sistema
        try:   # Intenta ejecutar el bloque 
            if id in self._clientes:  # Verifica si el ID del cliente ya existe en el sistema
                raise ClienteError("El cliente con este ID ya existe") # Si el ID ya existe, lanza una excepción personalizada ClienteError

            cliente = Cliente(id, nombre, email) # Crea una nueva instancia de Cliente con los datos proporcionados
            self._clientes[id] = cliente # Agrega el cliente al diccionario de clientes usando su ID como clave

            registrar_log(f"Cliente agregado: {cliente.mostrar_info()}") # Registra en el archivo log el cliente agregado
            return "Cliente agregado correctamente"  # Retorna un mensaje de confirmación

        except (ClienteError, ValueError) as e:  # Captura errores personalizados y errores de validación
            registrar_log(f"Error al agregar cliente: {e}") # Guarda el error en el archivo log

        finally:
            print("Proceso de registro de cliente finalizado") # Retorna el mensaje del error

    def agregar_servicio(self, id, nombre, tarifa_base, tipo): ### Método para agregar un servicio al sistema
        try:
            if id in self._servicios: ### Verifica si el ID del servicio ya existe en el sistema
                raise ServicioError("El servicio con este ID ya existe") ### Si el ID ya existe, lanza una excepción personalizada ServicioError

            if tipo == "Sala": ### Dependiendo del tipo de servicio, crea una instancia de la clase correspondiente (Sala, Equipo o Asesoria)
                servicio = Sala(id, nombre, tarifa_base) ### Si el tipo es "Sala", crea una instancia de la clase Sala
            elif tipo == "Equipo": ### Si el tipo es "Equipo", crea una instancia de la clase Equipo
                servicio = Equipo(id, nombre, tarifa_base) ### Si el tipo es "Asesoria", crea una instancia de la clase Asesoria
            elif tipo == "Asesoria":  ### Si el tipo es "Asesoria", crea una instancia de la clase Asesoria
                servicio = Asesoria(id, nombre, tarifa_base) ### Si el tipo es "Asesoria", crea una instancia de la clase Asesoria
            else:
                raise ValueError("Tipo de servicio inválido") ### Si el tipo de servicio no coincide con ninguno de los casos anteriores, lanza una excepción indicando que el tipo de servicio es inválido

            self._servicios[id] = servicio  ####    Agrega el servicio al diccionario de servicios usando su ID como clave
            registrar_log(f"Servicio agregado: {servicio.descripcion()} - Tarifa Base: ${tarifa_base:.2f}") # Log de servicio agregado

        except Exception as e:
            registrar_log(f"Error al agregar servicio: {e}") # Da error si se agrega un servicio invalido 

    def crear_reserva(self, id_cliente, id_servicio, duracion):
        # Método para crear reservas integrando cliente y servicio
        try:
            if id_cliente not in self._clientes:
                raise ClienteError("Cliente no existe")

            if id_servicio not in self._servicios:
                raise ServicioError("Servicio no existe")

            reserva = Reserva(self._clientes[id_cliente], self._servicios[id_servicio], duracion)

            self._reservas.append(reserva)
            registrar_log("Reserva creada correctamente")

            return reserva

        except Exception as e:
            registrar_log(f"Error al crear reserva: {e}")
            return None



# simulacion sistema


if _name_ == "_main_":

    sistema = app()

    # Registro de clientes (correcto e incorrecto)
    print(sistema.agregar_cliente(1, "Oscar", "oscar@gmail.com"))
    print(sistema.agregar_cliente(1, "", "malcorreo")) # error

    # Registro de servicios
    sistema.agregar_servicio(1, "Sala VIP", 50000, "Sala")
    sistema.agregar_servicio(2, "PC Gamer", 20000, "Equipo")
    sistema.agregar_servicio(3, "Consultoria", 100000, "Asesoria")

    # Crear reserva válida
    r1 = sistema.crear_reserva(1, 1, 2)

    if r1:
        r1.confirmar_reserva()
        r1.procesar()
        print(r1.mostrar_info())

    # Reserva inválida
    sistema.crear_reserva(99, 1, 2) # cliente no existe

    
# interfaz grafica TKINTER


class InterfazApp:
    def _init_(self, sistema):
        self.sistema = sistema

        # Ventana principal
        self.root = tk.Tk()
        self.root.title("Sistema de Reservas - Software FJ")
        self.root.geometry("500x500")

       
        # pantalla clientes 
                
        tk.Label(self.root, text="ID Cliente:").grid(row=0, column=0)
        self.id_cliente = tk.Entry(self.root)
        self.id_cliente.grid(row=0, column=1)

        tk.Label(self.root, text="Nombre:").grid(row=1, column=0)
        self.nombre_cliente = tk.Entry(self.root)
        self.nombre_cliente.grid(row=1, column=1)

        tk.Label(self.root, text="Email:").grid(row=2, column=0)
        self.email_cliente = tk.Entry(self.root)
        self.email_cliente.grid(row=2, column=1)

        tk.Button(self.root, text="Agregar Cliente", command=self.agregar_cliente).grid(row=3, column=0, columnspan=2)

       
        # pantalla servicios
        
        tk.Label(self.root, text="\nID Servicio:").grid(row=4, column=0)
        self.id_servicio = tk.Entry(self.root)
        self.id_servicio.grid(row=4, column=1)

        tk.Label(self.root, text="Nombre Servicio:").grid(row=5, column=0)
        self.nombre_servicio = tk.Entry(self.root)
        self.nombre_servicio.grid(row=5, column=1)

        tk.Label(self.root, text="Tarifa Base:").grid(row=6, column=0)
        self.tarifa_servicio = tk.Entry(self.root)
        self.tarifa_servicio.grid(row=6, column=1)

        tk.Label(self.root, text="Tipo (Sala/Equipo/Asesoria):").grid(row=7, column=0)
        self.tipo_servicio = tk.Entry(self.root)
        self.tipo_servicio.grid(row=7, column=1)

        tk.Button(self.root, text="Agregar Servicio", command=self.agregar_servicio).grid(row=8, column=0, columnspan=2)

        
        # pantalla reservas
        
        tk.Label(self.root, text="\nID Cliente:").grid(row=9, column=0)
        self.reserva_cliente = tk.Entry(self.root)
        self.reserva_cliente.grid(row=9, column=1)

        tk.Label(self.root, text="ID Servicio:").grid(row=10, column=0)
        self.reserva_servicio = tk.Entry(self.root)
        self.reserva_servicio.grid(row=10, column=1)

        tk.Label(self.root, text="Duración (horas):").grid(row=11, column=0)
        self.reserva_duracion = tk.Entry(self.root)
        self.reserva_duracion.grid(row=11, column=1)

        tk.Button(self.root, text="Crear Reserva", command=self.crear_reserva).grid(row=12, column=0, columnspan=2)

    
       
    def agregar_cliente(self): # Funciones botones 
        try:
            resultado = self.sistema.agregar_cliente(
                int(self.id_cliente.get()),
                self.nombre_cliente.get(),
                self.email_cliente.get()
            )
            messagebox.showinfo("Resultado", resultado)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def agregar_servicio(self):
        try:
            self.sistema.agregar_servicio(
                int(self.id_servicio.get()),
                self.nombre_servicio.get(),
                float(self.tarifa_servicio.get()),
                self.tipo_servicio.get()
            )
            messagebox.showinfo("Resultado", "Servicio agregado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def crear_reserva(self):
        try:
            reserva = self.sistema.crear_reserva(
                int(self.reserva_cliente.get()),
                int(self.reserva_servicio.get()),
                float(self.reserva_duracion.get())
            )

            if reserva:
                reserva.confirmar_reserva()
                messagebox.showinfo("Reserva", reserva.mostrar_info())
            else:
                messagebox.showerror("Error", "No se pudo crear la reserva")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ejecutar(self):
        self.root.mainloop()



# integrar el sistema 

if _name_ == "_main_":
    sistema = app()
    interfaz = InterfazApp(sistema)
    interfaz.ejecutar()

