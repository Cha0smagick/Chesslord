import random

# Definir el tablero de ajedrez
tablero = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# Dibujar el tablero de ajedrez
def dibujar_tablero(tablero):
    print("  a b c d e f g h")
    print(" ┌─┬─┬─┬─┬─┬─┬─┬─┐")
    for i in range(8):
        print(str(8 - i) + "│" + " ".join(tablero[i]) + "│" + str(8 - i))
        if i < 7:
            print(" ├─┼─┼─┼─┼─┼─┼─┼─┤")
    print(" └─┴─┴─┴─┴─┴─┴─┴─┘")
    print("  a b c d e f g h")

# Mapeo de letras a números para las columnas del tablero
columnas = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}

# Mapeo de números a letras para las columnas del tablero
letras = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h'
}

# Movimiento de una ficha
def mover_ficha(origen, destino):
    columna_origen, fila_origen = origen
    columna_destino, fila_destino = destino
    
    ficha = tablero[fila_origen][columna_origen]
    tablero[fila_origen][columna_origen] = ' '
    tablero[fila_destino][columna_destino] = ficha

# Turno del jugador
def turno_jugador():
    dibujar_tablero(tablero)
    origen = input("Ingrese la casilla de origen (por ejemplo, a2): ")
    destino = input("Ingrese la casilla de destino (por ejemplo, a4): ")
    
    origen_coord = notacion_a_casilla(origen)
    destino_coord = notacion_a_casilla(destino)
    
    if movimiento_valido(origen_coord, destino_coord, 'negro'):
        mover_ficha(origen_coord, destino_coord)
    else:
        print("Movimiento inválido. Intente nuevamente.")
        turno_jugador()

# Turno de la inteligencia artificial
def turno_ia():
    # Implementar una lógica básica de IA aquí
    posibles_movimientos = []
    
    for fila in range(8):
        for columna in range(8):
            if tablero[fila][columna].isupper():
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i != 0 or j != 0:
                            if fila + i >= 0 and fila + i < 8 and columna + j >= 0 and columna + j < 8:
                                if movimiento_valido((columna, fila), (columna + j, fila + i), 'blanco'):
                                    posibles_movimientos.append(((columna, fila), (columna + j, fila + i)))
    
    movimiento = random.choice(posibles_movimientos)
    mover_ficha(movimiento[0], movimiento[1])
    print("La IA movió la ficha", tablero[movimiento[0][1]][movimiento[0][0]], "de", casilla_a_notacion(movimiento[0]), "a", casilla_a_notacion(movimiento[1]))

# Verificar si una casilla está dentro del tablero
def dentro_del_tablero(fila, columna):
    return fila >= 0 and fila < 8 and columna >= 0 and columna < 8

# Verificar si una casilla está vacía
def casilla_vacia(fila, columna):
    return tablero[fila][columna] == ' '

# Verificar si una casilla contiene una ficha del jugador actual
def ficha_del_jugador(fila, columna, jugador):
    return tablero[fila][columna].islower() if jugador == 'negro' else tablero[fila][columna].isupper()

# Verificar si una casilla contiene una ficha del oponente
def ficha_del_oponente(fila, columna, jugador):
    return tablero[fila][columna].isupper() if jugador == 'negro' else tablero[fila][columna].islower()

# Verificar si el movimiento es válido para el peón
def movimiento_valido_peon(origen, destino, jugador):
    columna_origen, fila_origen = origen
    columna_destino, fila_destino = destino
    
    direccion = 1 if jugador == 'blanco' else -1
    
    if columna_origen == columna_destino:
        if fila_destino == fila_origen + direccion:
            return casilla_vacia(fila_destino, columna_destino)
        elif fila_destino == fila_origen + 2 * direccion and fila_origen in (1, 6) and casilla_vacia(fila_destino, columna_destino):
            intermedia_fila = fila_origen + direccion
            return casilla_vacia(intermedia_fila, columna_destino) and casilla_vacia(fila_destino, columna_destino)
    elif abs(columna_destino - columna_origen) == 1 and fila_destino == fila_origen + direccion:
        return ficha_del_oponente(fila_destino, columna_destino, jugador)
    
    return False

# Verificar si el movimiento es válido para el caballo
def movimiento_valido_caballo(origen, destino):
    columna_origen, fila_origen = origen
    columna_destino, fila_destino = destino
    
    filas_diferencia = abs(fila_destino - fila_origen)
    columnas_diferencia = abs(columna_destino - columna_origen)
    
    return (filas_diferencia == 2 and columnas_diferencia == 1) or (filas_diferencia == 1 and columnas_diferencia == 2)

# Verificar si el movimiento es válido para la torre
def movimiento_valido_torre(origen, destino):
    columna_origen, fila_origen = origen
    columna_destino, fila_destino = destino
    
    if columna_origen == columna_destino:
        if fila_origen == fila_destino:
            return False
        elif fila_origen < fila_destino:
            for i in range(fila_origen + 1, fila_destino):
                if not casilla_vacia(i, columna_origen):
                    return False
        else:
            for i in range(fila_origen - 1, fila_destino, -1):
                if not casilla_vacia(i, columna_origen):
                    return False
    elif fila_origen == fila_destino:
        if columna_origen < columna_destino:
            for i in range(columna_origen + 1, columna_destino):
                if not casilla_vacia(fila_origen, i):
                    return False
        else:
            for i in range(columna_origen - 1, columna_destino, -1):
                if not casilla_vacia(fila_origen, i):
                    return False
    else:
        return False
    
    return True

# Verificar si el movimiento es válido para el alfil
def movimiento_valido_alfil(origen, destino):
    columna_origen, fila_origen = origen
    columna_destino, fila_destino = destino
    
    if abs(fila_destino - fila_origen) != abs(columna_destino - columna_origen):
        return False
    
    if fila_origen < fila_destino:
        if columna_origen < columna_destino:
            for i in range(1, fila_destino - fila_origen):
                if not casilla_vacia(fila_origen + i, columna_origen + i):
                    return False
        else:
            for i in range(1, fila_destino - fila_origen):
                if not casilla_vacia(fila_origen + i, columna_origen - i):
                    return False
    else:
        if columna_origen < columna_destino:
            for i in range(1, fila_origen - fila_destino):
                if not casilla_vacia(fila_origen - i, columna_origen + i):
                    return False
        else:
            for i in range(1, fila_origen - fila_destino):
                if not casilla_vacia(fila_origen - i, columna_origen - i):
                    return False
    
    return True

# Verificar si el movimiento es válido para la reina
def movimiento_valido_reina(origen, destino):
    return movimiento_valido_torre(origen, destino) or movimiento_valido_alfil(origen, destino)

# Verificar si el movimiento es válido para el rey
def movimiento_valido_rey(origen, destino):
    columna_origen, fila_origen = origen
    columna_destino, fila_destino = destino
    
    filas_diferencia = abs(fila_destino - fila_origen)
    columnas_diferencia = abs(columna_destino - columna_origen)
    
    return filas_diferencia <= 1 and columnas_diferencia <= 1

# Validar si el movimiento es válido según las reglas de la pieza
def movimiento_valido(origen, destino, jugador):
    columna_origen, fila_origen = origen
    columna_destino, fila_destino = destino
    
    ficha = tablero[fila_origen][columna_origen]
    
    if ficha.lower() == 'p':
        return movimiento_valido_peon(origen, destino, jugador)
    elif ficha.lower() == 'n':
        return movimiento_valido_caballo(origen, destino)
    elif ficha.lower() == 'r':
        return movimiento_valido_torre(origen, destino)
    elif ficha.lower() == 'b':
        return movimiento_valido_alfil(origen, destino)
    elif ficha.lower() == 'q':
        return movimiento_valido_reina(origen, destino)
    elif ficha.lower() == 'k':
        return movimiento_valido_rey(origen, destino)
    
    return False

# Convertir notación de casilla a coordenadas
def notacion_a_casilla(notacion):
    columna = columnas[notacion[0]]
    fila = 8 - int(notacion[1])
    return columna, fila

# Convertir coordenadas a notación de casilla
def casilla_a_notacion(casilla):
    columna = letras[casilla[0]]
    fila = str(8 - casilla[1])
    return columna + fila

# Juego principal
def jugar_ajedrez():
    print("Bienvenido al juego de ajedrez!")
    print("Las fichas negras (minúsculas) juegan primero.")
    print("Ingrese las casillas de origen y destino en el formato 'columna'+'fila' (por ejemplo, a2).")
    print("¡Que empiece el juego!")
    print()
    dibujar_tablero(tablero)
    print()
    
    jugador_actual = 'negro'
    
    while True:
        if jugador_actual == 'negro':
            turno_jugador()
            jugador_actual = 'blanco'
        else:
            turno_ia()
            jugador_actual = 'negro'
        
        print()
        dibujar_tablero(tablero)
        print()

# Iniciar el juego
jugar_ajedrez()
