/**
   BasicHTTPClient.ino

    Created on: 24.05.2015

*/

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#define USE_SERIAL Serial

ESP8266WiFiMulti WiFiMulti;

enum RequestOperation {
  GET,
  POST
};

void HttpRequest(const char *url, enum RequestOperation operation, const char *payload) {
  HTTPClient http;

  USE_SERIAL.print("[HTTP] begin...\n");
  // configure traged server and url
  http.begin(url); //HTTP

  USE_SERIAL.print("[HTTP] Requesting...\n");
  // start connection and send HTTP header
  int httpCode = -1;
  switch (operation) {
    case GET:
      httpCode = http.GET();
      break;
    case POST:
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      httpCode = http.POST(payload);
      break;
  }

  // httpCode will be negative on error
  if (httpCode > 0) {
    // HTTP header has been send and Server response header has been handled
    USE_SERIAL.printf("[HTTP] code: %d\n", httpCode);

    // file found at server
    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      USE_SERIAL.println(payload);
    }
  } else {
    USE_SERIAL.printf("[HTTP] Request failed, error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();

}

void setup() {
  USE_SERIAL.begin(115200);
  WiFiMulti.addAP("WIFI SSID", "WIFI PASSWORD");
  int delayed = 0;
  while (WiFiMulti.run() != WL_CONNECTED) {
    delay(1000);
    delayed += 1;
    if (delayed > 15) {
      Serial.println("Connection timeout!");
      delay(600000);
    }
  }
  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // main loop to read sensor value

  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {
    int mq135 = analogRead(0);
    Serial.print("MQ135 = ");
    Serial.println(mq135);
    char payload[100] = {0};
    sprintf(payload, "air=%d", mq135);
    HttpRequest("http://192.168.21.192/kitchen/api/v1/air", POST, payload);
    delay(120000);
  }
}

