class LDR {
  public:
    // construtor que aceita o pino analógico como parâmetro
    LDR(int pin, int adcResolution, float refVoltage) {
      sensorPin = pin; // configura o pino analógico
      resolution = adcResolution;
      voltage = refVoltage;
      threshold = (1 << resolution) / 2; // limite para distinguir entre preto e branco
      gndPin = 0; // configura o pino GND (padrão)
    }

    // método para ler o valor do sensor e converter para qualitativo
    int readSensor() {
      int sensorValue = analogRead(sensorPin); // lê o valor do pino analógico (0 a 1023)
      if (sensorValue < threshold) {
        return 0; // cor preta
      } else {
        return 1; // cor branca
      }
    }

  private:
    int sensorPin; // pino analógico do sensor
    int gndPin; // pino GND (padrão)
    int resolution; // resolução ADC (bits)
    int voltage; // tensão de referência
    int threshold; // limite para distinguir entre preto e branco
};

// instancia o sensor LDR esquerdo no pino A0
LDR sensor_esquerdo(A0, 10, 5.0);

void setup() {
  Serial.begin(9600); // inicia a comunicação serial a 9600 bps - ARDUINO UNO (?)
}

void loop() {
  int result = sensor_esquerdo.readSensor(); // lê o valor qualitativo do sensor
  Serial.println(result); // imprime o resultado (0 ou 1) no monitor serial
  delay(300); // espera 0,3 segundos antes de ler novamente
}
