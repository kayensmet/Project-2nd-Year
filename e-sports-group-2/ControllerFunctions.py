import time
import serial
ser = serial.Serial("COM9", 50000)

# Met deze functie wordt alles naar standaarden gezet bij het opstarten van de game zo komen er geen plotse
# of onverwachte waarden op de controller (later komen hier nog waardes in voor de led array enz.)
def controller_init():
    ser.write(b's10x')
    ser.write(b's20x')

# Werkt niet helemaal
# def lees_seriele_poort(nieuwe_x, r_speler_x, nieuwe_y, r_speler_y, snelheid, is_bewegen):
#     while True:
#         data = ser.readline().decode().strip()
#         if data == "z":
#             nieuwe_x += r_speler_x * snelheid
#             nieuwe_y += r_speler_y * snelheid
#         time.sleep(1)


def show_xp_controller(xp):
    # Dit is eigenlijk niet nodig ofzo maar een beetje foutafhandeling kan nooit kwaad.
    if xp > 100:
        print("XP is over 100, please enter a number lower than 100")
        ser.write(b's10x')
        ser.write(b's20x')
    else:
        eenheden = xp % 10
        tientallen = xp // 10

        commandEenheden = "s2" + str(eenheden) + "x"
        commandTientallen = "s1" + str(tientallen) + "x"
        ser.write(commandEenheden.encode())
        ser.write(commandTientallen.encode())

def show_timer_controller(timer):
    if timer > 9:
        eenheden = timer % 10
        tientallen = timer // 10

        commandEenheden = "s2" + str(eenheden) + "x"
        commandTientallen = "s1" + str(tientallen) + "x"
        ser.write(commandEenheden.encode())
        ser.write(commandTientallen.encode())
    else:
        commandEenheden = "s2" + str(timer) + "x"
        ser.write(commandEenheden.encode())

def sound_vib_on_pickup():
    ser.write(b'v1x')