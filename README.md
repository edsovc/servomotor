# servomotor

Um exemplo ditatico de como controlar servomotor utilizando um joystick.

## Uso:
  Cada eixo do Jostick controla a posição absoluta de um dos servomotores.
  O botão do Joystick troca entre os leds verde e amarelo.
  
## Componentes:
- 1 Led Verde
- 1 Led Amarelo
- 2 Resistores 220 ohms
- 2 Servo Motores
- 1 Joystick
- 1 Raspberry Pico
- 1 Fonte 5V 1A
- 1 Fonte USB
  
## Portas Raspberry Pico:
- 3 GND: Terra
- 17 GP13: Positivo Led Amarelo
- 20 GP15: Positivo Led Verde
- 21 GP16: PWM ServoMotorY
- 23 GND: Terra
- 25 GP19: PWM ServoMotorX
- 31 GP26/ADC0: Joystick EixoY (VRY)
- 32 GP27/ADC1: Joystick EixoX (VRX)
- 34 GP28: Botão do Joystick (SW)
- 36 3V3V: Alimentação Joystick (+5V
- 38 GND: Terra Joystick (GND)

## Alimentação:
-  Raspberrypico: Fonte USB
-  Motores: Fonte 5V 1A

  Não esqueçar de interligar os terras.
  
## Ligação Leds:
-  Porta Raspberry Pico --- Resitor --- Led ---- Terra
  
## Ligação Motores:
-  Terra --- Fio Preto
-  Fonte Alimentação 5V 1A --- Fio Vermelho
-  Porta Raspberry Pico --- Fio Amarelo

## Ligação Joystick:
-  Diretamemte nas Portas do Raspberry 
