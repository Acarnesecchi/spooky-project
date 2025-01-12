#include "Arduino.h"
#include <60ghzbreathheart.h>
#include <SoftwareSerial.h>

// Define pins for SoftwareSerial
#define RX_Pin A1
#define TX_Pin A2

unsigned long previousMillis = 0;
const long interval = 200;


SoftwareSerial mySerial = SoftwareSerial(RX_Pin, TX_Pin);

// Initialize radar instance
BreathHeart_60GHz radar = BreathHeart_60GHz(&mySerial);

void setup() {
  Serial.begin(115200);
  mySerial.begin(115200);

  Serial.println("Ready");

  // Set radar to real-time transmission mode
  radar.ModeSelect_fuc(1);
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    // Your sensor data handling code

    radar.Breath_Heart();
    // Process breath and heart data
    if (radar.sensor_report != 0x00) {
      switch (radar.sensor_report) {
        case HEARTRATEVAL:
          Serial.print("MQTT:breathheart/heart_rate:");
          Serial.println(radar.heart_rate);
          break;
        case BREATHVAL:
          Serial.print("MQTT:breathheart/breath_rate:");
          Serial.println(radar.breath_rate);
          break;
        case BREATHNONE:
          Serial.println("MQTT:breathheart/status:0"); // No breathing detected.
          break;
        case BREATHRAPID:
          Serial.println("MQTT:breathheart/status:1"); // Breathing too fast.
          break;
        case BREATHSLOW:
          Serial.println("MQTT:breathheart/status:2"); // Breathing too slow.
          break;
        }
      }

    radar.HumanExis_Func(); // Read human presence and motion data

    // Process human presence and motion data
    if (radar.sensor_report != 0x00) {
      switch (radar.sensor_report) {
        case NOONE:
          Serial.println("MQTT:existance/status:0"); // Nobody detected
          break;
        case SOMEONE:
          Serial.println("MQTT:existance/status:1"); // Person detected
          break;
        case MOVE:
          Serial.println("MQTT:existance/status:2"); // Motion detected
          break;
        case STATION:
          Serial.println("MQTT:existance/status:3"); // Person stationary
          break;
        case DISVAL:
          Serial.print("MQTT:existance/distance:");
          Serial.println(radar.distance);
          
          break;
        case DIREVAL:
          Serial.print("MQTT:existance/direction: ");
          Serial.print(radar.Dir_x);
          Serial.print(" ");
          Serial.print(radar.Dir_y);
          Serial.print(" ");
          Serial.print(radar.Dir_z);
          break;
        }
      }
  }

}
