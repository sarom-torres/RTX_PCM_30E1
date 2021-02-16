#----------------------------------------|
#    read and reshape the file data      |
#----------------------------------------|
def read_file(file_path):
    file_data = open(file_path,'r')
    line = file_data.read()
    return line.replace(" ","")


#----------------------------------------|
#        do the realignment              |
#----------------------------------------|
def realignment(analysis_data):

    data = analysis_data.get('data')
    pos_bit_aux = analysis_data.get('pos_bit_aux')

    print('!!!!!!!!!!!!!! Lenght data: '+ str(len(data)))
    #find the possible paq position
    pos_temp_paq = data.find('10011011')
    
    print('pos: '+str(pos_temp_paq))
    #get the possible new
    new_data = data[pos_temp_paq:None]
    print('novo_frame: '+new_data)

    bit_aux = new_data[pos_bit_aux]
    print('bit_aux: '+ bit_aux)
    if (bit_aux=='1'):
        print('bit 1')
        check_paq = new_data[512:520]
        print("check_data: " + check_paq)

        if(check_paq=='10011011'):
            print('É payload')
            print('!!!!!!!!!!!!!! Lenght New data: '+ str(len(new_data)))
            analysis_data["data"] = new_data
            return 1
        else:
            print('NÃO é payload')
            analysis_data["data"] = data[pos_temp_paq+1:None]
            return 0
    else:
        print('bit0')
        analysis_data["data"] = data[pos_temp_paq+1:None]
        return 0

def get_channels(frame):
    count=7
    n_channel = 1
    pos=0
    while count < 257:
        print("Channel " + n_channel + ":" + frame[pos:count])
        pos = count
        count+=8
    

pos_bit_aux = 257
data = read_file('data.txt')
analysis_data = {
    "data": data,
    "pos_bit_aux": 257
}

count = 0
#len(analysis_data["data"])
while count < 10:
    print('-----------------------ciclo '+ str(count) + ' --------------------------------------------')
    result = realignment(analysis_data)
    print('ciclo '+ str(count) +': '+ analysis_data.get("data"))
    print('!!!!!!!!!!!!!! Lenght New data: '+ str(len(analysis_data.get("data"))))
    if(result == 1):
        frame = analysis_data.get("data")[:256]
        print('Lenght Payload: '+ str(len(frame)))
        print('FRAME '+ str(count) +': '+ frame)
        analysis_data["data"] = analysis_data.get("data")[256:None]
        print('ciclo '+ str(count) +': '+ analysis_data.get("data"))
    
    count+=1

#print('-----------------------ciclo 1--------------------------------------------')
#result = realignment(analysis_data)
#print('ciclo 1:'+ analysis_data.get("data"))
#print('----------------------------------------------------------------------------')

