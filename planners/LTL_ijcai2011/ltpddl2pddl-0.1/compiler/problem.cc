
#include "problem.h"
#include <assert.h>
using namespace std;

bool Instance::always_write_parameters_declaration = false;
bool Instance::always_write_requirements_declaration = false;
bool Instance::always_write_precondition = false;
bool Instance::always_write_conjunction = false;
int  Instance::default_trace_level = 0;

Instance::Instance(const Instance& ins)
  : cross_referenced(false),
    name(ins.name),
    atoms(ins.atoms),
    actions(ins.actions),
    init_atoms(ins.init_atoms),
    goal_atoms(ins.goal_atoms),
    trace_level(ins.trace_level)
{
}

Instance::Atom& Instance::new_atom(Name* name)
{
  Atom *a = new Atom( name, atoms.size() );
  atoms.push_back( a );
  if (trace_level > 2)
    std::cerr << "atom " << a->index << "." << a->name << " created" << std::endl;
  return *a;
}

Instance::Action& Instance::new_action(Name* name)
{
  Action *a = new Action( name, actions.size() );
  actions.push_back( a );
  if (trace_level > 2)
    std::cerr << "action " << a->index << "." << a->name << " created" << std::endl;
  return *a;
}

void Instance::cross_reference()
{
  if (cross_referenced) return;
  init_atoms.clear();
  goal_atoms.clear();
  for (size_t k = 0; k < atoms.size(); k++) {
    Atom& prop = *atoms[k];
    if (prop.init) init_atoms.insert(k);
    if (prop.goal) goal_atoms.insert(k);
  }
  cross_referenced = true;
}

void Instance::remap_atom_set(index_set& set, const index_vec& atom_map)
{
  index_set nset;
  for( index_set::iterator si = set.begin(); si != set.end(); ++si ) {
    if( atom_map[*si] != no_such_index ) {
      nset.insert( atom_map[*si] );
    }
  }
  set = nset;
}

void Instance::remove_actions(const bool_vec& set, index_vec& map)
{
  index_vec rm_map( actions.size() );
  size_t j = 0;
  for( size_t k = 0; k < actions.size(); ++k ) {
    if( !set[k] ) {
      if( j < k ) {
        actions[j] = actions[k];
        actions[j]->index = j;
      }
      rm_map[k] = j;
      ++j;
    }
    else
      rm_map[k] = no_such_index;
  }
  while( actions.size() > j ) actions.pop_back();

  for( size_t k = 0; k < map.size(); ++k ) {
    if( map[k] != no_such_index )
      map[k] = rm_map[map[k]];
  }
}

void Instance::remove_atoms(const bool_vec& set, index_vec& map)
{
  index_vec rm_map( atoms.size() );
  size_t j = 0;
  for( size_t k = 0; k < atoms.size(); ++k ) {
    if( !set[k] ) {
      if( j < k ) {
	atoms[j] = atoms[k];
	atoms[j]->index = j;
      }
      rm_map[k] = j;
      ++j;
    }
    else
      rm_map[k] = no_such_index;
  }
  while( atoms.size() > j ) atoms.pop_back();

  for( size_t k = 0; k < actions.size(); ++k ) {
    remap_atom_set( actions[k]->pre, rm_map );
    remap_atom_set( actions[k]->add, rm_map );
    remap_atom_set( actions[k]->del, rm_map );
  }

  for( size_t k = 0; k < map.size(); ++k ) {
    if( map[k] != no_such_index )
      map[k] = rm_map[map[k]];
  }
}

void Instance::set_initial(const index_set& init)
{
  for (size_t k = 0; k < n_atoms(); k++) atoms[k]->init = false;
  for ( index_set::const_iterator it = init.begin(); it != init.end(); ++it )
    atoms[*it]->init = true;
  init_atoms = init;
}

void Instance::set_goal(const index_set& goal)
{
  for (size_t k = 0; k < n_atoms(); k++) {
    atoms[k]->goal = false;
  }
  for( index_set::const_iterator gi = goal.begin(); gi != goal.end(); ++gi )
    atoms[*gi]->goal = true;
  goal_atoms = goal;
}

void Instance::clear_cross_reference()
{
  init_atoms.clear();
  goal_atoms.clear();
  cross_referenced = false;
}

void Instance::write_atom_set(std::ostream& s, const index_set& set) const
{
  s << '{';
  for( index_set::const_iterator si = set.begin(); si != set.end(); ++si ) {
    if( si != set.begin() ) s << ',';
    s << atoms[*si]->name;
  }
  s << '}';
}

void Instance::write_atom_set(std::ostream& s, const bool* set) const
{
  s << '{';
  bool need_comma = false;
  for (size_t k = 0; k < n_atoms(); k++) if (set[k]) {
    if (need_comma) s << ',';
    s << atoms[k]->name;
    need_comma = true;
  }
  s << '}';
}

void Instance::write_atom_set(std::ostream& s, const bool_vec& set) const
{
  s << '{';
  bool need_comma = false;
  for (size_t k = 0; k < n_atoms(); k++) if (set[k]) {
    if (need_comma) s << ',';
    s << atoms[k]->name;
    need_comma = true;
  }
  s << '}';
}

void Instance::write_atom_sets(std::ostream& s, const index_set_vec& sets) const
{
  s << '{';
  for (size_t k = 0; k < sets.size(); k++) {
    if (k > 0) s << ',';
    write_atom_set(s, sets[k]);
  }
  s << '}';
}

void Instance::write_action_set(std::ostream& s, const index_vec& set) const
{
  s << '{';
  for (size_t k = 0; k < set.size(); k++) {
    if (k > 0) s << ',';
    s << actions[set[k]]->name;
  }
  s << '}';
}

void Instance::write_action_set(std::ostream& s, const bool* set) const
{
  s << '{';
  bool need_comma = false;
  for (size_t k = 0; k < n_actions(); k++) if (set[k]) {
    if (need_comma) s << ',';
    s << actions[k]->name;
    need_comma = true;
  }
  s << '}';
}

void Instance::write_action_set(std::ostream& s, const bool_vec& set) const
{
  s << '{';
  bool need_comma = false;
  for (size_t k = 0; k < n_actions(); k++) if (set[k]) {
    if (need_comma) s << ',';
    s << actions[k]->name;
    need_comma = true;
  }
  s << '}';
}

void Instance::write_domain(std::ostream& s) const
{
  if (name) {
    Name::domain_name_only = true;
    s << "(define (domain " << name << ")" << std::endl;
    Name::domain_name_only = false;
  }
  else {
    s << "(define (domain NONAME)" << std::endl;
  }

  if (always_write_requirements_declaration) {
    s << " (:requirements :strips)" << std::endl;
  }

  if (n_atoms() > 0) {
    s << " (:predicates";
    for (size_t k = 0; k < n_atoms(); k++) {
      s << " (";
      atoms[k]->name->write(s, true);
      s << ")";
    }
    s << ")" << std::endl;
  }

  for (size_t k = 0; k < n_actions(); k++) {
    s << " (:action ";
    actions[k]->name->write(s, true);
    if (always_write_parameters_declaration) {
      s << std::endl << "  :parameters ()";
    }
    if (actions[k]->pre.size() > 0) {
      s << std::endl << "  :precondition";
      if ((actions[k]->pre.size() > 1) || always_write_conjunction)
        s << " (and";
      for( index_set::const_iterator pi = actions[k]->pre.begin(); pi != actions[k]->pre.end(); ++pi ) {
        s << " (";
        atoms[*pi<0?-(*pi)-1:(*pi)-1]->name->write(s, true);
        s << ")";
      }
      if ((actions[k]->pre.size() > 1) || always_write_conjunction)
        s << ")";
    }
    else if (always_write_precondition) {
      if (always_write_conjunction)
        s << std::endl << "  :precondition (and)";
      else
        s << std::endl << "  :precondition ()";
    }

    if ((actions[k]->add.size() + actions[k]->del.size()) > 0) {
      s << std::endl << "  :effect";
      if ((actions[k]->add.size() + actions[k]->del.size()) > 1)
        s << " (and";
      for( index_set::const_iterator ai = actions[k]->add.begin(); ai != actions[k]->add.end(); ++ai ) {
        s << " (";
        atoms[*ai]->name->write(s, true);
        s << ")";
      }
      for( index_set::const_iterator di = actions[k]->del.begin(); di != actions[k]->del.end(); ++di ) {
        s << " (not (";
        atoms[*di]->name->write(s, true);
        s << "))";
      }
      if ((actions[k]->add.size() + actions[k]->del.size()) > 1) s << ")";
    }
    s << ")" << std::endl;
  }
  s << ")" << std::endl;
}

void Instance::write_problem(std::ostream& s) const
{
  if (name) {
    Name::problem_name_only = true;
    s << "(define (problem " << name << ")" << std::endl;
    Name::problem_name_only = false;
    Name::domain_name_only = true;
    s << " (:domain " << name << ")" << std::endl;
    Name::domain_name_only = false;
  }
  else {
    s << "(define (problem NONAME)" << std::endl;
    s << " (:domain NONAME)" << std::endl;
  }

  bool write_init = false;
  for (size_t k = 0; (k < n_atoms()) && !write_init; k++)
    if (atoms[k]->init) write_init = true;
  if (write_init) {
    s << " (:init";
    for (size_t k = 0; k < n_atoms(); k++) if (atoms[k]->init) {
      s << " (";
      atoms[k]->name->write(s, true);
      s << ")";
    }
    s << ")" << std::endl;
  }

  size_t write_goal = 0;
  for (size_t k = 0; (k < n_atoms()) && (write_goal < 2); k++)
    if (atoms[k]->goal) write_goal += 1;
  if (write_goal > 0) {
    s << " (:goal";
    if (write_goal > 1) s << " (and";
    for (size_t k = 0; k < n_atoms(); k++) if (atoms[k]->goal) {
      s << " (";
      atoms[k]->name->write(s, true);
      s << ")";
    }
    if (write_goal > 1) s << ")";
    s << ")" << std::endl;
  }

  s << ")" << std::endl;
}

void Instance::print(std::ostream& s) const
{
  print_atoms(s);
  print_actions(s);
  s << "goals: ";
  write_atom_set(s, goal_atoms);
  s << std::endl;
}

//(FP) beginning of smv extension section --------------------------------------------------------------------------
void Instance::print_smv_main(std::ostream& s) const{
	s << "MODULE main" << endl;
	s << "\tVAR" << endl;
	s << "\t\tenvironment : system environment_module(agent);" << endl;
	s << "\t\tagent : system system_module(environment);" << endl;
	s << "\tDEFINE" << endl;
	s << "\t\tjx := agent.jx;" << endl;
	s << "-- end main " << endl;
}

void Instance::print_smv_action_list(std::ostream& s, string prefix) const{
	// (FP) Prints all actions plus the special one 
	s << prefix;
	for (size_t k = 0; k < n_actions(); k++) {
		s << actions[k] -> name -> to_string() << ", ";
		if ((k+1)%5 == 0 && k < n_actions()-1)
			cout << endl << prefix;
	}
	s << "smv_stop_action"; // (FP) Absence of special actions in the planning domain should be checked
}

void Instance::print_smv_system(std::ostream& s) const{
	s << "MODULE system_module(env)" << endl;
	s << "\tVAR" << endl;
	s << "\t\taction : {" << endl; 
	print_smv_action_list(s,"\t\t\t\t"); 
	s << "};" << endl;
	s << "\t\tjx : 1..1;" << endl;
	s << "\tINIT" << endl;
	s << "\t\t" << "action = smv_start_action" << endl;
	s << "\tTRANS" << endl;
	s << "\t\t" << "-- Special actions:" << endl;
	s << "\t\t" << "next(action) != smv_start_action &" << endl;
	s << "\t\t" << "((next(action) = smv_stop_action) <-> " << endl;
	if (goal_atoms.size() + goal_cls.size() == 0){//(FP) No goal specified: TRUE
		s << "\t\t\t" << "TRUE";
	}
	else{//(FP) A goal has been specified
		s << "\t\t\t" << "(";//(FP) Condition: all goal requirements are satisfied
		index_set::const_iterator goalIt = goal_atoms.begin();
		while (goalIt != goal_atoms.end()){//(FP) 1. All goal atoms are satisfied on next state
			if (*goalIt > 0){//(FP) Positive atom
				s << "next(env." << atoms[*goalIt-1] -> name -> to_string() << ")";
			}
			else{// (FP) Negative atom
				s << "!next(env." << atoms[-(*goalIt)-1] -> name -> to_string() << ")";
			}
			goalIt++;
			if (goalIt != goal_atoms.end() || goal_cls.size() > 0){
				s << " & ";
			}
			else{
				s << ")" << endl;
			}
		}
		//(FP) 2. All goal clauses are satisfied on next state
		for (size_t i = 0; i < goal_cls.size(); i++){
			s << "(";
			for (size_t j = 0; j < goal_cls[i].size(); j++){//(FP) within the clause
				if(goal_cls[i][j] > 0){//(FP) Postive atom
					s << "next(env." << atoms[goal_cls[i][j]-1] -> name -> to_string() << ")";					
				}
				else{//(FP) Negative atom
					s << "!next(env." << atoms[-goal_cls[i][j]-1] -> name -> to_string() << ")";					
				}
				if (j < goal_cls[i].size()-1){
					s << " | ";
				}
			}
			if (i < goal_cls.size()-1){
				s << " & ";
			}
			else{
				s << ")";
			}
		}
	}
	s << "\t\t" << ")&" << endl;
	s << "\t\t" << "-- Action preconditions" << endl;
	s << "\t\t" << "case" << endl;
	for (size_t i = 0; i < n_actions(); i++){
		index_set::const_iterator preIt = (actions[i]->pre).begin();
		if(preIt != (actions[i]->pre).end()){
			s << "\t\t\t" << "next(action) = " << actions[i] -> name -> to_string() << " : " ;
		}
		while( preIt != (actions[i]->pre).end()){
			if (*preIt > 0){// (FP) positive precondition
				s << "next(env." << atoms[*preIt-1] -> name -> to_string() << ")";
			}
			else{// (FP) negative precondition
				s << "!next(env." << atoms[-(*preIt)-1] -> name -> to_string() << ")";
			}
			preIt++;
			if (preIt != (actions[i]->pre).end()){
				s << " & ";
			}
			else{
				s << ";" << endl;
			}
		}
	}
	s << "\t\t\t" << "TRUE : TRUE; -- for special actions" << endl;
	s << "\t\t" << "esac" << endl;
	//(FP) output for justice requirements
	s << "\t\t" << "-- justice requirements: problem goal" << endl;
	s << "\t\t" << "JUSTICE" << endl;
	if (goal_atoms.size() + goal_cls.size() == 0){//(FP) No goal specified: TRUE
		s << "\t\t\t" << "TRUE" << endl;
	}
	else{//(FP) A goal has been specified
		s << "\t\t\t" << "(";//(FP) Condition: all goal requirements are satisfied
		index_set::const_iterator goalIt = goal_atoms.begin();
		while (goalIt != goal_atoms.end()){//(FP) 1. All goal atoms are satisfied on next state
			if (*goalIt > 0){//(FP) Positive atom
				s << "env." << atoms[*goalIt-1] -> name -> to_string();
			}
			else{// (FP) Negative atom
				s << "env." << atoms[-(*goalIt)-1] -> name -> to_string();
			}
			goalIt++;
			if (goalIt != goal_atoms.end() || goal_cls.size() > 0){
				s << " & ";
			}
			else{
				s << ")" << endl;
			}
		}
		//(FP) 2. All goal clauses are satisfied on next state
		for (size_t i = 0; i < goal_cls.size(); i++){
			s << "(";
			for (size_t j = 0; j < goal_cls[i].size(); j++){//(FP) within the clause
				if(goal_cls[i][j] > 0){//(FP) Postive atom
					s << "env." << atoms[goal_cls[i][j]-1] -> name -> to_string();					
				}
				else{//(FP) Negative atom
					s << "env." << atoms[-goal_cls[i][j]-1] -> name -> to_string();					
				}
				if (j < goal_cls[i].size()-1){
					s << " | ";
				}
			}
			if (i < goal_cls.size()-1){
				s << " & ";
			}
			else{
				s << ")";
			}
		}
	}
	s << "-- end system_module" << endl;
}

std::set<std::string> Instance::getFluents()const{// a set is used for avoiding multiple occurences
	std::set<std::string> r;
	for (size_t i = 0; i < n_atoms(); i++){
		r.insert(atoms[i] -> name -> to_string());
	}
	return r;
}

void Instance::print_smv_environment(std::ostream& s) const{
	//(FP) Main Module declaration
	s << "MODULE environment_module(ag)" << endl;
	//(FP) Variables declaration
	s << "\tVAR" << endl;
	s << "\t\t" << "-- domain fluents" << endl;
	set<std::string> fluents = getFluents();
	for (set<std::string>::const_iterator fIt = fluents.begin(); fIt != fluents.end(); fIt++){
		s << "\t\t\t" << *fIt << " : boolean; " << endl;
	}
	s << endl;
	//(FP) Initial conditions (not necessary, but useful for improving readability of plans produced by TLV
	s << "\tINIT" << endl;
		
	s << "\t\t" << "-- all fluents are initially set to false. They will be correctly initialized at the first step by smv_start_action" << endl;
	s << "\t\t\t";
	int f = 0;//(FP) Fluent counter (only for output readability purposes)
	set<std::string>::const_iterator fIt = fluents.begin();
	while( fIt != fluents.end()){
		s << "!" << *fIt;
		fIt++;
		if (fIt != fluents.end())
			s << " & ";
		if ((f+1)%5 == 0 || fIt == fluents.end())
			s << endl << "\t\t\t";
		f++;
	}
	//(FP) Transition Relation
	s << endl << "\tTRANS" << endl;	
	s << "\t--transition relation based on fluents and actions plus stop action for goal achievement" << endl;
	//(FP) One block per fluent
	//(FP) !!Warning!! There may be (safe) multiple occurrences of a same block! Not a problem but TB fixed, sooner or later...
	for (size_t i = 0; i < n_atoms(); i++){
		Instance::Atom* atom = atoms[i];
		string atom_name = atom -> name -> to_string();
		s << "\t\t" << "-- block for fluent " << atom_name << endl;
		s << "\t\t" << "case" << endl;
		//(FP)DIRECT EFFECTS:
		//(FP)negative direct effects
		if (atom -> neg_effect_of.size() + atom -> pos_effect_of.size() > 0)
			s << "\t\t\t" << "--direct effects" << endl;
		for(size_t j = 0; j < (atom -> neg_effect_of).size(); j++){
			string action_name = atom -> neg_effect_of[j] -> name -> to_string();
			s << "\t\t\t" << "ag.action = " << action_name << " : " << "!next(" << atom_name << ");" << endl;
		}
		//(FP)positive direct effects
		for(size_t j = 0; j < (atom -> pos_effect_of).size(); j++){
			string action_name = atom -> pos_effect_of[j] -> name -> to_string();
			s << "\t\t\t" << "ag.action = " << action_name << " : " << "next(" << atom_name << ");" << endl;
		}
		//(FP)CONDITIONAL EFFECTS
		if (atom -> neg_when_effect_of.size() + atom -> pos_when_effect_of.size() > 0)
			s << "\t\t\t" << "--conditional effects" << endl;
		//(FP) Negative conditional effects
		for(size_t j = 0; j < (atom -> neg_when_effect_of).size(); j++){
			Instance::Action* currentAction = atom -> neg_when_effect_of[j];
			string action_name = currentAction -> name -> to_string();
			//(FP) Search for the conditional effect in current action's conditional effect set
			for(size_t k = 0; k < currentAction -> when.size(); k++){
				index_set::const_iterator delIt = currentAction -> when[k].del.begin();
				while(delIt != currentAction -> when[k].del.end()){
					if (atoms[*delIt] == atom){
						s << "\t\t\t" << "ag.action = " << action_name << " & ";
						//(FP) retrieving and printing (conjunction of) conditions
						index_set::const_iterator preIt = currentAction -> when[k].pre.begin();
						while(preIt != currentAction -> when[k].pre.end()){
							if (*preIt > 0){// Positive atom
								s << atoms[*preIt-1] -> name -> to_string();
							}
							else{ // Negative atom
								s << "!" << atoms[-*preIt-1] -> name -> to_string();
							}
							preIt ++;
							if (preIt != currentAction -> when[k].pre.end()){
								s << " & ";
							}
						}
						s << " : " << "!next(" << atom_name << ");" << endl;
					}
					delIt++;
				}
			}
		}
		
		//(FP)positive conditional effects
		for(size_t j = 0; j < (atom -> pos_when_effect_of).size(); j++){
			Instance::Action* currentAction = atom -> pos_when_effect_of[j];
			string action_name = currentAction -> name -> to_string();
			//(FP) Search for the conditional effect in current action's conditional effect set
			for(size_t k = 0; k < currentAction -> when.size(); k++){
				index_set::const_iterator addIt = currentAction -> when[k].add.begin();
				while(addIt != currentAction -> when[k].add.end()){
					if (atoms[*addIt] == atom){
						s << "\t\t\t" << "ag.action = " << action_name << " & ";
						//(FP) retrieving and printing (conjunction of) conditions
						index_set::const_iterator preIt = currentAction -> when[k].pre.begin();
						while(preIt != currentAction -> when[k].pre.end()){
							if (*preIt > 0){// Positive atom
								s << atoms[*preIt-1] -> name -> to_string();
							}
							else{ // Negative atom
								s << "!" << atoms[-*preIt-1] -> name -> to_string();
							}
							preIt ++;
							if (preIt != currentAction -> when[k].pre.end()){
								s << " & ";
							}
						}
						s << " : " << "next(" << atom_name << ");" << endl;
					}
					addIt++;
				}
			}
		}
		//(FP) Nondeterministic (oneof) effects
				
		//(FP) Default. Fluents are inertial: no change unless an explicit reason holds.
		s << "\t\t\t" << "--default" << endl;
		s << "\t\t\t" << "TRUE : next(" << atom_name << ") = " << atom_name << ";" << endl;
		s << "\t\t" << "esac" << endl;
		if (i < n_atoms()-1){
			s << "\t\t" << "&" << endl;
		}
	}
	s << "\tJUSTICE" << endl;
	s << "\t\tTRUE" << endl;
	s << "-- end environment_module" << endl;
}

void Instance::print_smv(std::ostream& s) const{
	s << "-- Automatically generated by pddl2smv" << endl;
// MAIN module section
	print_smv_main(s);
	s << endl;
// system_module section
	print_smv_system(s);
	s<< endl;
// environment_module section	
	print_smv_environment(s);
}

//(FP) end of smv extension section --------------------------------------------------------------------------


void Instance::print_atoms(std::ostream& s) const
{
  for (size_t k = 0; k < n_atoms(); k++) {
    s << k << ". " << atoms[k]->name << std::endl;
    s << "  init: " << (atoms[k]->init ? 'T' : 'F')
      << ", goal: " << (atoms[k]->goal ? 'T' : 'F')
      << std::endl;
  }
}

void Instance::Action::print(std::ostream& s, const Instance &i ) const
{
  s << name << ":" << std::endl;
  if( pre.size() > 0 ) {
    s << "  pre:";
    for( index_set::const_iterator pi = pre.begin(); pi != pre.end(); ++pi )
      s << ' ' << (*pi<0?*pi+1:*pi-1) << '.' << i.atoms[*pi<0?-(*pi)-1:(*pi)-1]->name;
    s << std::endl;
  }
  if( add.size() > 0 ) {
    s << "  add:";
    for( index_set::const_iterator ai = add.begin(); ai != add.end(); ++ai )
      s << ' ' << (*ai) << '.' << i.atoms[*ai]->name;
    s << std::endl;
  }
  if( del.size() > 0 ) {
  s << "  del:";
    for( index_set::const_iterator di = del.begin(); di != del.end(); ++di )
      s << ' ' <<  (*di) << '.' << i.atoms[*di]->name;
    s << std::endl;
  }
  if( cls.size() > 0 ) {
    s << "  cls: ";
    for( index_vec_vec::const_iterator ci = cls.begin(); ci != cls.end(); ++ci ) {
      s << "(";
      for( index_vec::const_iterator li = (*ci).begin(); li != (*ci).end(); ++li ) {
        int l = (*li), p = (l<0?-l:l);
        s << ' ' << (l<0?-(p-1):p-1) << '.' << i.atoms[p-1]->name;
      }
      s << ") ";
    }
    s << std::endl;
  }
  if( oneof.size() > 0 ) {
    s << "  oneof: ";
    for( index_vec_vec::const_iterator oi = oneof.begin(); oi != oneof.end(); ++oi ) {
      s << "(";
      for( index_vec::const_iterator li = (*oi).begin(); li != (*oi).end(); ++li ) {
        int l = (*li), p = (l<0?-l:l);
        s << ' ' << (l<0?-(p-1):p-1) << '.' << i.atoms[p-1]->name;
      }
      s << ") ";
    }
    s << std::endl;
  }
  if( when.size() > 0 ) {
    s << "  when:";
    for( when_vec::const_iterator wi = when.begin(); wi != when.end(); ++wi ) {
      s << (wi==when.begin()?" ":"       ");
      for( index_set::const_iterator li = (*wi).pre.begin(); li != (*wi).pre.end(); ++li ) {
        int l = (*li), p = (l<0?-l:l);
        s << ' ' << (l<0?-p+1:p-1) << '.' << i.atoms[p-1]->name;
      }
      s << " ==> :add";
      for( index_set::const_iterator ai = (*wi).add.begin(); ai != (*wi).add.end(); ++ai )
        s << ' ' << (*ai) << '.' << i.atoms[*ai]->name;
      s << " :del";
      for( index_set::const_iterator di = (*wi).del.begin(); di != (*wi).del.end(); ++di )
        s << ' ' << (*di) << '.' << i.atoms[*di]->name;
      s << std::endl;
    }
  }
  if( cost != 1 ) s << "  cost: " << cost << std::endl;
}

void Instance::print_actions( std::ostream &os ) const
{
  for (size_t k = 0; k < n_actions(); k++) {
    os << k << ". ";
    actions[k]->print( os, *this );
  }
  if( goal_cls.size() > 0 ) {
    os << "  goal_cls: ";
    for( index_vec_vec::const_iterator ci = goal_cls.begin(); ci != goal_cls.end(); ++ci ) {
      os << "(";
      for( index_vec::const_iterator li = (*ci).begin(); li != (*ci).end(); ++li ) {
        int l = (*li), p = (l<0?-l:l);
        os << ' ' << (l<0?-(p-1):p-1) << '.' << atoms[p-1]->name;
      }
      os << ") ";
    }
    os << std::endl;
  }
}

