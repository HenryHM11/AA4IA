import cv2
import numpy as np

def contar_fichas_por_fila(imagen_path):
    imagen = cv2.imread(imagen_path)
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    imagen_suavizada = cv2.medianBlur(imagen_gris, 5)

    circulos = cv2.HoughCircles(
        imagen_suavizada,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=20,
        maxRadius=50
    )

    if circulos is not None:
        circulos = np.uint16(np.around(circulos))

        circulos = sorted(circulos[0, :], key=lambda x: x[1])

        fila_actual = circulos[0][1]
        fichas_por_fila = 0
        filas_detectadas = 0

        imagen_resultante = imagen.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        for circulo in circulos:
            x, y = circulo[0], circulo[1]

            if abs(y - fila_actual) < 10:
                fichas_por_fila += 1
                cv2.circle(imagen_resultante, (x, y), circulo[2], (0, 0, 0), 0)
            else:
                cv2.putText(imagen_resultante, f'{fichas_por_fila} fichas', (x + 30, fila_actual), font, 1.5, (0, 0, 255), 4, cv2.LINE_AA)
                fila_actual = y
                fichas_por_fila = 1
                filas_detectadas += 1

        cv2.putText(imagen_resultante, f'{fichas_por_fila} fichas', (x + 30, fila_actual), font, 1.5, (0, 0, 255), 4, cv2.LINE_AA)
        filas_detectadas += 1

        if filas_detectadas == 8:
            print('Se detectaron exactamente 8 filas en el tablero.')
        else:
            print(f'Se detectaron {filas_detectadas} filas en lugar de 8.')

        ruta_guardado = 'uploads/resultado_fila.jpg'
        cv2.imwrite(ruta_guardado, imagen_resultante)

        return ruta_guardado

    else:
        print('No se detectaron círculos en la imagen.')
