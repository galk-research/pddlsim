Author: Fabio Patrizi (fabio.patrizi@dis.uniroma1.it)
Created:  Aug 4, 2011
Updated: March 19, 2012, Fabio Patrizi & Nir Lipovetzky

This file provides (minimal) guidelines for the use of the compiler 
ltpddl2pddl-v0.1

For details about what the compiler does, please refer to:

Patrizi, F., Lipovetzky, N., De Giacomo, G., Geffner, H., 
Computing Infinite Plans for LTL Goals Using a Classical Planner.
In Proc. of IJCAI'11. Barcelona, Spain. Jul 2011.


The compiler is a prototypical release and comes "as is"

CONTENT
The distribution contains:

- ltl2ba-1.1/, a slightly modified version of the tool ltl2ba 
(http://www.lsv.ens-cachan.fr/~gastin/ltl2ba/index.php) 

- compiler/, the module that performs the translation 
(and uses ltl2ba-1.1). The parser is built from a 
version of the plan verifier for the 2006 International Planning Competition 5 
(IPC-5) developed by Blai Bonet, and available at http://ldc.usb.ve/~bonet/ipc5/

- dir tool/, wich contains the official scanner and parser 
generators Flex and Bison, and a slightly modified version of the 
planner FF (http://www.loria.fr/~hoffmanj/ff.html)

- dir example/, which contains some sample files.


REQUIREMENTS
In order to develop and build the compiler, you need:
- g++ compiler (current release tested on v.4.2.1)
- flex (current release tested on v.2.5.35)
- bison (current release tested on v.2.4)
Later releases of the SW above are likely fine, but were not tested.
Please note that if you are not planning to change the scanner or parser code 
(files .yy and .lex) you don't need flex or bison.

COMPILATION TIPS
The software is still a prototype and the makefile is incomplete. 


The compiler can be easily compiled as follows:

0. change to ltl2ba-1.1/ 

1. type ./buld.sh

	
This should build the executable ltpddl2pddl, which is the compiler.

To build the planner change to dir tools/FF_LTL and type
make 

(for this, however, have a look at the respective README file)
	
*important*: the version of FF we use here is slightly different than the 
original one. For details, please refer to the paper.


EXECUTION TIPS
The compiler takes 4 (mandatory) input parameters

-df <filename>: domain output file. It is the name of the file where you want the
PDDL output domain to be stored

-pf <filename>: problem output file. It is the name of the file where you want the
PDDL output problem to be stored

The remaining two parameters represent the input domain and the input problem, 
respectively.

For instance, to compile the sample domain and problem provided by this
distribution, from compiler/ type:
./ltpddl2pddl -df ../example/dom.out  -pf ../example/prob.out  ../example/domain.pddl ../example/p01.ltl.pddl

This generates the output files dom.out and prob.out in example/.
Such files represent a classical planning problems (with conditional effect)
described in PDDL, that can be solved by, e.g., FF.

As an example of usage

Assuming the current dir is compiler/ and that the FF bin is pointed by $PATH, 
to solve the obtained planning problem with FF, type:

ff -p ../example/ -o dom.out -f prob.out

For more information on FF, refer to the respective help (just type ff from the respective dir)
or the webpage (http://www.loria.fr/~hoffmanj/ff.html).

NOTE: so far, FF is the only planner that proved robust wrt conditional effects,
a feature necessary to deal with nondeterministic Buchi automata.

Good luck!
