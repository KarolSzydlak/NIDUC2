import random
import array

import crcmod as crcmod
from bitarray import bitarray
import crccheck
import crc8
import secrets
send  = True
packet_size  = 1024
def coder(transmission, coding,input_bits):
    if(transmission == 2):
        if(coding == 1):
            coded_packet = []
            iterations = int(len(input_bits)/1024)+1
            i = 0
            frame_nr = 0
            frame = []
            start_index = 0
            stop_start_bit = 1
            while(i<iterations):
                frame = []
                end_index = start_index + 1024
                if(end_index>len(input_bits)):
                   end_index = len(input_bits)
                random_bits = random.getrandbits(32)
                random_bits = bin(random_bits)[2:].zfill(32)                        #string 32-bit
                random_array = array.array('B',[int(bit) for bit in random_bits])   #tablica bitów
                message = input_bits[start_index:end_index]                         #tutaj dane do przesłania
                start_index = end_index

                frame_nr_bin =  bin(frame_nr)[2:].zfill(8)                          #numer ramki na 8bitach
                frame_nr_array = array.array('B',[int(bit) for bit in frame_nr_bin])

                random_array = ''.join(str(bit) for bit in random_array)
                frame_nr_array = ''.join(str(bit) for bit in frame_nr_array)
                message = ''.join(str(bit) for bit in message)

                toSend = random_array+frame_nr_array+message                        #do wysłania

                fill_bits = (8-(len(toSend)%8))%8                                   #uzupełnienie 0 na końcu aby dało się stworzyć tablicę bajtów
                toSend = toSend + '0'*fill_bits
                toSend_arr = int(toSend,2).to_bytes((len(toSend)+7)//8,byteorder='big')

                crc8_f = crcmod.mkCrcFun(poly=int('100000111',2))                   #obliczenie crc8
                crc8 = crc8_f(toSend_arr)
                toSend += format(crc8, '08b')                                       #dodanie crc8 do wiadomości


                coded_packet.append(toSend)
                if(frame_nr==255):
                    frame_nr = 0
                else:
                    frame_nr+=1
                i+=1
    return coded_packet

def retransmission(start_index,end_index, missing,codet_packet):
    i = 0
    while(i<len(missing)):
        packet  = missing[i]
        random_bits = packet[0:32]
        frame_nr = packet[32:40]
        message = packet[40:-8]
        crc8 = int(packet[-8:], 2)
        toSend = []
        j = start_index
        while(j<end_index):
            innerPacket = codet_packet[j]
            innerFrameNr = innerPacket[32:40]
            if(innerFrameNr==frame_nr):
                toSend.append(innerPacket)
                break
    return toSend


