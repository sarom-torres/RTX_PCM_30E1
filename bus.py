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
            #check the paq in third frame
            print("Checking PAQ of third frame...")
            if(check_paq=='10011011'):
                print("Checking OK. The third frame contain PAQ.")
                analysis_data["data"] = new_data
                break
            else:
                print("Checking NOT OK. The third frame NOT contain PAQ.")
                data = data[pos_temp_paq+1:None]
                continue
        else:
            print("Checking NOT OK. Isn't auxiliary bit.")
            data = data[pos_temp_paq+1:None]
            continue

    return analysis_data

def check_alignment(analysis_data,pos_in,pos_end):
    print ("Checking alignment...")
    paq = analysis_data.get("data")[pos_in:pos_end]
    return paq == "10011011"

def get_channels(frame,qt_frame):
    count=8
    half_count = count/2
    n_channel = 1
    pos=0

    print("====================================")
    print("               FRAME "+ str(qt_frame+1))
    print("========= =============== ==========")
    print("   SLOT       BINARY        HEX ")
    print("========= =============== ==========")
    while count < 257:
        print("  " + str(n_channel).zfill(2) + "/32" + "      " + frame[pos:pos+4] + " " + frame[pos+4:count] + "      " + str(hex(int(frame[pos:count],2))))
        print("========= =============== ==========")
        pos = count
        count+=8
        n_channel+=1
    
    qt_frame+=1
    return qt_frame

qt_frame = 0
data = read_file('data.txt')
analysis_data = {
    "data": data,
    "pos_bit_aux": 257
}

print("=================================")
print('        Receiving package        ')
print("=================================")
analysis_data = realignment(analysis_data)

size_data = len(analysis_data.get("data"))

while size_data != 0:
    
    if check_alignment(analysis_data,512,520) == 1:
        print("Checking OK. It's aligned.")
        frame1 = analysis_data.get("data")[:256]
        frame2 = analysis_data.get("data")[256:512]

        print('Reading frame... ')
        qt_frame = get_channels(frame1,qt_frame)
        print("\n")
        qt_frame = get_channels(frame2,qt_frame)
        print("\n")
        analysis_data["data"] = analysis_data.get("data")[512:None]

        if len(analysis_data.get("data")) < 512:
            frame3 = analysis_data.get("data")[:256] 
            qt_frame = get_channels(frame3,qt_frame)   
            break   
    else:    
        if check_alignment(analysis_data,1024,1032) == 1:
            print("Checking OK. It's aligned.")
            continue

        if check_alignment(analysis_data,1536,1544) == 1:
            print("Checking OK. It's aligned.")
            continue

        print("Checking NOT OK. Isn't aligned.")
        print("Realigning...")
        analysis_data = realignment(analysis_data)

    size_data = len(analysis_data.get("data")) 

print("End of Reception")
print("Number of Frames Received: " + str(qt_frame))

