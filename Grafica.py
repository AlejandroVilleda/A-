import queue
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp

class Grafica:
    # Nodos recorridos y por graficar
    Nodos = []
    Nodos_Ramificados = []
    Padre = None
    i = 0

    def __init__(self): self.tree = nx.DiGraph()

    # Agregar nodos a una lista para agregarlos al arbol después
    def Agregar_nodo(self, Coordenadas):

        # Asignando valores al padre del nodo
        if self.tree.size() == 0: self.Padre = None         # Caso inicial: t(0)
        elif self.Padre == None: self.Padre = self.Nodos[0] # Caso Inicial + 1:  t(1)

        Grafica.Nodos.append(Coordenadas)


    # Agregamos hijos de un nodo hoja a una lista para agregarlos al arbol después
    def Agregar_ramificacion(self, Coordenadas):
        self.Padre = self.Nodos[-1] # el padre será el nodo hoja
        Grafica.Nodos_Ramificados.append(Coordenadas)


    # Almacenar nodos al arbol
    def Generar_Nodos(self):
        It = Grafica.i  # Iterador

        # Agregamos los nodos dentro del arbol
        for x in range(Grafica.i, len(self.Nodos)): self.tree.add_node(self.Nodos[x])

        # Unimos los elementos siempre que existan más de un nodo almacenado
        #Requerimos mínimo 2 elementos para comenzar a unificarlos
        if len(self.Nodos) > 1 and Grafica.i >= 1:
            # Unimos nodos como: [Padre] -- [n] -- [n + 1] -- [n + 2]
            for x in range(Grafica.i, len(self.Nodos)): self.tree.add_edge(self.Nodos[x - 1], self.Nodos[x])

        # Unimos los nuevos elementos al padre proveniente de una ramificación, generando otra ramificación
        if (len(self.Nodos) == 1 and It > 1) or (len(self.Nodos) == 1 and self.tree.size() > 1) and (len(self.Nodos_Ramificados) == 0): # CHECAR PQ NO ESTA BIEN________________________________
            for x in range(Grafica.i, len(self.Nodos)):
                if self.Padre != self.Nodos[x]: self.tree.add_edge(self.Padre, self.Nodos[x])

        # Agregando los hijos de un nodo siemrpe que existan
        if len(Grafica.Nodos_Ramificados) != 0:
            for k in range(len(self.Nodos_Ramificados)): self.tree.add_node(self.Nodos_Ramificados[k])

            # Uniendo los nodos ramificados con su respectivo padre
            for k in range(len(self.Nodos_Ramificados)): self.tree.add_edge(self.Padre, self.Nodos_Ramificados[k])

            else: # al finalizar limpiamos los datos y reseteamos el iterador
                Grafica.Nodos.clear()
                Grafica.i = -1

        Grafica.Nodos_Ramificados.clear()
        Grafica.i += 1  # Avanzamos una posición al siguiente nodo
        pass

    # Actualiza el valor del padre en caso de saltos en el arbol
    def Agregar_Padre(self, Posicion):
        self.Padre = Posicion

    # Devuelve el valor del padre
    @property
    def Valor_padre(self): return self.Padre

    # Forzamos un reseteo de datos en caso de saltos en el arbol
    def Resetear(self):
        self.Nodos.clear()
        Grafica.i = 0

    # Generamos la gráfica del arbol en una ventana
    def Graficar(self):
        tree = self.tree
        pos = nx.kamada_kawai_layout(tree, scale=1) # Orientanción

        # Dibujar el árbol
        plt.figure(figsize=(4, 8))  # Tamaño de la figura
        nx.draw(tree, pos, with_labels=True, node_size=400, node_color='lightblue', font_size=8, arrows=False)
        plt.margins(0.2, 0.1)  # Centrar el árbol en la figura
        plt.axis('off')  # Ocultar ejes

        plt.show()