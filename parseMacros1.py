def _parse_macros(self):
    self._iter_macros(self._parse_macro) #_iter_lines za makroe 

def _parse_macro(self, line, p, o):
    if line[0] == "$":  #Ako naredba pocinje sa $ rijec je o makro naredbi
        macro_command = line[1:] # "$MV(A,B)" -> "MV(A,B)"
        command = macro_command.split("(")[0] #["MV", "A,B)"][0] -> "MV"
        
        if("(" not in macro_command): #END je posebna makro naredba koja nema argumente $END
            actual_arguments = []
        else:
            #Skupljam sve argumente i stavljam ih u listu
            arguments = macro_command.split("(")[1] #["MV", "A,B)"][1] -> "A,B)"
            arguments = arguments.split(")") # "A,B)" -> ["A,B , ""]
            actual_arguments = arguments[0].split(",") #["A,B , ""] -> ["A", "B"]
        
        
        #Pretvaranje makro naredbi u ekvivalentne asemblerske naredbe
        #U listu spremam linije asemblerskog koda za makro naredbu
        
        
        
        if(command == "MV"):
            
            #Asemblerski kod za MV:
            #@A
            #D=M
            #@B
            #M=D
            
            asm_lines = ["@" + actual_arguments[0], "D=M", "@" + actual_arguments[1], "M=D"] 
            return asm_lines
        
        
        
        elif(command == "SWP"):
            
            #Asemblerski kod za SWP:
             #@A
             #D=M
             #@temp
             #M=D
             #@B
             #D=M
             #@A
             #M=D
             #@temp
             #D=M
             #@B
             #M=D
            
            
            asm_lines = ["@" + actual_arguments[0], "D=M", "@temp", "M=D", "@"+ actual_arguments[1], "D=M", 
                         "@"+actual_arguments[0], "M=D", "@temp", "D=M",  "@"+actual_arguments[1], "M=D"]
            return asm_lines
        
        
        
        
        elif(command == "SUM"):
            
            #Asemblerski kod za SUM:
             #@A
             #D=M
             #@B
             #D=D+M
             #@D
             #M=D
            
            
            asm_lines = ["@" + actual_arguments[0], "D=M", "@" + actual_arguments[1], "D=D+M", 
                         "@" + actual_arguments[2], "M=D"]
            return asm_lines
        
        
        
        
        
        elif(command == "WHILE"):
            
            #Asemblerski kod za WHILE:
              #(WHILE)
              #  @A
              #  D=M
              #  @END
              #  D;JEQ
              #  @WHILE
              #  0;JMP
              #(END)
            
            
            self._loops_counter += 1 #Brojac koji mi prati koji while zatvaram ako ih imam vise
            asm_lines = ["(WHILE" + str(self._loops_counter) + ")", "@" + actual_arguments[0], "D=M"
                         , "@END" + str(self._loops_counter), "D;JEQ"]
            return asm_lines
        
        
        elif(command == "END"):
            asm_lines = ["@WHILE" + str(self._loops_counter), "0;JMP", "(END" + str(self._loops_counter) + ")"]
            self._loops_counter -= 1 #Smanjujem brojac jer smo zatvorili jedan loop
            return asm_lines
        
        
        
        else:
            self._flag = False
            self._line = o
            self._errm = "Invalid command"
            return ""
    else:
        return [line] #Nije makro naredba ako ne pocinje s "$"
