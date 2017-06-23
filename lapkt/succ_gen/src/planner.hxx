#ifndef __PLANNER__
#define __PLANNER__

#include <py_strips_prob.hxx>
#include <fwd_search_prob.hxx>
#include <strips_state.hxx>
#include <watched_lit_succ_gen.hxx>

typedef std::vector<std::string> StrList;
// using aptk::State;
using	aptk::WatchedLitSuccGen;

class	Planner : public STRIPS_Problem
{
public:

	Planner( );
	Planner( std::string, std::string );
	virtual ~Planner();

	
	virtual void setup();
	void	solve();

	std::string	m_log_filename;
	std::string	m_plan_filename;

	WatchedLitSuccGen* m_w_succ_gen;

	// added by Micha:
	std::string get_action_signature(int index);

	void load(std::string domain_file,std::string instance_file);
	void proceed_with_action(int action_index);
	StrList next_actions_from_current();
	StrList next_actions(aptk::State s);
	aptk::State create_state(boost::python::list& list);
	StrList next_actions_from_atoms(boost::python::list& atoms ,boost::python::dict& atom_table);
	// boost::python::list create_atoms(boost::python::dict& state);
protected:
	aptk::State* m_current_state;
	aptk::State state_from_fluent_vec(aptk::Fluent_Vec& I);
	float	do_search( );

};

#endif
