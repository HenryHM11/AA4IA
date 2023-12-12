import cv2
import numpy as np

def contar_circulos_por_color(imagen_path):
    # Cargar la imagen
    imagen = cv2.imread(imagen_path)

    # Verificar la forma de la imagen
    if len(imagen.shape) != 3 or imagen.shape[2] != 3:
        print("Error: La imagen no es válida.")
        return

    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para reducir el ruido y resaltar los bordes
    imagen_suavizada = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

    # Aplicar la transformada de Hough para detectar círculos
    circulos = cv2.HoughCircles(
        imagen_suavizada,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=60,
        param2=33,
        minRadius=20,
        maxRadius=80
    )

    # Si se detectan círculos, contarlos y mostrar la imagen
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))

        # Extraer colores de la imagen original en las posiciones de los círculos
        colores = [tuple(map(int, imagen[y, x])) for x, y, _ in circulos[0, :]]

        # Inicializar un diccionario para contar la cantidad de círculos por color
        contador_por_color = {}

        for color in colores:
            # Convertir la tupla de color a una cadena para usarla como clave en el diccionario
            color_str = str(color)

            # Incrementar el contador para el color actual en el diccionario
            contador_por_color[color_str] = contador_por_color.get(color_str, 0) + 1

        # Imprimir la cantidad de círculos por color
        for color, cantidad in contador_por_color.items():
            print(f'{color}: hay {cantidad} círculos')

        # Mostrar la imagen con círculos coloreados y la cantidad de colores
        mostrar_imagen_con_circulos(imagen, circulos, colores, contador_por_color)

        # Guardar la imagen resultante en el directorio 'uploads'
        ruta_guardado = 'uploads/resultado_color.jpg'
        for i, circulo in enumerate(circulos[0, :]):
            x, y, r = circulo[0], circulo[1], circulo[2]
            color = tuple(map(int, colores[i]))  # Convertir los valores a enteros
            # Aumentar el tamaño del radio
            cv2.circle(imagen, (x, y), r + 10, color, 2)
        
        # Agregar la cantidad de colores en una esquina de la imagen
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(imagen, f'Cantidad de colores: {len(contador_por_color)}', (10, 30), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        # Agregar la cantidad de cada color debajo del texto principal
        y_offset = 60
        for color, cantidad in contador_por_color.items():
            cv2.putText(imagen, f'{color}: {cantidad}', (10, y_offset), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            y_offset += 30

        cv2.imwrite(ruta_guardado, imagen)

        return ruta_guardado

    else:
        print('No se detectaron círculos en la imagen.')

def mostrar_imagen_con_circulos(imagen, circulos, colores, contador_por_color):
    imagen_resultante = imagen.copy()
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        for i, circulo in enumerate(circulos[0, :]):
            x, y, r = circulo[0], circulo[1], circulo[2]
            color = tuple(map(int, colores[i]))  # Convertir los valores a enteros
            # Aumentar el tamaño del radio
            cv2.circle(imagen_resultante, (x, y), r + 10, color, 2)
        
        # Agregar la cantidad de colores en una esquina de la imagen
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(imagen_resultante, f'Cantidad de colores: {len(contador_por_color)}', (10, 30), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        # Agregar la cantidad de cada color debajo del texto principal
        y_offset = 60
        for color, cantidad in contador_por_color.items():
            cv2.putText(imagen_resultante, f'{color}: {cantidad}', (10, y_offset), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            y_offset += 30

    cv2.waitKey(0)
    cv2.destroyAllWindows()
