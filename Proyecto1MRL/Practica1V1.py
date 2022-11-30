from machine import sleep, I2C, Pin, Timer
from utime import ticks_diff, ticks_us
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import ssd1306
from time import sleep
import gfx

def display_bpm(t):
    global beats
    global temp
    global sat
    global oled
    global historia_2
    oled = ssd1306.SSD1306_I2C(128, 64, I2C(1,scl=Pin(22),sda=Pin(21)))
    graphics = gfx.GFX(128, 64, oled.pixel)
    if beats == 0:
        oled.text("Coloque", 30, 0)
        oled.text("su dedo", 30, 10)
        oled.text("en el", 30, 20)
        oled.text("sensor", 30, 30)
        oled.show()
    else:
        #Frecuencia cardiaca
        oled.text("BPM", 15, 49)
        oled.text(beats, 20, 57)
        #corazon: 
        graphics.line(4, 49, 2, 49, 1)
        graphics.line(10, 49, 8, 49, 1)
        graphics.line(5, 50, 1, 50, 1)
        graphics.line(11, 50, 7, 50, 1)
        graphics.line(12, 51, 0, 51, 1)
        graphics.line(12, 52, 0, 52, 1)
        graphics.line(12, 53, 0, 53, 1)
        graphics.line(12, 54, 0, 54, 1)
        graphics.line(11, 55, 1, 55, 1)
        graphics.line(10, 56, 2, 56, 1)
        graphics.line(9, 57, 3, 57, 1)
        graphics.line(8, 58, 4, 58, 1)
        graphics.line(7, 59, 5, 59, 1)
        graphics.line(6, 60, 6, 60, 1)
        #temperatura
        #Termometro
        graphics.fill_circle(50, 58, 2, 1)
        graphics.fill_rect(49, 50, 3, 6,1)
        oled.pixel(50,49,1)
        oled.pixel(70,51,1)
        oled.pixel(69,51,1)
        oled.pixel(70,52,1)
        oled.pixel(69,52,1)
        oled.text("T(C)", 56, 49)
        oled.text(temp, 56, 57)
        #SpO2
        oled.text("Sp02", 97, 49)
        oled.text(sat, 99, 57)
        oled.text("%", 120, 57)
        graphics.rect(0, 0, 128, 47, 1)
        #graficar linea
        suma=2
        for i in range(len(historia_2)-1):
            suma = suma
            graphics.line(suma, historia_2[i+1], suma+1, historia_2[i], 1)
            suma= suma+2
            if suma == 128:
                suma = 0
          #   print(historia_2[i])
            #oled.pixel(i,historia_2[i],1)
         #  for j in range (30):
          #      oled.pixel(i,j,1)
           #     oled.pixel(i-1,j-1,0)
        oled.show()
  #  beat_sub = beat_sub
  #  beat_sub.append(beats)
    #suma = suma+1
  #  print('BPM: ', beats)
    #if suma == 15:
        #print('BPM: ', beat_sub)
        #suma = 0;
        #beat_sub = []

    
    
timer = Timer(1)
timer.init(period=2000, mode=Timer.PERIODIC, callback=display_bpm)


def main():
    global beats
    global temp
    global sat
    global historia_2
    beats_history = []
    MAX_HISTORY = 32
    historia = []
    historia_2 = []
    numgrafica = 32
    i2c = I2C(1,scl=Pin(22),sda=Pin(21))  #Se establece coneccion I2C
    #i2c_2 = I2C(2,scl=Pin(22),sda=Pin(21))
    #determinacion de valores de la pantalla oled
    
    #Sensor
    sensor = MAX30102(i2c=i2c)
    #Comprobacion
    i2c.scan();
    sensor.check_part_id()
    sensor.setup_sensor()
    t_start = ticks_us()
    
    while True:
        sensor.check()
        if sensor.available():
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage()
            #print(red_reading)
            value = red_reading
            historia.append(value)
            #print(historia)
            if len(historia) == numgrafica:
                minimo, maximo = min(historia), max(historia)
                dif = maximo-minimo
                for i in range(numgrafica):
                    historia[i]=historia[i] - minimo
                    historia[i] = historia[i]/dif
                    historia[i] = int(40 - historia[i] * 40)
                    historia_2.append(historia[i])
                historia_2 = historia_2[-64:]
                historia = []
                #print(historia_2)
                
            sat = str(int(100*red_reading/(red_reading + ir_reading)+ 40))
            if value > 1000:                  
                t_us = ticks_diff(ticks_us(), t_start)
                t_s = t_us/1000000
                f = 1/t_s
                bpm = f * 60
                if bpm < 500:
                    t_start = ticks_us()
                    beats_history.append(bpm)                    
                    beats_history = beats_history[-MAX_HISTORY:] 
                    beats = str(int(sum(beats_history)/len(beats_history))-400)
                    temp = str(round(sensor.read_temperature() ,1))
            else:
                beats = 0
            


if __name__ == '__main__':
    main()
