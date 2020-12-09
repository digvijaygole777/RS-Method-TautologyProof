# RS-Method-TautologyProof

The code for the project is written in the rs_method.py file. To execute the project:
1. Go to the directory where the rs_method.py file is saved in the terminal
2. Run the command "python rs_method.py"
3. It will prompt to enter the input expression, please enter the input expression as per guidelines which will be mentioned there
4. It will give the output on the terminal if it is tautology or not tautology.

The operands or the variables are limited to as mentioned below, if more operands are needed then you will have to add or initialize the variables as done for others in the code.

Enter the input in variables as either a,b,c,d,p,q,r,s
For 'not' operation use symbol '~' in the propositional expression
For 'and' operation use symbol '&' in the propositional expression
For 'or' operation use symbol '|' in the propositional expression
For '->' operation use symbol '>>' in the propositional expression
For '<->' operation use symbol '<<' in the propositional expression
Example Propositional Expression: (((~a | (b >> p)) & (a | b)) >> b)
if in case for other variables update the program logic in line number line-157 accordingly.


Input Samples:

1.	~(a>>c)>>[~(c|d)>>(a&~c)]  =The formula is tautology.
2.	~(a>>c)>>[~(c|d)>>(a&c)] =The formula is not a tautology.
3.	s1|a>>b | b>>a|s2=The formula is a tautology.
4.	s1|a>>b|s2=The formula is not a tautology.
