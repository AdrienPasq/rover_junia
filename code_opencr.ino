#include <DynamixelWorkbench.h>
#include <DHT.h>

// Définition des pins et paramètres
#define DHT_PIN 7          // Pin où le DHT11 est connecté
#define DHT_TYPE DHT11     // Type de capteur DHT
DHT dht(DHT_PIN, DHT_TYPE);

#define LEFT_MOTOR_ID 1    // ID du moteur gauche
#define RIGHT_MOTOR_ID 2   // ID du moteur droit
#define BAUDRATE 57600     // Vitesse de communication

DynamixelWorkbench dxl;

int motorSpeed = 200;

void setupMotors() {
  dxl.init("/dev/ttyUSB0", BAUDRATE);
  dxl.ping(LEFT_MOTOR_ID);
  dxl.ping(RIGHT_MOTOR_ID);
  dxl.torque(LEFT_MOTOR_ID, true);
  dxl.torque(RIGHT_MOTOR_ID, true);
}

void setup() {
  Serial.begin(115200);  // Port série pour communication avec le PC/Raspberry Pi
  dht.begin();           // Initialiser le capteur DHT11
  setupMotors();         // Configurer les moteurs
  Serial.println("OpenCR prêt");
}

void stopMotors() {
  dxl.goalVelocity(LEFT_MOTOR_ID, 0);
  dxl.goalVelocity(RIGHT_MOTOR_ID, 0);
}

// Fonction pour interpréter les commandes reçues
void executeCommand(String command) {
  if (command == "A") { // Avancer
    dxl.goalVelocity(LEFT_MOTOR_ID, motorSpeed);
    dxl.goalVelocity(RIGHT_MOTOR_ID, motorSpeed);
  } else if (command == "R") { // Reculer
    dxl.goalVelocity(LEFT_MOTOR_ID, -motorSpeed);
    dxl.goalVelocity(RIGHT_MOTOR_ID, -motorSpeed);
  } else if (command == "G") { // Tourner à gauche
    dxl.goalVelocity(LEFT_MOTOR_ID, -motorSpeed);
    dxl.goalVelocity(RIGHT_MOTOR_ID, motorSpeed);
  } else if (command == "D") { // Tourner à droite
    dxl.goalVelocity(LEFT_MOTOR_ID, motorSpeed);
    dxl.goalVelocity(RIGHT_MOTOR_ID, -motorSpeed);
  } else if (command == "AG") { // Avancer en tournant à gauche
    dxl.goalVelocity(LEFT_MOTOR_ID, motorSpeed / 2);
    dxl.goalVelocity(RIGHT_MOTOR_ID, motorSpeed);
  } else if (command == "AD") { // Avancer en tournant à droite
    dxl.goalVelocity(LEFT_MOTOR_ID, motorSpeed);
    dxl.goalVelocity(RIGHT_MOTOR_ID, motorSpeed / 2);
  } else if (command == "RG") { // Reculer en tournant à gauche
    dxl.goalVelocity(LEFT_MOTOR_ID, -motorSpeed / 2);
    dxl.goalVelocity(RIGHT_MOTOR_ID, -motorSpeed);
  } else if (command == "RD") { // Reculer en tournant à droite
    dxl.goalVelocity(LEFT_MOTOR_ID, -motorSpeed);
    dxl.goalVelocity(RIGHT_MOTOR_ID, -motorSpeed / 2);
  } else if (command == "M") {  // Lire la température et l'humidité
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    if (isnan(temp) || isnan(hum)) {
      Serial.println("Erreur lecture capteur");
    } else {
      String sensorData = String(temp, 2) + "," + String(hum, 2);
      Serial.println(sensorData);
    }
    delay(250);
    stopMotors();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    executeCommand(command);
  }
}
