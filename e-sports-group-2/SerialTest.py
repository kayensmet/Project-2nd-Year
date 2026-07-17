import serial
# import time
#
ser = serial.Serial("COM7", 9600)
#
# #time.sleep(2)  # Wacht tot de seriële verbinding tot stand komt
#
# def buzzer_on():
#     ser.write(b's13x')
#     ser.write(b's24x')
#     ser.write(b's17x')
#     #time.sleep(1)# Stuur '1' naar Arduino om de buzzer aan te zetten
#
# def buzzer_off():
#     ser.write(b'0')  # Stuur '0' naar Arduino om de buzzer uit te zetten
#
# # Test de buzzer
# buzzer_on()

waarde = 5
commandEenheden = "s1" + str(waarde) + "x"
ser.write(commandEenheden.encode("utf-8"))