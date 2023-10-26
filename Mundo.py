import pygame
import sys
import heapq
import time
from Grafica import Grafica


TAMANO_CUADRO = 30
TAMANO_MUNEQUITO = 17

GRIS = (71, 75, 78)
CAFE = (161, 130, 98)
AZUL  = (59, 131, 189)
AMARILLO = (229, 190, 1)
VERDE = (0, 149, 57)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0 ,0)
HUMANO = (253, 221, 202)       
PULPO = (87, 35, 100)    
MONO = (108, 59, 42)    

ANCHO = 450
ALTO = 450

#Posicion inicial del jugador
pos_x = 2
pos_y = 7
#Posicion final del jugador
pos_final_x = 8
pos_final_y = 3
#Inicializando el arbol de coordenadas
coord_tree={}

class Node:
    def __init__(self, x, y, g, h, parent):
        self.x = x
        self.y = y
        self.g = g # Costo acumulado desde el punto inicial hasta el punto final
        self.h = h # Heuristica
        self.parent = parent

    def f_score(self):
        return self.g + self.h
    def __lt__(self, other):
        # Comparar dos nodos en función de sus puntajes de costo estimado
        return self.f_score() < other.f_score()
    
# Funcion para calcular la ruta optima usando A*
def astar(matriz, inicio, final, personaje):
    open_list = []
    closed_set = set()

    start_node = Node(inicio[0], inicio[1], 0, manhattan_distance(inicio,final), None)
    heapq.heappush(open_list,(start_node.f_score(),start_node))
    while open_list:
            _ , current_node = heapq.heappop(open_list)

            if(current_node.x, current_node.y) == final:
                path = []
                while current_node:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                for coord, node in coord_tree.items():
                    #print(f'Coordenadas: ({coord[0]}, {coord[1]}) - Costo: {node.g}')
                    #time.sleep(2)
                    pass

                return list(reversed(path)) #Retornar el camino en reversa
            closed_set.add((current_node.x, current_node.y))
            grafica.Agregar_nodo(str([current_node.x, current_node.y]))

            for neighbour in get_neighbours(matriz, current_node):
                if (neighbour.x, neighbour.y) not in coord_tree:
                    coord_tree[(neighbour.x, neighbour.y)] = neighbour
                if (neighbour.x, neighbour.y) in closed_set:
                    continue

                
                tentative_g = current_node.g + cost(current_node, neighbour, personaje)
                if tentative_g < neighbour.g or (neighbour.f_score(), neighbour) not in open_list:
                    neighbour.g = tentative_g

                    grafica.Agregar_Padre(str([current_node.x, current_node.y]))
                    neighbour.parent = current_node
                    grafica.Agregar_ramificacion(str([neighbour.x, neighbour.y]))
                    if (neighbour.f_score(), neighbour) not in open_list:
                        heapq.heappush(open_list,(neighbour.f_score(),neighbour))

            else: grafica.Generar_Nodos()
    return None


def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def get_neighbours(matriz, node):
    neighbours = []
    x,y = node.x, node.y
    if x > 0 and matriz[y][x-1] != 0:
         neighbours.append(Node(x-1,y,0,manhattan_distance((x-1,y),(pos_final_x,pos_final_y)),None))
    if x < len(matriz[0])-1 and matriz[y][x+1] != 0:
        neighbours.append(Node(x+1,y,0,manhattan_distance((x+1,y),(pos_final_x,pos_final_y)),None))
    if y > 0 and matriz[y-1][x] != 0:
        neighbours.append(Node(x,y-1,0,manhattan_distance((x,y-1),(pos_final_x,pos_final_y)),None))
    if y < len(matriz)-1 and matriz[y+1][x] != 0:
        neighbours.append(Node(x,y+1,0,manhattan_distance((x,y+1),(pos_final_x,pos_final_y)),None))
    return neighbours

#Funcion de costo para agregar a la heuristica del astar
def cost(node1, node2, personaje):
    # 0 = Montaña
    # 1 = Tierra
    # 2 = Agua
    # 3 = Arena
    # 4 = Bosque
    if personaje == 'Humano':
        return 10 if matriz[node2.y][node2.x] == 0 else \
                1 if matriz[node2.y][node2.x] == 1 else \
                4 if matriz[node2.y][node2.x] == 2 else \
                3 if matriz[node2.y][node2.x] == 3 else \
                2 if matriz[node2.y][node2.x] == 4 else 0
    elif personaje == 'Pulpo':
        return 25 if matriz[node2.y][node2.x] == 0 else \
                2 if matriz[node2.y][node2.x] == 1 else \
                1 if matriz[node2.y][node2.x] == 2 else \
                25 if matriz[node2.y][node2.x] == 3 else \
                9 if matriz[node2.y][node2.x] == 4 else 0
    elif personaje == 'Mono':
        return 10 if matriz[node2.y][node2.x] == 0 else \
                2 if matriz[node2.y][node2.x] == 1 else \
                4 if matriz[node2.y][node2.x] == 2 else \
                3 if matriz[node2.y][node2.x] == 3 else \
                1 if matriz[node2.y][node2.x] == 4 else 0
    else: None


with open('./Mapa.txt', 'r') as f:
    lineas = f.readlines()
matriz = []
for linea in lineas:
    fila = [int(valor) for valor in linea.strip().split(',')]
    matriz.append(fila)


# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mapa")
paisaje = pygame.image.load("./paisaje.png")  # Cargar imágenes de los personajes y paisaje

def mostrar_menu(cerrar_menu):
    ventana.fill(BLANCO)
    ventana.blit(paisaje, (0, 0)) # Cargar imagen para el fondo
    if not cerrar_menu:
        pass
    else:
        pygame.display.update()

# Bucle principal del programa

grafica = Grafica()

ejecutando = True
while ejecutando:
    mostrar_menu(cerrar_menu=True)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.KEYDOWN:
#############################################################################################################################################################
            if evento.key == pygame.K_1: # Código para el Personaje HUMANO
                personaje = 'Humano'
                fuente_v = pygame.font.Font(None, 24)
                muneco_img = pygame.Surface((TAMANO_MUNEQUITO, TAMANO_MUNEQUITO))
                muneco_img.fill(BLANCO)
                muneco_img.set_colorkey(BLANCO)
                pygame.draw.circle(muneco_img, HUMANO, (TAMANO_MUNEQUITO // 2, TAMANO_MUNEQUITO // 2), TAMANO_MUNEQUITO // 2)
                muneco_img = muneco_img.convert_alpha()
                letra_v = fuente_v.render('V', True, ROJO)
                fuente_v = pygame.font.Font(None, 20)
                fuente = pygame.font.Font(None, 20)
                areas_visitadas = [[False for _ in fila] for fila in matriz]
                # Crear e inicializar una matriz para rastrear las áreas descubiertas
                areas_descubiertas = [[False for _ in fila] for fila in matriz]
                def dibujar_muneco():
                    ventana.blit(muneco_img, (pos_x * TAMANO_CUADRO, pos_y * TAMANO_CUADRO))
                def sensor_mirar():
                    areas_visitadas[pos_y][pos_x] = True
                    # Actualizar las áreas descubiertas
                    areas_descubiertas[pos_y][pos_x] = True
                    if pos_y + 1 < len(matriz):
                        areas_descubiertas[pos_y + 1][pos_x] = True
                    if pos_y - 1 >= 0:
                        areas_descubiertas[pos_y - 1][pos_x] = True
                    if pos_x + 1 < len(matriz[0]):
                        areas_descubiertas[pos_y][pos_x + 1] = True
                    if pos_x - 1 >= 0:
                        areas_descubiertas[pos_y][pos_x - 1] = True

                costo = 0                 
                ganado = False
                
                ruta_optima_humano = astar(matriz, (pos_x,pos_y), (pos_final_x,pos_final_y),personaje)
                print(ruta_optima_humano)
                if ruta_optima_humano is not None:
                    for x, y in ruta_optima_humano:
                        pos_x, pos_y = x, y
                        costo += 10 if matriz[y][x] == 0 else \
                                1 if matriz[y][x] == 1 else \
                                4 if matriz[y][x] == 2 else \
                                3 if matriz[y][x] == 3 else \
                                2 if matriz[y][x] == 4 else 0
                        for fila in range(len(matriz)):             
                            for columna in range(len(matriz[0])):
                                if matriz[fila][columna] == 0:
                                    color = GRIS
                                elif matriz[fila][columna] == 1:
                                    color = CAFE
                                elif matriz[fila][columna] == 2:
                                    color = AZUL
                                elif matriz[fila][columna] == 3:
                                    color = AMARILLO
                                elif matriz[fila][columna] == 4:
                                    color = VERDE
                                pygame.draw.rect(ventana, color, (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                                if not areas_descubiertas[fila][columna]:
                                    color = NEGRO
                                pygame.draw.rect(ventana, color, (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                                if areas_visitadas[fila][columna]:
                                    letra_v_rect = letra_v.get_rect()
                                    letra_v_rect.topleft = (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO)
                                    ventana.blit(letra_v, letra_v_rect)
                        dibujar_muneco()
                            
                        sensor_mirar()
                        pygame.display.update()
                        pygame.time.delay(100)

                        coordenadas = f'Coordenadas: ({pos_x}, {pos_y})'
                        texto = fuente.render(coordenadas, True, GRIS)
                        ventana.blit(texto, (10, 10))

                        cansancio = f'Cansancio: ({costo})'
                        texto = fuente.render(cansancio, True, GRIS)
                        ventana.blit(texto, (200, 10))


                        inicio = f'I'
                        texto = fuente.render(inicio, True, ROJO)
                        ventana.blit(texto, (0+5, 0+5))

                    if pos_x == pos_final_x and pos_y == pos_final_y:
                        fin = f'F'
                        texto = fuente.render(fin, True, ROJO)
                        ventana.blit(texto, (pos_x*30 + 5, pos_y*30 + 5))
                    pygame.display.update()
    
                    if pos_x == pos_final_x and pos_y == pos_final_y:
                        ganado = True
                    
                    if ganado:
                        mensaje = '¡Haz ganado!'
                        fuente_ganado = pygame.font.Font(None, 36)
                        mensaje_renderizado = fuente_ganado.render(mensaje, True, BLANCO)
                        ventana.blit(mensaje_renderizado, (ANCHO // 2 - mensaje_renderizado.get_width() // 2, ALTO // 2 - mensaje_renderizado.get_height() // 2))
                        pygame.display.update()
                        grafica.Graficar()
                        pygame.time.delay(3000)
                        pygame.quit()
                        sys.exit()
#############################################################################################################################################################
            #Codigo para el personaje PULPO
            if evento.key == pygame.K_2: # Código para el Personaje PULPO
                personaje = 'Pulpo'
                fuente_v = pygame.font.Font(None, 24)
                muneco_img = pygame.Surface((TAMANO_MUNEQUITO, TAMANO_MUNEQUITO))
                muneco_img.fill(BLANCO)
                muneco_img.set_colorkey(BLANCO)
                pygame.draw.circle(muneco_img, PULPO, (TAMANO_MUNEQUITO // 2, TAMANO_MUNEQUITO // 2), TAMANO_MUNEQUITO // 2)
                muneco_img = muneco_img.convert_alpha()
                letra_v = fuente_v.render('V', True, ROJO)
                fuente_v = pygame.font.Font(None, 20)
                fuente = pygame.font.Font(None, 20)
                areas_visitadas = [[False for _ in fila] for fila in matriz]
                # Crear e inicializar una matriz para rastrear las áreas descubiertas
                areas_descubiertas = [[False for _ in fila] for fila in matriz]

                def dibujar_muneco():
                    ventana.blit(muneco_img, (pos_x * TAMANO_CUADRO, pos_y * TAMANO_CUADRO))

                def sensor_mirar():
                    areas_visitadas[pos_y][pos_x] = True
                    # Actualizar las áreas descubiertas
                    areas_descubiertas[pos_y][pos_x] = True
                    if pos_y + 1 < len(matriz):
                        areas_descubiertas[pos_y + 1][pos_x] = True
                    if pos_y - 1 >= 0:
                        areas_descubiertas[pos_y - 1][pos_x] = True
                    if pos_x + 1 < len(matriz[0]):
                        areas_descubiertas[pos_y][pos_x + 1] = True
                    if pos_x - 1 >= 0:
                        areas_descubiertas[pos_y][pos_x - 1] = True

                costo = 0                 
                ganado = False
                ruta_optima_pulpo = astar(matriz, (pos_x,pos_y), (pos_final_x,pos_final_y), personaje)
                if ruta_optima_pulpo is not None:
                    for x, y in ruta_optima_pulpo:
                        pos_x, pos_y = x, y
                        costo += 10 if matriz[y][x] == 0 else \
                                1 if matriz[y][x] == 1 else \
                                4 if matriz[y][x] == 2 else \
                                3 if matriz[y][x] == 3 else \
                                2 if matriz[y][x] == 4 else 0
                        for fila in range(len(matriz)):             
                            for columna in range(len(matriz[0])):
                                if matriz[fila][columna] == 0:
                                    color = GRIS
                                elif matriz[fila][columna] == 1:
                                    color = CAFE
                                elif matriz[fila][columna] == 2:
                                    color = AZUL
                                elif matriz[fila][columna] == 3:
                                    color = AMARILLO
                                elif matriz[fila][columna] == 4:
                                    color = VERDE
                                pygame.draw.rect(ventana, color, (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                                if not areas_descubiertas[fila][columna]:
                                    color = NEGRO
                                pygame.draw.rect(ventana, color, (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                                if areas_visitadas[fila][columna]:
                                    letra_v_rect = letra_v.get_rect()
                                    letra_v_rect.topleft = (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO)
                                    ventana.blit(letra_v, letra_v_rect)
                        dibujar_muneco()
                            
                        sensor_mirar()
                        pygame.display.update()
                        pygame.time.delay(100)








                        coordenadas = f'Coordenadas: ({pos_x}, {pos_y})'
                        texto = fuente.render(coordenadas, True, GRIS)
                        ventana.blit(texto, (10, 10))

                        cansancio = f'Cansancio: ({costo})'
                        texto = fuente.render(cansancio, True, GRIS)
                        ventana.blit(texto, (200, 10))


                        inicio = f'I'
                        texto = fuente.render(inicio, True, ROJO)
                        ventana.blit(texto, (0+5, 0+5))

                    if pos_x == pos_final_x and pos_y == pos_final_y:
                        fin = f'F'
                        texto = fuente.render(fin, True, ROJO)
                        ventana.blit(texto, (pos_x*30 + 5, pos_y*30 + 5))
                    pygame.display.update()






                    if pos_x == pos_final_x and pos_y == pos_final_y:
                        ganado = True
                    
                    if ganado:
                        mensaje = '¡Haz ganado!'
                        fuente_ganado = pygame.font.Font(None, 36)
                        mensaje_renderizado = fuente_ganado.render(mensaje, True, BLANCO)
                        ventana.blit(mensaje_renderizado, (ANCHO // 2 - mensaje_renderizado.get_width() // 2, ALTO // 2 - mensaje_renderizado.get_height() // 2))
                        pygame.display.update()
                        grafica.Graficar()
                        pygame.time.delay(3000)  # Espera 5 segundos
                        pygame.quit()
                        sys.exit()
#############################################################################################################################################################
            #Codigo para el personaje MONO
            if evento.key == pygame.K_3: # Código para el Personaje HUMANO
                personaje = 'Mono'
                fuente_v = pygame.font.Font(None, 24)
                muneco_img = pygame.Surface((TAMANO_MUNEQUITO, TAMANO_MUNEQUITO))
                muneco_img.fill(BLANCO)
                muneco_img.set_colorkey(BLANCO)
                pygame.draw.circle(muneco_img, MONO, (TAMANO_MUNEQUITO // 2, TAMANO_MUNEQUITO // 2), TAMANO_MUNEQUITO // 2)
                muneco_img = muneco_img.convert_alpha()
                letra_v = fuente_v.render('V', True, ROJO)
                fuente_v = pygame.font.Font(None, 20)
                fuente = pygame.font.Font(None, 20)
                areas_visitadas = [[False for _ in fila] for fila in matriz]
                # Crear e inicializar una matriz para rastrear las áreas descubiertas
                areas_descubiertas = [[False for _ in fila] for fila in matriz]
                def dibujar_muneco():
                    ventana.blit(muneco_img, (pos_x * TAMANO_CUADRO, pos_y * TAMANO_CUADRO))
                def sensor_mirar():
                    areas_visitadas[pos_y][pos_x] = True
                    # Actualizar las áreas descubiertas
                    areas_descubiertas[pos_y][pos_x] = True
                    if pos_y + 1 < len(matriz):
                        areas_descubiertas[pos_y + 1][pos_x] = True
                    if pos_y - 1 >= 0:
                        areas_descubiertas[pos_y - 1][pos_x] = True
                    if pos_x + 1 < len(matriz[0]):
                        areas_descubiertas[pos_y][pos_x + 1] = True
                    if pos_x - 1 >= 0:
                        areas_descubiertas[pos_y][pos_x - 1] = True

                costo = 0                 
                ganado = False;
                ruta_optima_humano = astar(matriz, (pos_x,pos_y), (pos_final_x,pos_final_y), personaje)
                if ruta_optima_humano is not None:
                    for x, y in ruta_optima_humano:
                        pos_x, pos_y = x, y
                        costo += 10 if matriz[y][x] == 0 else \
                                1 if matriz[y][x] == 1 else \
                                4 if matriz[y][x] == 2 else \
                                3 if matriz[y][x] == 3 else \
                                2 if matriz[y][x] == 4 else 0
                        for fila in range(len(matriz)):             
                            for columna in range(len(matriz[0])):
                                if matriz[fila][columna] == 0:
                                    color = GRIS
                                elif matriz[fila][columna] == 1:
                                    color = CAFE
                                elif matriz[fila][columna] == 2:
                                    color = AZUL
                                elif matriz[fila][columna] == 3:
                                    color = AMARILLO
                                elif matriz[fila][columna] == 4:
                                    color = VERDE
                                pygame.draw.rect(ventana, color, (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                                if not areas_descubiertas[fila][columna]:
                                    color = NEGRO
                                pygame.draw.rect(ventana, color, (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                                if areas_visitadas[fila][columna]:
                                    letra_v_rect = letra_v.get_rect()
                                    letra_v_rect.topleft = (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO)
                                    ventana.blit(letra_v, letra_v_rect)
                        dibujar_muneco()
                            
                        sensor_mirar()
                        pygame.display.update()
                        pygame.time.delay(100)

                        coordenadas = f'Coordenadas: ({pos_x}, {pos_y})'
                        texto = fuente.render(coordenadas, True, GRIS)
                        ventana.blit(texto, (10, 10))

                        cansancio = f'Cansancio: ({costo})'
                        texto = fuente.render(cansancio, True, GRIS)
                        ventana.blit(texto, (200, 10))


                        inicio = f'I'
                        texto = fuente.render(inicio, True, ROJO)
                        ventana.blit(texto, (0+5, 0+5))

                    if pos_x == pos_final_x and pos_y == pos_final_y:
                        fin = f'F'
                        texto = fuente.render(fin, True, ROJO)
                        ventana.blit(texto, (pos_x*30 + 5, pos_y*30 + 5))
                    pygame.display.update()
    
                    if pos_x == pos_final_x and pos_y == pos_final_y:
                        ganado = True
                    
                    if ganado:
                        mensaje = '¡Haz ganado!'
                        fuente_ganado = pygame.font.Font(None, 36)
                        mensaje_renderizado = fuente_ganado.render(mensaje, True, BLANCO)
                        ventana.blit(mensaje_renderizado, (ANCHO // 2 - mensaje_renderizado.get_width() // 2, ALTO // 2 - mensaje_renderizado.get_height() // 2))
                        pygame.display.update()
                        grafica.Graficar()
                        pygame.time.delay(3000)  # Espera 5 segundos
                        pygame.quit()
                        sys.exit()
#############################################################################################################################################################
                
pygame.quit()
