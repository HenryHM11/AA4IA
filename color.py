import cv2
import numpy as np

def contar_circulos_por_color(imagen_path):
    imagen = cv2.imread(imagen_path)

    if len(imagen.shape) != 3 or imagen.shape[2] != 3:
        print("Error: La imagen no es válida.")
        return

    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    imagen_suavizada = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

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

    if circulos is not None:
        circulos = np.uint16(np.around(circulos))

        colores = [tuple(map(int, imagen[y, x])) for x, y, _ in circulos[0, :]]

        contador_por_color = {}

        for color in colores:
            color_str = str(color)

            contador_por_color[color_str] = contador_por_color.get(color_str, 0) + 1

        for color, cantidad in contador_por_color.items():
            print(f'{color}: hay {cantidad} círculos')

        mostrar_imagen_con_circulos(imagen, circulos, colores, contador_por_color)

        ruta_guardado = 'uploads/resultado_color.jpg'
        for i, circulo in enumerate(circulos[0, :]):
            x, y, r = circulo[0], circulo[1], circulo[2]
            color = tuple(map(int, colores[i]))  
            cv2.circle(imagen, (x, y), r + 10, color, 2)
        

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(imagen, f'Cantidad de colores: {len(contador_por_color)}', (10, 30), font, 1, (0, 0, 255), 3, cv2.LINE_AA)

        y_offset = 60
        for color, cantidad in contador_por_color.items():
            cv2.putText(imagen, f'{color}: {cantidad}', (10, y_offset), font, 1, (0, 0, 255), 3, cv2.LINE_AA)
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
            color = tuple(map(int, colores[i]))  
            cv2.circle(imagen_resultante, (x, y), r + 10, color, 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(imagen_resultante, f'Cantidad de colores: {len(contador_por_color)}', (10, 30), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)

        y_offset = 60
        for color, cantidad in contador_por_color.items():
            cv2.putText(imagen_resultante, f'{color}: {cantidad}', (10, y_offset), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
            y_offset += 30

    cv2.waitKey(0)
    cv2.destroyAllWindows()
