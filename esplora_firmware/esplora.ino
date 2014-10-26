/*
Esplora Firmware

Code polls esplora for states of switches, joystick, and slider.
Prints joystick position, slider value, and ordered switches to 
serial console with 10ms delay in between.
Switch 1 and Switch 4 each save the current time into memory.
Switch 2 will go to the position saved by 1. 3 will do the same for 4.
1 will default to the beginning; 4 will default to the end.
*/
#include <Esplora.h>

void setup(){
  Serial.begin(9600);
}

void loop(){  
  int slider = Esplora.readSlider();
  int lock_one = Esplora.readButton(SWITCH_1);
  int lock_two = Esplora.readButton(SWITCH_4);
  int goto_one = Esplora.readButton(SWITCH_2);
  int goto_two = Esplora.readButton(SWITCH_3);
  int stick = Esplora.readJoystickX();
  
  Serial.print(slider);
  Serial.print(",");
  Serial.print(lock_one);
  Serial.print(",");
  Serial.print(lock_two);
  Serial.print(",");
  Serial.print(goto_one);
  Serial.print(",");
  Serial.print(goto_two);
  Serial.print(",");
  Serial.println(stick);
  delay(10);
}
