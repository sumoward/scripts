"""
Clean up the vocollect a500 log files

Sample of file

(08/07/14 14:22:33 BST) 14:22:19.317 - 2557045: PLATFORM LOG: [pid 4194306] [tid 86638674] 2557024: NETWORKD: [14:22.19 - SDIO86881 - DFKHRF]  authenticated AP [00:a0:57:1b:43:7e]
(08/07/14 14:22:33 BST) 14:22:19.318 - 2557046: PLATFORM LOG: [pid 419
(08/07/14 14:25:04 BST) 14:24:51.047 - 2708775: ^^<sil>                  39635360 -1.00 <@@yB24H2dszxGNXjTo8TbCAD8CsYoE+gLsBiuJSMakqrrFSw5VFIDvgA==
(08/07/14 14:25:04 BST) 14:24:51.135 - 2708863: <@@xMtM0sQWa/ZWicA9BEGiTUg22ETMBhjCxuXXt57bP43kKjcPscXdjEbrH72EMtHO9hOCmP4/sBQ=
(08/07/14 14:25:04 BST) 14:24:51.138 - 2708866: ^^3                      39635360 6.28 <@@yB24H2dszxGPsvQCFaorzh/t/UGgekSRi0ITlmNJ4fXFSw5VFIDvgA==
(08/07/14 14:25:04 BST) 14:24:51.141 - 2708869: VKillSpeech called with killType 0
(08/07/14 14:25:04 BST) 14:24:51.143 - 2708871: Entering: <Node ("Initialize")> of dialog: Dialog 024ABB10 ("Digits")

"""
import time
import zipfile
import os

def scan_file(filename):
    #data structure is a dictionary
    output_file = 'cleaned_' + filename
    #remove older version of outputfile
    if os.path.isfile(output_file):
        os.remove(output_file)
    counter = 1
    #storage = {}   
    t0= time.clock()
    if filename:
        with open(filename) as fp:
            for line in fp:
                counter += 1
                line_date = line[1:9]
                #print(line_date)
                time_stamp = line[24:36]
                line_number = line[39:46]
                line_content = clean_line(line[46:])
                write_to_file(line_date, time_stamp ,line_content ,filename)
                #save_to_data_structure(time_stamp, line_number, line_content, storage)
                print ('reading log line :',counter)
    t= time.clock() - t0 # t is wall seconds elapsed (floating point)
    print ('finished read in :', t)
    return output_file

#clean up our lines to remove detritus  ': <@@' and   ': ^^'   identify noise detectionon the device           
def clean_line(line):
    if line[:5] == ': <@@' or line[:4] == ': ^^':
        #print(line)
        line = ''
    return line
    
def write_to_file(line_date, time_stamp, line_content, filename):
    output_file = 'cleaned_' + filename
    f = open(output_file,'a')
    f.write(line_date + ',' + time_stamp  + ','  + line_content)
    
#save our log file for future manipulation   
def save_to_data_structure(time_stamp, line_number, line_content, storage):
    dkey = time_stamp + '_' + line_number
    storage[dkey]= line_content
    
def zip(filename):
    outputfile = filename[:-3] + 'zip'
    #delete previous version of zip
    if os.path.isfile(outputfile):
        os.remove(outputfile)
    f = zipfile.ZipFile(outputfile,'w',zipfile.ZIP_DEFLATED)
    f.write(filename)
    f.close()
    print('File now zipped')
    
def main():
    #filename = 'Log_574224101_2014-07-03_17-24-03-744.txt'  
    filename = 'log.txt'
    outputfile = scan_file(filename)
    #print(storage)
    zip(outputfile)
    print('DONE')
    
     
if __name__ == "__main__": 
    main()
        
        

        
        
        