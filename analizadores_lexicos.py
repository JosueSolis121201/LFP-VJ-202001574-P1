



class clase_token:
    def __init__(self,valor,columna,fila,tipo,tieneErrorLexico,patron):
        self.valor = valor
        self.fila = fila
        self.tipo = tipo
        self.columna = columna
        self.tieneErrorLexico = tieneErrorLexico
        self.patron=patron
        #print(self,valor,columna,fila,tipo,tieneErrorLexico,patron)



    def html(self):
        return "<tr class=\"active-row\">" + "<td>"+ str(self.valor)+"</td>" + "<td>"+ str(self.tipo)+"</td>" + "<td>"+ str(self.columna)+"</td>"+"<td>"+ str(self.fila)+"</td>" +"<td>"+ str(self.tieneErrorLexico)+"</td>"+"<td>"+ str(self.patron)+"</td>" +"</tr>"
class automata_finito_determinista:
    def __init__(self,estado,caracter,lexema_reconocido,siguiente_estado):
        self.estado = estado
        self.caracter = caracter
        self.lexema_reconocido = lexema_reconocido
        self.siguiente_estado = siguiente_estado
        #print(self,estado,lexema_reconocido,siguiente_estado)
    def html(self):
        return "<tr class=\"active-row\">" + "<td>"+ str(self.estado)+"</td>" + "<td>"+ str(self.caracter)+"</td>" + "<td>"+ str(self.lexema_reconocido)+"</td>"+"<td>"+ str(self.siguiente_estado)+"</td>" +"</tr>"
class lexico():
    def __init__(self) -> None:
        self.texto=""
        self.lista_tokens=[]
        self.lista_errores = []
        self.AFD = []
        self.lexema_conocido=""
        self.linea = 1
        self.columna = 1
        self.contador_pruebas_especiales=1
    def genrarReporteToken(self):
        inicio="<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"estilo.css\"/></head><body>"
        cuerpo = "<table class=\"styled-table\"><tr class=\"active-row\"><th>LEXEMA</th><th>TIPO</th><th>COLUMNA</th><th>LINEA</th><th>ERROR LEXICO</th></th><th>PATRON</th></tr><tbody>"
        cuerpo_e = "<table class=\"styled-table\"><tr class=\"active-row\"><th>LEXEMA</th><th>TIPO</th><th>COLUMNA</th><th>LINEA</th><th>ERROR LEXICO</th></th><th>PATRON</th></tr><tbody>"
        cuerpo_AFD = "<table class=\"styled-table\"><tr class=\"active-row\"><th>ESTADO</th><th>CARACTER</th><th>LEXEMA CONOCIDO</th><th>SIGUIENTE ESTADO</th></tr><tbody>"
        concatenar = ""
        concatenar_e = ""
        concatenar_AFD= ""
        #!TOKENS
        for element in self.lista_tokens:
            concatenar = concatenar + element.html()
        #!ERRORES LEXISCOS
        for error in self.lista_errores:
            concatenar_e = concatenar_e + error.html()
        #!ERRORES AFD
        for siguimiento in self.AFD:
            concatenar_AFD = concatenar_AFD + siguimiento.html()


        cuerpo_token="<h1>REPORTE DE TOKENS</h1>"+ cuerpo +concatenar+ "</tbody></table>"
        cuerpo_errores="<h1>ERRORES LEXICOS</h1>"+ cuerpo_e +concatenar_e+ "</tbody></table>"
        cuerpo_AFD="<h1>SEGUIMIENTO DE AFDs</h1>"+ cuerpo_AFD +concatenar_AFD+ "</tbody></table>"
        final = inicio +cuerpo_token+cuerpo_errores +cuerpo_AFD+"</html></body>"
        f = open (input("introdusca el nombre del reporte HTML :")+".html",'w')
        f.write(final)
        f.close()
    def analizar(self):
        self.analizador()#!msg
    def analizador(self):
        #Directorios
        
       
        #!Mesanje de SC
        with open(input("introdusca el nombre del archivo :")+".sc") as f:
            print("archivo.sc aceptado ")
            msg = f.read()
        tieneErrorLexico=False
        self.texto = msg 
        while self.texto != "":
            letra = self.leer_letra()
            if letra.isalpha(): #!Automata Palabra reservada
                lectura = self.tipo_dato_S0()
                self.lexema_conocido=""
                self.tipo_dato_busqueda(lectura)
            elif letra == '/':#!Automata comentario(de una linea/varias lineas)
                lectura = self.comentario_s0()
               
                if '*/' in lectura:
                    if '\n' in lectura:
                        self.columna=self.columna+0 #! **********
                    else:
                        self.columna=self.columna-1 #! **********
                    self.columna=self.columna+1 #! **********
                    self.lexema_conocido=""
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"comentario_multilinea",tieneErrorLexico,"/*(\w|\n| )*[^*/]*/"))
                    self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                elif "divicion"  in lectura:
                    
                    self.columna=self.columna-1 #! *********
                    self.lexema_conocido=""
                    self.lista_tokens.append(clase_token("/",self.columna,self.linea,"divicion",tieneErrorLexico,"/"))
                    self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                else:
                    self.linea=self.linea-1
                    self.lexema_conocido=""
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"comentario_unilinea",tieneErrorLexico,"//(\w| )*"))
                    self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                    self.columna=1
                    self.linea=self.linea+1
            elif letra == "_" or letra.isalpha(): #!Automata Identificador
                lectura = self.identificador_S0()
                if ' ' in lectura:
                    print("esto no deberia estar aqui")
                self.lexema_conocido=""
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"identificador",tieneErrorLexico,"(_|[a-z])([a-z]|[0-9]|_)*"))
            elif letra.isnumeric(): #!Automata numeros (int/double)
                lectura = self.numero_s0()
                self.lexema_conocido=""
                if '.' in lectura:
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_double",tieneErrorLexico,"[0-9]+.[0-9]+"))
                    self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                else:
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_int",tieneErrorLexico,"[0-9]+"))
                    self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == '\"' or letra == "“" or letra == "”":#!Automata comillas(String)
                lectura = self.comillas_s0()
                self.lexema_conocido=""
                self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_string",tieneErrorLexico,"\"[^\"]*\""))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == '\'':#!Automata comillas(char)
                lectura = self.comillas_s0()
                if len(lectura) ==3:
                    self.lexema_conocido=""
                    self.lista_tokens.append(clase_token(lectura,self.columna,self.linea,"dato_char",tieneErrorLexico,"\'[^\']{1}\'"))
                    self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                else:
                    self.lexema_conocido=""
                    tieneErrorLexico=True
                    self.lista_errores.append(clase_token(lectura,self.columna,self.linea,"Error",tieneErrorLexico,"ERROR"))
                    self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                    tieneErrorLexico=False
            elif letra == "+" or letra == "-" or letra == "*"  or letra == "/" or letra == "%"  or letra == "!" or letra == ">" or letra == "<"or letra == "=" or letra == "&" or   letra == "|":                 #!Automata OPERADORES(simples)
                lectura = self.operadores_s0()
                self.operador_simple_busqueda(lectura)
            elif letra == "[":#![
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"corchete_abre",tieneErrorLexico,"["))
                self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == "]":#!]
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"corchete_cierra",tieneErrorLexico,"]"))
                self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == "(":#!(
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"parentesis_abre",tieneErrorLexico,"("))
                self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == ")":#!)
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"parentesis_cierra",tieneErrorLexico,")"))
                self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == "{":#!{
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"llave_abre",tieneErrorLexico,"{"))
                self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == "}":#!}
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"llave_cierra",tieneErrorLexico,"}"))
                self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == ".":#!.
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"punto",tieneErrorLexico,"."))
                self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == ";":#!}
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********true
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"punto_coma",tieneErrorLexico,";"))
                self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == ",":#!}
                self.quitar_primera_letra()
                self.columna=self.columna+1 #! **********
                self.lista_tokens.append(clase_token(letra,self.columna,self.linea,"coma",tieneErrorLexico,","))
                self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif letra == "\n" or letra == "\t" or letra == " ":#!Saltos de linea y cosas saltables  
                if letra== "\n":
                    self.columna=1 #! **********
                    self.linea=self.linea+1
                if letra== "\t":
                    self.columna=self.columna+1#! **********
                if letra==" ":
                    self.columna=self.columna+1 #! **********
                self.quitar_primera_letra()
                         

            else:
                err = self.leer_letra()
                self.quitar_primera_letra()
                tieneErrorLexico=True
                self.columna=self.columna+1 #! **********
                self.lista_errores.append(clase_token(err,self.columna,self.linea,"Error_lexico",tieneErrorLexico,"ERROR"))
                tieneErrorLexico=False
                print({"error":err}) 
    #!Automata comentario(de una linea/varias lineas)   //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def comentario_s0(self):
        letra = self.leer_letra()
        if letra == '/':
            self.quitar_primera_letra()
            self.lexema_conocido=letra
            self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
            self.columna=self.columna+1 #! **********
            return letra +  self.comentario_s1()
    def comentario_s1(self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra == '/':
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S1",letra,self.lexema_conocido,"S2"))
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s2()
        elif letra == '*':
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S1",letra,self.lexema_conocido,"S4"))
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s4()
        else:
            
            return "" + self.comentario_s7()
    def comentario_s2(self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra != '\n':
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S2",letra,self.lexema_conocido,"S2"))
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s2()
        else:
            self.AFD.append(automata_finito_determinista("S2",letra,self.lexema_conocido,"S3"))
            return letra + self.comentario_s3()
    def comentario_s3(self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra == '\n':
            self.AFD.append(automata_finito_determinista("S3",letra,self.lexema_conocido,"S3"))
            self.quitar_primera_letra()
            
            self.linea=self.linea+1
            return letra 
        else:
            return ""
    def comentario_s4(self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra != '*':
            self.AFD.append(automata_finito_determinista("S4",letra,self.lexema_conocido,"S4"))
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            if letra =="\n":
                
                self.columna=0
                self.linea=self.linea+1
            return letra + self.comentario_s4()
        if letra == '*':
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S4",letra,self.lexema_conocido,"S5"))
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s5()
        else:
            return ""
    def comentario_s5(self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra != '/':
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S5",letra,self.lexema_conocido,"S4"))
            self.columna=self.columna+1 #! **********
            return letra + self.comentario_s4()
        if letra == '/':
            self.AFD.append(automata_finito_determinista("S5",letra,self.lexema_conocido,"S6"))
            return letra + self.comentario_s6()
        else:
            return ""
    def comentario_s6(self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra == '/':
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! **********
            return ""
    def comentario_s7(self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        self.columna=self.columna+1 #! **********
        if letra == ' ' or letra.isalpha() or letra.isnumeric():
            self.AFD.append(automata_finito_determinista("S7",letra,self.lexema_conocido,"S7"))
            return "divicion"
        return "divicion"
    #!Automata OPERADORES //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
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
            return letra + self.operadores_s1()
        else:
            return ""
    def operador_simple_busqueda (self,lexema):
        tieneErrorLexico=False
        #diccionario
        diccionario ={"=":20,"+":14,"-":15,"*":16,"/":3,"%":4,"!":5,">":6,"<":7,"==":8,"!=":9,">=":10,"<=":11,"&&":12,"||":13
,"=!":0,"=>":1,"=<":2}
        tipo_encontrado = diccionario.get(lexema.lower(),None)
        if(tipo_encontrado == None):
                tieneErrorLexico=True
                self.lista_errores.append(clase_token(lexema,self.columna,self.linea,"Error",tieneErrorLexico,"ERROR"))
                tieneErrorLexico=False
        else:
            tipo = tipo_encontrado
            if tipo ==20:
                self.AFD.append(automata_finito_determinista("s0","=","","s1"))
                self.AFD.append(automata_finito_determinista("s1","","=","s1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("=",self.columna,self.linea,"igual",tieneErrorLexico,"="))
            if tipo ==14:
                self.AFD.append(automata_finito_determinista("s0","+","","s1"))
                self.AFD.append(automata_finito_determinista("s1","","+","s1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("+",self.columna,self.linea,"suma",tieneErrorLexico,"+"))
            if tipo ==15:
                self.AFD.append(automata_finito_determinista("s0","-","","s1"))
                self.AFD.append(automata_finito_determinista("s1","","-","s1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("-",self.columna,self.linea,"resta",tieneErrorLexico,"-"))
            if tipo ==16:
                self.AFD.append(automata_finito_determinista("s0","*","","s1"))
                self.AFD.append(automata_finito_determinista("s1","","*","s1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("*",self.columna,self.linea,"multiplicacion",tieneErrorLexico,"*"))
            if tipo ==3:
                self.AFD.append(automata_finito_determinista("s0","/","","s1"))
                self.AFD.append(automata_finito_determinista("s1","","/","s1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("/",self.columna,self.linea,"divicion",tieneErrorLexico,"/"))
            if tipo ==4:
                self.AFD.append(automata_finito_determinista("s0","%","","s1"))
                self.AFD.append(automata_finito_determinista("s1","","%","s1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("%",self.columna,self.linea,"resto",tieneErrorLexico,"%"))
            if tipo ==5:
                self.AFD.append(automata_finito_determinista("s0","!","","s1"))
                self.AFD.append(automata_finito_determinista("s1","","!","s1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("!",self.columna,self.linea,"not",tieneErrorLexico,"!"))
            if tipo ==6:
                self.AFD.append(automata_finito_determinista("s0",">","","s1"))
                self.AFD.append(automata_finito_determinista("s1","",">","s1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token(">",self.columna,self.linea,"mayor_que",tieneErrorLexico,">"))
            if tipo ==7:
                self.AFD.append(automata_finito_determinista("s0","<","","s1"))
                self.AFD.append(automata_finito_determinista("s1","","<","s1"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("<",self.columna,self.linea,"menor_que",tieneErrorLexico,"<"))
            if tipo ==8:
                self.AFD.append(automata_finito_determinista("s0","=","","s1"))
                self.AFD.append(automata_finito_determinista("s1","=","=","s1"))
                self.AFD.append(automata_finito_determinista("s1","","==","s2"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("==",self.columna,self.linea,"Igualacion",tieneErrorLexico,"=="))
            if tipo ==9:
                self.AFD.append(automata_finito_determinista("s0","!","","s1"))
                self.AFD.append(automata_finito_determinista("s1","=","!","s1"))
                self.AFD.append(automata_finito_determinista("s1","","!=","s2"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("!=",self.columna,self.linea,"Diferenciacion",tieneErrorLexico,"!="))
            if tipo ==10:
                self.AFD.append(automata_finito_determinista("s0",">","","s1"))
                self.AFD.append(automata_finito_determinista("s1","=",">","s1"))
                self.AFD.append(automata_finito_determinista("s1","",">=","s2"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token(">=",self.columna,self.linea,"mayor_igual",tieneErrorLexico,">="))
            if tipo ==11:
                self.AFD.append(automata_finito_determinista("s0","<","","s1"))
                self.AFD.append(automata_finito_determinista("s1","=","<","s1"))
                self.AFD.append(automata_finito_determinista("s1","","<=","s2"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("<=",self.columna,self.linea,"menor_igual",tieneErrorLexico,"<="))
            if tipo ==12:
                self.AFD.append(automata_finito_determinista("s0","&","","s1"))
                self.AFD.append(automata_finito_determinista("s1","&","&","s1"))
                self.AFD.append(automata_finito_determinista("s1","","&&","s2"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("&&",self.columna,self.linea,"AND",tieneErrorLexico,"&&"))
            if tipo ==13:
                self.AFD.append(automata_finito_determinista("s0","|","","s1"))
                self.AFD.append(automata_finito_determinista("s1","|","|","s1"))
                self.AFD.append(automata_finito_determinista("s1","","||","s2"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("||",self.columna,self.linea,"OR",tieneErrorLexico,"||"))
            if tipo ==0:
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("=!",self.columna,self.linea,"ERROR",tieneErrorLexico,"ERROR"))
            if tipo ==1:
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("=>",self.columna,self.linea,"ERROR",tieneErrorLexico,"ERROR"))
            if tipo ==2:
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
                self.lista_tokens.append(clase_token("=<",self.columna,self.linea,"ERROR",tieneErrorLexico,"ERROR"))
    #!Automata Identificador    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def identificador_S0 (self):
        letra = self.leer_letra()
        self.quitar_primera_letra()
        self.columna=self.columna+1 #! *********
        self.lexema_conocido=letra
        self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
        return letra + self.identificador_S1()
    def identificador_S1 (self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra.isalpha() or letra.isnumeric() or letra =="_":
            self.AFD.append(automata_finito_determinista("S1",letra,self.lexema_conocido,"S1"))
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra + self.identificador_S1()
        else:
            return ""
    #!Automata Palabra reservada  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def tipo_dato_S0 (self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra.isalpha() or letra.isnumeric() or letra =="_":
            self.AFD.append(automata_finito_determinista("S0",letra,self.lexema_conocido,"S1"))
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
        return letra + self.tipo_dato_S1()
    def tipo_dato_S1 (self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra.isalpha() or letra.isnumeric() or letra =="_":
            self.columna=self.columna+1 #! *********
            self.AFD.append(automata_finito_determinista("S1",letra,self.lexema_conocido,"S1"))
            self.quitar_primera_letra()
            return letra + self.tipo_dato_S2()
        else:
            return ""
    def tipo_dato_S2 (self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        self.AFD.append(automata_finito_determinista("S1",letra,self.lexema_conocido,"S1"))
        if letra.isalpha() or letra.isnumeric() or letra =="_":
            self.quitar_primera_letra()
            self.columna=self.columna+1 #! *********
            return letra + self.tipo_dato_S2()
        else:
            return ""
    def tipo_dato_busqueda (self,lexema):
        tieneErrorLexico=False
        #diccionario
        diccionario ={"int":0,"double":1,"string":2,"char":3,"boolean":4,"true":5,"false":6,"if":7,"else":8,"while":9,
        "do":10,"void":11,"return":12}
        tipo_encontrado = diccionario.get(lexema.lower(),None)
        if(tipo_encontrado == None):
            self.lista_tokens.append(clase_token(lexema,self.columna,self.linea,"identificador",tieneErrorLexico,"(_|[a-z])([a-z]|[0-9]|_)*"))
            self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
        else:
            tipo = tipo_encontrado
            if tipo ==0:
                self.lista_tokens.append(clase_token("int",self.columna,self.linea,"tipo_int",tieneErrorLexico,"int"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==1:
                self.lista_tokens.append(clase_token("double",self.columna,self.linea,"tipo_double",tieneErrorLexico,"double"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==2:
                
                self.lista_tokens.append(clase_token("string",self.columna,self.linea,"tipo_string",tieneErrorLexico,"string"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==3:
                self.lista_tokens.append(clase_token("char",self.columna,self.linea,"tipo_char",tieneErrorLexico,"char"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==4:
                self.lista_tokens.append(clase_token("boolean",self.columna,self.linea,"tipo_boolean",tieneErrorLexico,"boolean"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==5:
                self.lista_tokens.append(clase_token("true",self.columna,self.linea,"dato_boolean",tieneErrorLexico,"true"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==6:
                self.lista_tokens.append(clase_token("false",self.columna,self.linea,"dato_boolean",tieneErrorLexico,"false"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==7:
                self.lista_tokens.append(clase_token("if",self.columna,self.linea,"condicional_if",tieneErrorLexico,"if"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==8:
                self.lista_tokens.append(clase_token("else",self.columna,self.linea,"condicional_else",tieneErrorLexico,"else"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==9:
                self.lista_tokens.append(clase_token("while",self.columna,self.linea,"ciclo_while",tieneErrorLexico,"while"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==10:
                self.lista_tokens.append(clase_token("do",self.columna,self.linea,"ciclo_do",tieneErrorLexico,"do"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==11:
                self.lista_tokens.append(clase_token("void",self.columna,self.linea,"metodo_void",tieneErrorLexico,"void"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
            elif tipo ==12:
                self.lista_tokens.append(clase_token("return",self.columna,self.linea,"metodo_return",tieneErrorLexico,"return"))
                self.AFD.append(automata_finito_determinista("------------","--------------","------------------","-----------------"))
    #!Automata numero (int/double) //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def numero_s0(self):
        letra = self.leer_letra()
        if letra.isnumeric():
            self.quitar_primera_letra()
            self.lexema_conocido=letra
            self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
            self.columna=self.columna+1 #! *********
            return letra + self.numero_s1()
    def numero_s1(self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra.isnumeric():
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S1",letra,self.lexema_conocido,"S1"))
            self.columna=self.columna+1 #! *********
            return letra + self.numero_s1()
        if letra==".":
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S1",letra,self.lexema_conocido,"S1"))
            self.columna=self.columna+1 #! *********
            return letra + self.numero_s1()
        else:
            return ""
    #!Automata comillas(String) //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def comillas_s0(self):
        letra = self.leer_letra()
        self.lexema_conocido=letra
        if letra == '\"' or letra == "“" or letra == "”" or letra == "'":
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S0",letra,"","S1"))
            self.columna=self.columna+1 #! *********
            return letra +  self.comillas_s1()
    def comillas_s1(self):
        letra = self.leer_letra()
        self.lexema_conocido=self.lexema_conocido+letra
        if letra != '\"'and letra != "“" and letra != "”" and letra != "'":
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S1",letra,self.lexema_conocido,"S1"))
            self.columna=self.columna+1 #! *********
            return letra + self.comillas_s1()
        else:
            self.quitar_primera_letra()
            self.AFD.append(automata_finito_determinista("S1",letra,self.lexema_conocido,"S2"))
            self.columna=self.columna+1 #! *********
            return letra
   #!Automata comilla(char) //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
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








        