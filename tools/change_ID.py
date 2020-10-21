## model: Futaba RS304MD
## Temprate of move program

# import Library
import time, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from uart import uart

# main program
def main():    
    args = sys.argv
    servo = uart()
    ID=int(args[1])
    newID=int(args[2])
    servo.ChangeID(ID,newID)
    servo.Close()


if __name__ == '__main__':
    main()
