from machine import Pin, SPI
import time

# Stałe dla AS3935
AS3935_INT_LIGHTNING = 0x08
AS3935_INT_DISTURBER = 0x04
AS3935_INT_NOISE = 0x01

# Rejestry AS3935
AS3935_REG_INT = 0x03
AS3935_REG_DISTANCE = 0x07
AS3935_REG_TUNE_CAP = 0x08
AS3935_REG_DISP_LCO = 0x08
AS3935_REG_DISP_SRCO = 0x08
AS3935_REG_DISP_TRCO = 0x08
AS3935_REG_TUN_CAP = 0x08
AS3935_REG_CALIB_TRCO = 0x3A
AS3935_REG_CALIB_SRCO = 0x3B


class AS3935_SPI:
    def __init__(self, spi, cs_pin, int_pin=None):
        self.spi = spi
        self.cs = cs_pin
        self.int_pin = int_pin
        self.cs.init(Pin.OUT, value=1)
        if self.int_pin:
            self.int_pin.init(Pin.IN)

        # Podstawowa inicjalizacja
        self.reset()
        time.sleep_ms(2)

    def reset(self):
        """Resetuje AS3935"""
        self.write_register(0x3C, 0x96)
        time.sleep_ms(2)

    def write_register(self, register, value):
        """Zapisuje wartość do rejestru"""
        self.cs(0)
        self.spi.write(bytearray([register & 0x3F, value]))
        self.cs(1)

    def read_register(self, register):
        """Odczytuje wartość z rejestru"""
        self.cs(0)
        self.spi.write(bytearray([0x40 | (register & 0x3F)]))
        result = self.spi.read(1)
        self.cs(1)
        return result[0] if result else 0

    def get_interrupt_reason(self):
        """Pobiera powód przerwania"""
        int_val = self.read_register(AS3935_REG_INT)
        return int_val & 0x0F

    def get_distance(self):
        """Pobiera odległość pioruna"""
        distance = self.read_register(AS3935_REG_DISTANCE)
        return distance & 0x3F

    def set_indoors(self):
        """Ustawia tryb wewnętrzny"""
        reg_val = self.read_register(0x00)
        reg_val |= 0x20
        self.write_register(0x00, reg_val)

    def set_outdoors(self):
        """Ustawia tryb zewnętrzny"""
        reg_val = self.read_register(0x00)
        reg_val &= ~0x20
        self.write_register(0x00, reg_val)

    def calibrate_rco(self):
        """Kalibruje wewnętrzny oscylator RCO"""
        # Wyświetl oscylator TRCO na pin IRQ
        self.write_register(AS3935_REG_DISP_TRCO, 0x80)
        time.sleep_ms(2)

        # Wyłącz wyświetlanie
        self.write_register(AS3935_REG_DISP_TRCO, 0x00)

    def set_noise_floor(self, level):
        """Ustawia poziom szumu (0-7)"""
        if 0 <= level <= 7:
            reg_val = self.read_register(0x01)
            reg_val = (reg_val & 0x8F) | ((level & 0x07) << 4)
            self.write_register(0x01, reg_val)

    def set_watchdog_threshold(self, threshold):
        """Ustawia próg watchdog (0-15)"""
        if 0 <= threshold <= 15:
            reg_val = self.read_register(0x01)
            reg_val = (reg_val & 0xF0) | (threshold & 0x0F)
            self.write_register(0x01, reg_val)

    def set_spike_rejection(self, rejection):
        """Ustawia odrzucanie skoków (0-15)"""
        if 0 <= rejection <= 15:
            reg_val = self.read_register(0x02)
            reg_val = (reg_val & 0xF0) | (rejection & 0x0F)
            self.write_register(0x02, reg_val)

    def clear_statistics(self):
        """Czyści statystyki"""
        reg_val = self.read_register(0x02)
        reg_val |= 0x40
        self.write_register(0x02, reg_val)
        reg_val &= ~0x40
        self.write_register(0x02, reg_val)
