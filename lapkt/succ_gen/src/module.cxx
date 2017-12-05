#include <planner.hxx>
#include <strips_state.hxx>

#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

using namespace boost::python;
using aptk::State;

BOOST_PYTHON_MODULE( liblapkt )
{
	class_<StrList>("StrList")
        .def(vector_indexing_suite<StrList>() );

	class_<State>("State", no_init);

	class_<Planner>("Planner")
		.def( init< std::string, std::string >() )
		.def( "add_atom", &Planner::add_atom )
		.def( "add_action", &Planner::add_action )
		.def( "add_mutex_group", &Planner::add_mutex_group )
		.def( "num_atoms", &Planner::n_atoms )
		.def( "num_actions", &Planner::n_actions )
		.def( "get_atom_name", &Planner::get_atom_name )
		.def( "get_domain_name", &Planner::get_domain_name )
		.def( "get_problem_name", &Planner::get_problem_name )
		.def( "add_precondition", &Planner::add_precondition )
		.def( "add_effect", &Planner::add_effect )
		.def( "add_cond_effect", &Planner::add_cond_effect )
		.def( "set_cost", &Planner::set_cost )
		.def( "notify_negated_conditions", &Planner::notify_negated_conditions )
		.def( "create_negated_fluents", &Planner::create_negated_fluents )
		.def( "set_init", &Planner::set_init )
		.def( "set_goal", &Planner::set_goal )
		.def( "set_domain_name", &Planner::set_domain_name )
		.def( "set_problem_name", &Planner::set_problem_name )
		.def( "write_ground_pddl", &Planner::write_ground_pddl )
		.def( "print_action", &Planner::print_action )
		.def( "setup", &Planner::setup )
		.def( "solve", &Planner::solve )
		.def("print_actions",&Planner::print_actions)
		.def_readwrite( "parsing_time", &Planner::m_parsing_time )
		.def_readwrite( "ignore_action_costs", &Planner::m_ignore_action_costs )
		.def_readwrite( "log_filename", &Planner::m_log_filename )
		.def( "next_actions", &Planner::next_actions )
		.def("create_state",&Planner::create_state )
		.def("next_actions_from_atoms",&Planner::next_actions_from_atoms )
		.def("next_actions_from_current",&Planner::next_actions_from_current)
		.def("load", &Planner::load)
		.def("get_action_signature", &Planner::get_action_signature)
		.def("proceed_with_action",&Planner::proceed_with_action)
		// .def("create_atoms",&Planner::create_atoms)
	;

	
}

