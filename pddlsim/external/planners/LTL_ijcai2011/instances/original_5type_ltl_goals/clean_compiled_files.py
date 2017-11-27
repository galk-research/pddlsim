#!/usr/bin/python
import sys, os, glob
							
def clean_files( problems_path ) :
	current_dir = os.getcwd()
	os.chdir(problems_path)
	if os.path.exists("tars"):
            print("Removing: tars folder")
            cmd = "rm -rf tars"
            os.system(cmd)

	for infile in glob.glob( os.path.join( '*.pddl') ):
		basename, extension = os.path.splitext(infile)
		if os.path.exists(basename):
                    print("Removing: " + basename + " folder")
                    cmd = "rm -fr "+basename
                    os.system(cmd)
			

	os.chdir(current_dir)

def main() :
	   		
	clean_files( "Blocksworld/instances/"  )
	clean_files( "Gripper/instances/"  )
	clean_files( "Serial-Logistics/instances/" )

if __name__ == '__main__' :
	main()

