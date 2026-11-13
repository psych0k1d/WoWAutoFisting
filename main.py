import pydirectinput
import random
import pyautogui
import time
import numpy as np
import soundcard as sc
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def human_press(key):
    # Случайное удержание клавиши пальцем (от 50 до 120 мс)
    hold_time = random.uniform(0.04, 0.12) 
    pydirectinput.keyDown(key)
    time.sleep(hold_time)
    pydirectinput.keyUp(key)

print("=== НАСТРОЙКА ГРОМКОСТИ ИГРЫ ===")
try:
    master_vol = float(input("Введи 'Общую громкость' из игры в % (например, 1 или 100): ")) / 100.0
    sfx_vol = float(input("Введи громкость 'Эффектов' из игры в % (например, 100): ")) / 100.0
except ValueError:
    print("Ошибка ввода. Установлены значения по умолчанию: Общая 1%, Эффекты 100%")
    master_vol = 0.01
    sfx_vol = 1.0

# Твой базовый порог
BASE_THRESHOLD = 0.020  

VOLUME_THRESHOLD = BASE_THRESHOLD * master_vol * sfx_vol

if VOLUME_THRESHOLD < 0.0005:
    VOLUME_THRESHOLD = 0.0005

TARGET_SR = 44100
CHUNK_SAMPLES = int(TARGET_SR * 0.08)

default_speaker = sc.default_speaker()
loopback_microphone = sc.get_microphone(default_speaker.name, include_loopback=True)

print(f"\n[+] Бот запущен на устройстве: {default_speaker.name}")
print(f"[+] Рассчитанный порог: {VOLUME_THRESHOLD:.5f}")
print("[+] Держи курсор на поплавке. Нажми Ctrl+C для выхода.\n")

last_catch_time = 0

try:
    with loopback_microphone.recorder(samplerate=TARGET_SR, channels=1) as recorder:
        while True:
            data = recorder.record(numframes=CHUNK_SAMPLES)
            chunk = data.flatten()
            
            current_rms = np.sqrt(np.mean(chunk**2))
            current_time = time.time()
            
            print(f"Громкость игры: {current_rms:.5f} | Ждем пробития: {VOLUME_THRESHOLD:.5f}", end='\r')
            
            if current_rms > VOLUME_THRESHOLD:
                # Ограничение в 3.5 секунды
                            if current_time - last_catch_time > 3.5:
                                print(f"\n[!] ПОКЛЁВКА! (Громкость {current_rms:.5f} пробила порог {VOLUME_THRESHOLD:.5f})")

                                # 1. Микро-пауза перед кликом (имитация реакции)
                                time.sleep(random.uniform(0.35, 0.85))

                                # 2. Клик по поплавку (подсекаем и открываем лут)
                                human_press('=')
                                time.sleep(random.uniform(1.22, 2.12)) 
                                pydirectinput.mouseDown(button='right')
                                time.sleep(random.uniform(0.06, 0.12)) 
                                pydirectinput.mouseUp(button='right')
                                print("[*] Клик выполнен (Подсечка)")

                                # 3. УВЕЛИЧЕННАЯ ПАУЗА НА ЛУТ (от 2.2 до 3.0 секунд)
                                # Этого времени гарантированно хватит, чтобы игра перенесла рыбу в сумку
                                time.sleep(random.uniform(2.20, 3.00))

                                # 4. ПЕРВОЕ НАЖАТИЕ '=' — Достаем пустую удочку
                                human_press('=')
                                print("кинул удочку")
                                time.sleep(1)

                                last_catch_time = time.time()


except KeyboardInterrupt:
    print("\nСкрипт успешно остановлен.")
except Exception as e:
    print(f"\nКритическая ошибка: {e}")
