from persona import Persona

def main():
    per = Persona(1, 2, 1, False)
    print(per.pos_x())
    per.modificar_x(2)
    print(per.pos_x())
    print(per.x)

if __name__ == "__main__":
    main()