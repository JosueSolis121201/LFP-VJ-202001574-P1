class clase_token:
    def __init__(self,valor,columna,fila,tipo,tieneErrorLexico=False):
        self.valor = valor
        self.fila = fila
        self.tipo = tipo
        self.columna = columna
        self.tieneErrorLexico = tieneErrorLexico
        print(self,valor,columna,fila,tipo,tieneErrorLexico)
    def html(self):
        return "<tr>" + "<td>"+ str(self.valor)+"</td>" + "<td>"+ str(self.tipo)+"</td>" + "<td>"+ str(self.columna)+"</td>"+"</tr>"
    def string(self):
        return self.valor + "---" + str(self.tipo) + "---" + str(self.columna)
class lexico():
    def __init__(self) -> None:
        self.texto=""
        self.lista_tokens=[]
        
        self.linea = 1
        self.columna = 1
    def genrarReporteToken(self):
        inicio="<html><head></head><body>"
        cuerpo = "<table><tr><th>TOKEN</th><th>TIPO</th><th>COLUMNA</th></tr><tbody>"
        concatenar = ""
        for element in self.lista_tokens:
            concatenar = concatenar + element.html()
        final = inicio + cuerpo  +concatenar+ "</tbody></table></html></body>"
        f = open ('report_202001574.html','w')
        f.write(final)
        f.close()
    def analizar(self):
        self.analizador()#!msg
    def analizador(self):
        #Directorios
        

        #!Mesanje de SC
        msg=" intasdads _s double boolean char false 5555555555 32 \"wenas noches\" 7.777  '5'  'a156a' if \"if\" else \'else\' "

        tieneErrorLexico=False
        self.texto = msg
        while self.texto != "":
            letra = self.leer_letra()
            if letra.isalpha(): #!Automata Palabra reservada
                lectura = self.tipo_dato_S0()
                self.tipo_dato_busqueda(lectura)
            elif letra == "_" or letra.isalpha(): #!Automata Identificador
                lectura = self.identificador_S0()
                self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"identificador",tieneErrorLexico))
            elif letra.isnumeric(): #!Automata numeros (int/double)
                lectura = self.numero_s0()
                print(lectura)
                print("///////////////////////////////////////////////////////")
                if '.' in lectura:
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_double",tieneErrorLexico))
                else:
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_int",tieneErrorLexico))
            elif letra == '\"' or letra == "“" or letra == "”":#!Automata comillas(String)
                lectura = self.comillas_s0()
                self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_string",tieneErrorLexico))
            elif letra == '\'' or letra == "“" or letra == "”":#!Automata comillas(char)
                lectura = self.comillas_s0()
                if len(lectura) ==3:
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_char",tieneErrorLexico))
                else:
                    tieneErrorLexico=True
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_char",tieneErrorLexico))
                    tieneErrorLexico=False
            elif letra == "+" or letra == "-" or letra == "*" or letra == "+" or letra == "-" or letra == "/" or letra == "%" or letra == "=" or letra == "!" or letra == ">" or letra == "<" or letra == "&" or letra == "|" :                 #!Automata OPERADORES
                #lectura = self.operadores_s0()
                print(lectura)
                
            elif letra == " ": #!Salto espacio
                self.quitar_primera_letra()  
            else:
                print("error de lexico")

    #!Automata OPERADORES
    def operadores_s0 (self):
        letra = self.leer_letra()
        self.quitar_primera_letra()
        return letra + self.operadores_s0()                

    #!Automata Identificador    
    def identificador_S0 (self):
        letra = self.leer_letra()
        self.quitar_primera_letra()
        return letra + self.identificador_S1()
    def identificador_S1 (self):
        letra = self.leer_letra()
        if letra.isalpha() or letra.isnumeric() or letra =="_":
            self.quitar_primera_letra()
            return letra + self.identificador_S1()
        else:
            return ""
    #!Automata Palabra reservada  
    def tipo_dato_S0 (self):
        letra = self.leer_letra()
        self.quitar_primera_letra()
        return letra + self.identificador_S0()
    def tipo_dato_busqueda (self,lexema):
        tieneErrorLexico=False
        #diccionario
        diccionario ={"int":0,"double":1,"string":2,"char":3,"boolean":4,"true":5,"false":6,"if":7,"else":8,"while":9,
        "do":10,"void":11,"return":12}
        tipo_encontrado = diccionario.get(lexema.lower(),None)
        print(tipo_encontrado)
        if(tipo_encontrado == None):
            self.lista_tokens.append(clase_token(lexema,self.columna,self.linea,"identificador",tieneErrorLexico))
        else:
            tipo = tipo_encontrado
            if tipo ==0:
                self.lista_tokens.append(clase_token("int",self.columna,self.linea,"tipo_int",tieneErrorLexico))
            elif tipo ==1:
                self.lista_tokens.append(clase_token("double",self.columna,self.linea,"tipo_double",tieneErrorLexico))
            elif tipo ==2:
                self.lista_tokens.append(clase_token("string",self.columna,self.linea,"tipo_string",tieneErrorLexico))
            elif tipo ==3:
                self.lista_tokens.append(clase_token("char",self.columna,self.linea,"tipo_char",tieneErrorLexico))
            elif tipo ==4:
                self.lista_tokens.append(clase_token("boolean",self.columna,self.linea,"tipo_boolean",tieneErrorLexico))
            elif tipo ==5:
                self.lista_tokens.append(clase_token("true",self.columna,self.linea,"dato_boolean",tieneErrorLexico))
            elif tipo ==6:
                self.lista_tokens.append(clase_token("false",self.columna,self.linea,"dato_boolean",tieneErrorLexico))
            elif tipo ==7:
                self.lista_tokens.append(clase_token("if",self.columna,self.linea,"condicional_if",tieneErrorLexico))
            elif tipo ==8:
                self.lista_tokens.append(clase_token("else",self.columna,self.linea,"condicional_else",tieneErrorLexico))
            elif tipo ==9:
                self.lista_tokens.append(clase_token("while",self.columna,self.linea,"ciclo_while",tieneErrorLexico))
            elif tipo ==10:
                self.lista_tokens.append(clase_token("do",self.columna,self.linea,"ciclo_do",tieneErrorLexico))
            elif tipo ==11:
                self.lista_tokens.append(clase_token("void",self.columna,self.linea,"metodo_void",tieneErrorLexico))
            elif tipo ==12:
                self.lista_tokens.append(clase_token("return",self.columna,self.linea,"metodo_return",tieneErrorLexico))
    #!Automata numero (int/double)
    def numero_s0(self):
        letra = self.leer_letra()
        if letra.isnumeric():
            self.quitar_primera_letra()
            return letra + self.numero_s1()
    def numero_s1(self):
        letra = self.leer_letra()
        if letra.isnumeric():
            self.quitar_primera_letra()
            return letra + self.numero_s1()
        if letra==".":
            self.quitar_primera_letra()
            return letra + self.numero_s1()
        else:
            return ""
    #!Automata comillas(String)
    def comillas_s0(self):
        letra = self.leer_letra()
        if letra == '\"' or letra == "“" or letra == "”" or letra == "'":
            self.quitar_primera_letra()
            return letra +  self.comillas_s1()
    def comillas_s1(self):
        letra = self.leer_letra()
        if letra != '\"'and letra != "“" and letra != "”" and letra != "'":
            self.quitar_primera_letra()
            return letra + self.comillas_s1()
        else:
            self.quitar_primera_letra()
            return letra
   #!Automata comilla(char)
    def comilla_s0(self):
        letra = self.leer_letra()
        if letra == '\'' :
            self.quitar_primera_letra()
            return letra +  self.comilla_s1()
    def comilla_s1(self):
        letra = self.leer_letra()
        if letra != '\'':
            self.quitar_primera_letra()
            return letra + self.comilla_s1()
        else:
            self.quitar_primera_letra()
            return letra 
    
    #!Herramientas
    def leer_letra(self):
        if(self.texto != ""):
            return self.texto[0]
        else:
            return ""
    def quitar_primera_letra(self):
        if(self.texto != ""):
            self.texto=self.texto[1:]

    
    

    
a=lexico()
a.analizar()
a.genrarReporteToken








        