#ifndef PDDL_BASE_H
#define PDDL_BASE_H

#include "basic.h"
#include "BuchiAutomaton.h"
#include <assert.h>
#include <vector>
#include <map>

using namespace std;

class PDDL_Base {
public:
  static bool write_warnings;
  static bool write_info;
  
  char* domain_name;
  char* problem_name;
  bool  ready_to_instantiate;

  StringTable&  tab;
  Basic::symbol_vec		dom_requirements;
  Basic::type_vec     	dom_types;
  Basic::TypeSymbol*   	dom_top_type;
  Basic::symbol_vec    	dom_constants;

  Basic::PredicateSymbol* dom_eq_pred;
  Basic::predicate_vec dom_predicates;
  Basic::action_vec    dom_actions;

  // Constants introduced in domain description or needed for BA description
  set<Basic::Symbol*> pure_constants;
  
  //(FP) Init conditions
  Basic::atom_vec      dom_init_atoms;
  Basic::clause_vec    dom_init_cls;
  Basic::oneof_vec     dom_init_oneof;
  
  //(FP) Goal requirements
  string* ltl_goal;
  BuchiAutomaton* goal_ba;

  Basic::atom_vec      dom_goal_pos;
  Basic::atom_vec      dom_goal_neg;
  Basic::clause_vec    dom_goal_cls;

  PDDL_Base(StringTable& t);
  ~PDDL_Base();

  void set_variable_type( Basic::variable_vec& vec, size_t n, Basic::TypeSymbol* t );
  void set_type_type( Basic::type_vec& vec, size_t n, Basic::TypeSymbol* t );
  void set_constant_type( Basic::symbol_vec& vec, size_t n, Basic::TypeSymbol* t );
  void clear_param( Basic::variable_vec& vec, size_t start = 0 );
  void insert_atom( ptr_table& t, Basic::AtomBase* a );
  void post_process();
  void incorporateLTL();
  
  // Returns the set of effects to reset predicates end-p
  Basic::complex_vec getEndPredResetEffects(map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> endPredMap);
  
  // Returns clauses for implications (reqLoop S) -> (currentBAState S), for all BA acceptance states S
    vector<Basic::Clause*> getReqLoopGoals(Basic::PredicateSymbol* loopPred, Basic::symbol_vec acceptanceStateSymbols, Basic::PredicateSymbol *curBAStatePred);
    
  // Starting from ba, produces all (conditional) effects (to be added to domain actions) to embed ba into the planning domain
  vector <Basic::Complex*> positiveBaCondEff(BuchiAutomaton* ba, Basic::PredicateSymbol* curP, Basic::PredicateSymbol* nextP, map<BuchiState*,Basic::Symbol*> stateMap); 
  vector <Basic::Complex*> negativeBaCondEff(BuchiAutomaton* ba, Basic::PredicateSymbol* curP, map<BuchiState*,Basic::Symbol*> stateMap); 
  
  // returns the vector of all requirements on req-pred
  vector<Basic::Clause*> getReqGoals(map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> reqPredMap, map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> nreqPredMap);
  
  // Produces a single end action, behaing as all end-pred actions in one shot
  vector<Basic::ActionSymbol*> getEndAction(map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> reqPredMap, 
		  										map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> nreqPredMap, 
		  										map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> endPredMap,
		  										Basic::PredicateSymbol *tryEndExecutedPred,
		  										Basic::PredicateSymbol *inLoopPred,
		  										Basic::PredicateSymbol *baTurnPred,
		  										Basic::PredicateSymbol *endSexecutedPred,
		  										Basic::PredicateSymbol *curBAStatePred,
		  										Basic::PredicateSymbol *loopPred);
  
  // Produces all actions end-pred actions
  vector<Basic::ActionSymbol*> getEndActions(map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> reqPredMap, 
		  										map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> nreqPredMap, 
		  										map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> endPredMap,
		  										Basic::PredicateSymbol *tryEndExecutedPred,
		  										Basic::PredicateSymbol *inLoopPred);

  void instantiate( Instance& ins );
  void print( std::ostream& s );
  void printDomainPDDL(std::ostream& s);
  void printProblemPDDL(std::ostream& s);
  Basic::PredicateSymbol* find_type_predicate( Basic::Symbol* type_sym );
};

class InstanceName : public Name {
  char* domain_name;
  char* problem_name;
 public:
  InstanceName( char* d, char* p ) : domain_name(d), problem_name(p) { }
  virtual ~InstanceName() { }
  virtual void write( std::ostream& s, bool cat ) const;
};

#endif
