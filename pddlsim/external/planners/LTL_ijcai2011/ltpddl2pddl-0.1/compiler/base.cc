
#include "base.h"
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <map>

// (FP) including assert for checking assumptions
// When defined, deactivates assert: 
#define NDEBUG
#include "assert.h"

using namespace std;

bool PDDL_Base::write_warnings = true;
bool PDDL_Base::write_info = true;

PDDL_Base::PDDL_Base(StringTable& t)
  : domain_name(0), problem_name(0),
    ready_to_instantiate(false), tab(t), dom_top_type(0), ltl_goal(NULL), goal_ba(NULL)
{
  StringTable::Cell* sc = tab.inserta("domRootType");
  dom_top_type = new Basic::TypeSymbol(sc->text);
  sc->val = dom_top_type;
  sc = tab.inserta("=");
  //sc = tab.inserta("_equiv");
  dom_eq_pred = new Basic::PredicateSymbol(sc->text);
  sc->val = dom_eq_pred;
  //dom_eq_pred->n_param = 2;
}

PDDL_Base::~PDDL_Base() {
}

void PDDL_Base::set_variable_type(Basic::variable_vec& vec, size_t n, Basic::TypeSymbol* t)
{
  for (size_t k = n; k > 0; k--) {
    if (vec[k-1]->sym_type != 0) return;
    vec[k-1]->sym_type = t;
  }
}

void PDDL_Base::set_type_type(Basic::type_vec& vec, size_t n, Basic::TypeSymbol* t)
{
  for (size_t k = vec.size(); k > 0; k--) {
    if (vec[k-1]->sym_type != 0) return;
    vec[k-1]->sym_type = t;
  }
}

void PDDL_Base::set_constant_type(Basic::symbol_vec& vec, size_t n, Basic::TypeSymbol* t)
{
  for (size_t k = n; k > 0; k--) {
    if (vec[k-1]->sym_type != 0) return;
    vec[k-1]->sym_type = t;
    t->add_element(vec[k-1]);
  }
}

void PDDL_Base::clear_param( Basic::variable_vec& vec, size_t start )
{
  for( size_t k = start; k < vec.size(); ++k )
    tab.set( vec[k]->print_name, (void*)0 );
}


void PDDL_Base::insert_atom(ptr_table& t, Basic::AtomBase* a)
{
  ptr_table* r = &t;
  for (size_t k = 0; k < a->param.size(); k++)
    r = r->insert_next(a->param[k]);
  r->val = a;
}

void PDDL_Base::post_process()
{
  for( size_t k = 0; k < dom_actions.size(); ++k )
    dom_actions[k]->post_process();
  ready_to_instantiate = true;
}


void PDDL_Base::incorporateLTL(){
	// (Function by FP)
	/*
	 * Reads the BA representing the goal and extends the domain to capture its evolution
	 * 
	 */
	// 0. record original domain predicates (without BA-dependent additions)
	vector<Basic::PredicateSymbol*> originalDomPredicates = dom_predicates;
	// EOF 0.	
	
	// 1.i Add type "_baState" to capture BA states
	// create the new type symbol
	Basic::TypeSymbol* baStateType = new Basic::TypeSymbol("baState");
	// set symbol type to the basic domain type 	
	baStateType -> sym_type = dom_top_type;
	// Add type symbol to the domain
	dom_types.push_back(baStateType);
	
	/* Removed to avoid compatibility issues with planners that do not handle subtypes
	//1.ii Add type acceptanceBAState to capture acceptance BA states 
	Basic::TypeSymbol*accBAStateType = new Basic::TypeSymbol("accBAState");
	// Set symbol type
	accBAStateType -> sym_type = baStateType;
	// Add type symbol to the domain
	dom_types.push_back(accBAStateType);
	*/
		
	// EOF 1.
	
	// 2. Fill _ba_state with all BA states
	map<BuchiState*,Basic::Symbol*> stateMap; // Associates each BuchiState of BA goal_ba to its PDDL representation
	
	vector <BuchiState*> allBAStates = goal_ba->getAllStates();
	Basic::Symbol* initStateSymbol;
	Basic::symbol_vec acceptanceStateSymbols;
	Basic::symbol_vec allStateSymbols;
	for(vector <BuchiState*>::iterator it = allBAStates.begin(); it != allBAStates.end(); it++){
		 	//create and add the new state symbol
		ostringstream sStrName;
		sStrName << "BA-" << ((*it) -> getId());
		char* sName = new char[sStrName.str().size()+1];
		strcpy(sName,sStrName.str().c_str());
		Basic::Symbol* curStateSymbol = new Basic::Symbol(sName);
			// Associates current BA state to its corresponding PDDL Symbol (for future use)
		stateMap[*it]=curStateSymbol;
		
		if ((*it) == goal_ba -> getInit()){// Record the initial state symbol for future use
			initStateSymbol = curStateSymbol;
		}
		if ((*it) -> isAcceptance()){// Record acceptance state symbols for future use
			acceptanceStateSymbols.push_back(curStateSymbol);
		}
		allStateSymbols.push_back(curStateSymbol);
		dom_constants.push_back(curStateSymbol);
		pure_constants.insert(curStateSymbol);
	}
	// set types of all new constants, at once, to baStateType created in 1.
	set_constant_type(allStateSymbols, allStateSymbols.size(), baStateType);
	// EOF 2.
	
	// 3. Add BA-related predicates  
	
	// currentBAstate
	char* curBAStatePredName = "currentBAstate";
	Basic::PredicateSymbol *curBAStatePred = new Basic::PredicateSymbol(curBAStatePredName);
	// Create the parameter list  
	Basic::variable_vec predParams;
	predParams.push_back(new Basic::VariableSymbol("?state"));
	set_variable_type(predParams,predParams.size(),baStateType);
	// Set predicate param list
	curBAStatePred -> param = predParams;
	// Add the predicate to the domain
	dom_predicates.push_back(curBAStatePred);
	
	//acceptance
	char* acceptanceBAStatePredName = "acceptanceBAState";
	Basic::PredicateSymbol* acceptanceBAStatePred = new Basic::PredicateSymbol(acceptanceBAStatePredName);
	// re-use above param list
	predParams.clear();
	predParams.push_back(new Basic::VariableSymbol("?state"));
	set_variable_type(predParams,predParams.size(),baStateType);
	
	acceptanceBAStatePred -> param = predParams;//builds a copy of predParams
	// Add the predicate to the domain
	dom_predicates.push_back(acceptanceBAStatePred);
	
	//loopStarts
	char* loopStartsPredName = "loopStarted";
	Basic::PredicateSymbol* loopStartsPred = new Basic::PredicateSymbol(loopStartsPredName);
	// no parameters
	dom_predicates.push_back(loopStartsPred);	
	
	//BAturn
	char* baTurnPredName = "BAturn";
	Basic::PredicateSymbol* baTurnPred = new Basic::PredicateSymbol(baTurnPredName);
	// no parameters
	dom_predicates.push_back(baTurnPred);
	
	//moveBA-1-done
	char* moveBA1donePredName = "moveBA-1-done";
	Basic::PredicateSymbol* moveBA1Done = new Basic::PredicateSymbol(moveBA1donePredName);
	// no parameters
	dom_predicates.push_back(moveBA1Done);

	//nextBAStatePred
	char* nextBAstateName = "nextBAstate";
	Basic::PredicateSymbol* nextBAStatePred = new Basic::PredicateSymbol(nextBAstateName);
	// re-use above param list
	predParams.clear();
	predParams.push_back(new Basic::VariableSymbol("?state"));
	set_variable_type(predParams,predParams.size(),baStateType);
	nextBAStatePred -> param = predParams;//builds a copy of predParams

	dom_predicates.push_back(nextBAStatePred);

	// BAinAcceptanceState
	char* inLoopPredName = "inLoop";
	Basic::PredicateSymbol *inLoopPred = new Basic::PredicateSymbol(inLoopPredName);
	// parameter: 
	
	dom_predicates.push_back(inLoopPred);
	
	// TryEndExecuted
	char* tryEndExecutedPredName = "endAllExecuted";
	Basic::PredicateSymbol *tryEndExecutedPred = new Basic::PredicateSymbol(tryEndExecutedPredName);
	// no parameters
	dom_predicates.push_back(tryEndExecutedPred);
	
	// predicate end-BA to signal that the requested acceptance BA state has been reached
	char* endSexecutedPredName = "end-BA";
	Basic::PredicateSymbol* endSexecutedPred = new Basic::PredicateSymbol(endSexecutedPredName);
	dom_predicates.push_back(endSexecutedPred);	
	
	// nopExecuted (needed to state that after nop has been executed, no other regular action can be executed)
	char* nopExecutedPredName = "nopExecuted";
	Basic::PredicateSymbol *nopExecutedPred = new Basic::PredicateSymbol(nopExecutedPredName);
	// no parameters
	dom_predicates.push_back(nopExecutedPred);
	//
	// EOF 3.
	
	// 4. Set Buchi initial state to current state
		// create predicate Atom 
	Basic::Atom* initBAAtom = new Basic::Atom(curBAStatePred);
		// fill the atom with the initial BA state as a term
	initBAAtom -> param.push_back(initStateSymbol);
		// add the atom to the domain
	dom_init_atoms.push_back(initBAAtom);
	// EOF 4.
	
	// 5. Initialize acceptance BA states according to goal_ba
		// Fill finalBaStatePred w/ BA final states
	for(vector<Basic::Symbol*>::iterator it = acceptanceStateSymbols.begin(); it != acceptanceStateSymbols.end(); it++){
		Basic::Atom* accBAAtom = new Basic::Atom(acceptanceBAStatePred);
		accBAAtom -> param.push_back(*it);
		dom_init_atoms.push_back(accBAAtom);		
	}
	// EOF 5.
	
	// 6. 
	// Add predicates req-pred, nreq-pred, and end-pred for each predicate pred(...) in original specification
	// ( Needed to capture meta-predicate req(pred(...)) )	
	map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> reqPredMap; // Associates each predicate pred to its req-pred counterpart
	map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> nreqPredMap; // Associates each predicate pred to its nreq-pred counterpart
	map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> endPredMap; // Associates each predicate pred to its end-pred counterpart
	
	for(vector<Basic::PredicateSymbol*>::iterator it=originalDomPredicates.begin(); it != originalDomPredicates.end(); it++){
		// req-
		// Prepare name string
		ostringstream reqPredName;
		reqPredName << "req-" << (*it) -> print_name;
		char* name = new char[reqPredName.str().size()+1];
		strcpy(name,reqPredName.str().c_str());
		// Copy current predicate symbol
		Basic::PredicateSymbol* reqPred = new Basic::PredicateSymbol(*(*it));
		// change predicate name
		reqPred -> print_name = name;
		// Add topredicate vector
		dom_predicates.push_back(reqPred);
		// Insert into map
		reqPredMap[*it] = reqPred;
		
		// nreq-
		// Prepare name string 
		ostringstream nreqPredName;
		nreqPredName << "nreq-" << (*it) -> print_name;
		char* nname = new char[nreqPredName.str().size()+1];
		strcpy(nname,nreqPredName.str().c_str());
		// Copy current predicate symbol
		Basic::PredicateSymbol* nreqPred = new Basic::PredicateSymbol(*(*it));
		// change predicate name
		nreqPred -> print_name = nname;
		// Add topredicate vector
		dom_predicates.push_back(nreqPred);
		// Insert into map
		nreqPredMap[*it] = nreqPred;		
		
		// end-pred
		// Prepare name string 
		ostringstream endPredName;
		endPredName << "end-" << (*it) -> print_name;
		char* endName = new char[endPredName.str().size()+1];
		strcpy(endName,endPredName.str().c_str());
		// Copy current predicate symbol
		Basic::PredicateSymbol* endPred = new Basic::PredicateSymbol(*(*it));
		// change predicate name
		endPred -> print_name = endName;
		// Add topredicate vector
		dom_predicates.push_back(endPred);
		// Insert into map
		endPredMap[*it] = endPred;		
	}
	// EOF 6.
	
	// 7. Add predicate reqLoop(?s - _ba_state), used to record which BA state the loop has been requested for
	// 
	Basic::PredicateSymbol *loopPred = new Basic::PredicateSymbol("reqLoop");
	Basic::variable_vec loopPredParams;
	loopPredParams.push_back(new Basic::VariableSymbol("?state"));
	set_variable_type(loopPredParams,loopPredParams.size(),baStateType);
	loopPred -> param = loopPredParams;
	dom_predicates.push_back(loopPred);
	// EOF 7.
	
	
	// 8. Add action nop (added here, to be processed next, like a regular action)
	Basic::ActionSymbol* nopAction = new Basic::ActionSymbol("nop");
	
	//no parameters
	
	/* PRECONDITION: nop is the first action of the loop (there is no reason why executing it otherwise: 
	 * it can only be used to loop at the end of plan)
	*/
	// nop execution will inhibited by step 8.i
	
	Basic::Atom* nopPre2 = new Basic::Atom(loopStartsPred);	
	nopAction -> pos_atm.push_back(nopPre2);
	
	//EFFECT: nop has been executed (i.e., nopExecutedPred is true)
	Basic::Atom* nopPost = new Basic::Atom(nopExecutedPred);
	nopAction -> adds.push_back(nopPost);
	dom_actions.push_back(nopAction);
	//
	
	// Record all domain original actions (including nop) to distinguish between them and actions introduce for BA 
	Basic::action_vec originalDomActions = dom_actions;
	
	// 8.ii Add action moveBA
	/* 
	 * MoveBA is actually composed of 2 actions moveBA-1 and moveBA-2
	 * moveBA-1: i. stores the states that BA will move to next, into predicate nextBAstate; ii. resets currentBAState; iii.sets moveBa-1-done
	 * moveBA-2: i. fills currentBAstate with states from nextBAstate; ii. empties nextBAstate; iii. unsets moveBa-1-done; iv. unsets BAturn 
	 * Predicate moveBA-1-done (initialized false) is used to enable (only) moveBA-2 executions
	 */
	
	// MoveBA-1
	Basic::ActionSymbol* moveBaAction1 = new Basic::ActionSymbol("moveBA-1");
	// NO PARAMETERS
	// PRECONDITION
	// It's BA turn and not move-BA-1's 
	moveBaAction1 -> pos_atm.push_back(new Basic::Atom(baTurnPred));
	moveBaAction1 -> neg_atm.push_back(new Basic::Atom(moveBA1Done,true));
	// tryEndAction not executed yet
	moveBaAction1 -> neg_atm.push_back(new Basic::Atom(tryEndExecutedPred,true));
	// EFFECT
	// moveBA-1-done becomes true
	moveBaAction1 -> adds.push_back(new Basic::Atom(moveBA1Done));
	// Get all positive moveBA-1 effects:
	vector<Basic::Complex*> moveBA1Effects = positiveBaCondEff(goal_ba, curBAStatePred, nextBAStatePred, stateMap);	
	// Iterate on all positive effects:
	for (vector<Basic::Complex*>::iterator pit=moveBA1Effects.begin(); pit != moveBA1Effects.end(); pit++){
		moveBaAction1 -> complex.push_back(*pit);
	}
	// reset end-S
	moveBaAction1 -> dels.push_back(new Basic::Atom(endSexecutedPred,false));
	
	// Resets currentBAState
	for (int i =0; i<allStateSymbols.size(); i++){
		Basic::Atom* atom = new Basic::Atom(curBAStatePred,false);
		atom -> param.push_back(allStateSymbols[i]);
		moveBaAction1 -> dels.push_back(atom);
	}	

	
	dom_actions.push_back(moveBaAction1);
	// EOF MoveBA-1
	
	// MoveBA-2
	Basic::ActionSymbol* moveBaAction2 = new Basic::ActionSymbol("moveBA-2");
	// NO PARAMETERS
	// PRECONDITION
	// move-BA-1 turn 
	moveBaAction2 -> pos_atm.push_back(new Basic::Atom(moveBA1Done));
	// EFFECT
	// moveBA-1-done becomes false
	moveBaAction2 -> dels.push_back(new Basic::Atom(moveBA1Done));
	// BAturn becomes false
	moveBaAction2 -> dels.push_back(new Basic::Atom(baTurnPred));
	// Sets currentBAState
	for (int i =0; i<allStateSymbols.size(); i++){
		Basic::Atom* ant = new Basic::Atom(nextBAStatePred);
		ant -> param.push_back(allStateSymbols[i]);
		Basic::Atom* cons = new Basic::Atom(curBAStatePred);
		cons -> param.push_back(allStateSymbols[i]);
		
		Basic::Complex* condeff = new Basic::Complex();
		condeff -> pos_atm.push_back(ant);
		condeff -> adds.push_back(cons);
		moveBaAction2 -> complex.push_back(condeff);
	}	
	// Resets nextBAState
	for (int i =0; i<allStateSymbols.size(); i++){
		Basic::Atom* atom = new Basic::Atom(nextBAStatePred);
		atom -> param.push_back(allStateSymbols[i]);
		moveBaAction2 -> dels.push_back(atom);
	}
	dom_actions.push_back(moveBaAction2);
	// EOF MoveBA-2

	/*	Replaced by moveBa1 and moveBA2
	// Positive moveBA effects:
	vector<Basic::Complex*> baEffects = positiveBaCondEff(goal_ba, curBAStatePred, curBAStatePred, stateMap);
	// Negative moveBA effects:
	vector<Basic::Complex*> negativeBaEffects = negativeBaCondEff(goal_ba, curBAStatePred, stateMap);

	Basic::ActionSymbol* moveBaAction = new Basic::ActionSymbol("moveBA");
	//no parameters	
	// PRECONDITION: it's BA turn
	Basic::Atom* moveBaAtom = new Basic::Atom(baTurnPred);	
	moveBaAction -> pos_atm.push_back(moveBaAtom);
	// tryEndAction not executed yet
	Basic::Atom* moveBaTryAtom = new Basic::Atom(tryEndExecutedPred);	
	moveBaTryAtom -> neg = true;
	moveBaAction -> neg_atm.push_back(moveBaTryAtom);		
	//
	//EFFECT: 
	// Iterate on all positive BA effects:
	for (vector<Basic::Complex*>::iterator pit=baEffects.begin(); pit != baEffects.end(); pit++){
		moveBaAction -> complex.push_back(*pit);
	}
	// Iterate on all negative BA effects:
	for (vector<Basic::Complex*>::iterator nit=negativeBaEffects.begin(); nit != negativeBaEffects.end(); nit++){
		moveBaAction -> specialBa.push_back(*nit);
	}
	// Sets baTurnPred false
	Basic::Atom* nbaTurnAtom = new Basic::Atom(baTurnPred);
	nbaTurnAtom -> neg = true;
	moveBaAction -> dels.push_back(nbaTurnAtom);

	dom_actions.push_back(moveBaAction);
	*/
	
	// EOF 8.
	
	// 9. Add action loopHere(?state - s)
	Basic::ActionSymbol* loopAction = new Basic::ActionSymbol("loopHere");
	// Action Params
	loopAction -> param.push_back(new Basic::VariableSymbol("?state"));
	set_variable_type(loopAction->param,loopAction->param.size(),baStateType);
	
	// PRECONDITION: ?state is an acceptance state AND it is a state where the BA is currently in AND 
	// no other _loop_here(?s) has been previously requested (i.e., loopStarted is false)
	// Can be executed only after Ba has moved
	Basic::Atom* nbaTurnAtom = new Basic::Atom(baTurnPred,true);
	loopAction -> neg_atm.push_back(nbaTurnAtom);
	
	Basic::Atom* accStateAtom = new Basic::Atom(acceptanceBAStatePred);	// acceptanceBAStatePred defined above
	accStateAtom -> param.push_back(new Basic::VariableSymbol("?state"));
	loopAction -> pos_atm.push_back(accStateAtom);
	//
	Basic::Atom* loopCurStateAtom = new Basic::Atom(curBAStatePred);// curBAStatePred defined above
	loopCurStateAtom -> param.push_back(new Basic::VariableSymbol("?state"));
	loopAction -> pos_atm.push_back(loopCurStateAtom);
	//
	Basic::Atom* nloopAtom = new Basic::Atom(loopStartsPred);
	nloopAtom -> neg = true;
	loopAction -> neg_atm.push_back(nloopAtom);
	//
	loopAction -> neg_atm.push_back(new Basic::Atom(tryEndExecutedPred,false));
	
	
	// EFFECT
	// loop(?state) is true
	Basic::Atom* nextLoopAtom = new Basic::Atom(loopPred);
	nextLoopAtom -> param.push_back(new Basic::VariableSymbol("?state"));
	loopAction -> adds.push_back(nextLoopAtom);
	
	//loopStarts is true
	//(Defined above): Basic::Atom* loopStartsAtom = new Basic::Atom(loopStartsPred);
	loopAction -> adds.push_back(new Basic::Atom(loopStartsPred));
	
	// The BA is in state ?state AND not in any other state
	Basic::Atom* nextStateAtom = new Basic::Atom(curBAStatePred);
	nextStateAtom -> param.push_back(new Basic::VariableSymbol("?state"));
	loopAction -> adds.push_back(nextStateAtom);
	
	Basic::Complex* nextBAComplex = new Basic::Complex();
	nextBAComplex -> forall = true;
	nextBAComplex -> param.push_back(new Basic::VariableSymbol("?s"));
	set_variable_type(nextBAComplex->param,nextBAComplex->param.size(),baStateType);
	
	Basic::PredicateSymbol* predEq = new Basic::PredicateSymbol("=");
	Basic::variable_vec predEqParams;
	predEqParams.push_back(new Basic::VariableSymbol("?x"));
	predEqParams.push_back(new Basic::VariableSymbol("?y"));
	set_variable_type(predEqParams,predEqParams.size(),dom_top_type);
	predEq -> param = predEqParams;
	
	Basic::Atom* headAtom = new Basic::Atom(predEq);
	headAtom -> neg = true;
	headAtom->param.push_back(new Basic::VariableSymbol("?state"));
	headAtom->param.push_back(new Basic::VariableSymbol("?s"));
	nextBAComplex->neg_atm.push_back(headAtom);
	
	Basic::Atom* tailAtom = new Basic::Atom(curBAStatePred);
	tailAtom->neg=true;
	tailAtom->param.push_back(new Basic::VariableSymbol("?s"));
	nextBAComplex->dels.push_back(tailAtom);
	
	loopAction -> complex.push_back(nextBAComplex);
	//
			
	
	// Update requests for literals to be achieved in last state
	for(vector<Basic::PredicateSymbol*>::iterator it = originalDomPredicates.begin(); it != originalDomPredicates.end(); it++){
		// Positive Literals
		Basic::Complex* forallReq = new Basic::Complex();
		forallReq -> forall = true;
		forallReq -> param = (*it) -> param;
		Basic::Atom* h = new Basic::Atom(*it);
		for (vector<Basic::VariableSymbol*>::iterator it2 = (*it)->param.begin(); it2 != (*it) -> param.end(); it2++){			
			h -> param.push_back((Basic::Symbol*) *it2);
		}
		forallReq -> pos_atm.push_back(h);
		//
		Basic::Atom* t = new Basic::Atom((reqPredMap[*it]));
		for (vector<Basic::VariableSymbol*>::iterator it2 = (*it)->param.begin(); it2 != (*it) -> param.end(); it2++){			
			t -> param.push_back((Basic::Symbol*) *it2);
		}
		forallReq -> adds.push_back(t);				
		loopAction -> complex.push_back(forallReq);
		
		// Negative Literals
		Basic::Complex* nforallReq = new Basic::Complex();
		nforallReq -> forall = true;
		nforallReq -> param = (*it) -> param;
		Basic::Atom* nh = new Basic::Atom(*it);
		nh -> neg = true;
		for (vector<Basic::VariableSymbol*>::iterator it2 = (*it)->param.begin(); it2 != (*it) -> param.end(); it2++){			
			nh -> param.push_back((Basic::Symbol*) *it2);
		}
		nforallReq -> neg_atm.push_back(nh);
		//
		Basic::Atom* nt = new Basic::Atom((nreqPredMap[*it]));
		for (vector<Basic::VariableSymbol*>::iterator it2 = (*it)->param.begin(); it2 != (*it) -> param.end(); it2++){			
			nt -> param.push_back((Basic::Symbol*) *it2);
		}
		nforallReq -> adds.push_back(nt);
		loopAction -> complex.push_back(nforallReq);		
	}
	// Add loopAction to domain
	dom_actions.push_back(loopAction);
	
	
	
	// 9.i add action tryEndAction
	Basic::ActionSymbol* tryEndAction = new Basic::ActionSymbol("tryEndAction");
	// No params
	// Precondition: tryEndAction not executed yet && inLoop && not BATurn
	tryEndAction -> neg_atm.push_back(new Basic::Atom(tryEndExecutedPred,true));
	tryEndAction -> pos_atm.push_back(new Basic::Atom(inLoopPred));
	tryEndAction -> neg_atm.push_back(new Basic::Atom(baTurnPred,true));
	
	// Effect: tryEndExecuted
	tryEndAction -> adds.push_back(new Basic::Atom(tryEndExecutedPred));	
	//
	// dom_actions.push_back(tryEndAction);
	
	// 9.ii add action end-BA 
	Basic::ActionSymbol* endSAction = new Basic::ActionSymbol("end-BA");
	// Params ?s
		Basic::VariableSymbol* actParam = new Basic::VariableSymbol("?s");
		endSAction -> param.push_back(actParam);
		set_variable_type(endSAction->param,endSAction->param.size(),baStateType);

	// Precondition
		// ?s is a BA acceptance state
		Basic::Atom* acceptanceStateAtom = new Basic::Atom(acceptanceBAStatePred);
		acceptanceStateAtom -> param.push_back(actParam);
		
		// Inside loop
		endSAction -> pos_atm.push_back(new Basic::Atom(inLoopPred));
		
		// ?s is current ba-state
		Basic::Atom* inBAState = new Basic::Atom(curBAStatePred);
		inBAState -> param.push_back(actParam);
		endSAction -> pos_atm.push_back(inBAState);
		
		// ?s is the state that the loop was requested for
		Basic::Atom* loopReqState = new Basic::Atom(loopPred);
		loopReqState -> param.push_back(actParam);
		endSAction -> pos_atm.push_back(loopReqState);
		
		// tryEndAction has been executed before
		endSAction -> pos_atm.push_back(new Basic::Atom(tryEndExecutedPred));

	// Effect
	endSAction -> adds.push_back(new Basic::Atom(endSexecutedPred));
	//endSAction -> adds.push_back(new Basic::Atom(tryEndExecutedPred));
	
	// Add endSAction to domain
	// dom_actions.push_back(endSAction);	
	//
	
	// 9.iii add actions End1-pred and End2-pred
	// Add all end-pred actions to domain
	vector<Basic::ActionSymbol*> endActions = getEndAction(reqPredMap, nreqPredMap, endPredMap, tryEndExecutedPred, 
															inLoopPred, baTurnPred,endSexecutedPred, curBAStatePred, loopPred);
	for (vector<Basic::ActionSymbol*>::iterator it = endActions.begin(); it != endActions.end(); it++){
		dom_actions.push_back(*it);
	}
	
	// 9.iv Modify original actions (stored in originalDomActions)
	//Iterate on all actions to manage inLoop predicate and to reset end-p when executed
	
	//prepare inLoop effect
	Basic::Complex* inLoopEffect = new Basic::Complex();
	inLoopEffect -> pos_atm.push_back(new Basic::Atom(loopStartsPred));
	inLoopEffect -> adds.push_back(new Basic::Atom(inLoopPred));
	
	// prepare unconditioned effects that reset all end-p predicates
	Basic::complex_vec endPredResetEffects = getEndPredResetEffects(endPredMap);
	
	for (vector<Basic::ActionSymbol*>::iterator it=originalDomActions.begin(); it != originalDomActions.end(); it++){
		// precondition
		Basic::Atom* nbaTurnAtom = new Basic::Atom(baTurnPred);
		nbaTurnAtom -> neg = true;
		Basic::Atom* nopPre = new Basic::Atom(nopExecutedPred);	
		(*it) -> neg_atm.push_back(nbaTurnAtom);
		(*it) -> neg_atm.push_back(nopPre); // action "nop" has not been executed (as, when executed, this has to be the last one)
		(*it) -> complex.push_back(inLoopEffect);
		
		/*
		for(int i =0; i<endPredResetEffects.size(); i++){
			(*it) -> complex.push_back(endPredResetEffects[i]);
		}
		*/
		(*it) -> neg_atm.push_back(new Basic::Atom(tryEndExecutedPred,true));
		
		// effect
		Basic::Atom* baTurnAtom = new Basic::Atom(baTurnPred);
		nbaTurnAtom -> neg = false;

		(*it) -> adds.push_back(baTurnAtom);
	}		
	
	// EOF 9.
	
	// 10. Initialization of new predicates
	
	// init and goal
	
	//baTurnPred
	//init:
	Basic::Atom* baTurnAtom = new Basic::Atom(baTurnPred);
	baTurnAtom -> neg = false;
	dom_init_atoms.push_back(baTurnAtom);	
		
	Basic::Atom* nloopStartsAtom = new Basic::Atom(loopStartsPred);
	nloopStartsAtom -> neg = true;
	// not needed in init
	// dom_init_atoms.push_back(nloopStartsAtom);
	
	//goal:
	// ensure that loopHere is executed and we got into the loop
	dom_goal_pos.push_back(new Basic::Atom(inLoopPred));
	// loopStartspred is redunant as implied by inLoopPred. Though, it informative to planners
	dom_goal_pos.push_back(new Basic::Atom(loopStartsPred));
	
	// We want moveBA to be executed last
	// nbaTurnAtom defined above
	dom_goal_neg.push_back(nbaTurnAtom);
	
	
	
	for (map<Basic::PredicateSymbol*,Basic::PredicateSymbol*>::iterator it = endPredMap.begin(); it != endPredMap.end(); it++){
		Basic::Atom* curAtm = new Basic::Atom(it -> second);
		curAtm -> pushVarParams(it -> second -> param);		
		vector<Basic::Atom*> endAtms = curAtm -> getInstances();
		for (vector<Basic::Atom*>::iterator ita = endAtms.begin(); ita != endAtms.end(); ita++){
			dom_goal_pos.push_back(*ita);
		}
	}
	
	dom_goal_pos.push_back(new Basic::Atom(endSexecutedPred));
		
	// loop
	
	Basic::Atom* initLoop = new Basic::Atom(loopPred);
	for (vector<Basic::VariableSymbol*>::iterator it2 = loopPred->param.begin(); it2 != loopPred -> param.end(); it2++){			
		initLoop -> param.push_back((Basic::Symbol*) *it2);
	}
	vector<Basic::Atom*> loopAtoms = initLoop -> getInstances();
	
	/*
	// (reqLoop S -> currentState S), not necessary -- sometimes it improves efficiency
	vector<Basic::Clause*> reqGoals = getReqLoopGoals(loopPred, acceptanceStateSymbols, curBAStatePred);
	for (int i = 0; i < reqGoals.size(); i++){
		dom_goal_cls.push_back(reqGoals[i]);
	}
	*/
}


Basic::complex_vec PDDL_Base::getEndPredResetEffects(map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> endPredMap){
	// prepared unconditioned effects that reset all end-p predicates	
	Basic::complex_vec endPredResetEffects;
	// loop on all end-pred predicates
	for (map<Basic::PredicateSymbol*,Basic::PredicateSymbol*>::iterator it = endPredMap.begin(); it != endPredMap.end(); it++){
		Basic::Atom* curAtm = new Basic::Atom(it -> second, true);
		curAtm -> pushVarParams(it -> second -> param);
		//
		Basic::Complex* forallParamsReset = new Basic::Complex();
		forallParamsReset -> forall = true;
		forallParamsReset -> param = it -> second -> param;		
		forallParamsReset -> dels.push_back(curAtm);
	
		endPredResetEffects.push_back(forallParamsReset);
	}	
	return endPredResetEffects;
}



vector<Basic::Clause*> PDDL_Base::getReqLoopGoals(Basic::PredicateSymbol* loopPred, 
													Basic::symbol_vec acceptanceStateSymbols, 
													Basic::PredicateSymbol *curBAStatePred){
	vector<Basic::Clause*> result;
	for (int i = 0; i < acceptanceStateSymbols.size(); i++){
		Basic::Atom* loopAtm = new Basic::Atom(loopPred,true);
		loopAtm -> param.push_back(acceptanceStateSymbols[i]);	
		Basic::Atom* curAtm = new Basic::Atom(curBAStatePred);
		curAtm -> param.push_back(acceptanceStateSymbols[i]);
		Basic::Clause* cls = new Basic::Clause();
		
		cls->neg_atm.push_back(loopAtm);
		cls->pos_atm.push_back(curAtm);
		result.push_back(cls);
	}
	return result;
}

vector<Basic::ActionSymbol*> PDDL_Base::getEndAction(map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> reqPredMap, 
														map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> nreqPredMap, 
														map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> endPredMap,
														Basic::PredicateSymbol *tryEndExecutedPred,
														Basic::PredicateSymbol *inLoopPred,
														Basic::PredicateSymbol *baTurnPred,
				  										Basic::PredicateSymbol *endSexecutedPred,
				  										Basic::PredicateSymbol *curBAStatePred,
				  										Basic::PredicateSymbol *loopPred){
	
	vector<Basic::ActionSymbol*> result; // return a vector for compatiblity (and for flexiblity)

	// Prepare end Action
	Basic::ActionSymbol* endAction = new Basic::ActionSymbol("endAll");
	// Precondition
	endAction -> neg_atm.push_back(new Basic::Atom(tryEndExecutedPred,true));
	endAction -> neg_atm.push_back(new Basic::Atom(baTurnPred,true));
	endAction -> pos_atm.push_back(new Basic::Atom(inLoopPred));
	
	// Effect
	endAction -> adds.push_back(new Basic::Atom(tryEndExecutedPred));
	
	// Iterate on all end-p predicates
	for (map<Basic::PredicateSymbol*,Basic::PredicateSymbol*>::iterator it = endPredMap.begin(); it != endPredMap.end(); it++){
		
		// create conditional effect for positive req-p
		
		Basic::Complex* condEffPos = new Basic::Complex();
		Basic::variable_vec params = it -> first -> param;
		
		condEffPos -> forall = (params.size() > 0);
		condEffPos -> param = params;
		
		Basic::Atom* atm1 = new Basic::Atom(reqPredMap[it -> first]);
		atm1 -> param = params;		
		condEffPos -> pos_atm.push_back(atm1);
		
		Basic::Atom* atm2 = new Basic::Atom(it -> first);
		atm2 -> param = params;		
		condEffPos -> pos_atm.push_back(atm2);
		
		Basic::Atom* atm3 = new Basic::Atom(endPredMap[it -> first]);
		atm3 -> param = params;		
		condEffPos -> adds.push_back(atm3);
		
		endAction -> complex.push_back(condEffPos);
		
		// create conditional effect for negative req-p
		
		Basic::Complex* condEffNeg = new Basic::Complex();
		
		condEffNeg -> forall = (params.size() > 0);
		condEffNeg -> param = params;
		
		atm1 = new Basic::Atom(nreqPredMap[it -> first]);
		atm1 -> param = params;		
		condEffNeg -> pos_atm.push_back(atm1);
		
		atm2 = new Basic::Atom(it -> first,true);
		atm2 -> param = params;		
		condEffNeg -> neg_atm.push_back(atm2);
		
		condEffNeg -> adds.push_back(atm3);
		
		endAction -> complex.push_back(condEffNeg);
	}
	
	// create conditional effect for end-Ba
	Basic::variable_vec params = curBAStatePred -> param;
	Basic::Complex* baCondEff = new Basic::Complex();
	
	baCondEff -> forall = true;
	baCondEff -> param = params;
	
	Basic::Atom *atm1 = new Basic::Atom(curBAStatePred);
	atm1 -> param = curBAStatePred -> param;
	baCondEff -> pos_atm.push_back(atm1);
	
	Basic::Atom *atm2 = new Basic::Atom(loopPred);
	atm2 -> param = params;
	baCondEff -> pos_atm.push_back(atm2);
	
	baCondEff -> adds.push_back(new Basic::Atom(endSexecutedPred));
	
	endAction -> complex.push_back(baCondEff);
	
	// add to result
	result.push_back(endAction);
	
	return result;
}





vector<Basic::ActionSymbol*> PDDL_Base::getEndActions(map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> reqPredMap, 
														map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> nreqPredMap, 
														map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> endPredMap,
														Basic::PredicateSymbol *tryEndExecutedPred,
														Basic::PredicateSymbol *inLoopPred){
	vector<Basic::ActionSymbol*> result;
	// Iterate over all end-pred actions
	for (map<Basic::PredicateSymbol*,Basic::PredicateSymbol*>::iterator it = endPredMap.begin(); it != endPredMap.end(); it++){
		ostringstream actName1;
		actName1 << "end-1-" << it -> first -> print_name;
		char* cActName1 = new char[actName1.str().size()+1];
		strcpy(cActName1,actName1.str().c_str());
		// Create action
		Basic::ActionSymbol* endAct1 = new Basic::ActionSymbol(cActName1);
		// params
		endAct1 -> param = it -> second -> param;
		// precondition
		endAct1 -> pos_atm.push_back(new Basic::Atom(tryEndExecutedPred));
		endAct1 -> pos_atm.push_back(new Basic::Atom(inLoopPred));		
		Basic::PredicateSymbol* precPred11 = reqPredMap[it -> first];
		Basic::Atom* precAtm11 = new Basic::Atom(precPred11);
		Basic::variable_vec pv11 = precPred11 -> param;
		for (Basic::variable_vec::iterator vit = pv11.begin(); vit != pv11.end(); vit++){
			precAtm11 -> param.push_back(*vit);
		}
		endAct1 -> pos_atm.push_back(precAtm11);
		
		Basic::PredicateSymbol* precPred12 = it -> first;
		Basic::Atom* precAtm12 = new Basic::Atom(precPred12);
		Basic::variable_vec pv12 = precPred12 -> param;
		for (Basic::variable_vec::iterator vit = pv12.begin(); vit != pv12.end(); vit++){
			precAtm12 -> param.push_back(*vit);
		}
		endAct1 -> pos_atm.push_back(precAtm12);
		
		// effect
		Basic::Atom* addAtm1 = new Basic::Atom(it -> second);
		Basic::variable_vec v = it -> second -> param;
		for (Basic::variable_vec::iterator vit = v.begin(); vit != v.end(); vit++){
			addAtm1 -> param.push_back(*vit);
		}
		endAct1 -> adds.push_back(addAtm1);
		
		// add action to result
		result.push_back(endAct1);
		
		ostringstream actName2;
		actName2 << "end-2-" << it -> first -> print_name;
		char* cActName2 = new char[actName2.str().size()+1];
		strcpy(cActName2,actName2.str().c_str());
		// Create action
		Basic::ActionSymbol* endAct2 = new Basic::ActionSymbol(cActName2);
		// params
		endAct2 -> param = it -> second -> param;
		// precondition
		endAct2 -> pos_atm.push_back(new Basic::Atom(tryEndExecutedPred));
		endAct2 -> pos_atm.push_back(new Basic::Atom(inLoopPred));		
		Basic::PredicateSymbol* precPred21 = nreqPredMap[it -> first];
		Basic::Atom* precAtm21 = new Basic::Atom(precPred21);
		Basic::variable_vec pv21 = precPred21 -> param;
		for (Basic::variable_vec::iterator vit = pv21.begin(); vit != pv21.end(); vit++){
			precAtm21 -> param.push_back(*vit);
		}
		endAct2 -> pos_atm.push_back(precAtm21);
		
		Basic::PredicateSymbol* precPred22 = it -> first;
		Basic::Atom* precAtm22 = new Basic::Atom(precPred22);
		precAtm22 -> neg = true;
		Basic::variable_vec pv22 = precPred22 -> param;
		for (Basic::variable_vec::iterator vit = pv22.begin(); vit != pv22.end(); vit++){
			precAtm22 -> param.push_back(*vit);
		}
		endAct2 -> neg_atm.push_back(precAtm22);
		
		// effect
		Basic::Atom* addAtm2 = new Basic::Atom(it -> second);
		Basic::variable_vec v2 = it -> second -> param;
		for (Basic::variable_vec::iterator vit = v2.begin(); vit != v2.end(); vit++){
			addAtm2 -> param.push_back(*vit);
		}
		endAct2 -> adds.push_back(addAtm2);
		
		// add action to result
		result.push_back(endAct2);
	}
	return result;
}


vector<Basic::Clause*> PDDL_Base::getReqGoals(map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> reqPredMap, map<Basic::PredicateSymbol*,Basic::PredicateSymbol*> nreqPredMap){
	vector<Basic::Clause*> result;
	for(map<Basic::PredicateSymbol*,Basic::PredicateSymbol*>::iterator it=reqPredMap.begin(); it !=reqPredMap.end(); it++){
		
		Basic::Atom* curAtom = new Basic::Atom(it -> first);
		for (vector<Basic::VariableSymbol*>::iterator it2 = it->second->param.begin(); it2 != it -> second -> param.end(); it2++){			
			curAtom -> param.push_back((Basic::Symbol*) *it2);
		}
		
		//Instantiate all atom parameters
		vector<Basic::Atom*> curReqAtoms = curAtom -> getInstances();
		// Iterate over all gorund atoms
		for (vector<Basic::Atom*>::iterator it2 = curReqAtoms.begin(); it2 != curReqAtoms.end(); it2++){
			// Goal:
			// If: reqP -> P, i.e., (or (not reqP) (P))
			Basic::Clause* reqImpl = new Basic::Clause();
			Basic::Atom* h = new Basic::Atom(nreqPredMap[it->first]);
			h -> param = (*it2)->param;
			// h -> neg = true;
			reqImpl -> neg_atm.push_back(h);
			
			Basic::Atom* t = new Basic::Atom(**it2);
			t->neg = false;
			t -> pred = it -> first;			
			reqImpl -> pos_atm.push_back(t);
			
			result.push_back(reqImpl);
			
			//Only If: !reqP -> !P, i.e., (or (reqP)(not P))
			Basic::Clause* nreqImpl = new Basic::Clause();
			Basic::Atom* nh = new Basic::Atom(reqPredMap[it->first]);
			// nh-> neg = false;
			nh -> param = (*it2) -> param;
			nreqImpl -> pos_atm.push_back(nh);
			
			Basic::Atom* nt = new Basic::Atom(**it2);
			nt->neg = true;
			nt -> pred = it -> first;			
			nreqImpl -> neg_atm.push_back(nt);
			
			result.push_back(nreqImpl);
		}
	}
	return result;
}



vector<Basic::Complex*> PDDL_Base::positiveBaCondEff(BuchiAutomaton* ba, Basic::PredicateSymbol* curP,Basic::PredicateSymbol* nextP, map<BuchiState*,Basic::Symbol*> stateMap){
	// Starting from ba, generates all the effects to be added to each action to embed the BA into the planning domain
	// curP is a reference to the predicate representing the current state in the PDDL domain description
	// stateMap maps references to BuchiState into references to their PDDL representation as Symbol
	vector <Basic::Complex*> result;
		
	// Iterate over all states	
	vector<BuchiState*> allStates = ba -> getAllStates();
	for (vector<BuchiState*>::iterator stIt = allStates.begin(); stIt != allStates.end(); stIt++){
		// create an atom representing that the BA is in the state referenced by *stIt
		Basic::Atom* curAtom = new Basic::Atom(curP);
		curAtom -> param.push_back(stateMap[*stIt]);
		
		//Iterate over all current state outgoing transitions (to define the next state that the BA can move to from current state)
		vector<BuchiTransition*> outgoingTransitions = (*stIt) -> getOutgoingTransitions();
		for(vector<BuchiTransition*>::iterator trIt=outgoingTransitions.begin(); trIt != outgoingTransitions.end(); trIt++){
			 // create a when effect to store transition effects
			Basic::Complex* whenEffect = new Basic::Complex();
			
			// add the atom for current state to the positive preconditions of whenEffect
			whenEffect -> pos_atm.push_back(curAtom);
			
			// Fill the effect with pre and post conditions, according to current transition:
						
			// iterate over transition's positive atoms
			vector<Basic::Atom*> trPosAtoms = (*trIt) -> getPositiveAtoms();
			for(vector<Basic::Atom*>::iterator atIt = trPosAtoms.begin(); atIt != trPosAtoms.end(); atIt++){
				// positive preconditions are stored in pos_atm
				whenEffect -> pos_atm.push_back(*atIt);
			}
			// iterate over transition's negative atoms
			vector<Basic::Atom*> trNegAtoms = (*trIt) -> getNegativeAtoms();
			for(vector<Basic::Atom*>::iterator atIt = trNegAtoms.begin(); atIt != trNegAtoms.end(); atIt++){
				// negative preconditions are stored in neg_atm
				whenEffect -> neg_atm.push_back(*atIt);
			}
			// create an atom representing that the BA is in the state destination of current Transition
			Basic::Atom* nxtAtom = new Basic::Atom(nextP);
			nxtAtom -> param.push_back(stateMap[(*trIt)->getTo()]);
			// Add the atom to the positive effects of whenEffect (stored in adds)
			whenEffect -> adds.push_back(nxtAtom);
			
			result.push_back(whenEffect);
		}
	}
	
	return result;
}
	

vector<Basic::Complex*> PDDL_Base::negativeBaCondEff(BuchiAutomaton* ba, Basic::PredicateSymbol* curP, map<BuchiState*,Basic::Symbol*> stateMap){		
	vector <Basic::Complex*> result;
	
	// Iterate over all states
	vector<BuchiState*> allStates = ba -> getAllStates(); 
	for (vector<BuchiState*>::iterator stIt = allStates.begin(); stIt != allStates.end(); stIt++){
		Basic::Complex* CNFCondEffect = new Basic::Complex(); // new conditional effect (to define when after action execution we are no longer in current state)
		
		// Iterate over all current state's incoming transitions
		vector<BuchiTransition*> incomingTransitions = (*stIt) -> getIncomingTransitions();
		for(vector<BuchiTransition*>::iterator trIt=incomingTransitions.begin(); trIt != incomingTransitions.end(); trIt++){
			// each transition generates a clause (either we are not in transition source state or the label does not hold) to be added to the condition
			// at the end, CNFCondEffect contains a CNF condition
			Basic::Clause* c = new Basic::Clause();
			
			Basic::Atom* notInSource = new Basic::Atom(curP);// Atom representing that the domain is not currently in the source state of current transition
			notInSource -> param.push_back(stateMap[(*trIt)->getFrom()]);
			notInSource -> neg = true;
			
			c ->neg_atm.push_back(notInSource);// add the atom to c
			// iterate over all transition positive atoms, that are negated and added to negative c atoms
			vector<Basic::Atom*> trPositiveAtoms = (*trIt)->getPositiveAtoms();
			for (vector<Basic::Atom*>::iterator atIt = trPositiveAtoms.begin(); atIt != trPositiveAtoms.end(); atIt++){
				Basic::Atom* nAtom = new Basic::Atom(*(*atIt));// current atom is copied (copy constructor copies field2field)
				nAtom -> neg = true;
				c -> neg_atm.push_back(nAtom);
			}
			// iterate over all transition negative atoms, that are copied, negated and added to positive c atoms
			vector<Basic::Atom*> trNegativeAtoms = (*trIt)->getNegativeAtoms();
			for (vector<Basic::Atom*>::iterator atIt = trNegativeAtoms.begin(); atIt != trNegativeAtoms.end(); atIt++){
				Basic::Atom* nAtom = new Basic::Atom(*(*atIt));// current atom is copied (copy constructor copies field2field)
				nAtom -> neg = false;
				c -> pos_atm.push_back(nAtom);
			}
			CNFCondEffect->clauses.push_back(c); // add the computed clause to the conditional effect
		}
		// create an atom representing that the BA is no longer in current State
		Basic::Atom* nxtAtom = new Basic::Atom(curP);
		nxtAtom -> param.push_back(stateMap[(*stIt)]);
		nxtAtom -> neg = true;
		// Add the atom to the negative effects of CNFCondEffect (stored in dels)
		CNFCondEffect -> dels.push_back(nxtAtom);
		
		result.push_back(CNFCondEffect);// add the effect to the result
	}			
	return result;
}

void PDDL_Base::printDomainPDDL(std::ostream& s){
	s << goal_ba -> to_s() << endl;
	s << "(define (domain "<< domain_name << ")" << endl;
	
	//0. Requirements
	s << "\t";
	if (!dom_requirements.empty()){
		s << "(:requirements";
		for (vector<Basic::Symbol*>::iterator it = dom_requirements.begin(); it != dom_requirements.end(); it++){
			s << " " << (*it) -> print_name;
		}
		s << ")" << endl;
	}
	//
	
	// 1. Types
	s << "\t";
		if (!dom_types.empty()){
			s << "(:types";
			for (vector<Basic::TypeSymbol*>::iterator it = dom_types.begin(); it != dom_types.end(); it++){
				s << " " << (*it) -> print_name;
				//if ((*it) -> sym_type != dom_top_type){
					s << " - " << (*it) -> sym_type -> print_name;
				//}
			}
			s << ")" << endl;
		}
	//
		
	// 2. Constants
	s << "\t";
	set<Basic::Symbol*> printedConstants;
	if (!pure_constants.empty()){
		s << "(:constants";
		for (vector<Basic::TypeSymbol*>::iterator itp = dom_types.begin(); itp != dom_types.end(); itp++){
			if (*itp != dom_top_type && (*itp)->elements.size() != 0){
				for (vector<Basic::Symbol*>::iterator it = (*itp) -> elements.begin(); it != (*itp) ->elements.end(); it++){
							s << " " << (*it) -> print_name;
							printedConstants.insert(*it);
					}
					s << " - " << (*itp) -> print_name;
			}
		}
		// Untyped constants are printed as last
		for (vector<Basic::Symbol*>::iterator it = dom_top_type -> elements.begin(); it != dom_top_type ->elements.end(); it++){
			// Print the current constant only if not printed already
			if (printedConstants.find(*it) == printedConstants.end()){
				s << " " << (*it) -> print_name;
			}
		}
		
		s << ")" << endl;
	}
	//
	// 3. Predicates
	if (!dom_predicates.empty()){
		s << "\t" << "(:predicates " << endl;
		for (vector<Basic::PredicateSymbol*>::iterator it = dom_predicates.begin(); it != dom_predicates.end(); it++){
			s << "\t\t";
			(*it) -> printPDDL(s);
			s << endl;			
		}
		s << "\t)" << endl;
	}
	//
	// 4. Actions
		for (vector<Basic::ActionSymbol*>::iterator it = dom_actions.begin(); it != dom_actions.end(); it++){
			(*it) -> printPDDL(s,"\t");
		}
	//
	
	s << ")" << endl;	
}


void PDDL_Base::printProblemPDDL(std::ostream& s){	
	// 5. Problem	
	// Preamble
	s << endl << endl;
	s << "(define (problem " << problem_name <<")" << endl;
	s << "\t" << "(:domain " << domain_name << ")" << endl;
	
	// Objects need not be printed: they appear as domain constants
	s << "\t" << "(:objects ) ;empty: all appearing as domain constants" << endl;

	/*
	s << "\t" << "(:objects ";
	for (vector<Basic::TypeSymbol*>::iterator itp = dom_types.begin(); itp != dom_types.end(); itp++){
		if (*itp != dom_top_type){
			bool purePred= true;
			for (vector<Basic::Symbol*>::iterator it = (*itp) -> elements.begin(); it != (*itp) ->elements.end(); it++){
				if (pure_constants.find(*it) == pure_constants.end()){
					purePred = false;
					s << " " << (*it) -> print_name;
				}
			}
			if (!purePred){
				s << " - " << (*itp) -> print_name;
			}
		}
	}
	s << ")" << endl;
	*/
	
	//Init
	s << "\t" << "(:init ";
	int i = 0;
	for (Basic::atom_vec::const_iterator it = dom_init_atoms.begin(); it != dom_init_atoms.end(); it++){
		s << endl << "\t\t" ;
		(*it) -> print(s,(*it)->neg);
		i++;
	}
	for (Basic::clause_vec::const_iterator it = dom_init_cls.begin(); it != dom_init_cls.end(); it++){
		s << endl << "\t\t" ;
		(*it) -> print(s);
		i++;
	}
	s << endl << "\t)" << endl;
	
	// Goal
	s << "\t" << "(:goal " << endl << "\t\t(and";
	for (Basic::atom_vec::const_iterator it = dom_goal_pos.begin(); it != dom_goal_pos.end(); it++){
		s << endl << "\t\t\t" ;
		(*it) -> print(s,(*it)->neg);
		i++;
	}
	for (Basic::atom_vec::const_iterator it = dom_goal_neg.begin(); it != dom_goal_neg.end(); it++){
		s << endl << "\t\t\t" ;
		(*it) -> print(s,(*it)->neg);
		i++;
	}
	for (Basic::clause_vec::const_iterator it = dom_goal_cls.begin(); it != dom_goal_cls.end(); it++){
		s << endl << "\t\t\t" ;
		(*it) -> print(s);
		i++;
	}
	s << endl << "\t\t" << ")";
	s << endl << "\t" << ")" << endl;
	s << ")" << endl;
	
}


void PDDL_Base::instantiate( Instance& ins )
{
  if( !ready_to_instantiate ) post_process();

// (FP) The following atoms state the equivalence of each constant to itself
  for (size_t k = 0; k < dom_constants.size(); k++) {
    // (FP) Seems to be useless: a's scope is within loop and no side-effect is done...
    Basic::Atom* a = new Basic::Atom(dom_eq_pred);
    a->param.push_back( dom_constants[k] );
    a->param.push_back( dom_constants[k] );
  }
//

  ins.name =
    new InstanceName(domain_name ? tab.table_char_map().strdup(domain_name) :
		     tab.table_char_map().strdup("??"),
		     problem_name ? tab.table_char_map().strdup(problem_name) :
		     tab.table_char_map().strdup("??"));


  Basic::ActionSymbol *init = new Basic::ActionSymbol( "smv_start_action" );
  for( size_t k = 0; k < dom_init_atoms.size(); ++k ) {
    if( !dom_init_atoms[k]->neg )
      init->adds.push_back( dom_init_atoms[k] );
    else
      init->dels.push_back( dom_init_atoms[k] );
  }
  init->clauses = dom_init_cls;
  init->oneof = dom_init_oneof;
  init->build( ins, 0 );

  for (size_t k = 0; k < dom_actions.size(); k++)
    dom_actions[k]->instantiate(ins);

	for (size_t k = 0; k < dom_goal_pos.size(); k++) {
		Instance::Atom* p = dom_goal_pos[k]->find_prop(ins, false, true);
		p->goal = true;
		// (FP) Adding (positive) goal atom to instance
		ins.goal_atoms.insert( 1+p->index );
	}

  for (size_t k = 0; k < dom_goal_neg.size(); k++) {
    Instance::Atom* p = dom_goal_neg[k]->find_prop(ins, true, true);
    p->goal = true;
	// (FP) Adding (negative) goal atom to instance
	ins.goal_atoms.insert( -(1+p->index));
  }
  
  for( size_t k = 0; k < dom_goal_cls.size(); ++k )
    dom_goal_cls[k]->build_clauses(ins, ins.goal_cls);
}

Basic::PredicateSymbol* PDDL_Base::find_type_predicate(Basic::Symbol* type_sym)
{
  for (size_t k = 0; k < dom_predicates.size(); k++)
    if (dom_predicates[k]->print_name == type_sym->print_name)
      return dom_predicates[k];
  std::cerr << "error: no type predicate found for type "
	    << type_sym->print_name << std::endl;
  exit(255);
}

void PDDL_Base::print(std::ostream& s)
{
  s << "domain: " << (domain_name ? domain_name : "<not defined>") << std::endl;
  s << "problem: " << (problem_name ? problem_name : "<not defined>") << std::endl;

  s << "<" << dom_predicates.size() << "," << dom_actions.size() << ">" << std::endl;

  dom_top_type->print(s);
  for (size_t k = 0; k < dom_types.size(); k++) dom_types[k]->print(s);
  for (size_t k = 0; k < dom_predicates.size(); k++) dom_predicates[k]->print(s);
  for (size_t k = 0; k < dom_actions.size(); k++) dom_actions[k]->print(s);
  
  s << "(: init" << endl;
  for (size_t k = 0; k < dom_init_atoms.size(); k++) dom_init_atoms[k]->print(s,dom_init_atoms[k]->neg);
  for (size_t k = 0; k < dom_init_oneof.size(); k++) dom_init_oneof[k]->print(s);
  for (size_t k = 0; k < dom_init_cls.size(); k++) dom_init_cls[k]->print(s);
  s << ")" << endl;

  s << "(:pos_goals";
  for (size_t k = 0; k < dom_goal_pos.size(); k++) {
    s << " ";
    dom_goal_pos[k]->print(s);
  }
  s << ")" << std::endl;
  s << "(:neg_goals";
  for (size_t k = 0; k < dom_goal_neg.size(); k++) {
    s << " ";
    dom_goal_neg[k]->print(s);
  }
  s << ")" << std::endl;
  
  s << "(:cls_goals" << endl;
  for (size_t k = 0; k < dom_goal_cls.size(); k++) {
    s << " ";
    dom_goal_cls[k]->print(s);	
  }
  s << ")" << std::endl;

/*  
  if (goal_ba != NULL){
	  s << "LTL goal formula: " << *ltl_goal << endl;
	  s << "LTL goal Automaton: " << endl << goal_ba -> to_s() << endl;
  }
  */
}

void InstanceName::write(std::ostream& s, bool cat) const
{
  if (domain_name_only) s << domain_name;
  else if (problem_name_only) s << problem_name;
  else s << domain_name << "::" << problem_name;
}

PDDL_Name::PDDL_Name(Basic::Symbol* sym, Basic::symbol_vec arg, size_t n)
  : _neg(false), _sym(sym)
{
  _arg = arg;
}

PDDL_Name::PDDL_Name(Basic::Symbol* sym, Basic::variable_vec arg, size_t n)
  : _neg(false), _sym(sym)
{
  for (size_t k = 0; k < n; k++) _arg.push_back( arg[k]->value );
}

void PDDL_Name::add(Basic::Symbol* s)
{
  _arg.push_back( s );
}

void PDDL_Name::write(std::ostream& s, bool cat) const
{
  if (cat) {
//	(FP) removed for compatibility with smv
//    if (_neg) s << "not_" << _sym->print_name;
//    else 
	s << _sym->print_name;
    for (size_t k = 0; k < _arg.size(); k++)
      s << '_' << _arg[k]->print_name;
  }
  else {
	s << "(";
//(FP) removed for compatibility with smv
//    if (_neg) s << "not ";
    s << '(' << _sym->print_name;
    for (size_t k = 0; k < _arg.size(); k++)
      s << ' ' << _arg[k]->print_name;
    s << ')';
    if (_neg) s << ')';
  }
}  

