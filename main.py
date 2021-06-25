from simulacion import Simulacion

def main():
    poblacion = 30
    dias_simulacion = 30
    x_min = 0
    x_max = 20
    y_min = 0
    y_max = 20
    sim = Simulacion(poblacion, dias_simulacion, x_min, x_max, y_min, y_max, porcentaje_infectados=.1)

    sim.ejecutar()

    
if __name__ == "__main__":
    main()