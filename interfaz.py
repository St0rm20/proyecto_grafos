import tkinter as tk
from tkinter import messagebox as error
import math
import networkx as nx
import matplotlib.pyplot as plt


class AplicacionFloydWarshall:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo de Floyd-Warshall")  # Título de la ventana
        self.root.geometry("600x400")  # Tamaño inicial de la ventana
        self.root.configure(bg="#f0f0f0")  # Color de fondo de la ventana
        self.root.minsize(600, 400)  # Tamaño mínimo de la ventana

        # Crear la matriz inicial del ejercicio
        self.matriz_inicial = [
            [0, 12, 18, math.inf],
            [math.inf, 0, 9, math.inf],
            [math.inf, math.inf, 0, 5],
            [16, math.inf,math.inf, 0]
        ]
        
        self.configurar_interfaz_inicial()  # Configurar la interfaz inicial

    # Método para aplicar estilo a un texto (etiqueta)
    def estilo_texto(self, etiqueta):
        etiqueta.config(font=('Segoe UI', 10), bg="#f0f0f0", fg="#333")

    # Método para crear un botón con estilo personalizado
    def boton_estilizado(self, padre, texto, comando):
        return tk.Button(padre, text=texto, command=comando,
                         bg="#4CAF50", fg="white", activebackground="#45a049",
                         font=("Segoe UI", 10), padx=10, pady=5, relief="raised", bd=2)

    # Configura la interfaz inicial de la aplicación
    def configurar_interfaz_inicial(self):
        self.limpiar_marco_inicial()  # Limpiar cualquier interfaz anterior

        # Crear un marco inicial
        self.marco_inicial = tk.Frame(self.root, bg="#f0f0f0")
        self.marco_inicial.pack(padx=20, pady=20)

        # Título de la interfaz inicial
        titulo = tk.Label(self.marco_inicial, text="Ingrese la matriz de adyacencia", font=('Segoe UI', 14, 'bold'))
        self.estilo_texto(titulo)
        titulo.grid(row=0, column=0, columnspan=3, pady=10)

        # Entrada para el tamaño de la matriz
        tk.Label(self.marco_inicial, text="Tamaño (n x n):", bg="#f0f0f0").grid(row=1, column=0, sticky="e")
        self.entrada_tamano = tk.Entry(self.marco_inicial, width=5, font=('Segoe UI', 10))
        self.entrada_tamano.grid(row=1, column=1)
        self.entrada_tamano.insert(0, "4")  # Tamaño predeterminado

        # Botón para aplicar el tamaño de la matriz
        self.boton_estilizado(self.marco_inicial, "Aplicar", self.crear_cuadricula_matriz).grid(row=1, column=2, padx=5)

        # Marco para la matriz
        self.marco_matriz = tk.LabelFrame(self.marco_inicial, text="Matriz", bg="#f0f0f0", font=('Segoe UI', 10, 'bold'))
        self.marco_matriz.grid(row=2, column=0, columnspan=3, pady=10)

        self.crear_cuadricula_matriz()  # Crear la cuadrícula de la matriz

        # Botones de acción
        marco_botones = tk.Frame(self.marco_inicial, bg="#f0f0f0")
        marco_botones.grid(row=3, column=0, columnspan=3, pady=15)

        self.boton_estilizado(marco_botones, "Iniciar", self.iniciar_algoritmo).pack(side=tk.LEFT, padx=5)
        self.boton_estilizado(marco_botones, "Limpiar", self.limpiar_matriz).pack(side=tk.LEFT, padx=5)
        self.boton_estilizado(marco_botones, "Usar ejercicio", self.cargar_ejemplo).pack(side=tk.LEFT, padx=5)
        self.boton_estilizado(marco_botones, "Grafo", self.mostrar_grafo).pack(side=tk.LEFT, padx=5)

    # Crear la cuadrícula para la matriz de entrada
    def crear_cuadricula_matriz(self):
        for widget in self.marco_matriz.winfo_children():
            widget.destroy()

        try:
            tamano = int(self.entrada_tamano.get())
            if tamano < 2:
                raise ValueError("El tamaño debe ser al menos 2")
        except ValueError:
            error.showerror("Error", "Por favor ingrese un número válido para el tamaño de la matriz")
            return

        self.entradas_matriz = []
        for i in range(tamano):
            fila_entradas = []
            for j in range(tamano):
                entrada = tk.Entry(self.marco_matriz, width=6, justify="center", font=('Segoe UI', 10))
                entrada.grid(row=i, column=j, padx=3, pady=3)
                if i == j:
                    entrada.insert(0, "0")  # Los valores en la diagonal son 0
                fila_entradas.append(entrada)
            self.entradas_matriz.append(fila_entradas)

    # Limpiar los valores de la matriz
    def limpiar_matriz(self):
        for fila in self.entradas_matriz:
            for entrada in fila:
                entrada.delete(0, tk.END)

    # Cargar el ejemplo predefinido en la matriz
    def cargar_ejemplo(self):
        self.limpiar_matriz()
        tamano = len(self.matriz_inicial)
        self.entrada_tamano.delete(0, tk.END)
        self.entrada_tamano.insert(0, str(tamano))
        self.crear_cuadricula_matriz()

        for i in range(tamano):
            for j in range(tamano):
                valor = self.matriz_inicial[i][j]
                self.entradas_matriz[i][j].delete(0, tk.END)
                if not math.isinf(valor):
                    self.entradas_matriz[i][j].insert(0, str(valor))

    # Obtener la matriz desde las entradas
    def obtener_matriz_desde_entradas(self):
        matriz = []
        for i, fila in enumerate(self.entradas_matriz):
            fila_matriz = []
            for j, entrada in enumerate(fila):
                valor = entrada.get()
                if not valor:
                    fila_matriz.append(math.inf)
                else:
                    try:
                        fila_matriz.append(float(valor))
                    except ValueError:
                        error.showerror("Error", f"Valor inválido en la posición ({i+1}, {j+1})")
                        return None
            matriz.append(fila_matriz)
        return matriz



    def mostrar_grafo(self, dirigido=True, con_pesos=True):
        # Validar matriz
        if not self.matriz_inicial:
            print("Error: Matriz vacía")
            return

        # Crear grafo (dirigido o no)
        self.grafo = nx.DiGraph() if dirigido else nx.Graph()
        n = len(self.matriz_inicial)
        self.grafo.add_nodes_from(range(n))

        # Añadir aristas (ignorar 0 e infinito)
        for i in range(n):
            for j in range(n):
                peso = self.matriz_inicial[i][j]
                if peso != 0 and peso != float('inf'):
                    self.grafo.add_edge(i, j, weight=peso)

        # Dibujar
        pos = nx.spring_layout(self.grafo)
        nx.draw_networkx_nodes(self.grafo, pos, node_size=700, node_color='lightblue')
        nx.draw_networkx_labels(self.grafo, pos)

        # Estilo de aristas
        edge_style = '->' if dirigido else '-'
        nx.draw_networkx_edges(self.grafo, pos, arrowstyle=edge_style, width=2)

        # Mostrar pesos si está habilitado
        if con_pesos:
            edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
            nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=edge_labels)

        plt.title("Grafo desde Matriz Inicial")
        plt.axis('off')
        plt.show()

    # Iniciar el algoritmo de Floyd-Warshall
    def iniciar_algoritmo(self):
        matriz = self.obtener_matriz_desde_entradas()
        if matriz is None:
            return
        
        print("Matriz ingresada:", matriz)
        for i in range(len(matriz) - 1):
            matriz[i][len(matriz) - 1] += 5

        for i in range(len(matriz)-1):
            matriz[len(matriz) - 1][i] += 5

        tamano = len(matriz)
        for fila in matriz:
            if len(fila) != tamano:
                error.showerror("Error", "La matriz debe ser cuadrada (n x n)")
                return

        # Inicializar las iteraciones
        self.todas_iteraciones = [matriz]
        self.cambios_iteraciones = [[[0 for _ in range(tamano)] for _ in range(tamano)] for _ in range(tamano+1)]

        # Algoritmo de Floyd-Warshall
        for k in range(tamano):
            matriz_anterior = [fila[:] for fila in self.todas_iteraciones[-1]]
            nueva_matriz = [fila[:] for fila in matriz_anterior]
            matriz_cambios = [fila[:] for fila in self.cambios_iteraciones[k]]

            for i in range(tamano):
                for j in range(tamano):
                    nuevo_valor = min(matriz_anterior[i][j], matriz_anterior[i][k] + matriz_anterior[k][j])
                    if nuevo_valor != matriz_anterior[i][j]:
                        nueva_matriz[i][j] = nuevo_valor
                        matriz_cambios[i][j] = k + 1

            self.todas_iteraciones.append(nueva_matriz)
            self.cambios_iteraciones[k+1] = matriz_cambios

        self.mostrar_interfaz_algoritmo()

    # Mostrar la interfaz del algoritmo
    def mostrar_interfaz_algoritmo(self):
        self.limpiar_marco_inicial()

        # Crear el marco para mostrar los resultados del algoritmo
        self.marco_algoritmo = tk.Frame(self.root, bg="#f0f0f0")
        self.marco_algoritmo.pack(padx=20, pady=20)

        tk.Label(self.marco_algoritmo, text="Algoritmo de Floyd-Warshall", font=('Segoe UI', 14, 'bold'), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)

        # Marcos para las matrices de distancias y cambios
        self.marco_matriz_distancias = tk.LabelFrame(self.marco_algoritmo, text="Matriz de distancias", font=('Segoe UI', 10), bg="#f0f0f0")
        self.marco_matriz_distancias.grid(row=1, column=0, padx=10, pady=10)

        self.marco_matriz_cambios = tk.LabelFrame(self.marco_algoritmo, text="Matriz de cambios", font=('Segoe UI', 10), bg="#f0f0f0")
        self.marco_matriz_cambios.grid(row=1, column=1, padx=10, pady=10)

        # Controles de navegación
        marco_controles = tk.Frame(self.marco_algoritmo, bg="#f0f0f0")
        marco_controles.grid(row=2, column=0, columnspan=2, pady=10)

        self.iteracion_actual = 0
        self.etiqueta_iteracion = tk.Label(marco_controles, text="", font=('Segoe UI', 10), bg="#f0f0f0")
        self.etiqueta_iteracion.pack(pady=5)

        marco_navegacion = tk.Frame(marco_controles, bg="#f0f0f0")
        marco_navegacion.pack()

        self.boton_estilizado(marco_navegacion, "← Anterior", self.iteracion_anterior).pack(side=tk.LEFT, padx=5)
        self.boton_estilizado(marco_navegacion, "Siguiente →", self.siguiente_iteracion).pack(side=tk.LEFT, padx=5)
        self.boton_estilizado(marco_navegacion, "Ir a final", self.ir_a_final).pack(side=tk.LEFT, padx=5)
        self.boton_estilizado(marco_navegacion, "Volver", self.configurar_interfaz_inicial).pack(side=tk.LEFT, padx=5)

        self.actualizar_visualizacion_matrices()

    # Actualizar la visualización de las matrices
    def actualizar_visualizacion_matrices(self):
        for widget in self.marco_matriz_distancias.winfo_children():
            widget.destroy()
        for widget in self.marco_matriz_cambios.winfo_children():
            widget.destroy()

        matriz_actual = self.todas_iteraciones[self.iteracion_actual]
        matriz_cambios = self.cambios_iteraciones[self.iteracion_actual]
        tamano = len(matriz_actual)

        for i in range(tamano):
            for j in range(tamano):
                val = matriz_actual[i][j]
                texto = "∞" if math.isinf(val) else str(int(val))
                etiqueta = tk.Label(self.marco_matriz_distancias, text=texto, width=5, relief="solid", font=('Segoe UI', 10), bg="white")
                etiqueta.grid(row=i, column=j, padx=2, pady=2)

                cambio = matriz_cambios[i][j]
                etiqueta = tk.Label(self.marco_matriz_cambios, text=str(cambio), width=5, relief="solid", font=('Segoe UI', 10), bg="white")
                etiqueta.grid(row=i, column=j, padx=2, pady=2)

        self.etiqueta_iteracion.config(text=f"Iteración: {self.iteracion_actual}/{len(self.todas_iteraciones) - 1}")

    # Navegar a la iteración anterior
    def iteracion_anterior(self):
        if self.iteracion_actual > 0:
            self.iteracion_actual -= 1
            self.actualizar_visualizacion_matrices()

    # Navegar a la siguiente iteración
    def siguiente_iteracion(self):
        if self.iteracion_actual < len(self.todas_iteraciones) - 1:
            self.iteracion_actual += 1
            self.actualizar_visualizacion_matrices()

    # Ir directamente a la última iteración
    def ir_a_final(self):
        self.iteracion_actual = len(self.todas_iteraciones) - 1
        self.actualizar_visualizacion_matrices()

    # Limpiar el marco inicial
    def limpiar_marco_inicial(self):
        if hasattr(self, 'marco_inicial'):
            self.marco_inicial.destroy()
        if hasattr(self, 'marco_algoritmo'):
            self.marco_algoritmo.destroy()

# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionFloydWarshall(root)
    root.mainloop()