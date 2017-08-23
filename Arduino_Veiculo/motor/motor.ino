//Programa : Teste de motor DC12V com motor shield ponte H

#include <NewPing.h> //Sonar
#include <AFMotor.h> //Motor

//Define os pinos para o trigger e echo
#define pino_trigger_frente 26
#define pino_echo_frente 24

#define pino_trigger_tras 30
#define pino_echo_tras 28

//Inicializa o sensor nos pinos definidos acima
NewPing sonar_f(pino_trigger_frente, pino_echo_frente, 100); // NewPing setup of pins and maximum distance.
NewPing sonar_t(pino_trigger_tras, pino_echo_tras, 100); // NewPing setup of pins and maximum distance.

char mov;

int velocidade = 240;
int distancia_p = 60;
int distancia = 40;

unsigned long previousMillis = 0;    
const long interval = 300;

// Variável do sensor
long microsec_f;
long microsec_t;
int cmMsec_f;
int cmMsec_t;

// direção para o qual o modo autonomo vai girar primeiro
int direcao = 1; 

int posicao = 0;

unsigned int uSF = 0;
unsigned int uST = 0;

AF_DCMotor esquerdo1(4); //Seleciona o motor esquerdo
AF_DCMotor direito1(3); //Seleciona o motor direito
AF_DCMotor esquerdo2(1); //Seleciona o motor esquerdo
AF_DCMotor direito2(2); //Seleciona o motor esquerdo

 
void setup() {
  Serial.begin(9600);
  Serial3.begin(9600);
  
  esquerdo1.setSpeed(velocidade); //Define velocidade baixa
  direito1.setSpeed(velocidade);
  esquerdo2.setSpeed(velocidade); //Define velocidade baixa
  direito2.setSpeed(velocidade);

  pinMode(50, OUTPUT);
  digitalWrite(50, HIGH);  

  pinMode(51, OUTPUT);
}
 
void loop() {
   unsigned long currentMillis = millis();
  
   mov = Serial3.read();

   if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      uSF = sonar_f.ping(); // Send ping, get ping time in microseconds (uS).
      uST = sonar_t.ping(); // Send ping, get ping time in microseconds (uS).
   }

   if(mov == 'p') // Parar
     posicao = 0;
   else if(mov == 'F') // Frente
      posicao = 1;
   else if(mov == 'T') // Trás
    posicao = 3;
   else if(mov == 'E') // Esquerda
    posicao = 4;
   else if(mov == 'D') // Direita
    posicao = 2;
   else if(mov == 'P') // Piloto Automático
    posicao = 5;
   else if(mov == 'M') // Manual
    posicao = 0;
   else if(mov == 'd'){ //frente dados
    char data[16];
    sprintf(data, "%4d|%4d", sonar_f.convert_cm(uSF), sonar_f.convert_cm(uST));
    Serial3.print(data);
   }

  if(posicao == 0){ //parar
    parar();
  }
  else if(posicao == 1){ // frente
      if(sonar_f.convert_cm(uSF) >= distancia_p || sonar_f.convert_cm(uSF) == 0){
        frente();
        alterarVelocidade(velocidade); 
      }
      else if(sonar_f.convert_cm(uSF) >= distancia)
        alterarVelocidade(velocidade/2);
      else
        parar();
  }
  else if(posicao == 2 ){ // direita
    alterarVelocidade(velocidade);
    direita();  
  }
  else if(posicao == 3){ // atras
    if(sonar_f.convert_cm(uST) >= distancia_p || sonar_f.convert_cm(uST) == 0){
        atras();
        alterarVelocidade(velocidade); 
      }
      else if(sonar_f.convert_cm(uST) >= distancia)
        alterarVelocidade(velocidade/2);
      else
        parar();
  }
  else if(posicao == 4) { // esquerda
    alterarVelocidade(velocidade);
    esquerda();
  }
  else if(posicao == 5) { // autonomo
    alterarVelocidade(velocidade);
    autonomo();
  }
}

void autonomo(){
  //Le as informacoes do sensor, em cm e pol
  if(sonar_f.convert_cm(uSF) >= distancia_p || sonar_f.convert_cm(uSF) == 0){
    frente();
    alterarVelocidade(velocidade); 
  }
  else if(sonar_f.convert_cm(uST) >= distancia)
    alterarVelocidade(velocidade/2);
  else{
    if(direcao){
      esquerda();
      delay(700);
    }else{
      direita();
      delay(700);
    }
  }
  if(microsec_f % 2 == 0)
    direcao = 0;
  else
    direcao = 1;
}

void atras(){
  
  esquerdo1.run(BACKWARD); //Gira o motor sentido anti-horario
  direito1.run(FORWARD); //Gira o motor sentido anti-horario
  direito2.run(FORWARD); //Gira o motor sentido anti-horario
  esquerdo2.run(BACKWARD); //Gira o motor sentido anti-horario

  digitalWrite(51, HIGH); 
}

void frente(){

  esquerdo1.run(FORWARD); //Gira o motor sentido anti-horario
  direito1.run(BACKWARD); //Gira o motor sentido anti-horario
  direito2.run(BACKWARD); //Gira o motor sentido anti-horario
  esquerdo2.run(FORWARD); //Gira o motor sentido anti-horario

}

void esquerda(){
  
  esquerdo1.run(BACKWARD); //Gira o motor sentido anti-horario
  direito1.run(BACKWARD); //Gira o motor sentido anti-horario
  direito2.run(BACKWARD); //Gira o motor sentido anti-horario
  esquerdo2.run(BACKWARD); //Gira o motor sentido anti-horario

}
void direita(){
  
  esquerdo1.run(FORWARD); //Gira o motor sentido anti-horario
  direito1.run(FORWARD); //Gira o motor sentido anti-horario
  direito2.run(FORWARD); //Gira o motor sentido anti-horario
  esquerdo2.run(FORWARD); //Gira o motor sentido anti-horario

}

void alterarVelocidade(int vel){
  esquerdo1.setSpeed(vel); 
  direito1.setSpeed(vel);
  esquerdo2.setSpeed(vel); 
  direito2.setSpeed(vel);
}

void parar(){
  esquerdo1.run(RELEASE); 
  direito1.run(RELEASE); 
  direito2.run(RELEASE); 
  esquerdo2.run(RELEASE);

  digitalWrite(51, LOW); 
}




