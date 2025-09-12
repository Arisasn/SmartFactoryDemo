# Smart Factory AGV Network

A scalable **factory automation system** demonstrating two Autonomous Guided Vehicles (AGVs), one physical and one simulated.  
Designed to mirror **Industry 4.0 concepts** like those used in modern smart manufacturing (e.g., Foxconn).

## System Architecture
- **Pi 5 Hub**: Runs MQTT broker and control dashboard.
- **Pico W Robot**: Wi-Fi controlled robot with line following and obstacle detection.
- **Simulated Robot**: Software-only process for testing scalability.

## Current Hardware (Phase 1)
- 1x Raspberry Pi Pico W
- 1x UPS HAT with 18650 Li-ion battery
- 1x L298N motor driver
- 2x DC motors (TT Gear Motors)
- Line sensor (TCRT5000)
- Ultrasonic distance sensor (HC-SR04)
- OLED I2C display
- EMOZNY chassis kit

## Goals
- Live dashboard with telemetry from multiple robots.
- Autonomous line-following and obstacle detection.
- Demo video showing real-world robot and virtual robots working together.

## Folder Structure
