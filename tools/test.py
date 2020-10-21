## model: Futaba RS304MD
## Temprate of move program

# import Library
import serial
import time, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from uart import uart

def CheckSum(Data):
    check = 0x00
    for x in Data:
        check ^= int(x)
    return check

def ShortPacket(ID, Flag, Address, Cnt, Data):
    TxData = [0xFA, 0xAF]# packet header
    # array
    if type(Data)==type([]):
        Length  = len(Data)
        tmpData = [ID, Flag, Address, Length, Cnt]
        tmpData.extend(Data)
    # None data(ex.reboot)
    elif type(Data)==type(None):
        tmpData = [ID, Flag, Address, 0x00, Cnt]
    # not array
    else:
        Length  = 0x01
        tmpData = [ID, Flag, Address, Length, Cnt]
        tmpData.append(Data)
    # CheckSum
    tmpData.append(CheckSum(tmpData))
    TxData.extend(tmpData)
    return TxData

# main program
def main():    
    ID = 0x01
    Flag = 0x00
    OFF = 0x00
    ON = 0x01
    port='/dev/ttyS0'
    rate=115200
    uart = serial.Serial(port, rate)
    ADDRESS_ID       = 0x04
    ADDRESS_REVERSE  = 0x05
    ADDRESS_POSITION = 0x1E
    ADDRESS_TORQUE   = 0x24
    ALLSERVOS = 0xFF

    TxData = ShortPacket(ALLSERVOS, Flag, ADDRESS_TORQUE, 0x01, ON)
    uart.write(TxData)

    Angle   = int(10.0 *float(0))
    Speed   = int(100.0*float(0.01))
    tmpData = [Angle, (Angle>>8), Speed, (Speed>>8)]
    Data    = map(lambda x:x&0x00FF, tmpData)

    TxData = ShortPacket(ID, Flag, ADDRESS_POSITION, 0x01, Data)
    uart.write(TxData)

    time.sleep(1.0)

    Angle   = int(10.0 *float(60))
    Speed   = int(100.0*float(0.01))
    tmpData = [Angle, (Angle>>8), Speed, (Speed>>8)]
    Data    = map(lambda x:x&0x00FF, tmpData)

    TxData = ShortPacket(ID, Flag, ADDRESS_POSITION, 0x01, Data)
    uart.write(TxData)

    time.sleep(1.0)
    
    TxData = ShortPacket(ALLSERVOS, Flag, ADDRESS_TORQUE, 0x01, OFF)
    uart.write(TxData)

if __name__ == '__main__':
    main()
