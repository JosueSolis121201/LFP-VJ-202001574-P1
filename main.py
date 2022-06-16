from analizadores_lexicos import lexico

class Programa:
    def __init__(self):
        self.analizador=lexico()
        self.menu()

    def menu(self):
            while True:
                x=input('''
        1.Iniciar Programa
        2.Salir
        Escoja una opcion:''')
                if x =="1":
                    self.analizador.analizador()
                    self.analizador.genrarReporteToken()
                elif x =="2":
                    print("saliendo...")
                    break
                else:
                    print("Escoja un dato valido porfavor:")

                  
a = Programa()