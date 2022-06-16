



class clase_token:
    def __init__(self,valor,columna,fila,tipo,tieneErrorLexico,patron):
        self.valor = valor
        self.fila = fila
        self.tipo = tipo
        self.columna = columna
        self.tieneErrorLexico = tieneErrorLexico
        self.patron=patron
        print(self,valor,columna,fila,tipo,tieneErrorLexico,patron)



    def html(self):
        return "<tr class=\"active-row\">" + "<td>"+ str(self.valor)+"</td>" + "<td>"+ str(self.tipo)+"</td>" + "<td>"+ str(self.columna)+"</td>"+"<td>"+ str(self.fila)+"</td>" +"<td>"+ str(self.tieneErrorLexico)+"</td>"+"<td>"+ str(self.patron)+"</td>" +"</tr>"
    
class lexico():
    def __init__(self) -> None:
        self.texto=""
        self.lista_tokens=[]
        self.lista_errores = []
        
        self.linea = 1
        self.columna = 1
    def genrarReporteToken(self):
        inicio="<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"estilo.css\"/></head><body>"
        cuerpo = "<table class=\"styled-table\"><tr class=\"active-row\"><th>LEXEMA</th><th>TIPO</th><th>COLUMNA</th><th>LINEA</th><th>ERROR LEXICO</th></th><th>PATRON</th></tr><tbody>"
        cuerpo_e = "<table class=\"styled-table\"><tr class=\"active-row\"><th>LEXEMA</th><th>TIPO</th><th>COLUMNA</th><th>LINEA</th><th>ERROR LEXICO</th></th><th>PATRON</th></tr><tbody>"
        concatenar = ""
        concatenar_e = ""
        #!TOKENS
        for element in self.lista_tokens:
            concatenar = concatenar + element.html()
        #!ERRORES LEXISCOS
        for error in self.lista_errores:
            concatenar_e = concatenar_e + error.html()
        cuerpo_token="<h1>REPORTE DE TOKENS</h1>"+ cuerpo +concatenar+ "</tbody></table>"
        cuerpo_errores="<h1>ERRORES LEXICOS</h1>"+ cuerpo_e +concatenar_e+ "</tbody></table>"
        final = inicio +cuerpo_token+cuerpo_errores +"</html></body>"
        f = open ('report_202001574.html','w')
        f.write(final)
        f.close()
    def analizar(self):
        self.analizador()#!msg
    def analizador(self):
        #Directorios
        

        #!Mesanje de SC
        with open("archivo.sc") as f:
            msg = f.read()
        
    
        print(msg)
        tieneErrorLexico=False
        self.texto = msg 
        while self.texto != "":
            letra = self.leer_letra()
            if letra.isalpha(): #!Automata Palabra reservada
                lectura = self.tipo_dato_S0()
                self.tipo_dato_busqueda(lectura)
            elif letra == '/':#!Automata comentario(de una linea/varias lineas)
                lectura = self.comentario_s0()
                if '*/' in lectura:
                    self.columna=self.columna+1 #! **********
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"comentario_multilinea",tieneErrorLexico,"/*(\w|\n| )*[^*/]*/"))
                elif "divicion"  in lectura:
                    
                    self.columna=self.columna-1 #! *********
                    self.lista_tokens.append(clase_token("/",self.columna,self.linea,"divicion",tieneErrorLexico,"/"))
                else:
                    self.linea=self.linea-1
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"comentario_unilinea",tieneErrorLexico,"//(\w| )*"))
                    self.columna=1
                    self.linea=self.linea+1
            elif letra == "_" or letra.isalpha(): #!Automata Identificador
                lectura = self.identificador_S0()
                

                self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"identificador",tieneErrorLexico,"(_|[a-z])([a-z]|[0-9]|_)*"))
            elif letra.isnumeric(): #!Automata numeros (int/double)
                lectura = self.numero_s0()
                if '.' in lectura:
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_double",tieneErrorLexico,"[0-9]+.[0-9]+"))
                else:
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_int",tieneErrorLexico,"[0-9]+"))
            elif letra == '\"' or letra == "“" or letra == "”":#!Automata comillas(String)
                lectura = self.comillas_s0()
                self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_string",tieneErrorLexico,"\"[^\"]*\""))
            elif letra == '\'':#!Automata comillas(char)
                lectura = self.comillas_s0()
                if len(lectura) ==3:
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_char",tieneErrorLexico,"\'[^\']{1}\'"))
                else:
                    tieneErrorLexico=True
                    self.lista_errores.append(clase_token(lectura,self.columna,self.linea,"Error",tieneErrorLexico,"ERROR"))
                    tieneErrorLexico=False
            elif letra == "+" or letra == "-" or letra == "*"  or letra == "/" or letra == "%"  or letra == "!" or letra == ">" or letra == "<"or letra == "=" or letra == "&" or   letra == "|":                 #!Automata OPERADORES(simples)
                lectura = self.operadores_s0()
                self.operador_simple_busqueda(lectura)
            elif letra == "[":#![
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"corchete_abre",tieneErrorLexico,"["))
            elif letra == "]":#!]
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"corchete_cierra",tieneErrorLexico,"]"))
            elif letra == "(":#!(
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"parentesis_abre",tieneErrorLexico,"("))
            elif letra == ")":#!)
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"parentesis_cierra",tieneErrorLexico,")"))
            elif letra == "{":#!{
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"llave_abre",tieneErrorLexico,"{"))
            elif letra == "}":#!}
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"llave_cierra",tieneErrorLexico,"}"))
            elif letra == ";":#!}
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********true
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"punto_coma",tieneErrorLexico,";"))
            elif letra == ",":#!}
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"coma",tieneErrorLexico,","))
            elif letra == "\n" or letra == "\t" or letra == " ":#!Saltos de linea y cosas saltables  
                if letra== "\n":
                    self.columna=0 #! **********
                    self.linea=self.linea+1
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********         

            else:
                err = self.leer_letra()
                self.quitar_primera_letra()
                tieneErrorLexico=True
                self.columna=self.columna+1 #! **********
                self.lista_errores.append(clase_token(err,self.columna,self.linea,"Error_lexico",tieneErrorLexico,"ERROR"))
                tieneErrorLexico=False
                print({"error":err}) 
    #!Automata comentario(de una linea/varias lineas)
    def comentario_s0(self):
        letra = self.leer_letra()
        if letra == '/':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            return letra +  self.comentario_s1()
    def comentario_s1(self):
        letra = self.leer_letra()
        if letra == '/':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s2()
        elif letra == '*':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s4()
        else:
            
            return "" + self.comentario_s7()
    def comentario_s2(self):
        letra = self.leer_letra()
        if letra != '\n':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s2()
        else:
            return letra + self.comentario_s3()
    def comentario_s3(self):
        letra = self.leer_letra()
        if letra == '\n':
            self.quitar_primera_letra()
            
            self.linea=self.linea+1
            return letra 
        else:
            return ""
    def comentario_s4(self):
        letra = self.leer_letra()
        if letra != '*':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            if letra =="\n":
                self.columna=0
                self.linea=self.linea+1
            return letra + self.comentario_s4()
        if letra == '*':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s5()
        else:
            return ""
    def comentario_s5(self):
        letra = self.leer_letra()
        if letra != '/':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s4()
        if letra == '/':
            return letra + self.comentario_s6()
        else:
            return ""
    def comentario_s6(self):
        letra = self.leer_letra()
        if letra == '/':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            return ""
    def comentario_s7(self):
        letra = self.leer_letra()
        self.columna=self.columna+1 #! **********
        if letra == ' ' or letra.isalpha() or letra.isnumeric():
            return "divicion"
        return "divicion"

        
    #!Automata OPERADORES
    def operadores_s0 (self):
        letra = self.leer_letra()
        self.quitar_primera_letra()
        self.columna=self.columna+1 #! **********
        return letra + self.operadores_s1()
    def operadores_s1 (self):
        letra = self.leer_letra()
        if letra == "=" or letra == "&" or letra == "|":
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            return letra + self.identificador_S1()
        else:
            return ""
    def operador_simple_busqueda (self,lexema):
        tieneErrorLexico=False
        #diccionario
        diccionario ={"+":14,"-":15,"*":16,"/":3,"%":4,"!":5,">":6,"<":7,"==":8,"!=":9,">=":10,"<=":11,"&&":12,"||":13
,"=!":0,"=>":1,"=<":2}
        tipo_encontrado = diccionario.get(lexema.lower(),None)
        if(tipo_encontrado == None):
                tieneErrorLexico=True
                self.lista_errores.append(clase_token(lexema,self.columna,self.linea,"Error",tieneErrorLexico,"ERROR"))
                tieneErrorLexico=False
        else:
            tipo = tipo_encontrado
            if tipo ==14:
                self.lista_tokens.append(clase_token("+",self.columna,self.linea,"suma",tieneErrorLexico,"+"))
            if tipo ==15:
                self.lista_tokens.append(clase_token("-",self.columna,self.linea,"resta",tieneErrorLexico,"-"))
            if tipo ==16:
                self.lista_tokens.append(clase_token("*",self.columna,self.linea,"multiplicacion",tieneErrorLexico,"*"))
            if tipo ==3:
                self.lista_tokens.append(clase_token("/",self.columna,self.linea,"divicion",tieneErrorLexico,"/"))
            if tipo ==4:
                
                self.lista_tokens.append(clase_token("%",self.columna,self.linea,"resto",tieneErrorLexico,"%"))
            if tipo ==5:
                self.lista_tokens.append(clase_token("!",self.columna,self.linea,"not",tieneErrorLexico,"!"))
            if tipo ==6:
                self.lista_tokens.append(clase_token(">",self.columna,self.linea,"mayor_que",tieneErrorLexico,">"))
            if tipo ==7:
                self.lista_tokens.append(clase_token("<",self.columna,self.linea,"menor_que",tieneErrorLexico,"<"))
            if tipo ==8:
                self.lista_tokens.append(clase_token("==",self.columna,self.linea,"Igualacion",tieneErrorLexico,"=="))
            if tipo ==9:
                self.lista_tokens.append(clase_token("!=",self.columna,self.linea,"Diferenciacion",tieneErrorLexico,"!="))
            if tipo ==10:
                self.lista_tokens.append(clase_token(">=",self.columna,self.linea,"mayor_igual",tieneErrorLexico,">="))
            if tipo ==11:
                self.lista_tokens.append(clase_token("<=",self.columna,self.linea,"menor_igual",tieneErrorLexico,"<="))
            if tipo ==12:
                self.lista_tokens.append(clase_token("&&",self.columna,self.linea,"AND",tieneErrorLexico,"&&"))
            if tipo ==13:
                self.lista_tokens.append(clase_token("||",self.columna,self.linea,"OR",tieneErrorLexico,"||"))
            if tipo ==0:
                self.lista_tokens.append(clase_token("=!",self.columna,self.linea,"ERROR",tieneErrorLexico,"ERROR"))
            if tipo ==1:
                self.lista_tokens.append(clase_token("=>",self.columna,self.linea,"ERROR",tieneErrorLexico,"ERROR"))
            if tipo ==2:
                self.lista_tokens.append(clase_token("=<",self.columna,self.linea,"ERROR",tieneErrorLexico,"ERROR"))
    #!Automata Identificador    
    def identificador_S0 (self):
        letra = self.leer_letra()
        self.quitar_primera_letra()
        self.columna=self.columna+1 #! *********

        return letra + self.identificador_S1()
    def identificador_S1 (self):
        letra = self.leer_letra()
        if letra.isalpha() or letra.isnumeric() or letra =="_":
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********

            return letra + self.identificador_S1()
        else:
            return ""
    #!Automata Palabra reservada  
    def tipo_dato_S0 (self):
        letra = self.leer_letra()
        self.quitar_primera_letra()
        self.columna=self.columna+1 #! *********
        return letra + self.identificador_S0()
    def tipo_dato_busqueda (self,lexema):
        tieneErrorLexico=False
        #diccionario
        diccionario ={"int":0,"double":1,"string":2,"char":3,"boolean":4,"true":5,"false":6,"if":7,"else":8,"while":9,
        "do":10,"void":11,"return":12}
        tipo_encontrado = diccionario.get(lexema.lower(),None)
        if(tipo_encontrado == None):
            self.lista_tokens.append(clase_token(lexema,self.columna,self.linea,"identificador",tieneErrorLexico,"(_|[a-z])([a-z]|[0-9]|_)*"))
        else:
            tipo = tipo_encontrado
            if tipo ==0:
                self.lista_tokens.append(clase_token("int",self.columna,self.linea,"tipo_int",tieneErrorLexico,"int"))
            elif tipo ==1:
                self.lista_tokens.append(clase_token("double",self.columna,self.linea,"tipo_double",tieneErrorLexico,"double"))
            elif tipo ==2:
                self.lista_tokens.append(clase_token("string",self.columna,self.linea,"tipo_string",tieneErrorLexico,"string"))
            elif tipo ==3:
                self.lista_tokens.append(clase_token("char",self.columna,self.linea,"tipo_char",tieneErrorLexico,"char"))
            elif tipo ==4:
                self.lista_tokens.append(clase_token("boolean",self.columna,self.linea,"tipo_boolean",tieneErrorLexico,"boolean"))
            elif tipo ==5:
                self.lista_tokens.append(clase_token("true",self.columna,self.linea,"dato_boolean",tieneErrorLexico,"true"))
            elif tipo ==6:
                self.lista_tokens.append(clase_token("false",self.columna,self.linea,"dato_boolean",tieneErrorLexico,"false"))
            elif tipo ==7:
                self.lista_tokens.append(clase_token("if",self.columna,self.linea,"condicional_if",tieneErrorLexico,"if"))
            elif tipo ==8:
                self.lista_tokens.append(clase_token("else",self.columna,self.linea,"condicional_else",tieneErrorLexico,"else"))
            elif tipo ==9:
                self.lista_tokens.append(clase_token("while",self.columna,self.linea,"ciclo_while",tieneErrorLexico,"while"))
            elif tipo ==10:
                self.lista_tokens.append(clase_token("do",self.columna,self.linea,"ciclo_do",tieneErrorLexico,"do"))
            elif tipo ==11:
                self.lista_tokens.append(clase_token("void",self.columna,self.linea,"metodo_void",tieneErrorLexico,"void"))
            elif tipo ==12:
                self.lista_tokens.append(clase_token("return",self.columna,self.linea,"metodo_return",tieneErrorLexico,"return"))
    #!Automata numero (int/double)
    def numero_s0(self):
        letra = self.leer_letra()
        if letra.isnumeric():
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra + self.numero_s1()
    def numero_s1(self):
        letra = self.leer_letra()
        if letra.isnumeric():
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra + self.numero_s1()
        if letra==".":
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra + self.numero_s1()
        else:
            return ""
    #!Automata comillas(String)
    def comillas_s0(self):
        letra = self.leer_letra()
        if letra == '\"' or letra == "“" or letra == "”" or letra == "'":
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra +  self.comillas_s1()
    def comillas_s1(self):
        letra = self.leer_letra()
        if letra != '\"'and letra != "“" and letra != "”" and letra != "'":
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra + self.comillas_s1()
        else:
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra
   #!Automata comilla(char)
    def comilla_s0(self):
        letra = self.leer_letra()
        if letra == '\'' :
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra +  self.comilla_s1()
    def comilla_s1(self):
        letra = self.leer_letra()
        if letra != '\'':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra + self.comilla_s1()
        else:
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
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
a.genrarReporteToken()








        