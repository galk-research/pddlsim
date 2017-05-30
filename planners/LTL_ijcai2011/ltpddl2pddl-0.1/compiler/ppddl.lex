/* 
Created: December 2010
Author: Fabio Patrizi

This file was written following the C++ scanner example
at page 130 of the Bison 2.4.3 manual (v. 5 August 2010).
Please refer to the manual for any clarification.
*/

%{
	#include <string>
	#include "string_table.h"
	#include "defs.h"
	#include "ppddl.tab.hh"
	
	// Type shortcuts
	typedef yy::PddlParser::token token;
			  
	// Modify yyterminate() so as to return a token (by default it returns an int)
	#define yyterminate() return token::END
	
	// Boolean flag to record that the domain and the problem files have been read
	bool domain_read = false;
	bool problem_read = false;
		
	// Auxiliary function	
	FILE* open_input(char* file_name){
		FILE* result = fopen(file_name, "r");
		if (!result) {
			cerr << "error: can't open " << file_name << std::endl;
			exit(1);
		}
		return result;
	}
		
	// Init macro: initializes the input buffer with the domain file
	#define YY_USER_INIT yyin=open_input(domain_file_name); domain_read = true;		
%}

%option nounput

/* Abbreviations */

CHAR [a-zA-Z_]
DIGIT [0-9]
INT -?{DIGIT}*
FLOAT -?{DIGIT}+(\.{DIGIT}*)?
STRING {CHAR}+(-|{CHAR}|{DIGIT})*
WHITESPACE [ \t]+
NL \n
COMMENT ;.*$

%{
	#define YY_USER_ACTION yylloc -> columns(yyleng);
%}

%%

%{
	yylloc -> step();
%}


	

{WHITESPACE}+ {yylloc -> step();}

{COMMENT} {}

{NL}+	{
	yylloc -> lines(yyleng);
	yylloc -> step();
}

"(" {return token::TK_OPEN;}
")" {return token::TK_CLOSE;}
"[]" {return token::TK_ALW;}
"<->" {return token::TK_IFF;}
"<>" {return token::TK_EVT;}
"-" {return token::TK_HYPHEN;}
"=" {return token::TK_EQ;}
"&&" {return token::TK_LTL_AND;}
"||" {return token::TK_LTL_OR;}
"!" {return token::TK_EXCL;}
"->" {return token::TK_IMPL;}
"U" {return token::TK_UNTIL;}
"V" {return token::TK_RELEASE;}
"X" {return token::TK_NEXT;}

 
":requirements" {return token::KW_REQS;}
":constants" {return token::KW_CONSTANTS;}
":predicates" {return token::KW_PREDS;}
":types" {return token::KW_TYPES;}
"define" {return token::KW_DEFINE;}
"domain" {return token::KW_DOMAIN;}
":action" {return token::KW_ACTION;}
":parameters" {return token::KW_ARGS;}
":precondition" {return token::KW_PRE;}
":effect" {return token::KW_EFFECT;}
"and" {return token::KW_AND;}
"or" {return token::KW_OR;}
"exists" {return token::KW_EXISTS;}
"forall" {return token::KW_FORALL;}
"imply" {return token::KW_IMPLY;}
"not" {return token::KW_NOT;}
"when" {return token::KW_WHEN;}
"oneof" {return token::KW_ONEOF;}
"problem" {return token::KW_PROBLEM;}
":domain" {return token::KW_FORDOMAIN;}
":objects" {return token::KW_OBJECTS;}
":init" {return token::KW_INIT;}
":goal" {return token::KW_GOAL;}

":name" {return token::KW_NAME;}

\?{STRING} {
  yylval -> sym = _tab.inserta(yytext);
  if (yylval -> sym -> val == 0) return token::TK_NEW_VAR_SYMBOL;
  if (((Basic::Symbol*)yylval -> sym->val)->sym_class == Basic::sym_variable)
    return token::TK_VAR_SYMBOL;
  return token::TK_NEW_VAR_SYMBOL;
}

\:{STRING} {
  yylval -> sym = _tab.inserta(yytext);
  return token::TK_KEYWORD;
}

{STRING} {
  yylval -> sym = _tab.inserta(yytext);
  if (yylval->sym->val == 0) return token::TK_NEW_SYMBOL;
  else {
    switch (((Basic::Symbol*)yylval->sym->val)->sym_class) {
    case Basic::sym_object:
      return token::TK_OBJ_SYMBOL;
    case Basic::sym_typename:
      return token::TK_TYPE_SYMBOL;
    case Basic::sym_predicate:
      return token::TK_PRED_SYMBOL;
    case Basic::sym_action:
      return token::TK_ACTION_SYMBOL;
    default:
      return token::TK_MISC_SYMBOL;
    }
  }
}

{INT} {  yylval->ival = atoi(yytext); return token::TK_INT;}


<<EOF>> {
	fclose(yyin);
	if (!problem_read){
		problem_read = true;
		yyin=open_input(problem_file_name);
		yy_switch_to_buffer(yy_create_buffer(yyin, YY_BUF_SIZE));
	}
	else{
		yyterminate();
	}	
}

%%

	int yywrap() {
	  return 1;
	}
	
