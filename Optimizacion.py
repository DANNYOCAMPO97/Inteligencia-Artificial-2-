import random
import matplotlib.pyplot as plt

def generar_individuo(lista_numeros):
    return [random.choice(lista_numeros) for _ in range(len(lista_numeros))]

def generar_poblacion(lista_numeros, tam_poblacion):
    return [generar_individuo(lista_numeros) for _ in range(tam_poblacion)]

def evaluar_aptitud(individuo, objetivo):
    return objetivo - max(individuo)

def seleccionar_padres(poblacion, objetivo):
    return sorted(poblacion, key=lambda x: evaluar_aptitud(x, objetivo), reverse=True)[:2]

def cruzar(padre1, padre2):
    punto_corte = random.randint(0, len(padre1)-1)
    hijo = padre1[:punto_corte] + padre2[punto_corte:]
    return hijo

def mutar(individuo, lista_numeros):
    gen_mutado = random.choice(lista_numeros)
    idx_mutacion = random.randint(0, len(individuo) - 1)
    individuo[idx_mutacion] = gen_mutado
    return individuo

def algoritmo_genetico(lista_numeros, tam_poblacion, num_generaciones):
    objetivo = max(lista_numeros)
    poblacion = generar_poblacion(lista_numeros, tam_poblacion)
    mejores_aptitudes = []

    for _ in range(num_generaciones):
        nueva_poblacion = []

        for _ in range(tam_poblacion // 2):
            padre1, padre2 = seleccionar_padres(poblacion, objetivo)
            hijo = cruzar(padre1, padre2)
            if random.random() < 0.1:  # Probabilidad de mutación del 10%
                hijo = mutar(hijo, lista_numeros)
            nueva_poblacion.extend([padre1, padre2, hijo])

        poblacion = nueva_poblacion
        mejor_solucion = max(poblacion, key=lambda x: max(x))
        mejores_aptitudes.append(max(mejor_solucion))

    return mejores_aptitudes

# Prueba del algoritmo
lista_numeros = [12, 45, 67, 23, 89, 34, 56, 78, 98, 1]
tam_poblacion = 10
num_generaciones = 5

aptitudes = algoritmo_genetico(lista_numeros, tam_poblacion, num_generaciones)

# Visualización del proceso de optimización en una ventana gráfica
plt.plot(range(1, num_generaciones + 1), aptitudes, marker='o')
plt.xlabel('Generación')
plt.ylabel('Aptitud del mejor individuo')
plt.title('Optimización mediante Algoritmos Genéticos')
plt.grid(True)
plt.show()
