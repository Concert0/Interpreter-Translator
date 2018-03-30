#Main
#Python 3.6.4
import AL2PCL
import PCL_Interpreter

AL2PCL.main()
PCL_Interpreter.data_memory =AL2PCL.symbols_and_constants_values
PCL_Interpreter.main()
