from machine import Pin, I2C, SPI
import ssd1306
import as3935_spi
import time

# --- OLED Display Configuration (I2C) ---
oled_width = 128
oled_height = 64
i2c = I2C(0, scl=Pin(9), sda=Pin(8))

try:
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    print("OLED initialized (I2C).")
except Exception as e:
    print(f"OLED init error: {e}")
    while True:
        time.sleep(1)

# --- AS3935 Lightning Sensor Configuration (SPI) ---
spi = SPI(1, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(4), mosi=Pin(6), miso=Pin(5))

as3935_cs_pin = Pin(7, Pin.OUT)
as3935_int_pin = Pin(0, Pin.IN)

try:
    lightning_sensor = as3935_spi.AS3935_SPI(spi, as3935_cs_pin, as3935_int_pin)
    lightning_sensor.set_indoors()
    lightning_sensor.calibrate_rco()
    print("AS3935 sensor initialized (SPI).")
except Exception as e:
    print(f"AS3935 SPI init error: {e}")
    while True:
        time.sleep(1)

# --- Data storage for lightning events ---
lightning_events = []  # Tylko pioruny - dla wyświetlacza
last_event_time = 0


# --- Interrupt Handler for AS3935 ---
def int_handler(pin):
    global last_event_time
    current_time = time.ticks_ms()

    if time.ticks_diff(current_time, last_event_time) > 200:
        event_type = lightning_sensor.get_interrupt_reason()
        process_as3935_event(event_type)
        last_event_time = current_time


# --- Function to process AS3935 events ---
def process_as3935_event(event_type):
    global lightning_events

    if event_type == as3935_spi.AS3935_INT_LIGHTNING:  # 0x08 = 8
        # PIORUN - pokazuj w konsoli i na wyświetlaczu
        distance = lightning_sensor.get_distance()
        if distance == 0:
            event_str = "Piorun! Nad glowa"
        elif distance == 63:
            event_str = "Piorun! >63km"
        else:
            event_str = f"Piorun! {distance}km"

        # Dodaj do listy dla wyświetlacza
        lightning_events.insert(0, event_str)
        if len(lightning_events) > 5:
            lightning_events.pop()

        # Pokaż w konsoli
        print(f"[PIORUN] {event_str}")

    elif event_type == as3935_spi.AS3935_INT_NOISE:  # 0x01 = 1
        # SZUM - tylko w konsoli
        print("[SZUM] Wykryto szum elektromagnetyczny")

    elif event_type == as3935_spi.AS3935_INT_DISTURBER:  # 0x04 = 4
        # ZAKŁÓCENIE - tylko w konsoli
        print("[ZAKLOCENIE] Wykryto zaklocenie")

    elif event_type == 0:
        # Brak przerwania lub błąd odczytu
        print("[INFO] Brak aktywnego przerwania")

    elif event_type == 15:  # 0x0F
        # Możliwe zakłócenie lub błąd
        print("[ZAKLOCENIE] Silne zaklocenie (typ 15)")

    else:
        # Inne nieznane typy zdarzeń
        print(f"[NIEZNANE] Typ zdarzenia: {event_type} (0x{event_type:02X})")


# --- Function to update OLED display ---
def update_display():
    oled.fill(0)
    oled.text("Czujnik piorunow", 0, 0)
    oled.text("-" * 16, 0, 20)

    if lightning_events:
        y_pos = 30
        for i, event in enumerate(lightning_events):
            if i >= 3:  # Maksymalnie 3 wydarzenia na ekranie
                break
            oled.text(event[:16], 0, y_pos)
            y_pos += 10
    else:
        oled.text("Brak wykryc", 0, 30)
        oled.text("Czekam...", 0, 40)

    oled.show()


# --- Setup interrupt ---
as3935_int_pin.irq(int_handler, Pin.IRQ_FALLING)
print("AS3935 interrupt handler set.")


# --- Main program loop ---
def main():
    print("Starting lightning detector...")
    print("=== KONSOLA: Wszystkie wykrycia ===")
    print("=== WYŚWIETLACZ: Tylko pioruny ===")
    print("Testuj z mikrofalówką, suszarką, światłem...")
    print()

    update_display()

    while True:
        update_display()
        time.sleep(1)


# Run the program
if __name__ == "__main__":
    main()