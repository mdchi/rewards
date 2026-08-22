import os
import time
import datetime
from zoneinfo import ZoneInfo
import webbrowser
import pyautogui

URL = "https://margex.com/app/rewards-hub"
WAIT_AFTER_OPEN = 15            # Segundos para esperar a que cargue la página
WAIT_AFTER_CLAIM = 15           # Segundos a esperar antes de cerrar la ventana del navegador

IMAGE_FILENAMES = ["claim.png", "claimdorado.png"]
TZ_BSAS = ZoneInfo("America/Argentina/Buenos_Aires")
EXITO_TAG = "[\033[42;1;97m ÉXITO \033[0m]"
ERROR_TAG = "[\033[41;1;97m ERROR \033[0m]"


def get_next_run_wait_seconds(clicked: bool):
    now = datetime.datetime.now(TZ_BSAS)
    if clicked:
        # Próxima ejecución a las 21:15 hs horario Buenos Aires
        target = now.replace(hour=21, minute=15, second=0, microsecond=0)
        if now >= target:
            target += datetime.timedelta(days=1)
        wait_seconds = int((target - now).total_seconds())
        status_msg = "Botón detectado."
    else:
        # No se encontró el botón, reintentar en 6 horas
        wait_seconds = 6 * 3600
        target = now + datetime.timedelta(seconds=wait_seconds)
        status_msg = "No se encontró ningún botón."
    
    return wait_seconds, target, status_msg


def process_claim() -> bool:
    now_str = datetime.datetime.now(TZ_BSAS).strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n[{now_str}] Abriendo la página en el navegador predeterminado del sistema...")
    
    # Abre la URL en el navegador predeterminado (Chrome, Edge, Firefox, etc.)
    webbrowser.open(URL)
    
    print(f"[ESPERA] Esperando {WAIT_AFTER_OPEN} segundos a que la página cargue completamente...")
    time.sleep(WAIT_AFTER_OPEN)
    
    images_found_on_disk = [img for img in IMAGE_FILENAMES if os.path.exists(os.path.join(os.getcwd(), img))]
    clicked = False
    
    if not images_found_on_disk:
        print("=========================================================================")
        print(f"[¡ATENCIÓN!] No se encontró ninguna de las imágenes {IMAGE_FILENAMES} en:")
        print(f" -> {os.getcwd()}")
        print("\nPASOS PARA CONFIGURAR EL MÉTODO VISUAL:")
        print("1. Abre la página https://margex.com/app/rewards-hub en tu navegador.")
        print("2. Toma una captura de pantalla del recuadro o botón que dice 'Claim' (o 'Reclamar').")
        print(f"3. Guarda las imágenes recortadas ('claim.png', 'claimdorado.png')")
        print(f"   en la carpeta: {os.getcwd()}")
        print("=========================================================================\n")
    else:
        for img_name in IMAGE_FILENAMES:
            image_path = os.path.join(os.getcwd(), img_name)
            if not os.path.exists(image_path):
                print(f"[INFO] La imagen '{img_name}' no existe en el disco. Omitiendo...")
                continue
            
            print(f"[BÚSQUEDA VISUAL] Escaneando la pantalla para localizar '{img_name}'...")
            try:
                # Intenta encontrar las coordenadas del centro del botón en la pantalla
                location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                if location:
                    print(f"{EXITO_TAG} ¡Botón detectado visualmente con '{img_name}' en pantalla (X: {location.x}, Y: {location.y})!")
                    pyautogui.moveTo(location.x, location.y, duration=0.5)
                    pyautogui.click()
                    time.sleep(0.3)
                    pyautogui.click()
                    print("[INFO] Clic efectuado sobre las coordenadas exactas del botón.")
                    clicked = True
                    break
                else:
                    print(f"[ALERTA] La imagen '{img_name}' no se encontró en la pantalla actual.")
            except Exception:
                # Intentar búsqueda estándar sin parámetro de confianza (por si no está opencv)
                try:
                    location = pyautogui.locateCenterOnScreen(image_path)
                    if location:
                        print(f"{EXITO_TAG} ¡Botón localizado con '{img_name}' en pantalla (X: {location.x}, Y: {location.y})!")
                        pyautogui.click(location.x, location.y)
                        print("[INFO] Clic efectuado.")
                        clicked = True
                        break
                    else:
                        print(f"[ALERTA] No se encontró coincidencia visual en pantalla para '{img_name}'.")
                except Exception as ex:
                    print(f"{ERROR_TAG} Error al buscar la imagen '{img_name}': {ex}")
                    print("Se recomienda instalar opencv-python: pip install opencv-python pillow")

        if not clicked:
            print("[ALERTA] Ninguna de las imágenes configuradas fue detectada en la pantalla actual.")

    print(f"[ESPERA] Esperando {WAIT_AFTER_CLAIM} segundos antes de cerrar el navegador...")
    time.sleep(WAIT_AFTER_CLAIM)
    
    print("[CIERRE] Cerrando la ventana completa del navegador (Alt + F4)...")
    pyautogui.hotkey('alt', 'f4')
    print("[INFO] Navegador cerrado correctamente.")
    
    return clicked


def main():
    os.system('')  # Habilita el soporte de colores ANSI en la consola de Windows
    print("==========================================================")
    print(" Bot de Reclamo Margex (Reconocimiento Visual de Imagen)")
    print("==========================================================")
    print("Requisitos: pip install pyautogui pillow opencv-python\n")
    print("Si se detecta un botón: Próxima ejecución a las 21:15 hs (Horario BsAs).")
    print("Si NO se detecta un botón: Próxima ejecución en 6 horas.\n")
    
    pyautogui.FAILSAFE = True

    while True:
        clicked = process_claim()
        wait_seconds, target, status_msg = get_next_run_wait_seconds(clicked)
        target_str = target.strftime('%Y-%m-%d %H:%M:%S')
        
        for remaining in range(wait_seconds, 0, -1):
            hrs, remainder = divmod(remaining, 3600)
            mins, secs = divmod(remainder, 60)
            print(
                f"\r[INFO] {status_msg} Próxima ejecución: {target_str} (Buenos Aires) | Contador regresivo: {hrs:02d}:{mins:02d}:{secs:02d}",
                end="",
                flush=True
            )
            time.sleep(1)
        print("\n")


if __name__ == "__main__":
    main()


