
#include "name.h"
#include <sstream>

bool Name::domain_name_only = false;
bool Name::problem_name_only = false;

Name::~Name()
{
  // done
}

std::string Name::to_string() const
{
  std::ostringstream s;
  write(s, true);
  return s.str();
}

bool Name::equals(const Name* name) const
{
  return (to_string() == name->to_string());
}

void StringName::write(std::ostream& s, bool cat) const {
  s << _string;
}

void CopyName::write(std::ostream& s, bool cat) const {
  s << _string;
}
