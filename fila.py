import cv2
import numpy as np

def contar_fichas_por_fila(imagen_path):
    # Convertir la imagen a escala de grises
    imagen = cv2.imread(imagen_path)
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar un suavizado para reducir el ruido
    imagen_suavizada = cv2.medianBlur(imagen_gris, 5)

    # Aplicar la transformada de Hough para detectar círculos
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

    # Si se detectan círculos, procesar la disposición por filas
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))

        # Ordenar los círculos por coordenada y
        circulos = sorted(circulos[0, :], key=lambda x: x[1])

        # Inicializar variables para rastrear la fila actual y la cantidad de fichas por fila
        fila_actual = circulos[0][1]
        fichas_por_fila = 0
        filas_detectadas = 0

        # Crear una copia de la imagen original para dibujar círculos
        imagen_resultante = imagen.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        for circulo in circulos:
            x, y = circulo[0], circulo[1]

            # Verificar si el círculo pertenece a la misma fila
            if abs(y - fila_actual) < 10:
                fichas_por_fila += 1
                cv2.circle(imagen_resultante, (x, y), circulo[2], (0, 255, 0), 0)
            else:
                # Imprimir la cantidad de fichas para la fila actual y reiniciar para la nueva fila
                cv2.putText(imagen_resultante, f'{fichas_por_fila} fichas', (x + 30, fila_actual), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                fila_actual = y
                fichas_por_fila = 1
                filas_detectadas += 1

        # Imprimir la cantidad de fichas para la última fila
        cv2.putText(imagen_resultante, f'{fichas_por_fila} fichas', (x + 30, fila_actual), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        filas_detectadas += 1

        # Verificar si se detectaron exactamente 8 filas
        if filas_detectadas == 8:
            print('Se detectaron exactamente 8 filas en el tablero.')
        else:
            print(f'Se detectaron {filas_detectadas} filas en lugar de 8.')

        # Guardar la imagen resultante en el directorio 'uploads'
        ruta_guardado = 'uploads/resultado_fila.jpg'
        cv2.imwrite(ruta_guardado, imagen_resultante)

        return ruta_guardado

    else:
        print('No se detectaron círculos en la imagen.')
