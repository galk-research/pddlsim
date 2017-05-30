/* Fabio Patrizi, December 2010
 * This file includes definitions and data structures shared by the parser and the scanner
 */

#ifndef PDDL_PARSER_DEFS_H_
#define PDDL_PARSER_DEFS_H_

	#include "ppddl.tab.hh"

	#define YY_DECL yy::PddlParser::token_type yylex(yy::PddlParser::semantic_type* yylval, yy::PddlParser::location_type* yylloc, StringTable& _tab, char* domain_file_name, char* problem_file_name)
	YY_DECL;
	
#endif /*PDDL_PARSER_DEFS_H_*/


