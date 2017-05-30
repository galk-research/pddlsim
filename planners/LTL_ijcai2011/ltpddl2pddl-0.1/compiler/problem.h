#ifndef PROBLEM_H
#define PROBLEM_H

#include "name.h"
#include "index.h"

class Instance {
  bool         cross_referenced;

 public:
  static bool always_write_parameters_declaration;
  static bool always_write_requirements_declaration;
  static bool always_write_precondition;
  static bool always_write_conjunction;

  class Action;

  struct Atom {
    Name*      name;
	std::vector<Action*> pos_effect_of; // (FP) references actions this (positive) atom depends on
	std::vector<Action*> neg_effect_of; // (FP) references actions this (negative) atom depends on
    std::vector<Action*> neg_when_effect_of; // (FP) references actions this (negative) atom conditionally depends on
    std::vector<Action*> pos_when_effect_of; // (FP) references actions this (positive) atom conditionally depends on
    size_t     index;
    bool       init;
    bool       goal;
    Atom(Name* n = 0, size_t i = 0) : name(n), index(i), init(false), goal(false) { }
    Atom& operator=(const Atom& a) { name = a.name; index = a.index; init = a.init; goal = a.goal; return *this; }
    bool operator==(const Atom& a) { return (index == a.index); }
  };

  struct When {
    index_set pre;
    index_set add;
    index_set del;
    When() { }
  };
  struct when_vec : public std::vector<When> { };

  struct Action {
    Name*      name;
    size_t     index;
    index_set  pre;
    index_set  add;
    index_set  del;
    index_vec_vec cls;
    index_vec_vec oneof;
    when_vec   when;
    size_t     cost;
    Action(Name* n = 0, size_t i = 0) : name(n), index(i), cost(1) { }
    Action& operator=(const Action& a) { name = a.name; index = a.index; pre = a.pre; add = a.add; del = a.del; cost = a.cost; return *this; }
    bool operator==(const Action& a) { return (index == a.index); }
    void print( std::ostream &os, const Instance &i ) const;
  };

  class atom_vec : public std::vector<Atom*> { };
  class action_vec : public std::vector<Action*> { };

  Name*         name;
  atom_vec      atoms;
  action_vec    actions;
  index_set     init_atoms;
  index_set     goal_atoms;
  index_vec_vec goal_cls;
  static int    default_trace_level;
  int           trace_level;

  Instance(Name* n = 0) : cross_referenced(false), name(n), trace_level(default_trace_level) { }
  Instance(const Instance& ins);
  ~Instance() { }

  Atom&      new_atom(Name* name);
  Action&    new_action(Name* name);

  // change (remove from) instance
  void remove_actions(const bool_vec& set, index_vec& map);
  void remove_atoms(const bool_vec& set, index_vec& map);
  void remap_atom_set(index_set& set, const index_vec& atom_map);
  void set_initial(const index_set& init);
  void set_goal(const index_set& init);

  // compute/clear secondary instance info
  void cross_reference();
  void clear_cross_reference();

  // access instance information
  size_t n_atoms() const { return atoms.size(); }
  size_t n_actions() const { return actions.size(); }

  // write utilities
  void write_atom_set(std::ostream& s, const index_set& set) const;
  void write_atom_set(std::ostream& s, const bool* set) const;
  void write_atom_set(std::ostream& s, const bool_vec& set) const;
  void write_atom_sets(std::ostream& s, const index_set_vec& sets) const;
  void write_action_set(std::ostream& s, const index_vec& set) const;
  void write_action_set(std::ostream& s, const bool* set) const;
  void write_action_set(std::ostream& s, const bool_vec& set) const;
  void write_domain(std::ostream& s) const;
  void write_problem(std::ostream& s) const;
  void print_atoms(std::ostream& s) const;
  void print_actions(std::ostream& s) const;
  void print(std::ostream& s) const;
  
	// (FP) smv encoding functions:
	void print_smv_main(std::ostream& s) const;
	void print_smv_action_list(std::ostream& s, std::string) const;
	void print_smv_system(std::ostream& s) const;
	std::set<std::string> getFluents()const;
	void print_smv_environment(std::ostream& s) const;
	void print_smv(std::ostream& s) const;
	//
};

#endif
