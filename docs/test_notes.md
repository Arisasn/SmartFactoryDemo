## 2025-09-11 - Raw Ultrasonic Sensor Test
- Ran direct pin test on PORT_3 (D8/D9).
- Both cars consistently output 400 cm → sensor or wiring issue likely.
- Next step: swap to PORT_4 test and different RJ25 cable.
  
## 2025-09-11 - Ultrasonic Port/Pin Scanner
- Added scanner that tries PORT_3 (D6/D7) and PORT_4 (D10/D11) in both TRIG/ECHO orders.
- Issue persist. 

## 2025-09-12 - Migrate from Aurduino UNO to makeblock ide
- Issues persist so I will migrate to makeblcok ide to program makeblock car
