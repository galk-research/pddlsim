#ifndef BUCHIAUTOMATON_H_
#define BUCHIAUTOMATON_H_

#include <stdio.h>
#include <string>
#include <vector>
#include <map>
#include "basic.h"

using namespace std;

const int LINE_LENGTH=2048;

class BuchiTransition;

class BuchiState{
	friend class BuchiAutomaton; //BuchiAutomaton can set up the state
	private:
		string id;
		bool acceptance, initial;
		vector<BuchiTransition*> outgoingTransitions; // can be set only by BuchiAutomaton
		vector<BuchiTransition*> incomingTransitions; // can be set only by BuchiAutomaton
		BuchiState(string id, bool acc, bool init); // Instances can only be created by BuchiAutomaton
	public:
		string getId();
		bool isInitial();
		bool isAcceptance();
		vector<BuchiTransition*> getIncomingTransitions();
		vector<BuchiTransition*> getOutgoingTransitions();
		string to_s();
};

class BuchiTransition{
	friend class BuchiAutomaton; //BuchiAutomaton can set up the transition
	private:
		BuchiState* from;
		BuchiState* to;
		vector<Basic::Atom*> positive; // positive literals
		vector<Basic::Atom*> negative; // negative literals
		// The transition label is obtained as conjunction of positive and negative literals
		BuchiTransition(BuchiState* from, BuchiState* to, vector<Basic::Atom*> pos, vector<Basic::Atom*> neg); // Instances can only be created by BuchiAutomaton
	public:
		// No destroyer: transitions share states. They are removed by BuchiAutomaton		
		BuchiState* getTo();
		BuchiState* getFrom();
		vector<Basic::Atom*> getPositiveAtoms();
		vector<Basic::Atom*> getNegativeAtoms();
		string to_s();
};

class BuchiAutomaton{
	private:
		BuchiState* init;
		set<BuchiState*> acceptanceStates;
		vector<BuchiState*> allStates;
		vector<BuchiTransition*> transitions; // necessary for destroyer
		string spin_formula; // stores ltl formula, as read from the ltl2ba output file
	public:
		BuchiAutomaton(Basic::LTLNode*); 
		// Builds the automaton starting from the ltlFormula built by the parser
		~BuchiAutomaton(); // Destroyer ok: automata do not share states
		
		BuchiState* getInit();
		vector<BuchiState*> getAllStates();
		set<BuchiState*> getAcceptanceStates();
		vector<BuchiState*> getAllTransitions();		
		string to_s();
		
	private:
		string toSPIN(Basic::LTLNode* f, map<string, Basic::Atom*> &atomMap);
		/* returns a SPIN formula in SPIN (ready to be processed by ltl2BA)
		 * Also, returns a map associating each spin proposition to a PDDL atom, 
		 * that will be used to parse the ltl2BA output
		 */
		string addAtomToMap(Basic::Atom* a, map<string,Basic::Atom*> &atomMap);
		bool addTransition(BuchiTransition* trans);
		/*Auxiliary functions for file parsing */
		bool isFirstLine(string);
		bool isLastLine(string);
		bool stateStarts(string);
		bool isAcceptance(string);
		string newStateName();
		void cleanTransLine(string&);
		string getDestinationStateName(string);
		void removeDestinationPart(string&);
		vector<string> tokenize(string,string);
		vector<BuchiTransition*> getBuchiTransitions(BuchiState* from, BuchiState* dest, string, map<string,Basic::Atom*>);
		string extractFormula(const char* line);
};

#endif /*BUCHIAUTOMATON_H_*/
