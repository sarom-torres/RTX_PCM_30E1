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

    while data:
        print("\nRealigning...")
        #find the possible paq position
        print("Finding possible PAQ...")
        pos_temp_paq = data.find('10011011')
        
        #get the possible new data
        new_data = data[pos_temp_paq:None]
        bit_aux = new_data[pos_bit_aux]

        #check the auxiliary bit
        print("Checking auxiliary bit...")
        if (bit_aux=='1'):
            print("Checking OK. It's auxiliary bit.")
            check_paq = new_data[512:520]
            #check the paq's second frame
            print("Checking PAQ of second frame...")
            if(check_paq=='10011011'):
                print("Checking OK. The second frame contain PAQ.")
                analysis_data["data"] = new_data
                break
            else:
                print("Checking NOT OK. The second frame NOT contain PAQ.")
                data = data[pos_temp_paq+1:None]
                continue
        else:
            print("Checking NOT OK. Isn't auxiliary bit.")
            data = data[pos_temp_paq+1:None]
            continue

    return analysis_data

def check_alignment(analysis_data):
    print ("Checking alignment...")
    paq = analysis_data.get("data")[512:520]
    return paq == "10011011"

def get_channels(frame):
    count=8
    half_count = count/2
    n_channel = 1
    pos=0

    print("===================================")
    print("               FRAME               ")
    print("========= =============== ==========")
    print("   SLOT       BINARY        HEX ")
    print("========= =============== ==========")
    while count < 257:
        print("  " + str(n_channel).zfill(2) + "/32" + "      " + frame[pos:pos+4] + " " + frame[pos+4:count] + "      " + str(hex(int(frame[pos:count],2))))
        print("========= =============== ==========")
        pos = count
        count+=8
        n_channel+=1
    

pos_bit_aux = 257
data = read_file('data.txt')
analysis_data = {
    "data": data,
    "pos_bit_aux": 257
}



count = 1
print("=================================")
print('        Receiving package        ')
print("=================================")
analysis_data = realignment(analysis_data)

size_data = len(analysis_data.get("data"))

while size_data != 0:
    
    if check_alignment(analysis_data) == 1:
        print("Checking OK. It's aligned.")
        frame1 = analysis_data.get("data")[:256]
        frame2 = analysis_data.get("data")[256:512]
        print('Reading frame... ')
        get_channels(frame1)
        get_channels(frame2)
        analysis_data["data"] = analysis_data.get("data")[512:None]
        break
    else:
        print("Checking NOT OK. Isn't aligned.")
        print("Realigning...")
        analysis_data = realignment(analysis_data)

    size_data = analysis_data.get("data")  
    count += 1

print("End of Transmission")


""" while count < 10:
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
    
    count+=1 """


