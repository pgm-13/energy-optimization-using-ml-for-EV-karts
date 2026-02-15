# ML-Based Energy Optimization & Driver Performance Analytics for Electric Go-Karts

## Overview
This project presents a data-driven analytics and control system for electric go-karts. It converts raw telemetry data (voltage, current, speed, acceleration) into meaningful performance metrics including:

- Battery Energy Efficiency Score
- Driver Performance Score
- Lap-wise Strategy Suggestions
- Adaptive Throttle Restriction (Prototype)

The system bridges machine learning analytics with embedded hardware to promote sustainable racing without compromising performance.

## Key Features
- Machine learning–based energy efficiency prediction
- Deterministic driver performance scoring
- Independent evaluation of racing performance and sustainability
- Lap-wise telemetry aggregation
- Real-time dashboard visualization
- Embedded throttle restriction prototype using ESP32
- Low-cost and scalable architecture


## System Architecture
Telemetry Sensors → ESP32 → Processing Unit (Laptop / Raspberry Pi) → ML Inference → TFT Display + Throttle Control


## Technologies Used
- Python
- Pandas / NumPy
- Scikit-Learn (Random Forest Regression)
- Streamlit (Dashboard)
- Arduino IDE
- ESP32 Microcontroller
- TFT Display Module


## Applications
- Electric kart racing teams
- EV research laboratories
- Student formula competitions
- Sustainable mobility prototyping


## Future Scope
- Real-time lap prediction
- Full onboard deployment
- Advanced telemetry visualization
- Expanded EV platform integration
