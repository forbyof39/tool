import subprocess
import numpy as np

diretIN = "/content/"

diretOUT = "/content/"

an = np.load( diretIN +"KyarrilKara.npy")


for ss in an:
    
    A = ss[0][0][:-4]
    B = ss[0][0][:-4]
    
    result = subprocess.Popen(
        "ffmpeg -i "+'"'+diretIN+A+".aac"+'"'+" -acodec pcm_s16le -ar 48000 "+'"'+ diretOUT+B+".wav"+'"', 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    output, error = result.communicate()
    #print(output)
    result.kill()
    
    A = ss[1][0][:-4]
    B = ss[1][0][:-4]
    
    result = subprocess.Popen(
        "ffmpeg -i "+'"'+diretIN+A+".aac"+'"'+" -acodec pcm_s16le -ar 48000 "+'"'+ diretOUT+B+".wav"+'"', 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    output, error = result.communicate()
    #print(output)
    result.kill()
    
    print( ss[0][0][:-4] )
    #print( ss[1][0][:-4] )
