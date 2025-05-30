import math

def dijkstra(matriz, nodo_inicial):
    n = len(matriz)
    distancias = [math.inf] * n
    predecesores = [-1] * n
    permanentes = [False] * n
    distancias[nodo_inicial] = 0
    predecesores[nodo_inicial] = nodo_inicial
    
    tabla = []
    for i in range(n):
        fila = [f"{i}"]
        if i == nodo_inicial:
            fila.append(f"(0,{nodo_inicial})")
        else:
            if matriz[nodo_inicial][i] != 0 and matriz[nodo_inicial][i] != math.inf:
                fila.append(f"({matriz[nodo_inicial][i]},{nodo_inicial})")
            else:
                fila.append("∞")
        tabla.append(fila)
    
    paso_actual = 1
    
    while True:
        min_dist = math.inf
        u = -1
        for i in range(n):
            if not permanentes[i] and distancias[i] < min_dist:
                min_dist = distancias[i]
                u = i
        
        if u == -1: 
            break
        
        permanentes[u] = True
        paso_actual += 1
        
        for v in range(n):
            if matriz[u][v] != 0 and matriz[u][v] != math.inf and not permanentes[v]:
                nueva_dist = distancias[u] + matriz[u][v]
                if nueva_dist < distancias[v]:
                    distancias[v] = nueva_dist
                    predecesores[v] = u
        
        for i in range(n):
            if permanentes[i]:
                tabla[i].append("*")
            else:
                if distancias[i] != math.inf:
                    tabla[i].append(f"({distancias[i]},{predecesores[i]})")
                else:
                    tabla[i].append("∞")
    
    max_pasos = max(len(fila) for fila in tabla)
    for fila in tabla:
        while len(fila) < max_pasos:
            if "*" in fila:
                fila.append("*")
            else:
                fila.append(fila[-1])
    
    return tabla

# Matriz de adyacencia
matriz = [
    [0, 12, 18, math.inf],
    [math.inf, 0, 9, math.inf],
    [math.inf, math.inf, 0, 10],
    [21, math.inf, math.inf, 0]
]

nodo_inicial = int(input("Ingrese el nodo inicial (0-3): "))
if nodo_inicial < 0 or nodo_inicial > 3:
    print("Nodo inválido. Debe ser entre 0 y 3.")
    exit()

tabla_resultados = dijkstra(matriz, nodo_inicial)

print(f"\nSe eligió el Nodo {nodo_inicial}\n")
encabezados = ["Nodos"] + [f"Paso {i+1}" for i in range(len(tabla_resultados[0])-1)]
print("{:<8}".format(encabezados[0]), end="")
for h in encabezados[1:]:
    print("{:>10}".format(h), end="")
print()

for fila in tabla_resultados:
    for i, celda in enumerate(fila):
        if i == 0:
            print("{:<8}".format(celda), end="")
        else:
            print("{:>10}".format(celda), end="")
    print()