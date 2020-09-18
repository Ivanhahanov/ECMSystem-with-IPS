#include <ESP8266WiFi.h>    //For ESP8266
#include <PubSubClient.h>   //For MQTT
#include <ESP8266mDNS.h>    //For OTA
#include <WiFiUdp.h>        //For OTA
#include <ArduinoOTA.h>     //For OTA

// WIFI configuration
#define wifi_ssid "Explabs-Development"
#define wifi_password "Huttka12"

// MQTT configuration
#define mqtt_server "192.168.31.66"
String mqtt_client_id="OtaClient";
#define mqtt_temp_topic "topic/temp/temp_1"

// Start MQTT client
WiFiClient espClient;
PubSubClient mqtt_client(espClient);

IPAddress ip(192,168,31,230);
IPAddress gateway(192,168,31,1);
IPAddress subnet(255,255,255,0);

void setup_wifi() {
  delay(10);
  Serial.print("Connecting to ");
  Serial.print(wifi_ssid);
  WiFi.begin(wifi_ssid, wifi_password);
  WiFi.config(ip, gateway, subnet);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("OK");
  Serial.print("   IP address: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  Serial.println("\r\nSetting up....");

  setup_wifi();

  Serial.print("Configuring OTA device...");
//  TelnetServer.begin();   //Necesary to make Arduino Software autodetect OTA device
  ArduinoOTA.onStart([]() {Serial.println("OTA starting...");});
  ArduinoOTA.onEnd([]() {Serial.println("OTA update finished!");Serial.println("Rebooting...");});
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {Serial.printf("OTA in progress: %u%%\r\n", (progress / (total / 100)));});
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed");
  });
  ArduinoOTA.begin();
  Serial.println("OK");

  Serial.println("Configuring MQTT server...");
  mqtt_client.setServer(mqtt_server, 1883);
  Serial.printf("   Server IP: %s\r\n",mqtt_server);
  Serial.println("   Cliend Id: "+mqtt_client_id);
  Serial.println("   MQTT configured!");

  Serial.println("Setup complete. Running loop...");
}

void mqtt_reconnect() {
  // Loop until we're reconnected
  while (!mqtt_client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (mqtt_client.connect(mqtt_client_id.c_str())) {
      Serial.println("connected");
      mqtt_client.subscribe("topic/light/light_1");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqtt_client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

long = 0;    //in ms
int wait_ms = 2000;
int count = 0;

void loop() {

  ArduinoOTA.handle();

  if (!mqtt_client.connected()) {
    mqtt_reconnect();
  }
  mqtt_client.loop();
  if (millis() > next_msg) {
      mqtt_client.publish(mqtt_temp_topic, "22", true);
      next_msg = millis() + wait_ms;
    }
  }