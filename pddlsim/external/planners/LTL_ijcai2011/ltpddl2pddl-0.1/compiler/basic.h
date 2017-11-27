#ifndef BASIC_H_
#define BASIC_H_

#include <iostream>
#include <iomanip>
#include <assert.h>
#include "ptr_table.h"
#include "string_table.h"
#include "problem.h"

using namespace std;

class Basic{
	public: 
	  enum symbol_class { sym_object, sym_typename, sym_predicate, sym_action, sym_variable};
	  
	  struct Symbol {
	    symbol_class sym_class;
	    char*  print_name;
	    Symbol*      sym_type;
	    Symbol(char *n, symbol_class c = sym_object ) : sym_class(c), print_name(n), sym_type(0) {}
	    void print( std::ostream& os ) const { os << print_name; }
	  };
	
	  struct symbol_vec : public std::vector<Symbol*> { };

	  struct TypeSymbol : public Symbol {
	    symbol_vec  elements;
	    TypeSymbol(char* n) : Symbol(n,sym_typename) { }
	    void add_element(Symbol* e);
	    void print(std::ostream& s);
	  };
	  struct type_vec : public std::vector<TypeSymbol*> { };
	
	  struct VariableSymbol : public Symbol {
	    Symbol*  value;
	    VariableSymbol(char* n) : Symbol(n,sym_variable), value(0) { }
	    void print( std::ostream& os ) { os << print_name; if( sym_type ) os << " - " << sym_type->print_name; }
	  };
	  struct variable_vec : public std::vector<VariableSymbol*> { 
		  //Cast to symbol_vec
		  operator const symbol_vec();
	  };
	  
	  struct PredicateSymbol : public Symbol {
	    variable_vec param;
	    ptr_table    pos_goal;
	    ptr_table    neg_goal;
	    ptr_table    pos_prop;
	    ptr_table    neg_prop;
	    PredicateSymbol(char* n) : Symbol(n,sym_predicate) { }
	    void print(std::ostream& s);
	    void printPDDL(std::ostream& s);
	  };
	  struct predicate_vec : public std::vector<PredicateSymbol*> { };
	
	  struct AtomBase {
	    symbol_vec     param;
	    bool           neg;
	    void pushVarParams(variable_vec v);
	    AtomBase( bool n = false ) : neg(n) { }
	    bool equals(AtomBase& b);
	    void print(std::ostream& s);
	  };
	
	  struct Atom : AtomBase {
	    PredicateSymbol* pred;
	    Atom( PredicateSymbol* p, bool neg = false ) : AtomBase(neg), pred(p) { }
	    bool equals(Atom& a);
	    Instance::Atom* find_prop(Instance& ins, bool neg, bool create);
	    vector<Atom*> getInstances();
	    void print(std::ostream& s, bool neg);
	    void print(std::ostream& s) { print(s, false); }
	  };
	  struct atom_vec : public std::vector<Atom*> { };
	
	  struct Effect {
	    atom_vec adds; 
	    atom_vec dels; 
	    atom_vec pos_atm;
	    atom_vec neg_atm; 
	    void printVecPDDL(std::ostream& s, atom_vec v, bool neg = false) const;
	    void printCondPDDL(std::ostream& s) const;
	  };
	
	  struct OneOf : public Effect {
	    OneOf() { }
	    void print( std::ostream& os, size_t i = 0 ) const;
	    void build_effects( Instance& ins, Instance::Action &act );
	  };
	  struct oneof_vec : public std::vector<OneOf*> { };
	  
	  struct Clause : public Effect {
	    Clause() { }
	    void print( std::ostream& os, size_t i = 0 ) const;
	    void build_clauses( Instance& ins, index_vec_vec &cls );
	
	  };
	  struct clause_vec : public std::vector<Clause*> { };
	
	  struct Complex : public Effect {
		bool forall;
	    variable_vec   param;
	    clause_vec     clauses;
	    Complex() {forall = false;}
	    void print( std::ostream& os, size_t i = 0 ) const;
	    void printPDDL( std::ostream& os, const char* indent="") const;
	    void printClsPDDL( std::ostream& os) const;
	    void build( Instance& ins, size_t p, Instance::Action &act );
	    void build_effects( Instance& ins, Instance::Action &act, bool topl );
	    
	  };
	  struct complex_vec : public std::vector<Complex*> { };
	
	  struct ActionSymbol : public Symbol, public Complex {
		//clause_vec disj_precs; // for disjunctive preconditions
	    complex_vec complex;
	    complex_vec specialBa; // for BA representation: stores conditional effects with disjunctive conditions
	    
	    oneof_vec oneof;
	    ActionSymbol(char* n) : Symbol(n,sym_action) { }
	    void instantiate( Instance &ins );
	    void print( std::ostream& os ) const;
	    void printPDDL( std::ostream& os, char* indent = "") const;
	    void build( Instance& ins, size_t p );
	    void post_process();
	    size_t param_index(VariableSymbol* p);
	  };
	  struct action_vec : public std::vector<ActionSymbol*> { };
	  
	  /*(FP) data structures for ltl parsing */
	  enum ltl_operator {AND, OR, NOT, IMPL, ALW, EVT, UNTIL, RELEASE, NEXT, NN, IFF};
	  
	  struct LTLNode{
		  // LTL nodes with op=NN represent LITERALS
		  ltl_operator op;
		  LTLNode* left; // Significant only if op != NN
		  LTLNode* right; // Significant only if op is binary
		  Atom* atom; // Significant only if op=NN
		  
		  LTLNode(){
			  op = NN;
			  left = NULL;
			  right =NULL;
			  atom = NULL;
		  };
		  
		  ~LTLNode(){
			  if (left != NULL)
				  delete(left);
			  if (right != NULL)
				  delete(right);
			  if (atom != NULL)
				  delete(atom);
		  }
		  
		  void print(ostream &o) const;  
	  };
	  /***************************************/
	  
};

class PDDL_Name : public Name {
  bool _neg;
  Basic::Symbol* _sym;
  Basic::symbol_vec _arg;
 public:
  PDDL_Name( Basic::Symbol* sym, bool n = false ) : _neg(n), _sym(sym) { };
  PDDL_Name( Basic::Symbol* sym, Basic::symbol_vec arg, size_t n );
  PDDL_Name( Basic::Symbol* sym, Basic::variable_vec arg, size_t n );
  virtual ~PDDL_Name() { }
  void add(Basic::Symbol* s );
  virtual void write( std::ostream& s, bool cat ) const;
};





  #endif /*BASIC__H_*/
