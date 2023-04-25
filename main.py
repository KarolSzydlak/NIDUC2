import io
from PIL import Image
import channel
import receiver
import sender
import time

def main():
    with open('xp.jpg', 'rb') as f:
        img_bytes = bytearray(f.read())
    img_bits = []

    for byte in img_bytes:
        bits = bin(byte)[2:].rjust(8,'0')
        img_bits.extend([int(bit) for bit in bits])
    data = sender.coder(2, 1, img_bits)
    datames = []
    for element in data:
        mes = element[40:-8]
        datames.append(mes)

    start_index = 0
    endindex = 256
    mes = ''
    channelOut = []
    receiverarr = []
    frames_to_retransmit_from_sender = []
    while(start_index<len(data)):
        transmissionErrorFromSender = []
        transmissionErrorFromReceiver = []
        data_to_send = data[start_index:endindex]
        data_received = []
        for i in range (256):
            if(start_index+i)>len(data):
                break
            channelOut = (channel.gilbert_eliot_channel(data_to_send[i],0,0.2,0,0.02))
            mes = receiver.receiver(2,1,channelOut,receiverarr, transmissionErrorFromSender)
            receiverarr.append(mes)
            start_index+=1
            #for row in receiverarr:
                #if(len(row)>5):
                    #print(row)
                    #print()
        #start_index+=256
        endindex+=256
    #while(len(transmissionErrorFromSender)>0):
       # senderRet = sender.retransmission(start_index-256,endindex-256,transmissionErrorFromSender,data)
        #for i in range (len(senderRet)):
         #   channelOut = channel.gilbert_eliot_channel(senderRet[i],0,0.2,0,0.02)
          #  mes = receiver.receiver(2, 1, channelOut, receiverarr, transmissionErrorFromSender)
    #print(type(receiverarr))
    #print(len(receiverarr))
    #print(receiverarr)
    imagetodis = []
    for row in receiverarr:
        imagetodis.append(row)
    print(imagetodis)
    binaryImage = b''.join(bytes([int(b[i:i+8],2)]) for b in receiverarr)
    if img_bytes == binaryImage:
        print("takie same")
    else:
        print("rzone")
    img = io.BytesIO(binaryImage)
    img = Image.open(img)
    img.show()

main()