import os
import time
import datetime
import webbrowser
import pyautogui

URL = "https://margex.com/app/rewards-hub"
INTERVAL_SECONDS = 6 * 60 * 60  # 6 horas (21600 segundos)
WAIT_AFTER_OPEN = 15            # Segundos para esperar a que cargue la página
WAIT_AFTER_CLAIM = 15           # Segundos a esperar antes de cerrar la ventana del navegador

IMAGE_FILENAME = "claim.png"


def process_claim():
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n[{now_str}] Abriendo la página en el navegador predeterminado del sistema...")
    
    # Abre la URL en el navegador predeterminado (Chrome, Edge, Firefox, etc.)
    webbrowser.open(URL)
    
    print(f"[ESPERA] Esperando {WAIT_AFTER_OPEN} segundos a que la página cargue completamente...")
    time.sleep(WAIT_AFTER_OPEN)
    
    image_path = os.path.join(os.getcwd(), IMAGE_FILENAME)
    
    if not os.path.exists(image_path):
        print("=========================================================================")
        print(f"[¡ATENCIÓN!] No se encontró la imagen '{IMAGE_FILENAME}' en:")
        print(f" -> {image_path}")
        print("\nPASOS PARA CONFIGURAR EL MÉTODO VISUAL (MÉTODO 2):")
        print("1. Abre la página https://margex.com/app/rewards-hub en tu navegador.")
        print("2. Toma una captura de pantalla del recuadro o botón que dice 'Claim' (o 'Reclamar').")
        print(f"3. Guarda esa pequeña imagen recortada con el nombre exacto: {IMAGE_FILENAME}")
        print("   en la carpeta: d:\\0proyectos\\claim.png")
        print("=========================================================================\n")
    else:
        print(f"[BÚSQUEDA VISUAL] Escaneando la pantalla para localizar '{IMAGE_FILENAME}'...")
        try:
            # Intenta encontrar las coordenadas del centro del botón en la pantalla
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location:
                print(f"[ÉXITO] ¡Botón 'Claim' detectado visualmente en pantalla (X: {location.x}, Y: {location.y})!")
                pyautogui.moveTo(location.x, location.y, duration=0.5)
                pyautogui.click()
                time.sleep(0.3)
                pyautogui.click()
                print("[INFO] Clic efectuado sobre las coordenadas exactas del botón.")
            else:
                print("[ALERTA] La imagen 'claim.png' no se encontró en la pantalla actual.")
        except Exception as e:
            # Intentar búsqueda estándar sin parámetro de confianza (por si no está opencv)
            try:
                location = pyautogui.locateCenterOnScreen(image_path)
                if location:
                    print(f"[ÉXITO] Botón localizado en pantalla (X: {location.x}, Y: {location.y})!")
                    pyautogui.click(location.x, location.y)
                    print("[INFO] Clic efectuado.")
                else:
                    print("[ALERTA] No se encontró coincidencia visual en pantalla.")
            except Exception as ex:
                print(f"[ERROR] Error al buscar la imagen: {ex}")
                print("Se recomienda instalar opencv-python: pip install opencv-python pillow")

    print(f"[ESPERA] Esperando {WAIT_AFTER_CLAIM} segundos antes de cerrar el navegador...")
    time.sleep(WAIT_AFTER_CLAIM)
    
    print("[CIERRE] Cerrando la ventana completa del navegador (Alt + F4)...")
    pyautogui.hotkey('alt', 'f4')
    print("[INFO] Navegador cerrado correctamente.")


def main():
    print("==========================================================")
    print(" Bot de Reclamo Margex (Reconocimiento Visual de Imagen)")
    print("==========================================================")
    print("Requisitos: pip install pyautogui pillow opencv-python\n")
    print("El proceso se ejecutará inmediatamente y se repetirá cada 6 horas.\n")
    
    pyautogui.FAILSAFE = True

    while True:
        process_claim()
        next_run = datetime.datetime.now() + datetime.timedelta(seconds=INTERVAL_SECONDS)
        print(f"\n[INFO] Próxima ejecución programada para: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Esperando 6 horas ({INTERVAL_SECONDS} segundos)...\n")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
