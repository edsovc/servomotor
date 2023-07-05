from machine import Pin, PWM, ADC
import utime

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

botao=Pin(PINOBOTAO,Pin.IN, Pin.PULL_UP) #Em qual porta está ligado o botão do Joystick 
eixoX = ADC(Pin(PINOEIXOX)) #Conversor Analogico para Digital para ler o Eixo X
eixoY = ADC(Pin(PINOEIXOY))

servoY = Servo(PINOSERVOY) #Controlador do MotorY
servoX = Servo(PINOSERVOX)

#Posiciona o servo na posição do meio=90 graus
servoY.moverParaAngulo(90) 
servoX.moverParaAngulo(90) 

ultimaTrocaLed=0 #Quando ocorreu a última mudanca apagado-acesso do Led on Board. Iniciado com Zero para garantir que irá mudar no primeiro ciclo.
PERIODOTROCALED=100 #Periodo em milisegundos para trocar o estado do led onboard
ultimaApertadaBotao=0 #Para fazer o debounce do botão (  https://www.makerhero.com/blog/debounce-o-que-e-e-como-resolver-via-software/  )
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
  #Como são tratados diversos eventos que não são sincronizados, o melhor método é loop e não delay
  agora=utime.ticks_ms() #Milisegundos atual
  #O led onboard piscando é para saber se o programa está rodando.
  if agora>ultimaTrocaLed+PERIODOTROCALED: #Se já passou o tempo para trocar o estado do led
    ultimaTrocaLed=agora #Guarda quando que ocorreu a ultima troca, para saber quando deverá ocorrer a próxima
    ledOnBoard.toggle() #Troca o estado do Led (Apagado - Acesso)
  if agora>ultimaApertadaBotao+PERIODOTESTEBOTAO: #Se já passou o tempo para testar a tecla
    if botao.value()==0: #Se o botão foi/está apertado
      ultimaApertadaBotao=agora #Guarda quando o botão foi pressionado e não trata mais o botão até passar PERIODOTESTEBOTAO milisegundos
      ledAmarelo.toggle() #Troca o estado do Led (Apagado - Acesso)
      ledVerde.toggle() #Troca o estado do Led (Apagado - Acesso)
  #Le o Joystick
  valorY = eixoY.read_u16()
  valorX = eixoX.read_u16()
  #Converter o valor lido do joystick para faixa 0-180
  anguloY=valorY/(65536/180) 
  anguloX=valorX/(65536/180)
  #Move na direção, como é um loop move apenas 1 grau por vez
  moveNaDirecao(servoY,anguloY)
  moveNaDirecao(servoX,anguloX)
