from simulacion import Simulacion

def main():
    """Código principal

    Se puede jugar con los parámetros acá.
    """
    # Personas en la simulacion
    poblacion = 30
    # Vacunas disponible en el juego
    vacunas = 5
    # Dias de simulacion
    dias_simulacion = 30
    # Tamaño del "mundo"
    x_min = 0
    x_max = 20
    y_min = 0
    y_max = 20
    # Porcentaje inicial de infectados
    porcentaje_infectados = 0.1
    sim = Simulacion(poblacion, vacunas, dias_simulacion, x_min, x_max, y_min, y_max, porc_infectados=porcentaje_infectados)
    # Ejecutar la simulacion
    sim.ejecutar()
    
if __name__ == "__main__":
    main()