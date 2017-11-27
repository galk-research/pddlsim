#ifndef INDEX_H
#define INDEX_H

#include <set>
#include <vector>
#include <limits.h>

#define no_such_index UINT_MAX

class index_vec : public std::vector<int> {
 public:
   index_vec( size_t n = 0, int i = 0 ) : std::vector<int>(n,i) { }
};
class bool_vec : public std::vector<bool> {
 public:
   bool_vec( size_t n = 0, bool b = false ) : std::vector<bool>(n,b) { }
   void bitwise_complement() { for( size_t k = 0; k < size(); ++k ) (*this)[k] = !(*this)[k]; }
   void bitwise_or( const bool_vec &b ) { for( size_t k = 0; (k < b.size()) && (k < size()); ++k ) (*this)[k] = (*this)[k] || b[k]; }

};
class index_set : public std::set<int> {
 public:
  bool intersect( const index_set &s ) const
  {
    for( const_iterator si = s.begin(); si != s.end(); ++si )
      if( find( *si ) != end() ) return( true );
    return( false );
  }
  bool contains( size_t e ) const { return( find(e) != end() ); }
  bool contains( const index_set &s ) const { for( const_iterator si = s.begin(); si != s.end(); ++si ) if( !contains(*si) ) return( false ); return( true ); }
};

class index_vec_vec : public std::vector<index_vec> { };
class index_set_vec : public std::vector<index_set> { };

#endif
