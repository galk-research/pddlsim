#include <iostream>
#include <sstream>
#include <map>
#include <vector>
#include <algorithm>
#include "BuchiAutomaton.h"

extern "C" {
	#include "../ltl2ba-1.1/ltl2ba.h"
}

using namespace std;

/* BuchiState */
BuchiState::BuchiState(string id, bool acceptance, bool initial){
	this -> id = id;
	this -> acceptance = acceptance;
	this -> initial = initial;
}

string BuchiState::getId(){
	return id;
}
		
bool BuchiState::isAcceptance(){
	return acceptance;
}
		
vector<BuchiTransition*> BuchiState::getIncomingTransitions(){
	return incomingTransitions;
}

vector<BuchiTransition*> BuchiState::getOutgoingTransitions(){
	return outgoingTransitions;
}

string BuchiState::to_s(){
	ostringstream o;
	o << "; " << id;
	if (acceptance){
		o << " (acceptance)";
	}
	o << ":\n";
	for (vector<BuchiTransition*>::iterator it = outgoingTransitions.begin(); it != outgoingTransitions.end(); it++){
		o <<"; \t" << (*it) -> to_s() << "\n";
	}
	/*
	o << ";\n\tin: \n";
	for (vector<BuchiTransition*>::iterator it = incomingTransitions.begin(); it != incomingTransitions.end(); it++){
		o << ";\t\t" << (*it) -> to_s() << "\n";
	}
	*/
	o << ";";
	return o.str();
}

/*******************/

/* BuchiTransition */
BuchiTransition::BuchiTransition(BuchiState* from, BuchiState* to, vector<Basic::Atom*> pos, vector<Basic::Atom*> neg){
	this -> to = to;
	this -> from = from;
	this -> positive = pos;
	this -> negative = neg;
}

BuchiState* BuchiTransition::getTo(){
	return to;
}

BuchiState* BuchiTransition::getFrom(){
	return from;
}

vector<Basic::Atom*> BuchiTransition::getPositiveAtoms(){
	return positive;
}

vector<Basic::Atom*> BuchiTransition::getNegativeAtoms(){
	return negative;
}

string BuchiTransition::to_s(){
	ostringstream o;
	o << from -> getId();
	for(vector<Basic::Atom*>::iterator posIt=positive.begin(); posIt != positive.end(); posIt++){
		o << "-";
		(*posIt) -> print(o);
	}
	for(vector<Basic::Atom*>::iterator negIt=negative.begin(); negIt != negative.end(); negIt++){
		o << "-!";
		(*negIt) -> print(o);
	}
	o << "->" << to->getId();
	return o.str();
}

/*******************/


/* BuchiAutomaton */

BuchiAutomaton::BuchiAutomaton(Basic::LTLNode* f){
	// reads the ltl formula as passed by the parser, executes ltl2BA 
	// and builds the corresponding BuchiAutomaton
	map<string,Basic::Atom*> atomMap;
	string ltlFormula = toSPIN(f,atomMap);
	
	FILE* file = fopen("tmp-automaton","w+");
	//FILE* automaton_txt = tmpfile();
	
	// Calls buchi_automaton, which outputs a textual description of the BA associated to ltlFormula to file
	// function buchi_automaton is declared in "ltl2ba-1.1/ltl2ba.h" and defined in "ltl2ba-1.1/main.c"
	
	// prepare the command line
	char* commandLine[3];
	commandLine[0]=NULL;
	string prefix("-f");
	commandLine[1]=new char[prefix.size()+1];
	strcpy(commandLine[1],prefix.c_str());
	commandLine[2]=new char[ltlFormula.size()+1];	
	strcpy(commandLine[2],ltlFormula.c_str());
	
	//execute the translation
	buchi_automaton(3, commandLine, file);
	// The ba is now in file!
	
	// Build the automaton by parsing the content of file
	init = NULL; // initialize init state
	rewind(file);// Rewind the cursor to the beginning of file, to start reading
	char* l=new char[LINE_LENGTH]; // buffer to extract next file line (will be casted to string)
	map<string,BuchiState*> nameMap; // Used to map spin state names to BuchiState
	// copy first line into spin_formula
	fgets(l,LINE_LENGTH,file);
	spin_formula = extractFormula(l);
	while (fgets(l,LINE_LENGTH,file)){// Builds the automaton, line by line
		string line(l); // cast l to string, to enable string functions
		// check if it is first or last line
		if (isLastLine(line)){
			//first or last line: do nothing
		}
		else{// inner line fetched
			if (stateStarts(line)){// beginning of state description
				BuchiState* bs; // pointer to current BuchiState
				
				// extract (SPIN) name of state 
				string stateName = line.substr(0,line.size()-2);
				
				// check if a state with name stateName is already mapped
				map<string,BuchiState*>::iterator mapIt = nameMap.find(stateName);				
				if (mapIt == nameMap.end()){// the state is not mapped
					// if init is NULL, then the state is initial (as it is the first in the file)
					bs = new BuchiState(newStateName(),isAcceptance(stateName), init==NULL);// create a new state
					nameMap[stateName]=bs; //map the state
					allStates.push_back(bs);// update allStates
					if (bs -> isAcceptance()){// update acceptanceStates
						acceptanceStates.insert(bs);
					}
					// checks if init is to be set
					if (init == NULL){
						// if init is not initialized, bs is initial (as it is the first in the file)
						init = bs;
					}
				}
				else{// the state is mapped					
					bs = mapIt -> second;// extract the mapped state
				}
				// now, bs transitions can be updated
				string trans;
				do{//iterate over transition lines
					fgets(l,LINE_LENGTH,file);
					trans = string(l);
					if (trans == string("\tskip\n")){//trans contains an "accept all" transition
						// example: trans="\tskip\n"
						// Create a self-loop tansition with label "true"
						vector<Basic::Atom*> pos;// empty pos
						vector<Basic::Atom*> neg;// empty neg
						// A transition w/ empty pos and neg stands for "true"
						BuchiTransition* bt = new BuchiTransition(bs,bs,pos,neg);//self loop
						addTransition(bt);
					}
					else{// normal state (no accept all)
						if (trans.find("\t::") == 0){// trans contains an actual transition line
							// example: trans="\t:: (p && !r) || (p && q) -> goto accept_S4\n"
							cleanTransLine(trans);//remove (leading and trailing) formatting substrings from trans
							
							// 1.Extract SPIN name of destination state 
							string toStateName = getDestinationStateName(trans);
							removeDestinationPart(trans); // removes everything after " ->", included
							
							BuchiState* toState; // BuchiState destination of the transition

							// 2.Check if a state with SPIN  name toStateName is already mapped
							map<string,BuchiState*>::iterator mapIt = nameMap.find(toStateName);
							if (mapIt == nameMap.end()){// the state is not mapped								
								toState = new BuchiState(newStateName(),isAcceptance(toStateName),false);// create a new BuchiState, which is not initial
								nameMap[toStateName]=toState;// update nameMap								
								allStates.push_back(toState);// update allStates
								if (toState -> isAcceptance()){ // update acceptanceStates
									acceptanceStates.insert(toState);
								}
							}
							else{// the state is mapped
								toState = mapIt -> second; // extract mapped state
							}
							
							// 3.Builds the set of all transitions to state toState, based on line "trans"
							vector<BuchiTransition*> allTrans = getBuchiTransitions(bs,toState,trans,atomMap);
							
							// 4.Updates bs transitions
							for (vector<BuchiTransition*>::iterator transIt = allTrans.begin(); transIt != allTrans.end(); transIt++){
								addTransition(*transIt);
							}
						}
					}
				}while(trans.find("\tfi;") == string::npos && trans.find("}") == string::npos);
			}
		}
	}

	fclose(file);
}

string BuchiAutomaton::toSPIN(Basic::LTLNode* f, map<string, Basic::Atom*> &atomMap){
	/* returns formula f in LTL for SPIN (ready to be processed by ltl2BA)
	 * Also, returns a map associating each SPIN proposition to the PDDL atom it was derived from,
	 * that will be used to parse the ltl2BA output		
	*/
	ostringstream result;

	switch (f -> op){
			case (Basic::NN):
				if (f ->atom != NULL){
					result << addAtomToMap(f->atom,atomMap);
				}
				break;
			case (Basic::NEXT):
				if (f -> left != NULL){
					result << "X (" << toSPIN(f -> left,atomMap) << ")";
				}
				break;
			case (Basic::RELEASE):
				if (f -> left != NULL && f -> right != NULL){
					result << "(" << toSPIN(f -> left, atomMap) << ") V (" << toSPIN(f->right,atomMap)<<")";
				}
				break;
			case (Basic::UNTIL):
				if (f -> left != NULL && f -> right != NULL){
					result << "(" << toSPIN(f -> left, atomMap) << ") U (" << toSPIN(f->right,atomMap)<<")";
				}
				break;
				case (Basic::ALW):
					if (f -> left != NULL){
						result << "[] (" << toSPIN(f -> left,atomMap) << ")";
					}
				break;
				case (Basic::EVT):
					if (f -> left != NULL){
						result << "<> (" << toSPIN(f -> left,atomMap) << ")";
					}
				break;
				case (Basic::IFF):
					if (f -> left != NULL && f -> right != NULL){
						result << "(" << toSPIN(f -> left, atomMap) << ") <-> (" << toSPIN(f->right,atomMap)<<")";
					}
					break;
				case (Basic::IMPL):
					if (f -> left != NULL && f -> right != NULL){
						result << "(" << toSPIN(f -> left, atomMap) << ") -> (" << toSPIN(f->right,atomMap)<<")";
					}
					break;
				case (Basic::NOT):
					if (f -> left != NULL){// in this case, f can never be an atom (as negation is pushed into atom during parsing)
						result << "!(" << toSPIN(f -> left,atomMap) << ")";
					}
					break;
				case (Basic::AND):
					if (f -> left != NULL && f -> right != NULL){
						result << "(" << toSPIN(f -> left, atomMap) << ") && (" << toSPIN(f->right,atomMap)<<")";
					}
					break;
				case (Basic::OR):
					if (f -> left != NULL && f -> right != NULL){
						result << "(" << toSPIN(f -> left, atomMap) << ") || (" << toSPIN(f->right,atomMap)<<")";
					}
					break;
			default: 
				break;
		}	
	return result.str();
}

string BuchiAutomaton::addAtomToMap(Basic::Atom* a, map<string,Basic::Atom*> &atomMap){
	// p(x y z) is translated into p_x_y_z
		//	predicate name
	ostringstream result;
	
	if (a -> neg){// negated atom
		result << "!";
	}
	result << a -> pred -> print_name;
	// iterate on atom arguments and append _p for each oarameter p encountered
	vector<Basic::Symbol*>::iterator it;
	for (it=a -> param.begin(); it != a -> param.end(); it++){
		result << "_" << (*it) -> print_name;
	}
	// associate the obtained proposition to the atom it has been built from 
	if (atomMap.find(result.str()) == atomMap.end()){// add the entry only if it is not already mapped
		atomMap[result.str()] = a;
	}
	return result.str();
}

string BuchiAutomaton::to_s(){
	ostringstream o;
	o << "; LTL formula: " << spin_formula << endl;
	o << "; Buchi Automaton: " << endl;
	o << "; init = " << init -> id << endl;
	for(vector<BuchiState*>::iterator it = allStates.begin(); it != allStates.end(); it++){
		o << (*it) -> to_s() << endl;
	}
	return o.str();
}

/* Auxiliary functions for file parsing*/
bool BuchiAutomaton::isFirstLine(string line){
	return (line.find("never")==0);
}

bool BuchiAutomaton::isLastLine(string line){
	return (line.find("}")==0);
}

bool BuchiAutomaton::stateStarts(string line){
	return (
			!isFirstLine(line) &&
			!isLastLine(line) &&
			line.find("\t")!=0
		);
}

bool BuchiAutomaton::isAcceptance(string sn){
	return sn.find("accept") != string::npos;
}

string BuchiAutomaton::newStateName(){
	//create new BuchiState and update the map
	ostringstream newStateName;
	newStateName << "S" << allStates.size();
	return newStateName.str();
}

void BuchiAutomaton::cleanTransLine(string& trans){
	trans.replace(0,4,"");// remove prefix "\t:: "
	trans.replace(trans.size()-1,1,"");// remove eol
}

string BuchiAutomaton::getDestinationStateName(string trans){
	return trans.substr(trans.rfind(" ")+1,trans.size());
}

void BuchiAutomaton::removeDestinationPart(string& trans){
	int start = trans.find(" ->");
	int length = trans.size() - start;
	trans.replace(start,length,"");// remove destination part from line
}

vector<string> BuchiAutomaton::tokenize(string str, string delimiter){
	vector<string> result;
	size_t curPos = 0; // token start point
	while(curPos != string::npos){
		size_t last=str.find(delimiter,curPos); // token end point
		string token = str.substr(curPos,last-curPos);
		result.push_back(token);// add token to result
		curPos = str.find_first_not_of(delimiter,last);
	}
	return result;
}

vector<BuchiTransition*> BuchiAutomaton::getBuchiTransitions(BuchiState* from, BuchiState* dest, string trans, map<string,Basic::Atom*> atomMap){
	vector<BuchiTransition*> result;
	vector<string> transTokens = tokenize(trans," || "); // Each vector component corresponds to a transition label to dest
	
	// Iterate over each label, example: "(p && q && !r)"
	for(vector<string>::iterator transIt = transTokens.begin(); transIt!=transTokens.end(); transIt++){
		string curToken = *transIt;
		vector<Basic::Atom*> pos; // positive transition literals
		vector<Basic::Atom*> neg; // negative transition literals
		// remove enclosing parenthesis from curToken (enclosing parenthesis are always present)
		curToken.replace(0,1,""); // remove leading "("
		curToken.replace(curToken.find(")"),1,""); // remove trailing ")"
		vector<string> literals = tokenize(curToken," && ");
		//iterate over each literal
		for (vector<string>::iterator litIt = literals.begin(); litIt != literals.end(); litIt++){
			if (litIt -> find("!") != string::npos){
				neg.push_back((Basic::Atom*) atomMap[litIt -> substr(1)]);
			}
			else{
				if(*litIt != string("1")){
					pos.push_back((Basic::Atom*) atomMap[*litIt]);
				}
				/* if (*litIt -= string("1")){ 
				 * nothing to be done, as a transition with no labelling atoms
				 * corresponds to "true"
				 * }
				 */
			}
		}
		//create the transition and add to result 
		BuchiTransition* bt = new BuchiTransition(from,dest,pos,neg);
		result.push_back(bt);
	}
	return result;
}


string BuchiAutomaton::extractFormula(const char* line){
	// extracts the ltl formula from the first line of ltl2ba output file
	string str(line);
	str = str.substr(11); // remove leading /* "never{ /* "
	return str.substr(0,str.size()-3); // remove trailing "*/\n" 
}


/***********************/

BuchiAutomaton::~BuchiAutomaton(){
	// State deletion also deletes the respective transitions
	for(vector<BuchiState*>::iterator it = allStates.begin(); it != allStates.end(); it++)
		delete(*it);
}

BuchiState* BuchiAutomaton::getInit(){
	return init;
}

vector<BuchiState*> BuchiAutomaton::getAllStates(){
	return allStates;
}

set<BuchiState*> BuchiAutomaton::getAcceptanceStates(){
	return acceptanceStates;
}

bool BuchiAutomaton::addTransition(BuchiTransition* trans){
	if (trans -> from != NULL && trans -> to != NULL){
		trans -> from -> outgoingTransitions.push_back(trans); // adds the outgoing transition 
		trans -> to -> incomingTransitions.push_back(trans); // adds the incoming transition
		transitions.push_back(trans);
		return true;
	}
	else return false;
}



/*******************/

