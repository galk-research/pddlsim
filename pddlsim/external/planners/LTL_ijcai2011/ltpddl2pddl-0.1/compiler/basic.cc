#include "basic.h"
#include <sstream>


Basic::variable_vec::operator const symbol_vec(){
	symbol_vec result;
	for(int i =0; i< this -> size(); i++){
		result.push_back((*this)[i]);
	}
	return result;
}



void Basic::TypeSymbol::add_element(Symbol* e)
{
  elements.push_back( e );
  if (sym_type != 0) ((TypeSymbol*)sym_type)->add_element(e);
}

bool Basic::AtomBase::equals(AtomBase& b)
{
  if (param.size() != b.param.size()) return false;
  for (size_t k = 0; k < param.size(); k++)
    if (param[k] != b.param[k]) return false;
  return true;
}

bool Basic::Atom::equals(Atom& a)
{
  if (pred != a.pred) return false;
  return AtomBase::equals(a);
}

Instance::Atom*
Basic::Atom::find_prop(Instance& ins, bool neg, bool create)
{  
  ptr_table* r = (neg ? &(pred->neg_prop) : &(pred->pos_prop));
  for (size_t k = 0; k < param.size(); k++) {
    if (param[k]->sym_class == sym_variable)
      r = r->insert_next(((VariableSymbol*)param[k])->value);
    else
      r = r->insert_next(param[k]);
  }
  if (!r->val) {
    if (!create) return 0;
    PDDL_Name* a_name = new PDDL_Name(pred, neg);
    for (size_t k = 0; k < param.size(); k++) {
      if (param[k]->sym_class == sym_variable)
	a_name->add(((VariableSymbol*)param[k])->value);
      else
	a_name->add(param[k]);
    }
	// (FP) An instanced atom  is either created or found:
    Instance::Atom& p = ins.new_atom(a_name);
    bool init_val = false;
    p.init = (init_val != neg);
	r->val = &p;
  }
  Instance::Atom *pp = (Instance::Atom*)r->val;
  return (Instance::Atom*)r->val;
}



void Basic::ActionSymbol::post_process()
{
}


size_t Basic::ActionSymbol::param_index(VariableSymbol* p)
{
  for( size_t k = 0; k < param.size(); ++k )
    if( param[k] == p ) return k;
  return no_such_index;
}

void Basic::ActionSymbol::build( Instance& ins, size_t p )
{
  if( p < param.size() ) {
    TypeSymbol* t = (TypeSymbol*)param[p]->sym_type;
    for( size_t k = 0; k < t->elements.size(); ++k ) {
      param[p]->value = t->elements[k];
      build( ins, p+1 );
    }
    param[p]->value = 0;
  }
  else {
    Instance::Action& act = ins.new_action( new PDDL_Name(this,param,param.size()) );
	
	//(FP) Action preconditions:
    for( size_t k = 0; k < pos_atm.size(); ++k ) {// (FP) positive preconditions
	  Instance::Atom* pp = pos_atm[k]->find_prop( ins, false, true);
      act.pre.insert( 1+pp->index );
    }

    for( size_t k = 0; k < neg_atm.size(); ++k ) {// (FP) negative preconditions
	  Instance::Atom* np = neg_atm[k]->find_prop( ins, false, true);
      act.pre.insert( -(1+np->index) );
    }
	//
	//(FP) action effects:
    Complex::build_effects( ins, act, true ); // (FP) direct deterministic effects?
	
    for( size_t k = 0; k < oneof.size(); ++k )
      oneof[k]->build_effects( ins, act );

    for( size_t k = 0; k < complex.size(); ++k ) {
      for( size_t j = 0; j < p; ++j )
        complex[k]->param[j]->value = param[j]->value;
      complex[k]->build( ins, p, act );
    }

    act.cost = 1;
  }
}

void Basic::ActionSymbol::instantiate( Instance& ins )
{
  for( size_t k = 0; k < param.size(); ++k ) param[k]->value = 0;
  build( ins, 0 );
}

void Basic::Complex::build( Instance& ins, size_t p, Instance::Action &act  )
{
  if( p < param.size() ) {
    TypeSymbol* t = (TypeSymbol*)param[p]->sym_type;
    for( size_t k = 0; k < t->elements.size(); ++k ) {
      param[p]->value = t->elements[k];
      build( ins, p+1, act );
    }
    param[p]->value = 0;
  }
  else {
    build_effects( ins, act, false );
  }
}

void Basic::Complex::build_effects( Instance& ins, Instance::Action& act, bool topl )
{
	//(FP) clauses not considered in action effects, checking for this assumption:
	assert(clauses.size() == 0);
	//
  for( size_t k = 0; k < clauses.size(); ++k ){
    clauses[k]->build_clauses( ins, act.cls );
	}	
  //(FP) direct effects
  if( topl || (neg_atm.empty() && pos_atm.empty()) ) {//neg_atm.empty() && pos_atm.empty(): not a when condition
    for (size_t k = 0; k < adds.size(); k++)  {
      Instance::Atom* pp = adds[k]->find_prop(ins, false, true);
      act.add.insert(pp->index);
	  //(FP) stating that (positive) atom pp depends on action act
	  (pp -> pos_effect_of).push_back(&act);
    }
    for (size_t k = 0; k < dels.size(); k++)  {
      Instance::Atom* pp = dels[k]->find_prop(ins, false, true);
      act.del.insert(pp->index);
	  //(FP) stating that (negative) atom pp depends on action act
	  (pp -> neg_effect_of).push_back(&act);
    }
  }
  else {
    Instance::When w;
    for( size_t k = 0; k < pos_atm.size(); ++k ) {//(FP) inserting positive conditions for effect activations
      Instance::Atom* pp = pos_atm[k]->find_prop( ins, false, true );
      w.pre.insert( 1+pp->index );
    }
    for( size_t k = 0; k < neg_atm.size(); ++k ) {//(FP) inserting negative conditions for effect activations
      Instance::Atom* np = neg_atm[k]->find_prop( ins, false, true );
      w.pre.insert( -(1+np->index) );
    }
    for (size_t k = 0; k < adds.size(); k++)  {//(FP) inserting positive effects actived by the conjunction of all (when) conditions
      Instance::Atom* pp = adds[k]->find_prop(ins, false, true);
      w.add.insert(pp->index);
	  //(FP) stating that (positive) atom pp conditionally depends on action act
	  (pp -> pos_when_effect_of).push_back(&act);	  
    }
    for (size_t k = 0; k < dels.size(); k++)  {//(FP) inserting negative effects actived by the conjunction of all (when) conditions
      Instance::Atom* pp = dels[k]->find_prop(ins, false, true);
      w.del.insert(pp->index);
	  //(FP) stating that (negative) atom pp conditionally depends on action act
	  (pp -> neg_when_effect_of).push_back(&act);	  
    }
    act.when.push_back( w );
  }
}

void Basic::Clause::build_clauses( Instance &ins, index_vec_vec &cls )
{
  index_vec cl;
  for (size_t k = 0; k < pos_atm.size(); k++)  {
    Instance::Atom* pp = pos_atm[k]->find_prop(ins, false, true);
    cl.push_back(1+pp->index);
  }
  for (size_t k = 0; k < neg_atm.size(); k++)  {
    Instance::Atom* pp = neg_atm[k]->find_prop(ins, false, true);
    cl.push_back(-(1+pp->index));
  }
  cls.push_back( cl );
}

void Basic::OneOf::build_effects( Instance &ins, Instance::Action &act )
{
  index_vec oneof;
  for (size_t k = 0; k < adds.size(); k++)  {
    Instance::Atom* pp = adds[k]->find_prop(ins, false, true);
    oneof.push_back(1+pp->index);
	
  }
  for (size_t k = 0; k < dels.size(); k++)  {
    Instance::Atom* pp = dels[k]->find_prop(ins, false, true);
    oneof.push_back(-(1+pp->index));
  }
  act.oneof.push_back( oneof );
}

void Basic::LTLNode::print(ostream &o) const{ 
	switch (op){
	//AND, OR, NOT, IMPL, ALW, EVT, UNTIL, RELEASE, NEXT, NN
		case (NN):
			if (atom != NULL){
				o << "(";
				atom -> print(o);
				o << ")";
			}
			break;
		case (NEXT):
			if (left != NULL){
				o << "X(";
				left -> print(o);
				o << ")";
			}
			break;
		case (RELEASE):
			if (left != NULL && right != NULL){
				o << "(";
				left -> print(o);
				o<< ") V (";
				right -> print(o);
				o<< ")";
			}
			break;
		case (UNTIL):
			if (left != NULL && right != NULL){
				o << "(";
				left -> print(o);
				o<< ") U (";
				right -> print(o);
				o<< ")";
			}
			break;
		case (ALW):
			if (left != NULL){
				o << "G(";
				left -> print(o);
				o << ")";
			}
			break;
		case (EVT):
			if (left != NULL){
				o << "F(";
				left -> print(o);
				o << ")";
			}
			break;
		case (IFF):
			if (left != NULL && right != NULL){
				o << "(";
				left -> print(o);
				o<< ") <-> (";
				right -> print(o);
				o<< ")";
			}
			break;
		case (IMPL):
			if (left != NULL && right != NULL){
				o << "(";
				left -> print(o);
				o<< ") -> (";
				right -> print(o);
				o<< ")";
			}
			break;
		case (NOT):
			if (left != NULL){
				o << "!(";
				left -> print(o);
				o << ")";
			}
			break;
		case (AND):
			if (left != NULL && right != NULL){
				o << "(";
				left -> print(o);
				o<< ") && (";
				right -> print(o);
				o<< ")";
			}
			break;
		case (OR):
			if (left != NULL && right != NULL){
				o << "(";
				left -> print(o);
				o<< ") || (";
				right -> print(o);
				o<< ")";
			}
			break;
		default: 
			break;
	}
}



void Basic::TypeSymbol::print(std::ostream& s)
{
  s << "(:type " << print_name;
  if (sym_type) s << " - " << sym_type->print_name;
  s << "): {";
  for (size_t k = 0; k < elements.size(); k++) {
    elements[k]->print(s);
    if (k < elements.size() - 1) s << ", ";
  }
  s << "}" << std::endl;
}

void Basic::PredicateSymbol::print(std::ostream& s)
{
  s << "(:predicate " << print_name;
  for (size_t k = 0; k < param.size(); k++) {
    s << " ";
    param[k]->print(s);
  }
  s << ")" << std::endl;
}


void Basic::PredicateSymbol::printPDDL(std::ostream& s){
	  s << "(" << print_name << " ";
  if (param.size() != 0){
	  for (size_t k = 0; k < param.size(); k++) {
	    param[k]->print(s);
	    s << " ";
	  }
  }
  s << ")";
}


void Basic::OneOf::print( std::ostream &os, size_t i ) const
{
  os << "(oneof";
  for( size_t k = 0; k < adds.size(); ++k ) {
    os << " ";
    adds[k]->print(os);
  }
  for( size_t k = 0; k < dels.size(); ++k ) {
    os << " (not ";
    dels[k]->print(os);
    os << ")";
  }
  os << ")" << std::endl;
}

void Basic::Clause::print( std::ostream &os, size_t i ) const
{
  if(pos_atm.size() + neg_atm.size() > 1){
	  os << "(or ";
  }
  for( size_t k = 0; k < neg_atm.size(); ++k ) {
    //os << " (not ";
    neg_atm[k]->print(os,neg_atm[k]->neg);
    //os << ")";
  }
  for( size_t k = 0; k < pos_atm.size(); ++k ) {
    os << " ";
    pos_atm[k]->print(os,pos_atm[k]->neg);
  }
  if(pos_atm.size() + neg_atm.size() > 1){
	  os << ")";
  }
}

void Basic::Complex::print( std::ostream &os, size_t i ) const
{
  os << std::setw(i) << "" << "(:complex" << std::endl;
  os << std::setw(i) << "" << "  :parameters (";
  for (size_t k = 0; k < param.size(); k++) {
    if (k > 0) os << ' ';
    param[k]->print(os);
  }
  os << ")" << std::endl;
  os << std::setw(i) << "" << "  :pos_prec (";
  for (size_t k = 0; k < pos_atm.size(); k++) {
    pos_atm[k]->print(os);
    if (k < pos_atm.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << std::setw(i) << "" << "  :neg_prec (";
  for (size_t k = 0; k < neg_atm.size(); k++) {
    neg_atm[k]->print(os);
    if (k < neg_atm.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << std::setw(i) << "" << "  :add (";
  for (size_t k = 0; k < adds.size(); k++) {
    adds[k]->print(os);
    if (k < adds.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << std::setw(i) << "" << "  :del (";
  for (size_t k = 0; k < dels.size(); k++) {
    dels[k]->print(os);
    if (k < dels.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << std::setw(i) << "" << "  :clauses (";
  for (size_t k = 0; k < clauses.size(); k++) {
    clauses[k]->print(os);
    if (k < clauses.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << std::setw(i) << "" << ")" << std::endl;
}
 
void Basic::Effect::printVecPDDL(std::ostream& s, atom_vec v, bool neg) const{
	for (atom_vec::const_iterator it = v.begin(); it != v.end(); it++){
		(*it) -> print(s,neg);
	}
}

void Basic::Effect::printCondPDDL(std::ostream& s) const{
	if (!pos_atm.empty() || !neg_atm.empty()){// conditional effect
		s << "(when ";
		if ((pos_atm.size() + neg_atm.size()) > 1){
			s << "(and ";
		}
		printVecPDDL(s,pos_atm);
		printVecPDDL(s,neg_atm,true);
		if ((pos_atm.size() + neg_atm.size()) > 1){
			s << ")";
		}
	}
	if (adds.size() + dels.size() > 1){
		s << "(and ";
	}
	printVecPDDL(s,adds);
	printVecPDDL(s,dels,true);	
	if (adds.size() + dels.size() > 1){
		s<<")";
	}
	if (!pos_atm.empty() || !neg_atm.empty()){
		s << ")";
	}
}

void Basic::Complex::printClsPDDL( std::ostream& s) const{
	if (clauses.size() > 1){
		s << "(and ";
	}
	for (clause_vec::const_iterator it = clauses.begin(); it != clauses.end(); it++){
		(*it) -> print(s);
	}	
	if (clauses.size() > 1){
		s << ")";
	}
}


void Basic::Complex::printPDDL( std::ostream& s, const char* indent) const{
	if (forall && param.size() > 0){
		s << indent << "(forall ( ";
		for (variable_vec::const_iterator it = param.begin(); it != param.end(); it++){
			(*it) -> print(s);
			s << " ";
		}
		s << ")";	
		if (!clauses.empty()){//Clausal part
			printClsPDDL(s);
		}
		else{// Conditional part
			printCondPDDL(s);
		}
		s << ")";// eof (forall (...) (...) )
		return;
	}
	if (clauses.empty()){// when
		s << indent;
		printCondPDDL(s);
		return;
	}
	// special Buchi Automaton effect (conditional with disjunctive condition)
	//s << indent;
	if (!clauses.empty()){
		//s << "; special Ba Action: " << endl;
		s << indent << "(when ";
		printClsPDDL(s);
		printCondPDDL(s);
		s << ")";
	}	
}


void Basic::ActionSymbol::print( std::ostream& os ) const
{
  os << "(:action " << print_name << std::endl;
  os << "  :parameters (";
  for (size_t k = 0; k < param.size(); k++) {
    if (k > 0) os << ' ';
    param[k]->print(os);
  }
  os << ")" << std::endl;
  os << "  :pos_prec (";
  for (size_t k = 0; k < pos_atm.size(); k++) {
    pos_atm[k]->print(os);
    if (k < pos_atm.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << "  :neg_prec (";
  for (size_t k = 0; k < neg_atm.size(); k++) {
    neg_atm[k]->print(os);
    if (k < neg_atm.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << "  :add (";
  for (size_t k = 0; k < adds.size(); k++) {
    adds[k]->print(os);
    if (k < adds.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << "  :del (";
  for (size_t k = 0; k < dels.size(); k++) {
    dels[k]->print(os);
    if (k < dels.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << "  :clauses (";
  for (size_t k = 0; k < clauses.size(); k++) {
    clauses[k]->print(os);
    if (k < clauses.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  os << "  :oneof (";
  for (size_t k = 0; k < oneof.size(); k++) {
    oneof[k]->print(os);
    if (k < oneof.size() - 1) os << " ";
  }
  os << ")" << std::endl;
  for( size_t k = 0; k < complex.size(); ++k )
    complex[k]->print( os, 2 );
  os << ")" << std::endl;
}


void Basic::ActionSymbol::printPDDL(ostream& s, char* indent) const{ 
	s << indent << "(:action " << print_name << endl;
	// 1. Parameters
	// printed even if parameters are nor present, to be compliant with VAL
	s << indent << "\t" << ":parameters ( ";
	for (Basic::variable_vec::const_iterator it = param.begin(); it != param.end(); it++){
		s << (*it) -> print_name << " - " << (*it) -> sym_type -> print_name << " ";
	}
	s << ")" << endl;
	//
	// 2. Precondition
	if(!pos_atm.empty() || !neg_atm.empty() /*|| !disj_precs.empty()*/){
		s << indent << "\t" << ":precondition (and ";
		// positive atoms
		for (Basic::atom_vec::const_iterator it = pos_atm.begin(); it != pos_atm.end(); it++){
			(*it) -> print(s);
		}
		// negative atoms
		for (Basic::atom_vec::const_iterator it = neg_atm.begin(); it != neg_atm.end(); it++){
			(*it) -> print(s,true);
		}
		/*
		// clauses
		for (Basic::clause_vec::const_iterator it = disj_precs.begin(); it != disj_precs.end(); it++){
			cout << endl << "\t\t\t";
			(*it) -> print(s);
		}
		*/
		
		s << endl << "\t\t)" << endl;
	}
	//
	// 3. Effects
	if(!adds.empty() || !dels.empty() || !clauses.empty() || !complex.empty() || !oneof.empty()){
		s << indent << "\t" << ":effect (and " << endl;
		// Add list		
		if (!adds.empty()){
			s << indent << "\t\t\t";
			for (Basic::atom_vec::const_iterator it = adds.begin(); it != adds.end(); it++){
				(*it) -> print(s);
			}
			s << endl;
		}
		//
		// Del list
		if (!dels.empty()){
			s << indent << "\t\t\t";
			for (Basic::atom_vec::const_iterator it = dels.begin(); it != dels.end(); it++){
				(*it) -> print(s,true);
			}
			s << endl;
		}
		//
		// Clauses
		for (Basic::clause_vec::const_iterator it = clauses.begin(); it != clauses.end(); it++){
			s << indent << "\t\t\t";
			(*it) -> print(s);
			s << endl;
		}
		//
		// Complex (forall, when and effects for BA description)
		for (Basic::complex_vec::const_iterator it = complex.begin(); it != complex.end(); it++){
			ostringstream ind;
			ind << indent << "\t\t\t";
			(*it) -> printPDDL(s, ind.str().c_str());
			s << endl;
		}
		
		//Special Ba actions (conditional with disjunctive preconditions)
		for (Basic::complex_vec::const_iterator it = specialBa.begin(); it != specialBa.end(); it++){
			ostringstream ind;
			ind << indent << "\t\t\t";
			(*it) -> printPDDL(s,ind.str().c_str());
			s << endl;
		}
		
		s << indent << "\t)" << endl;
	}
	//
	
	s << indent << ")" << endl;
}


void Basic::AtomBase::print(std::ostream& s)
{
  for (size_t k = 0; k < param.size(); k++)
    param[k]->print(s << ' ');
}

void Basic::Atom::print(std::ostream& s, bool neg)
{
  if (neg) s << "(not ";
  s << "(" << pred->print_name;
  AtomBase::print(s);
  s << ")";
  if (neg) s << ")";
}

void Basic::AtomBase::pushVarParams(variable_vec v){
	for (variable_vec::iterator it = v.begin(); it != v.end(); it++){
		param.push_back(*it);
	}
}


vector<Basic::Atom*> Basic::Atom::getInstances(){
	vector<Basic::Atom*> result;
	
	vector<symbol_vec> partial;
	vector<symbol_vec> complete;
	
	partial.push_back(param);
	
	while(!partial.empty()){
		symbol_vec tuple = partial.back();		
		partial.pop_back();
		int i = 0;
		// Set i to first non-ground parameter
		for (i=0; (i<tuple.size() && tuple[i] -> sym_class != Basic::sym_variable); i++);
		
		if (i == tuple.size()){// all parameters are ground
			complete.push_back(tuple);
		}
		else{// i-th parameter is grounded
			Basic::TypeSymbol* t = (Basic::TypeSymbol*) tuple[i] -> sym_type;
			for(vector<Basic::Symbol*>::iterator elementIt = t ->elements.begin(); elementIt != t->elements.end(); elementIt++){
				symbol_vec* newTuple = new symbol_vec(tuple);
				(*newTuple)[i]= *elementIt;
				partial.push_back(*newTuple);
			}			
		}
	}	
	for(vector<symbol_vec>::iterator it = complete.begin(); it != complete.end(); it++){
		Basic::Atom* atom = new Atom(pred);
		atom -> neg = neg;
		atom -> param = *it;
		result.push_back(atom);
	}
		
	return result;
}



















