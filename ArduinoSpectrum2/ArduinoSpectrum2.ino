int color;
String bars,temp;
int sizeB;
float RGB[3];
int buttonPin = 8;
bool buttonState;
int opt;
int R, G, B;
#include <UltrasonicDistance.h>

int trig_pin0=4;
int echo_pin0=5;
int trig_pin=6;
int echo_pin=7;
int prevOPT=0;
UltrasonicDistance slider(trig_pin0, echo_pin0);
UltrasonicDistance edit(trig_pin, echo_pin);


int red_light_pin= 11;
int green_light_pin = 10;
int blue_light_pin = 9;
bool act=false;
int Lmode = 6;
int prev=0;
const long interval = 5*1000;
unsigned long previousMillis = 0;   
void setup(){
  pinMode(A4, INPUT);
pinMode(A5, INPUT);
  digitalWrite(buttonPin, HIGH);
    Serial.begin(9600);
  pinMode(red_light_pin, OUTPUT);
  pinMode(green_light_pin, OUTPUT);
  pinMode(blue_light_pin, OUTPUT);
  rgb(255,255,255);
  }
//////////////////////////////////////////////////////////
bool onRelease(int bPIN) {
  bool bState = !digitalRead(bPIN);
  bool released;
  if (bState) {
    bState = !digitalRead(bPIN);
    while (bState != 0) {
      bState = !digitalRead(bPIN); //do nothing
    }
    return true;
  }
  else {
    return false;
  }
}

int change(bool state, int mode, int maX) {
  int  add = mode;
  if (state) {
    add++;
  }
  if (mode > maX) {
    rgb(255,255,255);
    add = 0;
  }
  //Serial.println(add);
  return add;
}
 ////////////////////////////////////////////////////////////////// 
void loop(){
buttonState = onRelease(buttonPin);
Lmode = change(buttonState, Lmode, 6);
//Music reactive lights
if(Lmode==0)  {
  if(Serial.available()){
    R = Serial.parseInt();
    G = Serial.parseInt();
    B = Serial.parseInt();
    Serial.println(sizeB);
rgb(255-R,255-G,255-B);
}
}
// Mood Lamp
else if(Lmode==1){
  
    for (float x = 0; x < PI; x = x + 0.00005) {
      buttonState = onRelease(buttonPin);
      Lmode = change(buttonState, Lmode, 6);
      if (Lmode != 1) {
        analogWrite(red_light_pin, 255 - random(0, 255));
        analogWrite(green_light_pin, random(0, 255));
        analogWrite(blue_light_pin, random(0, 255));
        break;
      }


      RGB[0] = 255 * abs(sin(x * (180 / PI)));   // calculate the brightness for the red led
      RGB[1] = 255 * abs(sin((x + PI / 3) * (180 / PI))); // calculate the brightness for the green led
      RGB[2] = 255 * abs(sin((x + (2 * PI) / 3) * (180 / PI))); // calculate the brightness for the blue led
      int ambientLight = 601; // read an store the ambient light
      if (ambientLight > 600) { // start only if the ambient light is very low
        //  write the brightness on the leds
        analogWrite(red_light_pin, 255 - RGB[0]);
        analogWrite(green_light_pin, 255 - RGB[1]);
        analogWrite(blue_light_pin, 255 - RGB[2]);
      }
      else {
        digitalWrite(red_light_pin, LOW);
        digitalWrite(green_light_pin, LOW);
        digitalWrite(blue_light_pin, LOW);
      }
      for (int i = 0; i < 3; i++) {
        if (RGB[i] < 1) {
          delay(100);
        }
        if (RGB[i] < 5) {
          delay(50);
        }
        if (RGB[i] < 10) {
          delay(10);
        }
        if (RGB[i] < 100) {
          delay(5);
        }
      }
      delay(1);
    }
  }



else if(Lmode==2){
  rgb(255-255,255-0,255-0);
  }
else if(Lmode==3){
  rgb(255-0,255-255,255-0);
  }
else if(Lmode==4){
  rgb(255-0,255-0,255-255);
  }
else if(Lmode==5){
  rgb(255-0,255-255,255-255);
  }
else if(Lmode==6){
  rgb(0,0,0);
  delay(100);
  rgb(255,255,255);
  delay(100);
  rgb(0,0,0);
  delay(100);
  rgb(255,255,255);
  delay(100);
  bool distance=!digitalRead(2);
  while(true){
    unsigned long currentMillis = millis();
    buttonState = onRelease(buttonPin);
    Lmode = change(buttonState, Lmode, 6);
    if(Lmode!=6){break;}
    
    distance=!digitalRead(2);
    color = Serial.parseInt();
    //Serial.println(color.length());
    //Serial.println(color);
    if(color>0){
    //Serial.print(color);

    switch(color)
    {
      case 1: //red
        rgb(0,255,255);
        break;
      case 2:  //green
        rgb(255,0,255);
        break;
      case 3: //blue
        rgb(255,255,0);
        break;
      case 4: //purple
        rgb(0,255,0);
        break;
      case 5: //yellow
        rgb(0,0,255);
        break;
      case 6: //light blue
        rgb(255,0,0);
        break;
    }
     
    }
    //Serial.println(distance);
    if (distance && !act){
      Serial.println("w");
      //rgb(random(0,255),random(0,255),random(0,255));
      previousMillis = currentMillis;
      act=true;
      }
    
    else if(currentMillis - previousMillis >= interval){
      if(!distance && act){
      previousMillis = currentMillis;
      //Serial.println("Activable again");
      act=false;
      }}
    else if(distance && act){
      previousMillis = currentMillis;
      }
        int valueX = analogRead(A5);
  int valueY = analogRead(A4);
  valueX=map(valueX, 0,1024,-2,3);
  valueY=map(valueY, 0,1024,-2,3);
  //value = map(value, 0, 1023, 0, 255);
  Serial.print(valueX);
  Serial.print(":");
  Serial.print(valueY);
  Serial.print(":");
       Serial.println(edit.getDistance());
      //Serial.println(slider.getDistance());
    
  }
  }
  }  
   
   
void rgb(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(red_light_pin, red_light_value);
  analogWrite(green_light_pin, green_light_value);
  analogWrite(blue_light_pin, blue_light_value);
}
