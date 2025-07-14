# Lightning Detector - Detektor Piorunów

System wykrywania piorunów oparty na czujniku AS3935 z wyświetlaczem OLED dla mikrokontrolerów MicroPython.

## Opis projektu

Projekt implementuje detektor piorunów wykorzystujący czujnik AS3935 komunikujący się przez interfejs SPI oraz wyświetlacz OLED 128x64 przez I2C. System wykrywa wyładowania atmosferyczne, określa ich odległość i wyświetla informacje na ekranie.

## Funkcjonalności

- **Wykrywanie piorunów** z określeniem odległości (do 63km)
- **Filtrowanie zakłóceń** - rozróżnienie między piorunami a szumem elektromagnetycznym
- **Wyświetlanie na OLED** - ostatnie 5 wykryć piorunów (3 widoczne na ekranie)
- **Logowanie w konsoli** - wszystkie zdarzenia (pioruny, szum, zakłócenia)
- **Obsługa przerwań** - szybka reakcja na zdarzenia z czujnika
- **Kalibracja automatyczna** - dostrojenie czujnika do warunków wewnętrznych

## Sprzęt

### Wymagane komponenty:
- Mikrokontroler z MicroPython (np. Raspberry Pi Pico)
- Czujnik piorunów AS3935
- Wyświetlacz OLED 128x64 (SSD1306)
- Przewody połączeniowe

### Schemat połączeń:

#### OLED Display (I2C):
- SDA → Pin 8
- SCL → Pin 9
- VCC → 3.3V
- GND → GND

#### AS3935 Lightning Sensor (SPI):
- SCK → Pin 4
- MOSI → Pin 6
- MISO → Pin 5
- CS → Pin 7
- IRQ → Pin 0
- VCC → 3.3V
- GND → GND

## Instalacja

1. Sklonuj repozytorium: