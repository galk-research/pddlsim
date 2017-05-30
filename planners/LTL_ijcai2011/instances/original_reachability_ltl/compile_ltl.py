#!/usr/bin/python
import sys, os, glob
							
def call_pddl2smmv( domain_file, problems_path, path_pddl2smv   ) :
	current_dir = os.getcwd()
	os.chdir(problems_path)
	if not os.path.exists("tars"):
		os.mkdir("tars")
	else:
		cmd = "rm -f tars/*tar.bz2"
		os.system(cmd)

	for infile in glob.glob( os.path.join( '*.pddl') ):
		print("Processing: " + infile)
		basename, extension = os.path.splitext(infile)
		if not os.path.exists(basename):
			os.mkdir(basename)
			
		os.chdir(basename)
		cmd = path_pddl2smv + 'pddl2smv -df domain.pddl -pf '+basename+'_ba'+extension+' '+current_dir+'/'+domain_file+' '+'../'+infile		
		os.system(cmd)
		
		if os.path.getsize( "domain.pddl" ) != 0:
			outstream = open( 'MANIFEST', 'w')
			outstream.write("domain=domain.pddl\nproblem="+basename+'_ba'+extension)
			outstream.close()

			cmd = "tar -jcf ../tars/"+basename+".tar.bz2 *"
			os.system(cmd)
			os.chdir("..")
		else:
			os.chdir("..")
			cmd = "rm -fr "+basename
			os.system(cmd)


	os.chdir(current_dir)

def main() :
	

	if len( sys.argv ) != 2 :
		print >> sys.stderr, "Missing arguments!"
		print >> sys.stderr, "Usage: ./generate_grid.py <pddl2smv_absolut_path> (absolute path to pddl2smv binary)"
		sys.exit(1)

	path_pddl2smv = sys.argv[1]

	if not os.path.exists( path_pddl2smv ) :
		print >> sys.stderr, "Could not find pddl2smv path", domain_file
		sys.exit(1)
		
	call_pddl2smmv( "Blocksworld/domain-blocksaips.pddl", "Blocksworld/instances/", path_pddl2smv  )
	call_pddl2smmv( "Grid/grid-strips.pddl", "Grid/instances/", path_pddl2smv  )
	call_pddl2smmv( "Gripper/domain.pddl", "Gripper/instances/", path_pddl2smv  )
	call_pddl2smmv( "Satellite/stripsSat.pddl", "Satellite/instances/", path_pddl2smv ) 
	call_pddl2smmv( "Serial-Logistics/domain.pddl", "Serial-Logistics/instances/", path_pddl2smv )
	call_pddl2smmv( "Tpp/domain.pddl", "Tpp/instances/", path_pddl2smv ) 

	print "Files generated in each domain/instances/tars folder! \n Have Fun!"

if __name__ == '__main__' :
	main()

