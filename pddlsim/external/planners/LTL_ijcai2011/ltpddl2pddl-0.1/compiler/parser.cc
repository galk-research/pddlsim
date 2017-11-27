#include "parser.h"

Parser::Parser(char* domain, char* problem) : yyParser(domain,problem,instance){};

void Parser::parse(){
	yyParser.parse(); // this assigns the result of pasing to instance
}

void Parser::incorporateLTL(){
	instance->incorporateLTL();
}

void Parser::printDomainPDDL(std::ostream& s){
	instance->printDomainPDDL(s);
}

void Parser::printProblemPDDL(std::ostream& s){
	instance->printProblemPDDL(s);
}
