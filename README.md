

# Python Interpreter
The purpose of this assignment is to build an interpreter for a very simple programming language that looks like assembly. The first way of doing it is a direct interpretation of the Asselmbly-like language. The second way is translating it to another simple language(PCL) then interpreting PCL which is somehow similar to what happens during compilation.

##### Version `python3`
- [x] AL to PCL
- [x] PCL Interpreter
- [x] AL Interpreter



#### AL_Interpreter.py: Assembly-like language interpreter

     -To run: python3 AL_Interpreter  
     -Input: One of the text files in the ALfiles Directory (Change input in line 230 to one of the ALfiles)
     -Output generated in outpulAL.txt


#### AL2PCL.py: Is the ‘Compiler’ from AL to PCL

	-To run: python3 AL2PCL.py
	-Input: One of the text files in the ALfiles Directory (Change input in line 55 to one of the ALfiles)
	-Output generated in al2pcl.txt (translated PCL to AL)

#### PCL_Interpreter.py: Is the PCL interpreter

	-To run: python3 PCL_Interpreter
	-Input: al2pcl.txt
	-Output generated in outpulPCL.txt

##### main.sh: shell command that runs both AL2PCL(translation) and PCL_Interpreter.
    -To run: bash main.sh
  
