#include <Arduino.h>
#include <HX711.h>
#include <PID_v1.h>

const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;

double tension = 0;
long raw = 0;
long threshold = 0;

const int dirPin = 4;
const int stepPin = 5;
int step_delay = 1100;

double num_steps = 0;
double setpoint = 0.0;
double Kp = 0.0001, Ki = 0, Kd = 0.0000001;
PID myPID(&tension, &num_steps, &setpoint, Kp, Ki, Kd, DIRECT);

HX711 scale;

void setup()
{
    Serial.begin(115200);
    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    scale.set_scale();
    myPID.SetOutputLimits(-30,30);

    myPID.SetMode(AUTOMATIC);
    
    Serial.print("Tare strain gauge: threshold = ");
    delay(2000);
    scale.tare();
    threshold = scale.get_units(1);
    Serial.println(String(threshold));

    pinMode(dirPin, OUTPUT);
    pinMode(stepPin, OUTPUT);
    digitalWrite(dirPin, HIGH);
}

void loop()
{
    tension = scale.get_units(1);
    myPID.Compute();
    Serial.print(">tension:" + String(tension) + "\r\n");

    if(num_steps < 0) { digitalWrite(dirPin,LOW); }
    else { digitalWrite(dirPin,HIGH); }

    for (int x = 0; x < abs((int)num_steps); x++)
    {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(step_delay);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(step_delay);
    }
}