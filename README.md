# 🩺Real Time Disease Diagnosis And Wound Analysis
## 📝Overview
- The advancement of smart healthcare systems has led to innovative solutions for real-time patient monitoring and disease detection. This project introduces an IoT-based Health Monitoring System designed to track vital health parameters and detect potential diseases using multiple biosensors and machine learning techniques.
- The system integrates PPG, DHT11, gas sensors, piezoelectric sensors, flex sensors, MAX30100, and an ESP32 camera module to collect physiological data such as heart rate, temperature, oxygen saturation, sweat analysis, bone health conditions and detects wound.
- The collected data is processed using NodeMCU, MCP3008, and a Buck Converter for efficient sensor interfacing and power management. The system employs machine learning algorithms, including K-Nearest Neighbors (KNN) and Convolutional Neural Networks (CNN), for accurate disease classification and wound detection. TensorFlow’s Adam optimizer enhances the model’s training efficiency, improving detection accuracy.
- The processed health data is then transmitted to a web-based interface with cloud connectivity (ThingSpeak) for real-time remote monitoring, enabling healthcare providers and patients to access insights into health conditions.
- This smart healthcare solution can detect 10 different diseases, ensuring early intervention and preventive care. The integration of IoT, machine learning, and cloud computing in this system makes it an efficient, cost-effective, and scalable solution for remote health monitoring.
- The proposed system aims to enhance healthcare accessibility, improve early disease detection, and provide real-time health insights, contributing to modern telemedicine and patient-centric care.

## 🛠️📟 Hardware Required

| Component            | Quantity |
|----------------------|----------|
| ESP8266 Development Board | 1        |
| Buck Converter  | 1     |
| PPG Sensor (Photoplethysmography)  | 1      |
| pH Sensor    |  1    | 
| IR Transmitter & Receiver  |   1     |
| MPU6050 (Gyro + Accelerometer) | 1        |
| Temperature Sensor   | 1        |
| MAX30102 (Heart rate + SPO2) | 1    |
| ADC Converter  | 1      |
| Wires         | As needed |
| Switch           | 1        |
| Power Supply (e.g. USB Cable) | 1        | 

## 📟Software Used
1) Programming : python, Embedded C
2) Thonny IDE
3) Thingspeak
4) Visual Studio Code

## Machine Learning Algorithm
1) CNN (Convolutional Neural Network) - Deep Learning 
    - used for Wound detection by using training image and mask.
2) KNN (K-Nearest Neighbor)
    - Used for Disease Prediction
3) U-net
    - deep learning algorithm used for semantic segmentation.
   

   
