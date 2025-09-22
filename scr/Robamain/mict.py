import speech_recognition as sr

def main():
    smc = sr.Microphone.list_microphone_names()
    print(" ")
    print("............................................")
    print(" ")
    intx=0
    for i in range(len(smc)):
        try:
                print(smc[i],"  ",i)
        
                if 'GS3: USB Audio (hw:2,0)'== smc[i]:
                    print("GS3: USB Audio" , i)
                    intx=i
                
        except:
            pass
    mic = sr.Microphone(device_index=intx,sample_rate=48000)
    print("start roba")
if __name__ == "__main__":
    main()