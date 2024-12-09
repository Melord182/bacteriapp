import numpy as np
from scipy.optimize import curve_fit
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
import matplotlib.pyplot as plt

# Definir la función exponencial
def modelo_exponencial(x, a, b):
    return a * np.exp(b * x)

class BacteriApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BacteriApp")
        
        # Variables de los puntos
        self.x_datos = []
        self.y_datos = []
        self.a = None
        self.b = None
        
        # Crear la interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Título
        tk.Label(self.root, text="BacteriApp", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=10)
        
        # Ingreso de puntos
        self.lbl_num_puntos = tk.Label(self.root, text="¿Cuántos puntos vas a ingresar?")
        self.lbl_num_puntos.grid(row=1, column=0, pady=5)
        
        self.ent_num_puntos = tk.Entry(self.root)
        self.ent_num_puntos.grid(row=1, column=1)
        
        self.btn_ingresar_puntos = tk.Button(self.root, text="Ingresar Puntos", command=self.ingresar_puntos)
        self.btn_ingresar_puntos.grid(row=1, column=2)
        
        # Mostrar ecuación
        self.lbl_ecuacion = tk.Label(self.root, text="Ecuación: ", font=("Helvetica", 12))
        self.lbl_ecuacion.grid(row=2, column=0, columnspan=3, pady=10)

        # Botones de acción
        self.btn_guardar = tk.Button(self.root, text="Guardar Ecuación", command=self.guardar_ecuacion)
        self.btn_guardar.grid(row=3, column=0, pady=5)

        self.btn_calcular_bacterias = tk.Button(self.root, text="Calcular Bacterias", command=self.calcular_bacterias)
        self.btn_calcular_bacterias.grid(row=3, column=1, pady=5)

        self.btn_calcular_horas = tk.Button(self.root, text="Calcular Horas", command=self.calcular_horas)
        self.btn_calcular_horas.grid(row=3, column=2, pady=5)

        self.btn_historial = tk.Button(self.root, text="Historial de Simulaciones", command=self.mostrar_historial)
        self.btn_historial.grid(row=4, column=0, columnspan=3, pady=5)
        
        self.btn_mostrar_grafico = tk.Button(self.root, text="Mostrar Gráfico", command=self.mostrar_grafico)
        self.btn_mostrar_grafico.grid(row=5, column=0, columnspan=3, pady=5)

    def ingresar_puntos(self):
        try:
            num_puntos = int(self.ent_num_puntos.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido de puntos.")
            return
        
        self.x_datos.clear()
        self.y_datos.clear()
        
        self.ventana_puntos = tk.Toplevel(self.root)
        self.ventana_puntos.title("Ingresar Puntos")
        
        for i in range(num_puntos):
            tk.Label(self.ventana_puntos, text=f"Hora {i+1}:").grid(row=i, column=0)
            tk.Label(self.ventana_puntos, text=f"Bacterias {i+1}:").grid(row=i, column=2)
            
            x_entry = tk.Entry(self.ventana_puntos)
            y_entry = tk.Entry(self.ventana_puntos)
            
            x_entry.grid(row=i, column=1)
            y_entry.grid(row=i, column=3)
            
            self.x_datos.append(x_entry)
            self.y_datos.append(y_entry)
        
        btn_ajustar = tk.Button(self.ventana_puntos, text="Ajustar Curva", command=self.ajustar_curva)
        btn_ajustar.grid(row=num_puntos, column=0, columnspan=4, pady=10)

    def ajustar_curva(self):
        try:
            x = np.array([float(x_entry.get()) for x_entry in self.x_datos])
            y = np.array([float(y_entry.get()) for y_entry in self.y_datos])
            
            # Ajuste de la curva
            parametros, _ = curve_fit(modelo_exponencial, x, y)
            self.a, self.b = parametros
            
            # Mostrar ecuación
            ecuacion = f"f(x) = {self.a:.4f} * e^({self.b:.4f} * x)"
            self.lbl_ecuacion.config(text=f"Ecuación: {ecuacion}")
            
            # Guardar los datos para graficar
            self.x_plot = x
            self.y_plot = y
            
            # Cerrar la ventana de ingresar puntos
            self.ventana_puntos.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa todos los puntos correctamente.")

    def mostrar_historial(self):
        self.ventana_historial = tk.Toplevel(self.root)
        self.ventana_historial.title("Historial de Simulaciones")
        
        archivos = [f for f in os.listdir() if f.endswith(".txt")]
        if not archivos:
            messagebox.showinfo("Historial", "No hay simulaciones guardadas.")
            self.ventana_historial.destroy()
            return
        
        tk.Label(self.ventana_historial, text="Simulaciones Guardadas:").pack(pady=10)
        self.listbox_archivos = tk.Listbox(self.ventana_historial)
        self.listbox_archivos.pack(padx=10, pady=10)
        
        for archivo in archivos:
            self.listbox_archivos.insert(tk.END, archivo)
        
        btn_cargar = tk.Button(self.ventana_historial, text="Cargar", command=self.cargar_simulacion)
        btn_cargar.pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_eliminar = tk.Button(self.ventana_historial, text="Eliminar", command=self.eliminar_simulacion)
        btn_eliminar.pack(side=tk.RIGHT, padx=10, pady=10)

    def cargar_simulacion(self):
        seleccion = self.listbox_archivos.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una simulación para cargar.")
            return
        
        archivo = self.listbox_archivos.get(seleccion)
        with open(archivo, 'r') as file:
            contenido = file.readlines()
        
        # Leer los datos del archivo
        self.nombre_bacteria = contenido[0].split(":")[1].strip()
        self.medio_propagacion = contenido[1].split(":")[1].strip()
        ecuacion = contenido[2].strip()
        
        self.lbl_ecuacion.config(text=f"Ecuación: {ecuacion}")
        
        # Extraer parámetros de la ecuación
        parametros = ecuacion.split("=")[1].split("*")
        self.a = float(parametros[0].strip())
        self.b = float(parametros[1].split("^")[1].strip()[1:-1])
        
        messagebox.showinfo("Cargar Simulación", f"Simulación '{archivo}' cargada con éxito.")
        self.ventana_historial.destroy()

    def eliminar_simulacion(self):
        seleccion = self.listbox_archivos.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una simulación para eliminar.")
            return
        
        archivo = self.listbox_archivos.get(seleccion)
        os.remove(archivo)
        messagebox.showinfo("Eliminar Simulación", f"Simulación '{archivo}' eliminada con éxito.")
        self.listbox_archivos.delete(seleccion)

    def guardar_ecuacion(self):
        if self.a is None or self.b is None:
            messagebox.showerror("Error", "No hay ninguna ecuación para guardar.")
            return
        
        # Pedir el nombre de la bacteria y del medio de propagación
        self.nombre_bacteria = simpledialog.askstring("Guardar Ecuación", "Ingresa el nombre de la bacteria:")
        if not self.nombre_bacteria:
            messagebox.showerror("Error", "El nombre de la bacteria es obligatorio.")
            return
        
        self.medio_propagacion = simpledialog.askstring("Guardar Ecuación", "Ingresa el medio de propagación:")
        if not self.medio_propagacion:
            messagebox.showerror("Error", "El medio de propagación es obligatorio.")
            return
        
        # Crear el nombre del archivo usando la bacteria y el medio
        nombre_archivo = f"{self.nombre_bacteria}_{self.medio_propagacion}.txt"
        
        # Guardar la ecuación en el archivo
        with open(nombre_archivo, 'w') as file:
            file.write(f"Bacteria: {self.nombre_bacteria}\n")
            file.write(f"Medio de Propagación: {self.medio_propagacion}\n")
            file.write(f"Ecuación: f(x) = {self.a:.4f} * e^({self.b:.4f} * x)\n")
        
        messagebox.showinfo("Guardar Ecuación", f"Ecuación guardada como {nombre_archivo}")

    def calcular_bacterias(self):
        if self.a is None or self.b is None:
            messagebox.showerror("Error", "No hay ninguna ecuación cargada.")
            return
        
        x_horas = simpledialog.askfloat("Calcular Bacterias", "Ingresa el número de horas:")
        if x_horas is None:
            return
        
        y_bacterias = modelo_exponencial(x_horas, self.a, self.b)
        messagebox.showinfo("Calcular Bacterias", f"Número estimado de bacterias: {y_bacterias:.2f}")

    def calcular_horas(self):
        if self.a is None or self.b is None:
            messagebox.showerror("Error", "No hay ninguna ecuación cargada.")
            return
        
        y_objetivo = simpledialog.askfloat("Calcular Horas", "Ingresa el número de bacterias objetivo:")
        if y_objetivo is None or y_objetivo <= 0 or y_objetivo < self.a:
            messagebox.showerror("Error", "Número de bacterias no válido.")
            return
        
        x_horas = np.log(y_objetivo / self.a) / self.b
        messagebox.showinfo("Calcular Horas", f"Tiempo estimado: {x_horas:.2f} horas")

    def mostrar_grafico(self):
        if not hasattr(self, 'x_plot') or not hasattr(self, 'y_plot'):
            messagebox.showerror("Error", "No hay datos para graficar.")
            return
        
        plt.scatter(self.x_plot, self.y_plot, color='blue', label='Datos')
        x_line = np.linspace(min(self.x_plot), max(self.x_plot), 100)
        y_line = modelo_exponencial(x_line, self.a, self.b)
        plt.plot(x_line, y_line, color='red', label='Ajuste')
        plt.xlabel("Horas")
        plt.ylabel("Número de Bacterias")
        plt.title("Crecimiento de Bacterias")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BacteriApp(root)
    root.mainloop()
