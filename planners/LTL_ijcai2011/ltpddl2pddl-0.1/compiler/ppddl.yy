// December 2010
// Author: Fabio Patrizi

// directives for C++ code generation
%skeleton "lalr1.cc"
%defines
//

%locations // for location tracking
%debug // for parser tracing
%error-verbose // for verbose error messages

// Includes and namespaces needed to define the %union
%code requires{
	#include <stdlib.h>
	#include <string.h>
	#include <list>
	#include "base.h"
	#include "BuchiAutomaton.h"
	
	using namespace std;
}

%code {
	#include "defs.h"
	
	// Anything defined here is accessible from within rules
	
	// Variables
	Basic::variable_vec current_param;
	size_t              stored_n_param;
	Basic::AtomBase*   	current_atom;
	std::list<Basic::Effect *> context;
	StringTable symbols(50, lowercase_map);
	PDDL_Base* ast = new PDDL_Base(symbols);
	
	extern "C" FILE* yyin;
	
}

// Generated parser class name
%define parser_class_name "PddlParser"

// Declaration of parameters of parsing function
%parse-param{char* domain_file} // the input domain file name
%parse-param{char* problem_file} // the input problem file name
%parse-param{PDDL_Base*& result} // Side effect on result, to return the result of parsing

// Assignment to parameters of scanning function (params defined in yylex of def.h)
%lex-param{StringTable& symbols}
%lex-param{char* domain_file}
%lex-param{char* problem_file}
//

%union {
  StringTable::Cell* sym;
  Basic::Clause*     clause;
  Basic::OneOf*      oneof;
  int                ival;
  Basic::LTLNode* 	 ltl; // (FP) For LTL goal formula
}

%token END 0 "end of file"

%token TK_OPEN TK_CLOSE TK_EQ TK_HYPHEN TK_ALW TK_EVT TK_LTL_AND  TK_LTL_OR TK_EXCL 
		TK_IMPL TK_UNTIL TK_RELEASE TK_NEXT  TK_IFF
		

%nonassoc TK_RELEASE TK_UNTIL // binary temporal operators "U" and "V" have the lowest precedence
%left TK_IMPL TK_IFF // "->" and "<->" have higher precedence than "U" and "V"
%left TK_LTL_OR // "||" has higher precedence than "->" and "<->"
%left TK_LTL_AND // "&&" has higher precedence than "||"
%right TK_NEXT TK_ALW TK_EVT TK_EXCL  // Unary operators have the highest precedence
		
		

%token <sym>  TK_NEW_SYMBOL TK_OBJ_SYMBOL TK_TYPE_SYMBOL TK_PRED_SYMBOL
              TK_FUN_SYMBOL TK_VAR_SYMBOL TK_ACTION_SYMBOL TK_MISC_SYMBOL
              TK_KEYWORD TK_NEW_VAR_SYMBOL 
              
%token <ival> TK_INT

%token KW_REQS KW_CONSTANTS KW_PREDS KW_TYPES KW_DEFINE KW_DOMAIN
       KW_ACTION KW_ARGS KW_PRE KW_COND KW_EFFECT KW_AND
       KW_OR KW_EXISTS KW_FORALL KW_IMPLY KW_NOT KW_WHEN KW_ONEOF
       KW_PROBLEM KW_FORDOMAIN KW_OBJECTS KW_INIT KW_GOAL KW_NAME 

%type <sym>    arg_symbol action_symbol any_symbol
%type <clause> cnf_clause
%type <oneof>  oneof_effect
%type <ltl>  ltl_spec

%start pddl_declarations

%%

pddl_declarations:
	{
		// preliminary instructions
		result = ast; // sets result to the abstract syntax tree obtained from the parsing process
	} 
pddl_domain pddl_problem
;

pddl_domain:
TK_OPEN KW_DEFINE domain_name domain_elements TK_CLOSE
;

domain_elements:
domain_requires domain_elements
| domain_types domain_elements
| domain_constants
{
	for (Basic::symbol_vec::const_iterator it=ast->dom_constants.begin(); it != ast->dom_constants.end(); it++){
		ast->pure_constants.insert(*it);
	}
} 
domain_elements
| domain_predicates domain_elements
| domain_structure domain_elements
| /* empty */
;

domain_name:
TK_OPEN KW_DOMAIN any_symbol TK_CLOSE
{
  ast->domain_name = $3->text;
}
;

any_symbol:
TK_NEW_SYMBOL { $$ = $1; }
| TK_OBJ_SYMBOL { $$ = $1; }
| TK_TYPE_SYMBOL { $$ = $1; }
| TK_PRED_SYMBOL { $$ = $1; }
| TK_FUN_SYMBOL { $$ = $1; }
| TK_VAR_SYMBOL { $$ = $1; }
| TK_ACTION_SYMBOL { $$ = $1; }
| TK_MISC_SYMBOL { $$ = $1; }
;

arg_symbol:
TK_OBJ_SYMBOL { $$ = $1; }
| TK_VAR_SYMBOL { $$ = $1; }
;

action_symbol:
TK_NEW_SYMBOL { $$ = $1; }
| TK_ACTION_SYMBOL { $$ = $1; }
;

// requirement declarations

domain_requires:
TK_OPEN KW_REQS require_list TK_CLOSE
;

require_list:
require_list KW_TYPES{
	ast->dom_requirements.push_back(new Basic::Symbol(":types"));
}
| require_list TK_KEYWORD{
	ast->dom_requirements.push_back(new Basic::Symbol($2->text));
}

| /* empty */
;

// predicate declarations

domain_predicates:
TK_OPEN KW_PREDS predicate_list TK_CLOSE
;

predicate_list:
predicate_decl predicate_list
| predicate_decl
;

predicate_decl:
TK_OPEN TK_NEW_SYMBOL
{
  current_param.clear();
}
typed_param_list TK_CLOSE
{
  Basic::PredicateSymbol *p = new Basic::PredicateSymbol( $2->text );
  ast->dom_predicates.push_back( p );
  p->param = current_param;
  ast->clear_param( current_param );
  $2->val = p;
}
;

typed_param_list:
typed_param_list typed_param_sym_list TK_HYPHEN TK_TYPE_SYMBOL
{
  ast->set_variable_type( current_param, current_param.size(), (Basic::TypeSymbol*)$4->val );
}
| typed_param_list typed_param_sym_list
{
  ast->set_variable_type( current_param, current_param.size(), ast->dom_top_type );
}
| /* empty */
;

typed_param_sym_list:
typed_param_sym_list TK_NEW_VAR_SYMBOL
{
  $2->val = new Basic::VariableSymbol( $2->text );
  current_param.push_back( (Basic::VariableSymbol*)$2->val );
}
| /* empty */
;

// type declarations

domain_types:
TK_OPEN KW_TYPES typed_type_list TK_CLOSE
;

typed_type_list:
typed_type_list primitive_type_list TK_HYPHEN TK_TYPE_SYMBOL
{
  ast->set_type_type( ast->dom_types, ast->dom_types.size(), (Basic::TypeSymbol*)$4->val );
}
| typed_type_list primitive_type_list TK_HYPHEN TK_NEW_SYMBOL
{
  $4->val = new Basic::TypeSymbol( $4->text );
  if( ast->write_warnings ) std::cerr << "warning: assuming " << $4->text << " - " << ast->dom_top_type->print_name << std::endl;
  ((Basic::TypeSymbol*)$4->val)->sym_type = ast->dom_top_type;
  ast->set_type_type( ast->dom_types, ast->dom_types.size(), (Basic::TypeSymbol*)$4->val );
  ast->dom_types.push_back( (Basic::TypeSymbol*)$4->val );
}
| typed_type_list primitive_type_list
{
  ast->set_type_type( ast->dom_types, ast->dom_types.size(), ast->dom_top_type );
}
| /* empty */
;

primitive_type_list:
primitive_type_list TK_TYPE_SYMBOL
{
  /* the type is already (implicitly) declared */
}
| primitive_type_list TK_NEW_SYMBOL
{
  $2->val = new Basic::TypeSymbol( $2->text );
  ast->dom_types.push_back( (Basic::TypeSymbol*)$2->val );
}
| /* empty */
;

// constant declarations

domain_constants:
TK_OPEN KW_CONSTANTS typed_constant_list TK_CLOSE
| TK_OPEN KW_OBJECTS typed_constant_list TK_CLOSE
;

typed_constant_list:
typed_constant_list ne_constant_sym_list TK_HYPHEN TK_TYPE_SYMBOL
{
  ast->set_constant_type( ast->dom_constants, ast->dom_constants.size(), (Basic::TypeSymbol*)$4->val );
}
| typed_constant_list ne_constant_sym_list
{
  ast->set_constant_type( ast->dom_constants, ast->dom_constants.size(), ast->dom_top_type );
}
| /* empty */
;

ne_constant_sym_list:
ne_constant_sym_list TK_NEW_SYMBOL
{
  $2->val = new Basic::Symbol( $2->text );
  ast->dom_constants.push_back( (Basic::Symbol*)$2->val );
}
| TK_NEW_SYMBOL
{
  $1->val = new Basic::Symbol( $1->text );
  ast->dom_constants.push_back( (Basic::Symbol*)$1->val );
}
;

// structure declarations

domain_structure:
action_declaration
;

// structure declarations

action_declaration:
TK_OPEN KW_ACTION action_symbol
{
  Basic::ActionSymbol *a = new Basic::ActionSymbol( $3->text );
  ast->dom_actions.push_back( a );
  context.push_front( a );
}
action_elements TK_CLOSE
{
  // post-processing should actually be done on all actions after the complete
  // domain and problem have been read (calling PDDL_Base::post_process())
  ast->dom_actions.back()->post_process();
  ast->clear_param( current_param );
  $3->val = context.front();
  context.pop_front();
}
;

action_elements:
action_elements KW_ARGS TK_OPEN
{
  current_param.clear();
}
typed_param_list TK_CLOSE
{
  ((Basic::Complex*)context.front())->param = current_param;
}
| action_elements KW_EFFECT action_effect
| action_elements KW_PRE condition
| /* empty */
;

condition:
single_condition
| TK_OPEN KW_AND condition_list TK_CLOSE
;

condition_list:
single_condition condition_list
| single_condition
;

single_condition:
positive_atom
| negative_atom
;

positive_atom:
TK_OPEN TK_PRED_SYMBOL
{
  current_atom = new Basic::Atom( (Basic::PredicateSymbol*)$2->val );
}
atom_argument_list TK_CLOSE
{
  context.front()->pos_atm.push_back( (Basic::Atom*)current_atom );
}
| TK_OPEN TK_EQ arg_symbol arg_symbol TK_CLOSE
{
  Basic::Atom* eq_atom = new Basic::Atom( ast->dom_eq_pred );
  eq_atom->param.push_back( (Basic::Symbol*)$3->val );
  eq_atom->param.push_back( (Basic::Symbol*)$4->val );
  context.front()->pos_atm.push_back( eq_atom );
}
;

negative_atom:
TK_OPEN KW_NOT TK_OPEN TK_PRED_SYMBOL
{
  current_atom = new Basic::Atom( (Basic::PredicateSymbol*)$4->val );
  current_atom->neg = true;
}
atom_argument_list TK_CLOSE TK_CLOSE
{
  context.front()->neg_atm.push_back( (Basic::Atom*)current_atom );
}
| TK_OPEN KW_NOT TK_OPEN TK_EQ arg_symbol arg_symbol TK_CLOSE TK_CLOSE
{
  Basic::Atom* eq_atom = new Basic::Atom(ast->dom_eq_pred);
  eq_atom->neg = true;
  eq_atom->param.push_back( (Basic::Symbol*)$5->val );
  eq_atom->param.push_back( (Basic::Symbol*)$6->val );
  context.front()->neg_atm.push_back( eq_atom );
}
;

atom_argument_list:
atom_argument_list TK_VAR_SYMBOL
{
  if ($2->val == 0) {
    cout << ( "undeclared variable in atom args list" );
  }
  else {
    current_atom->param.push_back( (Basic::VariableSymbol*)$2->val );
  }
}
| atom_argument_list TK_OBJ_SYMBOL
{
  current_atom->param.push_back( (Basic::Symbol*)$2->val );
}
| /* empty */
;

action_effect:
single_action_effect
| TK_OPEN KW_AND action_effect_list TK_CLOSE
;

action_effect_list:
single_action_effect action_effect_list
| single_action_effect
;

single_action_effect:
TK_OPEN KW_FORALL TK_OPEN
{
  stored_n_param = current_param.size();
  Basic::Complex* c = new Basic::Complex();
  c -> forall = true;
  context.push_front(c);
}
typed_param_list TK_CLOSE
{
  Basic::Complex* s = (Basic::Complex*)context.front();
  for( size_t k = stored_n_param; k < current_param.size(); ++k )
    s->param.push_back( current_param[k] );
}
quantified_effect_body TK_CLOSE
{
  Basic::Complex *c = (Basic::Complex*)context.front();
  context.pop_front();
  ((Basic::ActionSymbol*)context.front())->complex.push_back( c );
  ast->clear_param( current_param, stored_n_param );
  while( current_param.size() > stored_n_param ) current_param.pop_back();
}
| TK_OPEN KW_WHEN
{
  Basic::Complex* c = new Basic::Complex();
  for( size_t k = 0; k < current_param.size(); ++k )
    c->param.push_back( current_param[k] );
  context.push_front( c );
}
condition atomic_effect_kw_list TK_CLOSE
{
  Basic::Complex *c = (Basic::Complex*)context.front();
  context.pop_front();
  ((Basic::ActionSymbol*)context.front())->complex.push_back( c );
}
| atomic_effect
| cnf_clause
{
  ((Basic::Complex*)context.front())->clauses.push_back( $1 );
}
| oneof_effect
{
  ((Basic::ActionSymbol*)context.front())->oneof.push_back( $1 );
}
;

quantified_effect_body:
TK_OPEN KW_WHEN condition atomic_effect_kw_list TK_CLOSE
| atomic_effect_kw_list
| clause_kw_list
;

atomic_effect_kw_list:
TK_OPEN KW_AND atomic_effect_list TK_CLOSE
| atomic_effect
;

atomic_effect_list:
atomic_effect_list atomic_effect
| atomic_effect
;

atomic_effect:
positive_atom_effect
| negative_atom_effect
;

positive_atom_effect:
TK_OPEN TK_PRED_SYMBOL
{
  current_atom = new Basic::Atom( (Basic::PredicateSymbol*)$2->val );
}
atom_argument_list TK_CLOSE
{
  context.front()->adds.push_back( (Basic::Atom*)current_atom );
}
;

negative_atom_effect:
TK_OPEN KW_NOT TK_OPEN TK_PRED_SYMBOL
{
  current_atom = new Basic::Atom( (Basic::PredicateSymbol*)$4->val, true );
}
atom_argument_list TK_CLOSE TK_CLOSE
{
  context.front()->dels.push_back( (Basic::Atom*)current_atom );
}
;

cnf_clause:
TK_OPEN KW_OR
{
  context.push_front( new Basic::Clause() );
}
condition_list TK_CLOSE
{
  $$ = (Basic::Clause*)context.front();
  context.pop_front();
}
;

clause_kw_list:
TK_OPEN KW_AND clause_list TK_CLOSE
| cnf_clause
{
  ((Basic::Complex*)context.front())->clauses.push_back( $1 );
}
;

clause_list:
clause_list cnf_clause
{
  ((Basic::Complex*)context.front())->clauses.push_back( $2 );
}
| cnf_clause
{
  ((Basic::Complex*)context.front())->clauses.push_back( $1 );
}
;

oneof_effect:
TK_OPEN KW_ONEOF
{
  context.push_front( new Basic::OneOf() );
}
atomic_effect_list TK_CLOSE
{
  $$ = (Basic::OneOf*)context.front();
  context.pop_front();
}
;

// problem definition

pddl_problem:
TK_OPEN KW_DEFINE TK_OPEN KW_PROBLEM any_symbol TK_CLOSE
{
  ast->problem_name = $5->text;
}
TK_OPEN KW_FORDOMAIN any_symbol TK_CLOSE problem_elements TK_CLOSE
| TK_OPEN KW_DEFINE TK_OPEN KW_PROBLEM error TK_CLOSE
{
  cerr << "syntax error in problem definition.";
}
;

problem_elements:
domain_requires problem_elements
| domain_constants problem_elements
| initial_state problem_elements 
| goal_spec
;

initial_state:
TK_OPEN KW_INIT init_elements TK_CLOSE
/*| TK_OPEN KW_INIT TK_OPEN KW_AND init_elements TK_CLOSE TK_CLOSE*/
;

init_elements:
init_elements init_atom
| init_elements cnf_clause
{
  ast->dom_init_cls.push_back( $2 );
}
| init_elements oneof_effect
{
  ast->dom_init_oneof.push_back( $2 );
}
| /* empty */
;

init_atom:
TK_OPEN TK_PRED_SYMBOL
{
  current_atom = new Basic::Atom((Basic::PredicateSymbol*)$2->val);
}
atom_argument_list TK_CLOSE
{
  Basic::PredicateSymbol* p = (Basic::PredicateSymbol*)$2->val;
  if (p->param.size() != current_atom->param.size()) {
    cerr << "wrong number of arguments for predicate in (:init ...";
  }
  //insert_atom(p->init, (Basic::Atom*)current_atom);
  ast->dom_init_atoms.push_back( (Basic::Atom*)current_atom );
}
;

goal_spec:
TK_OPEN KW_GOAL ltl_spec TK_CLOSE
{
	ast->goal_ba = new BuchiAutomaton($3);
	//cout << goal_ba -> to_s() << endl;
}
;

ltl_spec:
	positive_atom_ltl
	{
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::NN;
		$$ -> atom = (Basic::Atom*) current_atom;
	}
	|
	TK_EXCL ltl_spec
	{
		if ($2 -> op == Basic::NN){
			$2 -> atom -> neg = true;
			$$ = $2;			
		}
		else{
			$$ = new Basic::LTLNode();
			$$ -> op = Basic::NOT;
			$$ -> left = $2;		
		}
	}
	|
	TK_NEXT ltl_spec
	{	
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::NEXT;
		$$ -> left = $2;
	}	
	|
	TK_OPEN ltl_spec TK_CLOSE
	{
		$$ = $2;
	}
	|
	TK_ALW ltl_spec
	{	
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::ALW;
		$$ -> left = $2;
	}
	|
	TK_EVT ltl_spec
	{	
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::EVT;
		$$ -> left = $2;
	}
	|
	ltl_spec TK_LTL_AND ltl_spec
	{
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::AND;
		$$ -> left = $1;
		$$ -> right = $3;
	}
	|
	ltl_spec TK_LTL_OR ltl_spec
	{
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::OR;
		$$ -> left = $1;
		$$ -> right = $3;
	}
	|
	ltl_spec TK_IMPL ltl_spec
	{
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::IMPL;
		$$ -> left = $1;
		$$ -> right = $3;		
	}
	|
	ltl_spec TK_IFF ltl_spec
	{
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::IFF;
		$$ -> left = $1;
		$$ -> right = $3;		
	}
	|
	ltl_spec TK_UNTIL ltl_spec
	{
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::UNTIL;
		$$ -> left = $1;
		$$ -> right = $3;		
	}
	|
	ltl_spec TK_RELEASE ltl_spec
	{
		$$ = new Basic::LTLNode();
		$$ -> op = Basic::RELEASE;
		$$ -> left = $1;
		$$ -> right = $3;	
	}
	;
		
positive_atom_ltl:
	TK_OPEN TK_PRED_SYMBOL
	{
	  current_atom = new Basic::Atom((Basic::PredicateSymbol*)$2->val);
	}
	atom_argument_list TK_CLOSE
	;

goal_list:
single_goal goal_list
| cnf_clause goal_list
{
  dom_goal_cls.push_back( $1 );
}
| single_goal
| cnf_clause
{
  dom_goal_cls.push_back( $1 );
}
;

single_goal:
positive_atom_goal
| negative_atom_goal
;

positive_atom_goal:
TK_OPEN TK_PRED_SYMBOL
{
  current_atom = new Basic::Atom((Basic::PredicateSymbol*)$2->val);
}
atom_argument_list TK_CLOSE
{
  dom_goal_pos.push_back( (Basic::Atom*)current_atom );
  insert_atom(((Basic::Atom*)current_atom)->pred->pos_goal, (Basic::Atom*)current_atom);
}
;

negative_atom_goal:
TK_OPEN KW_NOT TK_OPEN TK_PRED_SYMBOL
{
  current_atom = new Basic::Atom((Basic::PredicateSymbol*)$4->val);
  current_atom->neg = true;
}
atom_argument_list TK_CLOSE TK_CLOSE
{
  dom_goal_neg.push_back( (Basic::Atom*)current_atom );
  insert_atom(((Basic::Atom*)current_atom)->pred->neg_goal, (Basic::Atom*)current_atom);
}
;

clause_kw_list_goal:
TK_OPEN KW_AND clause_list_goal TK_CLOSE
| cnf_clause
{
  dom_goal_cls.push_back( $1 );
}
;

clause_list_goal:
clause_list_goal cnf_clause
{
  dom_goal_cls.push_back( $2 );
}
| cnf_clause
{
  dom_goal_cls.push_back( $1 );
}
;

%%


void yy::PddlParser::error(const yy::location& l, const string& message){
	cerr << l << " : error : " << message << endl;
}
