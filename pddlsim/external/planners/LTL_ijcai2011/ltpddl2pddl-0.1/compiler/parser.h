#ifndef PARSER_H
#define INPUT_H

#include "ppddl.tab.hh"
#include <stdlib.h>
#include <stdio.h>

class Parser{
	private:
		yy::PddlParser yyParser;
		PDDL_Base* instance;//this is assigned by parse() (passed by reference to yyParser's constructor)

	public:
		Parser(char* domain, char* problem);
		void parse();
		void incorporateLTL();
		void printDomainPDDL(std::ostream& s);
		void printProblemPDDL(std::ostream& s);
		  
};
#endif
