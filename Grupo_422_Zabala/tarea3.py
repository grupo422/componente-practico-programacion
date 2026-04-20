import tkinter as tk                    # importa libreria para crear interfaz
from tkinter import ttk, messagebox     # importa componentes como mensajes
import json                             # permite guardar y leer datos en formato JSON
import os                               # permite interactuar con archivos del sistema

ARCHIVO = "employees.json"              # nombre del archivo donde se almacenan los empleados


class Empleado:                                                 # clase base empleado
    def __init__(self, nombre, identificacion, salario_base):   # constructor de la clase
        self.nombre = nombre                                    # guarda el nombre del empleado
        self.identificacion = identificacion                    # guarda el ID del empleado
        self.salario_base = salario_base                        # asigna el salario base usando el setter

    @property
    def salario_base(self):                                     # metodo para obtener el salario base
        return self.__salario_base                              # retorna el atributo privado

    @salario_base.setter
    def salario_base(self, valor):                              # metodo para modificar el salario base
        if valor < 0:                                            # validación no puede ser negativo
            raise ValueError("Salary cannot be negative")         # lanza error si es negativo
        self.__salario_base = valor                               # guarda el valor en variable privada

    def calcular_salario(self):                                   # metodo que sera sobrescrito en clases hijas
        raise NotImplementedError()                               # obliga a implementarlo en clases hijas

    def a_diccionario(self):                                      # convierte el objeto en diccionario para JSON
        return {
            "type": self.__class__.__name__,                      # guarda el tipo de empleado
            "name": self.nombre,                                  # guarda el nombre
            "identification": self.identificacion,                # guarda el ID
            "base_salary": self.salario_base                      # guarda el salario base
        }


class EmpleadoTiempoCompleto(Empleado):                               # clase hija tiempo completa
    def __init__(self, nombre, identificacion, salario_base, bono):
        super().__init__(nombre, identificacion, salario_base)         # hereda de la clase padre
        self.bono = bono                                               # asigna el bono

    @property
    def bono(self):                                                    # obtiene el bono
        return self.__bono

    @bono.setter
    def bono(self, valor):                                              # modifica el bono
        if valor < 0:                                                    # validacion
            raise ValueError("Bonus cannot be negative")
        self.__bono = valor                                             # guarda el bono

    def calcular_salario(self):                                          # calcula salario total
        return self.salario_base + self.bono                             # suma salario base + bono

    def a_diccionario(self):                                              # convierte a diccionario
        datos = super().a_diccionario()                                   # obtiene datos base
        datos["bonus"] = self.bono                                        # agrega bono
        return datos


class EmpleadoPorHoras(Empleado):                                       # clase hija por horas
    def __init__(self, nombre, identificacion, horas, tarifa):
        super().__init__(nombre, identificacion, 0)                     # salario base 0
        self.horas = horas                                              # horas trabajadas
        self.tarifa = tarifa                                            # pago por hora

    @property
    def horas(self):                                                    # obtiene horas
        return self.__horas

    @horas.setter
    def horas(self, valor):                                              # modifica horas
        if valor < 0:                                                    # validacion
            raise ValueError("Hours cannot be negative")
        self.__horas = valor

    @property
    def tarifa(self):                                                    # obtiene tarifa
        return self.__tarifa

    @tarifa.setter
    def tarifa(self, valor):                                               # modifica tarifa
        if valor < 0:                                                       # validacio
            raise ValueError("Rate cannot be negative")
        self.__tarifa = valor

    def calcular_salario(self):                                             # calcula salario
        return self.horas * self.tarifa                                     # multiplica horas por tarifa

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["hours"] = self.horas
        datos["rate"] = self.tarifa
        return datos


class EmpleadoComision(Empleado):                                                   # calse hija comision
    def __init__(self, nombre, identificacion, salario_base, ventas, porcentaje):
        super().__init__(nombre, identificacion, salario_base)
        self.ventas = ventas                                                         # total de ventas
        self.porcentaje = porcentaje                                                 # porcentaje de comision

    @property
    def ventas(self):
        return self.__ventas

    @ventas.setter
    def ventas(self, valor):
        if valor < 0:
            raise ValueError("Sales cannot be negative")
        self.__ventas = valor

    @property
    def porcentaje(self):
        return self.__porcentaje

    @porcentaje.setter
    def porcentaje(self, valor):
        if not (0 <= valor <= 1):                                                      # validacion entre 0 y 1
            raise ValueError("Percentage must be between 0 and 1")
        self.__porcentaje = valor

    def calcular_salario(self):
        return self.salario_base + (self.ventas * self.porcentaje)

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["sales"] = self.ventas
        datos["percentage"] = self.porcentaje
        return datos


class SistemaNomina:                                                     # sistema de nomina                                        
    def __init__(self):
        self.empleados = []                                               # lista de empleados
        self.cargar()                                                     # carga datos del archivo

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)                                  # agrega empleado a lista
        self.guardar()                                                    # guarda cambios

    def eliminar_empleado(self, index):
        if 0 <= index < len(self.empleados):                              # verifica indice valido
            del self.empleados[index]                                     # elimina empleado
            self.guardar()                                                # guarda cambios

    def calcular_nomina(self):
        return sum(emp.calcular_salario() for emp in self.empleados)      # suma salarios

    def guardar(self):
        datos = [emp.a_diccionario() for emp in self.empleados]           # convierte a lista de diccionarios
        with open(ARCHIVO, "w") as f:
            json.dump(datos, f, indent=4)                                 # guarda en JSON

    def cargar(self):
        if not os.path.exists(ARCHIVO):                                   # si no existe el archivo
            return
        with open(ARCHIVO, "r") as f:
            datos = json.load(f)                                          # carga datos
        for emp in datos:                                                 # recorre datos
            t = emp["type"]
            if t == "EmpleadoTiempoCompleto":
                obj = EmpleadoTiempoCompleto(emp["name"], emp["identification"], emp["base_salary"], emp["bonus"])
            elif t == "EmpleadoPorHoras":
                obj = EmpleadoPorHoras(emp["name"], emp["identification"], emp["hours"], emp["rate"])
            elif t == "EmpleadoComision":
                obj = EmpleadoComision(emp["name"], emp["identification"], emp["base_salary"], emp["sales"], emp["percentage"])
            else:
                continue
            self.empleados.append(obj)


class App:                                                              # interfaz grafica
    def __init__(self, root):
        self.root = root                                                # ventana principal
        self.root.title("Payroll System")                               # título
        self.system = SistemaNomina()                                   # instancia del sistema

        tk.Label(root, text="Name").grid(row=0, column=0)               # etiqueta nombre
        self.name = tk.Entry(root)                                      # campo nombre
        self.name.grid(row=0, column=1)

        tk.Label(root, text="ID").grid(row=1, column=0)                 # etiqueta ID
        self.id = tk.Entry(root)                                        # campo ID
        self.id.grid(row=1, column=1)

        tk.Label(root, text="Employee Type").grid(row=2, column=0)      # tipo de empleado
        self.type = ttk.Combobox(root, values=["Full Time", "Hourly", "Commission"])  # lista desplegable
        self.type.grid(row=2, column=1)
        self.type.bind("<<ComboboxSelected>>", self.fields)             # evento al seleccionar

        self.extra1 = tk.Entry(root)                                     # campo extra 1
        self.extra2 = tk.Entry(root)                                     # campo extra 2

        self.label1 = tk.Label(root, text="")                            # label reutilizable
        self.label2 = tk.Label(root, text="")

        tk.Button(root, text="Add Employee", command=self.add).grid(row=6, column=0)                 # boton agregar
        tk.Button(root, text="Calculate Payroll", command=self.calculate).grid(row=6, column=1)      # boton calcular
        tk.Button(root, text="Delete Selected", command=self.delete).grid(row=8, column=0, columnspan=2)  # boton eliminar

        self.table = ttk.Treeview(root, columns=("Name", "Salary"), show="headings")                      # tabla
        self.table.heading("Name", text="Name")
        self.table.heading("Salary", text="Salary")
        self.table.grid(row=7, column=0, columnspan=2)

        self.load_table()                                                 # cargar datos en tabla

    def validate(self):
        if not self.name.get().strip() or not self.id.get().strip():      # validar campos vacíos
            messagebox.showerror("Error", "Empty fields")
            return False
        return True

    def fields(self, e):
        self.extra1.grid_forget()                                           #oculta campo
        self.extra2.grid_forget()
        self.label1.grid_forget()                                           # oculta label
        self.label2.grid_forget()

        t = self.type.get()                                                 # obtiene tipo seleccionado

        if t == "Full Time":
            self.label1.config(text="Base Salary")
            self.label1.grid(row=3, column=0)
            self.extra1.grid(row=3, column=1)

            self.label2.config(text="Bonus")
            self.label2.grid(row=4, column=0)
            self.extra2.grid(row=4, column=1)

        elif t == "Hourly":
            self.label1.config(text="Hours")
            self.label1.grid(row=3, column=0)
            self.extra1.grid(row=3, column=1)

            self.label2.config(text="Rate")
            self.label2.grid(row=4, column=0)
            self.extra2.grid(row=4, column=1)

        elif t == "Commission":
            self.label1.config(text="Base Salary")
            self.label1.grid(row=3, column=0)
            self.extra1.grid(row=3, column=1)

            self.label2.config(text="Sales")
            self.label2.grid(row=4, column=0)
            self.extra2.grid(row=4, column=1)

    def add(self):
        if not self.validate():
            return

        try:
            nombre = self.name.get()                                      # obtener nombre
            identificacion = self.id.get()                                # obtener ID
            t = self.type.get()                                           # tipo empleado

            v1 = self.extra1.get()
            v2 = self.extra2.get()

            if not v1 or not v2:
                raise ValueError("Numeric fields required")

            v1 = float(v1)                                                 # convertir a numero
            v2 = float(v2)

            if t == "Full Time":
                emp = EmpleadoTiempoCompleto(nombre, identificacion, v1, v2)
            elif t == "Hourly":
                emp = EmpleadoPorHoras(nombre, identificacion, v1, v2)
            elif t == "Commission":
                emp = EmpleadoComision(nombre, identificacion, v1, v2, 0.1)
            else:
                messagebox.showerror("Error", "Select a type")
                return

            self.system.agregar_empleado(emp)                            # guardar empleado
            self.load_table()                                            # actualizar tabla

            messagebox.showinfo("Success", "Saved to JSON")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete(self):
        seleccionado = self.table.selection()                            # obtener fila seleccionada

        if not seleccionado:
            messagebox.showerror("Error", "Select a row")
            return

        index = self.table.index(seleccionado)                   # obtener índice
        self.system.eliminar_empleado(index)                     # eliminar
        self.load_table()                                        # refrescar tabla

        messagebox.showinfo("Success", "Employee deleted")

    def calculate(self):
        total = self.system.calcular_nomina()                   # calcular valor total
        messagebox.showinfo("Total Payroll", f"{total:.2f}")

    def load_table(self):
        for item in self.table.get_children():                 # limpiar tabla
            self.table.delete(item)

        for emp in self.system.empleados:                      # insertar datos
            self.table.insert("", "end", values=(emp.nombre, emp.calcular_salario()))


if __name__ == "__main__":                             # ejecucioin del programa
    root = tk.Tk()                                     # craer ventana
    app = App(root)                                    # crear aplicacion
    root.mainloop()                                    # ejecutar interfaz



