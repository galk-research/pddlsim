#ifndef NAME_H
#define NAME_H

#include <string>
#include <iostream>
#include <vector>

class Name {
 public:
  static bool domain_name_only;
  static bool problem_name_only;

  virtual ~Name();
  virtual void write(std::ostream& s, bool cat) const = 0;

  std::string to_string() const;
  bool equals(const Name* name) const;
};

class name_vec : public std::vector<const Name*> { };

inline std::ostream& operator<<(std::ostream& s, const Name& n)
{
  n.write(s, false);
  return s;
}

inline std::ostream& operator<<(std::ostream& s, const Name* n)
{
  n->write(s, false);
  return s;
}

class StringName : public Name {
  const char* _string;
 public:
  StringName(const char* s) : _string(s) { };
  virtual ~StringName() { };
  virtual void write(std::ostream& s, bool cat) const;
};

class CopyName : public Name {
  char* _string;
 public:
  CopyName(const char* s) : _string(strdup(s)) { };
  virtual ~CopyName() { delete _string; };
  virtual void write(std::ostream& s, bool cat) const;
};

#endif
