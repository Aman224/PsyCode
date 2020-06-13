with open("final_output.txt","r") as File:
    Lines = File.readlines()
with open("Temp.c","w") as OPFile:
    intendLevel = 0
    for line in Lines:
        flag = False
        for char in line:
            if char == '{':
                print("{",file=OPFile)
                intendLevel += 1
                flag = True

            elif char == '}':
                intendLevel -= 1
                print("\n"+"\t"*intendLevel+"}",file=OPFile)
                flag = True
            elif char == '\n':
                print("\n"+"\t"*intendLevel,end="",file=OPFile)
            
            else:
                print(char,end="",file=OPFile)
with open("Temp.c","r") as FinalF:
    Lines = FinalF.readlines()
    for line in Lines:
        tline = line.lstrip("\t")
        # if line in ['\t\n', '\n']:
        #     continue
        if tline == "\n":
            continue
        else:
            line = line.rstrip('\n')
            print(line)