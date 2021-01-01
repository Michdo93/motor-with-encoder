#include<SoftwareSerial.h>
// include the library code:
#include <LiquidCrystal.h>
LiquidCrystal lcd(47,45,43,41,39,37);


int pulses;                              //Output pulses.
int deg = 0;
const int butA=35;
const int butB=33;
int encoderA = 19;
int encoderB = 20;
int pulsesChanged = 0;

const int pwm = 5;                      //Power of motor.                       
const int motor_A1 = 7;
const int motor_B1 = 8;
const int En_Motor_1 = A0;

unsigned long gulTimer = 0;

#define motorSpeed 180                   //Change speed of the motor.

void setup()
{ 
  pinMode(pwm, OUTPUT); 
  analogWrite(pwm, 0);
  pinMode(motor_A1, OUTPUT);
  digitalWrite(motor_A1, HIGH);
  pinMode(motor_B1, OUTPUT);
  digitalWrite(motor_B1, HIGH);
  pinMode(En_Motor_1, OUTPUT);
  digitalWrite(En_Motor_1, HIGH);
  
  pinMode(butA, INPUT);
  digitalWrite(butA, HIGH);
  pinMode(butB, INPUT);
  digitalWrite(butB, HIGH);
  pinMode(encoderA, INPUT);
  pinMode(encoderB, INPUT);
  lcd.begin(16, 2);
  lcd.print("Pulses:"); 
  lcd.setCursor(0,1);
  lcd.print(pulses);
  attachInterrupt(digitalPinToInterrupt(encoderA), A_CHANGE, CHANGE);
  Serial.begin(115200);
  gulTimer = millis();
}//setup

void loop() 
{
  if(digitalRead(butA) == 0)
  {
    analogWrite(pwm, motorSpeed);
    digitalWrite(motor_A1, LOW);
    digitalWrite(motor_B1, HIGH);
  }
  else if(digitalRead(butB) == 0)
  {
    analogWrite(pwm, motorSpeed);
    digitalWrite(motor_A1, HIGH);
    digitalWrite(motor_B1, LOW);
  }
  else
  {
    analogWrite(pwm, 0);
  }

  if(pulsesChanged != 0) 
  {
    pulsesChanged = 0;

    Serial.println(pulses);
  }

 if((millis() - gulTimer) >= 100)
 {
    lcd.clear();
    lcd.print("Pulses:"); 
    lcd.setCursor(0,1);
    lcd.print(pulses);  
    gulTimer = millis();
 }

}

void A_CHANGE() { 
  //Interrupt function to read the x2 pulses of the encoder.
  if ( digitalRead(encoderB) == 0 ) {
    if ( digitalRead(encoderA) == 0 ) {
      // A fell, B is low
      pulses--; // Moving forward
    } else {
      // A rose, B is high
      pulses++; // Moving reverse
    }
  } else {
    if ( digitalRead(encoderA) == 0 ) {


      pulses++; // Moving reverse
    } else {
      // A rose, B is low
      pulses--; // Moving forward
    }
  }
  pulsesChanged = 1;
}
