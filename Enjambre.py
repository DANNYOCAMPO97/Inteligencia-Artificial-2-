import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo
NUM_ENTIDADES = 50
TAMANO_MUNDO = 100
VEL_MAX = 0.5
DISTANCIA_VISTA = 10
RADIO_SEPARACION = 2
PESO_SEPARACION = 1.5
PESO_ALINEACION = 1.0
PESO_COHESION = 1.0
PESO_LIDERAZGO = 2.0

class Entidad:
    def __init__(self, posicion, velocidad):
        self.posicion = posicion
        self.velocidad = velocidad

def distancia(entidad1, entidad2):
    return np.linalg.norm(entidad1.posicion - entidad2.posicion)

def obtener_vecindario(entidades, entidad, distancia_vista):
    vecindario = []
    for e in entidades:
        if e != entidad and distancia(entidad, e) < distancia_vista:
            vecindario.append(e)
    return vecindario

def aplicar_reglas(entidades, entidad, vecindario):
    separacion = np.zeros(2)
    alineacion = entidad.velocidad
    cohesion = entidad.posicion
    liderazgo = np.zeros(2)

    vecinos_cercanos = 0

    for vecino in vecindario:
        d = distancia(entidad, vecino)
        if d < RADIO_SEPARACION:
            separacion -= (vecino.posicion - entidad.posicion) / d
        if d < DISTANCIA_VISTA:
            alineacion += vecino.velocidad
            cohesion += vecino.posicion
            vecinos_cercanos += 1

    if vecinos_cercanos > 0:
        alineacion /= vecinos_cercanos
        cohesion /= vecinos_cercanos

    if vecinos_cercanos == 0:
        liderazgo = np.array([TAMANO_MUNDO / 2, TAMANO_MUNDO / 2]) - entidad.posicion
    else:
        liderazgo = np.array([TAMANO_MUNDO / 2, TAMANO_MUNDO / 2]) - cohesion

    return (
        PESO_SEPARACION * separacion,
        PESO_ALINEACION * alineacion,
        PESO_COHESION * (cohesion - entidad.posicion),
        PESO_LIDERAZGO * liderazgo
    )

def limitar_velocidad(velocidad, velocidad_maxima):
    if np.linalg.norm(velocidad) > velocidad_maxima:
        return velocidad / np.linalg.norm(velocidad) * velocidad_maxima
    return velocidad

def simular():
    entidades = []
    for _ in range(NUM_ENTIDADES):
        posicion = np.random.rand(2) * TAMANO_MUNDO
        velocidad = np.random.rand(2) * VEL_MAX
        entidad = Entidad(posicion, velocidad)
        entidades.append(entidad)

    plt.figure()

    for _ in range(200):
        plt.clf()

        for entidad in entidades:
            vecindario = obtener_vecindario(entidades, entidad, DISTANCIA_VISTA)
            separacion, alineacion, cohesion, liderazgo = aplicar_reglas(entidades, entidad, vecindario)

            entidad.velocidad += separacion + alineacion + cohesion + liderazgo
            entidad.velocidad = limitar_velocidad(entidad.velocidad, VEL_MAX)
            entidad.posicion += entidad.velocidad

            # Envolver el mundo
            entidad.posicion = np.mod(entidad.posicion, TAMANO_MUNDO)

            plt.plot(entidad.posicion[0], entidad.posicion[1], 'bo')

        plt.xlim(0, TAMANO_MUNDO)
        plt.ylim(0, TAMANO_MUNDO)
        plt.pause(0.01)

    plt.show()

if __name__ == "__main__":
    simular()
