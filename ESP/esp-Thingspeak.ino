#include <Wire.h>
#include <LCD_I2C.h>
#include "ESP_Wahaj.h"
#include "ThingSpeak.h"
#include <Wire.h>
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#define REPORTING_PERIOD_MS     1000
PulseOximeter pox;
int gas,piezo,flex,mov;
uint32_t tsLastReport = 0;
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
Adafruit_MPU6050 mpu;
// Declare variables for storing previous readings
float prevX = 0, prevY = 0, prevZ = 0;
// Initialize change counters
int ax = 0, ay = 0, az = 0;



void detectChange(float currentX, float currentY, float currentZ) {
    // Check if the x value has changed
    if (currentX > prevX+1 || currentX < prevX-1) {
        ax++;          // Increment x change counter
        prevX = currentX; // Update previous x value
    }

    // Check if the y value has changed
    if (currentY > prevY+1 || currentY < prevY-1) {
        ay++;          // Increment y change counter
        prevY = currentY; // Update previous y value
    }

    // Check if the z value has changed
    if (currentZ > prevZ+1 || currentZ < prevZ-1) {
        az++;          // Increment z change counter
        prevZ = currentZ; // Update previous z value
    }
}
// Callback (registered below) fired when a pulse is detected
void onBeatDetected()
{
    Serial.println("Beat!");
}

#include <SimpleDHT.h>
#include <Adafruit_MCP3008.h>
int sweat=0;
Adafruit_MCP3008 adc;

int pinDHT11 = D0;
SimpleDHT11 dht11(pinDHT11);
LCD_I2C lcd(0x27);
int pwm = 0;
float te,bpm,spo2,ph,ppg;
#include <Wire.h>

#define REPORTING_PERIOD_MS     1000
void setup() {
  pinMode(A0,INPUT);
  adc.begin();
  Serial.begin(115200);
  start("Project","12345678");
  lcd.begin();
  lcd.backlight();
    if (!pox.begin()) {
        Serial.println("FAILED");
        for(;;);
    } else {
        Serial.println("SUCCESS");
    }
mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

    // The default current for the IR LED is 50mA and it could be changed
    //   by uncommenting the following line. Check MAX30100_Registers.h for all the
    //   available options.
    // pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
ThingSpeak.begin(client);
    // Register a callback for the beat detection
    pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop() {
  // Make sure to call update as fast as possible
    pox.update();

    // Asynchronously dump heart rate and oxidation levels to the serial
    // For both, a value of 0 means "invalid"
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        Serial.print("Heart rate:");
        bpm=pox.getHeartRate();
        Serial.print(bpm);
        Serial.print("bpm / SpO2:");
        spo2=pox.getSpO2();
        Serial.print(spo2);
        Serial.println("%");
if(bpm>50 && spo2>90)
{   
      // read without samples.
 byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.println(err);delay(1000);
    return;
  }
  te=temperature;
  Serial.print(te); Serial.print(" *C, "); 
  //Serial.print(hu); Serial.println(" H");
  
   float currentX =0; /* read from accelerometer */;
    float currentY =0; /* read from accelerometer */;
    float currentZ =0;
 for(int yu=0;yu<100;yu++)
 {
 int pi=adc.readADC(0);
  ppg=ppg+pi;
   sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
   currentX =a.acceleration.x; /* read from accelerometer */;
   currentY =a.acceleration.y; /* read from accelerometer */;
    currentZ =a.acceleration.z; /* read from accelerometer */;

    // Call the function to detect changes
    detectChange(currentX, currentY, currentZ);
  delay(20);
  }
  mov=ax+ay+az;
gas=adc.readADC(1);
piezo=adc.readADC(2);
flex=adc.readADC(3);

// digitalWrite(D4,HIGH);
//digitalWrite(D3,HIGH);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("T: ");
  lcd.print(te, 2); // Print with 2 decimal places
  lcd.print(" C");

  lcd.setCursor(0, 1);
  lcd.print("PPG: ");
  lcd.print(ppg, 2); // Print with 2 decimal places
  lcd.print(" %");

  delay(2000); // Display for 2 seconds

lcd.clear();
 // Print with 2 decimal places
   lcd.setCursor(0, 0);
  lcd.print("BPM:");
  lcd.print(bpm);
 lcd.print(",");
  lcd.print("S:");
  lcd.print(spo2); // Print with 2 decimal places
  lcd.print(" %");
  lcd.setCursor(0, 1);
  lcd.print("F:");
  lcd.print(flex);
 lcd.print(",");
  lcd.print("G:");
  lcd.print(gas); // Print with 2 decimal places
  lcd.print(" %");
  delay(2000);
lcd.clear();
 // Print with 2 decimal places
   lcd.setCursor(0, 0);
  lcd.print("MOV:");
  lcd.print(mov);
 lcd.print(",");
  lcd.print("P:");
  lcd.print(piezo); // Print with 2 decimal places

  delay(2000);
   ThingSpeak.setField(1, bpm);
  ThingSpeak.setField(2, spo2);
  ThingSpeak.setField(3, te);
   ThingSpeak.setField(4, ppg);
  ThingSpeak.setField(5, mov);
  ThingSpeak.setField(6, piezo);
   ThingSpeak.setField(7, flex);
  ThingSpeak.setField(8, gas);
  // write to the ThingSpeak channel
  int x = ThingSpeak.writeFields(565129,"3J6LJDI7PCAU2IVL");

  ppg=0;
  ax=0,ay=0,az=0;
   }      
      //  analogWrite(PWM_PIN, pwm);
   
       
      
     tsLastReport = millis(); 
    }
}
  

