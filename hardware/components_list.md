# Smart Factory Demo - Components List

This document tracks all hardware components used for building the Smart Factory AGV system.

---

## 1. Core Electronics
| Component | Qty | Purpose | Link |
|------------|-----|---------|------|
| mini-pc | 1 | Central factory hub, MQTT broker, dashboard | [Amazon](#) |
| Raspberry Pi Pico W | 1 | Wi-Fi controller for robot | [Amazon](#) |
| GeeekPi UPS HAT | 1 | Power supply for Pico W + sensors | [Amazon](#) |
| 18650 Li-ion battery | 1 | UPS HAT power source | [Amazon](#) |
| OLED I2C Display (128x64) | 1 | Robot status screen | [Amazon](#) |

---

## 2. Robotics Hardware
| Component | Qty | Purpose | Link |
|------------|-----|---------|------|
| EMOZNY Robot Chassis Kit | 1 | Base frame for motors + electronics | [Amazon](#) |
| TT Gear Motors (included with chassis) | 2 | Robot drive wheels | – |
| L298N Motor Driver | 1 | Motor control interface for Pico W | [Amazon](#) |
| AA Battery Pack (4×AA) | 1 | Power for motors | – |
| AA Batteries (rechargeable recommended) | 4 | Motor power | – |

---

## 3. Sensors
| Sensor | Qty | Purpose | Link |
|--------|-----|---------|------|
| HC-SR04 Ultrasonic Sensor | 1 | Obstacle detection | [Amazon](#) |
| TCRT5000 Line Sensor | 1 | Line following on track | [Amazon](#) |

---

## 4. Optional / Future Expansion
| Component | Qty | Purpose |
|------------|-----|---------|
| Second Raspberry Pi Pico W | 1 | For second physical robot |
| Additional line sensors | 2 | For more precise navigation |
| Camera module for Pi 5 | 1 | Vision-based tracking |

---

## 5. Total Cost Estimate
| Category | Cost (USD) |
|-----------|------------|
| Core Electronics | ~$50 |
| Robotics Hardware | ~$45 |
| Sensors | ~$12 |
| **Total per robot** | **~$110** |

---

## Notes
- Power systems are **isolated**:
  - **UPS HAT** powers Pico W + sensors + OLED.
  - **AA pack** powers motors through L298N.
- Shared ground between UPS HAT and L298N is required for signal reference.

