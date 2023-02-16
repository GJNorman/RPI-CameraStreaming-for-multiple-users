from ProgramSettings import *
import sys                              #argument parsing

primitiveTypes = (int,str,bool,float)

listOrTupleTypes = (list,tuple)
"""
    convert a dictionary into a string for writing to file
"""
indentationLevel = 1
def convertDictionary(dictionary):
    global indentationLevel
    output = "{\n" + "\t"*indentationLevel
    indentationLevel+=1
    for key in dictionary:
        Value = dictionary[key]
        Value = convertToPrintable(Value)
        output += "\"" + key + "\":" +Value + ",\n\t"
    indentationLevel-=1
    output += "}"
    print(output)
    return output
"""
    convert a list or tuple into a string for writing to file
"""
def convertListOrTuple(var):
    newlist = []
    
    """
        convert individual elements
    """
    for i in range (0,len(var)):
        newlist.append(convertToPrintable(var[i]))
    
    """
        convert boiler plate elements into strings
    """
    finalChar = ']'
    if isinstance(var,list):
        var = "["
    else:
        var = "("
        finalChar = ")"
    
    for i in range (0,len(newlist)):
        var += newlist[i] + ','
        
    #remove final comma
    var = var[:-1]
    
    var+=finalChar
    
    return var
"""
    take a python data type and convert into a string for writing to a file
"""
def convertToPrintable(var):

    if isinstance(var,primitiveTypes):
        if isinstance(var, str) :
            var = "\"" + var + "\""
        else:
            var = str(var)
    else:
        if isinstance(var,dict):
            var =  convertDictionary(var)
        if isinstance(var,listOrTupleTypes):
            var = convertListOrTuple(var)

    return var

def saveSettings(new_global_Settings):
    #Back up the current file
    #os.system("chmod -R 777 /var/www/html/scripts");
    File = open("/var/www/html/scripts/ProgramSettings.py","r").read()
    File2 = open("/var/www/html/scripts/ProgramSettingsArchive.py","w")
    File2.write(File) 
    File2.close()
    #Write the new file
    File = open("/var/www/html/scripts/ProgramSettings.py","w")
    
    File.write("#this file is overwritten programmatically; don't add any data outside of this dictionary\n#all dictionary keys must be strings\nglobal_Settings = ")
    
    output = convertDictionary(new_global_Settings)

    File.write(output)

    File.close()

"""
    for system calls
    used to set dictionary values from non-python programs
"""

if (len(sys.argv)-1) == 4:
    #format "ModuleName" "Name" "ModuleType" "Type"
    #arg      1             3       3        4
    from ProgramSettings import *           #import global variables
    global_Settings[sys.argv[1]] = sys.argv[2]
    global_Settings[sys.argv[3]] = sys.argv[4]
    saveSettings(global_Settings)    
