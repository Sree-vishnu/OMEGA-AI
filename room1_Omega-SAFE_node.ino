#include <ESP8266WiFi.h>
#include "DHT.h"
#define DHTTYPE DHT11
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#define LED_PIN 12
#define WLAN_SSID "FBI_van"    
#define WLAN_PASS     "pks12345"  
#define MQTT_SERVER  "192.168.43.114"
#define MQTT_PORT  1883
#define DHTPIN 4
#define MQTT_USERNAME   ""               // Set to any username for the MQTT server (default none/empty).
#define MQTT_KEY   ""               // MQTT user password (default none/empty).

#define VIB_PIN 5

WiFiClient client;

Adafruit_MQTT_Client mqtt(&client, MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_KEY);

Adafruit_MQTT_Subscribe esp8266_led = Adafruit_MQTT_Subscribe(&mqtt, "leds");
Adafruit_MQTT_Publish room_1 = Adafruit_MQTT_Publish(&mqtt, MQTT_USERNAME "room_one");
//Adafruit_MQTT_Publish room_2 = Adafruit_MQTT_Publish(&mqtt, MQTT_USERNAME "/room_two/pi");


DHT dht(DHTPIN, DHTTYPE);


void setup() {
  Serial.begin(115200);
  delay(10);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  dht.begin();

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");
  Serial.println("IP address: "); 
  Serial.println(WiFi.localIP());

  mqtt.subscribe(&esp8266_led);


  pinMode(VIB_PIN, INPUT);

}

void loop() {

  MQTT_connect();
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription())) {
    // Check if the update is for the /leds/esp8266 topic.
    if (subscription == &esp8266_led) {
      // Grab the message data and print it out.
      char* message = (char*)esp8266_led.lastread;
      Serial.print("/room_one/leds got: ");
      Serial.println(message);
      // Check if the message was ON, OFF, or TOGGLE.
      if (strncmp(message, "ON", 2) == 0) {
        // Turn the LED on.
        digitalWrite(LED_PIN, HIGH);
      }
      else if (strncmp(message, "OFF", 3) == 0) {
        // Turn the LED off.
        digitalWrite(LED_PIN, LOW);
      }
      else if (strncmp(message, "TOGGLE", 6) == 0) {
        // Toggle the LED.
        digitalWrite(LED_PIN, !digitalRead(LED_PIN));
      }
    }
}

 delay(1000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  int h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  int t = dht.readTemperature();
  int co = analogRead(A0);
  //Serial.println(co);

//Seismic readings
 long l=pulseIn (VIB_PIN, HIGH);
  delay(50);
 // Serial.print("measurment = ");
  Serial.println(l);
  if (l > 1000){
    Serial.println("ALERT");
  }
  else{
    Serial.println("SAFE"); 
  }
 
 
 
 if((h !=2147483647)&&(t !=2147483647))
 {
  String payload ;
  payload += t;
  payload += ":";
  payload += h;
  payload += ":";
  payload += (co-200);
  payload += ":";
  payload += l;
// Serial.print(h);
// Serial.print(",");
// Serial.println(t);
Serial.println(payload);
room_1.publish((char*) payload.c_str());
// humidity.publish(h);
// temperature.publish(t);
 }
 delay(1000);
}
void MQTT_connect() {
  int8_t ret;
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { 
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);
       retries--;
       if (retries == 0) {
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
}


