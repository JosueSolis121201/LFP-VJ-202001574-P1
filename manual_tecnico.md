# 1. LFP (Manual tecnico)
## 1.1. 17/06/2022
- Josue Daniel Solis osorio
- 202001574
#  2. 2.0 Guía de uso
- [1. LFP (Manual tecnico)](#1-lfp-manual-tecnico)
  - [1.1. 17/06/2022](#11-17062022)
- [2. 2.0 Guía de uso](#2-20-guía-de-uso)
  - [2.1. Glosario](#21-glosario)
  - [2.2. Introducción](#22-introducción)
  - [2.3. Objetivo de los procedimientos](#23-objetivo-de-los-procedimientos)
  - [2.4. Especificaciones técnicas](#24-especificaciones-técnicas)
- [3. AFDs por el método del árbol](#3-afds-por-el-método-del-árbol)
  - [3.1. Primer AFD por el método del árbol (identificado)](#31-primer-afd-por-el-método-del-árbol-identificado)
    - [3.1.1. Exprecion regular](#311-exprecion-regular)
    - [3.1.2. Metodo del arbol](#312-metodo-del-arbol)
    - [3.1.3. Folllow](#313-folllow)
    - [3.1.4. Subconjuntos](#314-subconjuntos)
    - [3.1.5. Transiciones](#315-transiciones)
    - [3.1.6. grafo](#316-grafo)
  - [3.2. Primer AFD por el método del árbol (comentario unilinea)](#32-primer-afd-por-el-método-del-árbol-comentario-unilinea)
    - [3.2.1. Exprecion regular](#321-exprecion-regular)
    - [3.2.2. Metodo del arbol](#322-metodo-del-arbol)
    - [3.2.3. Folllow](#323-folllow)
    - [3.2.4. Subconjuntos](#324-subconjuntos)
    - [3.2.5. Transiciones](#325-transiciones)
    - [3.2.6. grafo](#326-grafo)
##  2.1. Glosario
| **palabra** | **significado**
| --- | ---
| LFP | Lenguaje formales de programacion
##  2.2. Introducción
El presente documento describe los aspectos técnicos informáticos del sistema de información. El documento familiariza las persona que utilicen el programa para su correcta ejecución.

##  2.3. Objetivo de los procedimientos
La elaboración de una aplicación que sea capaz de leer un archivo de entrada con la terminacion ".sc" y dar como resultado una serie de tokens perteneciente al lenguaje

##  2.4. Especificaciones técnicas
El sistema operativo con el que se trabajó con Windows 10, utilizando el lenguaje de programación denominado Python

# 3. AFDs por el método del árbol

## 3.1. Primer AFD por el método del árbol (identificado)
### 3.1.1. Exprecion regular
Se llego a la siguiente exprecion regular: ([a-z]|_){1}(\w)*
### 3.1.2. Metodo del arbol

!["Metodo del arbol"](metodoarbol_identificador.png)

### 3.1.3. Folllow

!["Folllow"](follow_identificador.png)

### 3.1.4. Subconjuntos

!["Subconjuntos"](sub_identificador.png)

### 3.1.5. Transiciones

!["Transiciones"](transiciones_identificador.png)

### 3.1.6. grafo

!["grafo"](grafo1_identificador.png)

## 3.2. Primer AFD por el método del árbol (comentario unilinea)
### 3.2.1. Exprecion regular
Se llego a la siguiente exprecion regular: //\\.*
### 3.2.2. Metodo del arbol

!["Metodo del arbol_1"](metodoarbol1_identificador.png)

### 3.2.3. Folllow

!["Folllow"](follow1_identificador.png)

### 3.2.4. Subconjuntos

!["Subconjuntos"](sub1_identificador.png)

### 3.2.5. Transiciones

!["Transiciones"](transiciones1_identificador.png)

### 3.2.6. grafo

!["grafo"](grafo2_identificador.png)











