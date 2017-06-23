#include <planner.hxx>
#include <strips_state.hxx>
#include <aptk/string_conversions.hxx>

#include <iostream>
#include <fstream>
#include <ff_to_aptk.hxx>


using	aptk::agnostic::Fwd_Search_Problem;
using 	aptk::State;


using namespace boost::python;
Planner::Planner()
	: STRIPS_Problem(), m_log_filename( "planner.log"), m_plan_filename( "plan.ipc" ) {

}

Planner::Planner( std::string domain_file, std::string instance_file )
	: STRIPS_Problem( domain_file, instance_file ),  m_log_filename( "planner.log" ), m_plan_filename( "plan.ipc" ) {
}

Planner::~Planner() {
	delete m_w_succ_gen;
	delete m_current_state;
}

void Planner::load(std::string domain_file,std::string instance_file) {
	aptk::FF_Parser::get_problem_description( domain_file, instance_file, *instance());
}
void	
Planner::setup() {
	//Call superclass method, then do you own thing here
	STRIPS_Problem::setup();
	instance()->initialize_successor_generator();

	//NIR: Initialize both successor generators
	instance()->make_action_tables();
	// aptk::STRIPS_Problem prob = this.m_problem;
	m_w_succ_gen = new WatchedLitSuccGen(*instance());
	
	Fwd_Search_Problem	search_prob( instance() );
	m_current_state = search_prob.init();
	// WatchedLitSuccGen w_succ_gen(*instance());

	// std::cout << "PDDL problem description loaded: " << std::endl;
	// std::cout << "\tDomain: " << instance()->domain_name() << std::endl;
	// std::cout << "\tProblem: " << instance()->problem_name() << std::endl;
	// std::cout << "\t#Actions: " << instance()->num_actions() << std::endl;
	// std::cout << "\t#Fluents: " << instance()->num_fluents() << std::endl;

}

float
Planner::do_search(  ) {
    return 0.0;
}

void	
Planner::solve() {

	Fwd_Search_Problem	search_prob( instance() );

	do_search(  );
	

}

//added by Micha 
// StrList Planner::next_actions(State s) {
// 	std::cout << "Calculating applicable actions" << std::endl;

// 	Fwd_Search_Problem	search_prob( instance() );
// 	State* s0 = &s;

// 	instance()->initialize_successor_generator();

// 	//NIR: Initialize both successor generators
// 	instance()->make_action_tables();
// 	// aptk::STRIPS_Problem prob = this.m_problem;
	
// 	WatchedLitSuccGen w_succ_gen(*instance());

// 	std::cout << "Applicable actions at root with successor generator: " << std::endl;	
	
// 	std::vector< aptk::Action_Idx > app_set;
	
// 	search_prob.applicable_set( *s0, app_set );

// 	StrList actions(app_set.size());

// 	for ( unsigned i = 0; i < app_set.size(); i++ ) {
					
// 		// std::cout << instance()->actions()[app_set[i]]->signature() << std::endl;
// 		actions[i] = instance()->actions()[app_set[i]]->signature();
// 		//std::cout << '.';
// 	}	

// 	return actions;
// }

std::string Planner::get_action_signature(int index) {
	return instance()->actions()[index]->signature();
}

StrList Planner::next_actions_from_current() {
	return next_actions(*m_current_state);
}
void Planner::proceed_with_action(int action_index) {
	m_current_state = m_current_state->progress_through(*instance()->actions()[action_index]);
}

StrList Planner::next_actions(aptk::State s) {
		
	aptk::State* s0 = &s;

	StrList actions;

	for (auto i = m_w_succ_gen->applicable_actions(*s0) ; !i.finished(); ++i){			
			actions.push_back(instance()->actions()[*i]->signature());
	}

	return actions;
}

aptk::State Planner::state_from_fluent_vec(aptk::Fluent_Vec& I) {
	aptk::State* s = new aptk::State( *instance() );

		for(unsigned i = 0; i < I.size(); i++)
				s->set(I[i]);

		std::sort( s->fluent_vec().begin(), s->fluent_vec().end() );

		s->update_hash();

		return *s;	
}

aptk::State Planner::create_state(boost::python::list& lits){
	aptk::Fluent_Vec I;

		for( int i = 0; i < len(lits); i++ ) {
			boost::python::tuple li = extract< tuple >( lits[i] );
			int 	fl_idx 		= extract<int>(li[0]);
			bool	negated 	= extract<bool>(li[1]);
			if ( negated ) {
				assert( m_negated[fl_idx] );
				I.push_back( m_negated[fl_idx]->index() );
				continue;
			}
			I.push_back( fl_idx );
		}

		// complete initial state under negation
		for ( unsigned p = 0; p < instance()->num_fluents(); p++ ) {
			if ( p >= m_negated.size() ) continue; // p is a negated fluent!
			if ( std::find( I.begin(), I.end(), p ) != I.end() ) 
				continue;
			assert( p < m_negated.size() );
			if ( m_negated.at(p) ) 
				I.push_back( m_negated[ p ]->index() );
		} 	

		return state_from_fluent_vec(I);
}

StrList Planner::next_actions_from_atoms(boost::python::list& atoms ,boost::python::dict& atom_table) {

	aptk::Fluent_Vec I;
	// std::cout << "ENCODING: " << std::endl;	
	for( int i = 0; i < len(atoms); i++ ) {
			boost::python::tuple li = extract< tuple >(atoms[i]);
			std::string atom = extract<std::string>(li[0]);
			bool	negated 	= extract<bool>(li[1]);		
			
			// atom_table.get(atom)
			if(atom_table.has_key(atom)){
				// std::cout << "HAS KEY: " << atom << std::endl;		
				int 	fl_idx 		= extract<int>(atom_table.get(atom));
				// std::cout <<  fl_idx << std::endl;
				if ( negated ) {
					assert( m_negated[fl_idx] );
					I.push_back( m_negated[fl_idx]->index() );
					continue;
				}
				I.push_back( fl_idx );	
			}
		}
		// complete initial state under negation
		for ( unsigned p = 0; p < instance()->num_fluents(); p++ ) {
			if ( p >= m_negated.size() ) continue; // p is a negated fluent!
			if ( std::find( I.begin(), I.end(), p ) != I.end() ) 
				continue;
			assert( p < m_negated.size() );
			if ( m_negated.at(p) ) 
				I.push_back( m_negated[ p ]->index() );
		} 	
	
	return next_actions(state_from_fluent_vec(I));
}

// boost::python::list Planner::create_atoms(boost::python::dict& state) {
// 	//  d.iterkeys().attr("next")() 
// 	boost::python::object objectKey, objectValue; 
// 	const boost::python::object objectKeys = state.iterkeys();
// 	const boost::python::object objectValues = state.itervalues();
// 	unsigned long ulCount = boost::python::extract<unsigned long>(state.attr("__len__")());
// 	for( unsigned long u = 0; u < ulCount; u++ )
// 	{
// 		objectKey = objectKeys.attr( "next" )();
// 		objectValue = objectValues.attr( "next" )();

// 		// for (auto i = state.iterkeys().attr("next")() ; !i.finished(); ++i){			
// 		// 			// actions.push_back(instance()->actions()[*i]->signature());
// 		// 	boost::python::tuple li = extract< tuple >(state[i]);			
// 		// 	std::string predicate_name = extract<std::string>(li[0]);
// 		// 	std::cout << predicate_name << std::endl;
// 		// }
// 		std::string predicate_name = extract<std::string>(objectKey);
// 		std::string predicate_set = extract<boost::python::list>(objectValues);
		
// 		std::cout << predicate_name << std::endl;
// 	}
// 	return boost::python::list();
// }