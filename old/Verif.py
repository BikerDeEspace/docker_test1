import DockerfileParser as dfp

#Parser Init
parser = dfp.DockerfileParser()

#Parsing file
parser.parse()

#Checking if errors
if(parser.hasError()):
    print(parser.error)
else:  
    parseResult = parser.fileparsed

    from_instruction = False
    expose_Instruction = False
    
    #Foreach instruction
    # -- Inst[i][0] = Instruction name (never null)
    # -- Inst[i][1] = arguments list (never null)
    for i in range(0, len(parseResult)):
        instruction = parseResult[i][0]
        params = parseResult[i][1]

        print(str(instruction) + ' ' + str(params))