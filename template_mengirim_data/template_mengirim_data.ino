#include <WiFi.h> // Untuk ESP32 atau ESP8266 gunakan <ESP8266WiFi.h>
#include <PubSubClient.h>

// Ganti dengan kredensial WiFi Anda
const char* ssid = "SSID_WIFI_ANDA";
const char* password = "PASSWORD_WIFI_ANDA";

// Ganti dengan alamat IP broker MQTT Anda (bisa localhost jika di komputer yang sama)
const char* mqtt_server = "192.168.100.110"; 

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  
  // Hubungkan ke WiFi
  setup_wifi();
  
  // Atur server MQTT
  client.setServer(mqtt_server, 1883);
  
  // Coba hubungkan ke MQTT
  while (!client.connected()) {
    Serial.print("Menghubungkan ke MQTT...");
    
    if (client.connect("ArduinoClient")) {
      Serial.println("Terhubung");
      
      // Kirim pesan setelah terhubung
      client.publish("test/ahnaf", "Hello from Arduino");
    } else {
      Serial.print("gagal, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void loop() {
  // Tetap terhubung ke MQTT
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Contoh mengirim data secara berkala
  static unsigned long lastMsg = 0;
  unsigned long now = millis();
  if (now - lastMsg > 2000) { // setiap 2 detik
    lastMsg = now;
    String msg = "Data waktu: " + String(now);
    client.publish("test/ahnaf", msg.c_str());
  }
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Menghubungkan ke ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi terhubung");
  Serial.println("Alamat IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Coba hubungkan lagi jika terputus
  while (!client.connected()) {
    Serial.print("Coba hubungkan kembali ke MQTT...");
    if (client.connect("ArduinoClient")) {
      Serial.println("Terhubung");
    } else {
      Serial.print("gagal, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}
