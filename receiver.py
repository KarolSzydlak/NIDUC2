import random
import array
import bitarray

import crcmod as crcmod
from bitarray import bitarray
import crccheck
import crc8
import secrets


def receiver(transmission, coding, receivedPacket, received, retransmission):
    if(transmission==2):
        if(coding==1):
            i = 0
            iterations = 256
            frame_nr = 0
            errors = 0
            arr = [format(i,'08b') for i in range(256)]
            start_index = 0
            stop_start_bit = 1
            crc8_f = crcmod.mkCrcFun(poly=int('100000111', 2))  # obliczenie crc8
            while(i<1):
                i+=1
                received = 'error'
                length = 0

                packet = receivedPacket

                random_bits = packet[0:32]

                frame_nr = packet[32:40]

                message = packet[40:-8]

                #crc8 = int(packet[-8:],2)
                crc8 = packet[-8:]
                crc8 = ''.join(str(bit) for bit in crc8)
                crc8 = int(crc8,2)



                #random_bits = array.array('B', [int(bit) for bit in random_bits])
                #frame_nr = array.array('B', [int(bit) for bit in frame_nr])
                #message = array.array('B', [int(bit) for bit in message])

                random_bits = ''.join(str(bit) for bit in random_bits)
                frame_nr = ''.join(str(bit) for bit in frame_nr)
                message = ''.join(str(bit) for bit in message)


                toCheck = random_bits + frame_nr + message


                fill_bits = (8 - (len(toCheck) % 8)) % 8
                toCheck += fill_bits * '0'
                toCheck = [str(item) for item in toCheck]
                toCheck = ''.join(toCheck)

                toCheck_arr = int(toCheck, 2).to_bytes((len(toCheck) + 7) // 8, byteorder='big')

                crc8_f = crcmod.mkCrcFun(poly=int('100000111', 2))
                calculated_crc8 = crc8_f(toCheck_arr)

                if(calculated_crc8==crc8):
                    #no errors
                    received = message
                    for value in arr:
                        if value == frame_nr:
                            del arr[arr.index(value)]
                    #numRec.append(frame_nr)

                else:
                    errors += 1
        if arr:
            for frame_nr in arr:
                random_bits = random.getrandbits(32)
                random_bits = bin(random_bits)[2:].zfill(32)  # string 32-bit
                random_array = array.array('B', [int(bit) for bit in random_bits])  # tablica bitów
                random_array = ''.join(str(bit) for bit in random_array)
                message =   '1'*1024
                start_index = end_index = '1'


                toSend = random_array + frame_nr + message

                fill_bits = (8 - (len(toSend) % 8)) % 8  # uzupełnienie 0 na końcu aby dało się stworzyć tablicę bajtów
                toSend = toSend + '0' * fill_bits
                toSend_arr = int(toSend, 2).to_bytes((len(toSend) + 7) // 8, byteorder='big')

                crc = crc8_f(toSend_arr)
                toSend += format(crc, '08b')
                retransmission.append(toSend)
    return received

def retransmission(input_frames, missing):
    i = 0
    while(i<len(missing)):
        packet  = missing[i]
        frame_nr = packet[32:40]
        toSend = []
        j = 0
        while(j<len(input_frames)):
            innerPacket = input_frames[j]
            innerFrameNr = innerPacket[32:40]
            if(innerFrameNr==frame_nr):
                toSend.append(innerPacket)

    return toSend