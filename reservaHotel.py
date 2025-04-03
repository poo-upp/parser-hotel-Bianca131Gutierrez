#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sistema de Reservaciones para un Hotel

from datetime import datetime, timedelta


# Clase base Habitacion que representa cualquier tipo de habitación en el hotel
class Habitacion:
    def __init__(self, numero, capacidad, precio, disponible=True):
        # Inicializa los atributos básicos de la habitación
        self.numero = numero
        self.capacidad = capacidad
        self.precio = precio
        self._disponible = disponible  # atributo privado para manejar disponibilidad

    @property
    def disponible(self):
        # Devuelve el estado de disponibilidad de la habitación
        return self._disponible

    @disponible.setter
    def disponible(self, estado):
        # Permite modificar la disponibilidad de la habitación
        self._disponible = estado

    def __eq__(self, otra):
        # Compara dos habitaciones en función de su número, capacidad y precio
        return (self.numero == otra.numero and
                self.capacidad == otra.capacidad and
                self.precio == otra.precio)

    def __add__(self, otra):
        # Calcula el costo total al sumar el precio de dos habitaciones
        return self.precio + otra.precio


# Clase HabitacionSimple con características específicas
# Habitación simple: capacidad para 1 persona y precio fijo
class HabitacionSimple(Habitacion):
    def __init__(self, numero):
        super().__init__(numero, capacidad=1, precio=500)


# Clase HabitacionDoble con características específicas
# Habitación doble: capacidad para 2 personas y precio fijo
class HabitacionDoble(Habitacion):
    def __init__(self, numero, balcon=False):
        super().__init__(numero, capacidad=2, precio=900)
        self.balcon = balcon  # Nuevo atributo


# Clase Suite con opción adicional de jacuzzi
# Suite: capacidad para 4 personas y precio base más alto
class Suite(Habitacion):
    def __init__(self, numero, jacuzzi=False):
        super().__init__(numero, capacidad=4, precio=2000)
        self.jacuzzi = jacuzzi  # Nuevo atributo


# Clase Cliente que gestiona la información del cliente y sus reservas
class Cliente:
    def __init__(self, nombre, correo):
        self.nom = nombre
        self.correo = correo
        # Lista para almacenar todas las reservas del cliente
        self.reservas = []

    # Clase Reserva que crea una relación entre cliente, habitación y fechas


class Reserva:
    def __init__(self, cliente, habitacion, fecha_inicio, fecha_fin):
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        # Se agrega la reserva al historial del cliente
        self.cliente.reservas.append(self)
        # La habitación se marca como no disponible
        self.habitacion.disponible = False  # cambia

#
def parser(documento):
    with open(documento, 'r') as file:
        cliente = None
        habitaciones = []
        numero_noches = None
        fecha_inicio = None
        fecha_fin = None
        for line in file:
            line = line.strip()
            if "Nombre del cliente" in line:
                nombre = next(file).strip()
            elif "correo" in line.lower():
                correo = str(line.split()[-1])
                cliente = Cliente(nombre, correo)
            elif "habitacion sencilla" in line.lower():
                habitaciones.append(HabitacionSimple(1))
            elif "habitacion doble" in line.lower():
                habitaciones.append(HabitacionDoble(3))
            elif "suite" in line.lower():
                habitaciones.append(Suite(2))
            elif "numero de noches" in line.lower():
                numero_noches = int(line.split()[-1])
            elif "fecha inicio" in line.lower():
                fecha_inicio = datetime.strptime(line.split()[-1], "%d-%m-%Y")
                if numero_noches is not None:
                    fecha_fin = fecha_inicio + timedelta(days=numero_noches)
        return cliente, habitaciones, fecha_inicio, fecha_fin



def generar_resumen(cliente, habitaciones, fecha_inicio, fecha_fin, archivo_salida):
    total_personas = sum(h.capacidad for h in habitaciones)
    total_precio = sum(h.precio for h in habitaciones)
    with open(archivo_salida, 'w') as file:
        file.write(f"Hola {cliente.nom}! aqui tienes los detalles de tu reserva:\n\n")
        file.write(f"Entrada:\t{fecha_inicio.strftime('%d-%m-%Y')}\n")
        file.write(f"Salida:\t{fecha_fin.strftime('%d-%m-%Y')}\n\n")
        file.write(f"Reservaste\t[{(fecha_fin - fecha_inicio).days}] noches, "
                f"[{len(habitaciones)}] habitaciones, [{total_personas}] personas\n\n")
        file.write("Detalles de reserva\n")
        for h in habitaciones:
            file.write(f"[1]\t{h.__class__.__name__}\n")
        file.write(f"\nCorreo electronico de contacto:\t[{cliente.correo}]\n\n")
        file.write("Detalles del precio:\n")
        for h in habitaciones:
            file.write(f"[1]\t{h.__class__.__name__}\t\t\t{h.precio:.2f}$\n")
        file.write("----------------------------------------------\n")
        file.write(f"Total:\t\t\t\t\t\t{total_precio:.2f}$\n")


# Archivo de entrada y salida
doc = "input.txt"
salida = "ejemplo-out.txt"

# Procesar archivo de entrada y generar resumen
cliente, habitaciones, fecha_inicio, fecha_fin = parser(doc)
generar_resumen(cliente, habitaciones, fecha_inicio, fecha_fin, salida)

