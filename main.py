from machine import Pin, PWM, ADC
import utime

"""
Uso:
  Cada eixo do Jostick controla a posição absoluta de um dos servomotores
  O botão do Joystick troca entre os leds verde e amarelo
  
Componentes:
  1 Led Verde
  1 Led Amarelo
  2 Resistores 220 ohms
  2 Servo Motores
  1 Joystick
  1 Raspberry Pico
  1 Fonte 5V 1A
  1 Fonte USB
  
Portas Raspberry Pico:
  3 GND: Terra
  17 GP13: Positivo Led Amarelo
  20 GP15: Positivo Led Verde
  21 GP16: PWM ServoMotorY
  23 GND: Terra
  25 GP19: PWM ServoMotorX
  31 GP26/ADC0: Joystick EixoY (VRY)
  32 GP27/ADC1: Joystick EixoX (VRX)
  34 GP28: Botão do Joystick (SW)
  36 3V3V: Alimentação Joystick (+5V
  38 GND: Terra Joystick (GND)

Alimentação:
  Raspberrypico: Fonte USB
  Motores: Fonte 5V 1A
  Não esqueçar de interligar os terras
  
Ligação Leds:
  Porta Raspberry Pico --- Resitor --- Led ---- Terra
  
Ligação Motores:
  Terra --- Fio Preto
  Fonte Alimentação 5V 1A --- Fio Vermelho
  Porta Raspberry Pico --- Fio Amarelo

Ligação Joystick:
  Diretamemte nas Portas do Raspberry 

"""

PINOLEDAMARELO=13
PINOLEDVERDE=15
PINOBOTAO=28
PINOEIXOX=26
PINOEIXOY=27
PINOSERVOY=16
PINOSERVOX=19

class Servo:
    def __init__(self, pin):
        pin = Pin(pin, Pin.OUT)
        self.__pwm = PWM(pin)
        self.__pwm.freq(50)
        self.minVal = 2500
        self.maxVal = 7500
        self.anguloAtual = 0
 
    def moverParaAngulo(self, angulo: int):
        if angulo < 0:
            angulo = 0
        if angulo > 180:
            angulo = 180
        delta = self.maxVal-self.minVal
        target = int(self.minVal + ((angulo / 180) * delta))
        self.__pwm.duty_u16(target)
        self.anguloAtual=angulo

ledOnBoard = Pin(25, Pin.OUT) #Para piscar continuadamente o Led OnBoard

ledAmarelo=Pin(PINOLEDAMARELO,Pin.OUT)  
ledAmarelo.value(0) #Começa apagado
ledVerde=Pin(PINOLEDVERDE,Pin.OUT)
ledVerde.value(1) #Começa ligado

botao=Pin(PINOBOTAO,Pin.IN, Pin.PULL_UP)  
eixoX = ADC(Pin(PINOEIXOX))
eixoY = ADC(Pin(PINOEIXOY))

servoY = Servo(PINOSERVOY)
servoX = Servo(PINOSERVOX)

#Posiciona o servo na posição do meio
servoY.moverParaAngulo(90) 
servoX.moverParaAngulo(90) 

ultimaTrocaLed=0
PERIODOTROCALED=100 #Periodo em milisegundos para trocar o estado do led onboard
ultimaApertadaBotao=0
PERIODOTESTEBOTAO=300 #Periodo em milisegundos para testar o botão pressionado. Faz o debounce e repetição se mantido pressionado.

def moveNaDirecao(servo, angulo): #Move 1 grau o servo na direção da posição desejada. Deve ser chamada inúmeras vezes até chegar na posição. A intenção das chamadas é estar em um loop.
  anguloServo=servo.anguloAtual
  if abs(angulo-anguloServo)>1: #Para evitar de ficar oscilando
    if angulo<anguloServo: #Se o angulo desejado é menor que onde está, mover para um grau a menos
      anguloServo=anguloServo-1
    else:
      if angulo>anguloServo:
        anguloServo=anguloServo+1
    servo.moverParaAngulo(anguloServo)

while True:
  #No loop não pode ter delay, pois é tratado a entrada do usuário
  agora=utime.ticks_ms() #Milisegundos atual
  #O led onboard piscando é para saber se o programa está rodando.
  if agora>ultimaTrocaLed+PERIODOTROCALED: #Se já passou o tempo para trocar o estado do led
    ultimaTrocaLed=agora
    ledOnBoard.toggle()
  if agora>ultimaApertadaBotao+PERIODOTESTEBOTAO: #Se já passou o tempo para testar a tecla
    if botao.value()==0: #Se o botão foi/está apertado
      ultimaApertadaBotao=agora
      ledAmarelo.toggle()
      ledVerde.toggle()
  #Le o Joystick
  valorY = eixoY.read_u16()
  valorX = eixoX.read_u16()
  #Converter o valor lido do joystick para faixa 0-180
  anguloY=valorY/(65536/180) 
  anguloX=valorX/(65536/180)
  #Move na direção, como é um loop move apenas 1 grau por vez
  moveNaDirecao(servoY,anguloY)
  moveNaDirecao(servoX,anguloX)
