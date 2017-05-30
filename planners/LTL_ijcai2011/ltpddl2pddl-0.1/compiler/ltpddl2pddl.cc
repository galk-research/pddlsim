
#include "problem.h"
#include "parser.h"
#include <fstream>

using namespace std;

int main(int argc, char *argv[]){
	ostream *domainOut = &cout, *problemOut = &cout;// by default, print everything to cout
	char *domainIn = NULL, *problemIn = NULL;
	
	if( argc == 1 ) {
		std::cerr << "Usage: " << argv[0] << " [<options>] <pddl-files>"
			<< std::endl << std::endl
			<< "Example: " << argv[0] << " -df domain-out-file -pf problem-out-file examples/sortn.pddl examples/s3.pddl"
			<< std::endl << endl;
		exit(0);
	}

	// Input arguments: 
	for( int k = 1; k < argc; ++k ) {
		  if (strcmp(argv[k],"-df") == 0) {
			  // an output domain file has been specified
			  domainOut = new ofstream(argv[++k]);
		  }
		  else if (strcmp(argv[k],"-pf") == 0) {
			  // an output problem file has been specified
			  problemOut = new ofstream(argv[++k]);
		  }
	
		  // files
		  else if (*argv[k] != '-') {
			  if (domainIn == NULL){
				  domainIn = argv[k];
			  }
			  else{ // problemIn == NULL
				  problemIn = argv[k];
			  }
		  }
	}

	Parser parser(domainIn, problemIn);
	parser.parse();  
	parser.incorporateLTL(); // Changes reader so as to include the BA and the goal to find an infinite plan
	parser.printDomainPDDL(*domainOut);
	parser.printProblemPDDL(*problemOut);
  
	ofstream* oDomainOut = dynamic_cast<ofstream*>(domainOut);
	if(oDomainOut != NULL){	  
		oDomainOut -> close();
	}
  
  ofstream* oProblemOut = dynamic_cast<ofstream*>(problemOut);
  if(oProblemOut != NULL){	  
	  oProblemOut -> close();
  }

  return 0;
}

