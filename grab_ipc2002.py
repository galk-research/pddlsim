
import cloud_solver.planning_domains_api as api
import os
import urllib

COLLECTION_ID = 3
OUT_DIR = 'ipc2002'
TEST_ALL_DOMAIN_FILES_ARE_THE_SAME = True

if __name__ == '__main__':
    # domains_in_collection = api.get_collection(COLLECTION_ID)['domain_set']

    if not os.path.exists(OUT_DIR):            
        os.mkdir(OUT_DIR)

    domains = {}
    problem_data = {}
    domain_data = api.get_domains(COLLECTION_ID)
    domain_names = [dom['domain_name'] for dom in domain_data]
    
    for dom in domain_data:

        dname = dom['domain_name']

        # Map the domain name to the list of domain-problem pairs and problem data
        domains[dname] = []
        problem_data[dname] = []

        # Make the directory for the domain
        if not TEST_ALL_DOMAIN_FILES_ARE_THE_SAME:
            os.mkdir(os.path.join(OUT_DIR, dname))

        # Turn the links into relative paths for this machine
        probs = map(api.localize, api.get_problems(dom['domain_id']))

        dpath = os.path.join(dname, "domain.pddl")
        current_domain_url = None
        # print probs
        # Copy the domain and problem files to their appropriate directory
        for i in range(len(probs)):
            
            ppath = os.path.join(dname, "prob%.2d.pddl" % (i+1))
            domain_url = probs[i]['domain_url']
            if TEST_ALL_DOMAIN_FILES_ARE_THE_SAME:
                if current_domain_url is None:
                    current_domain_url = domain_url
                elif current_domain_url != domain_url:
                    raise Exception('Domain url is not like the others')
            else:
                if not os.path.exists(dpath):            
                    urllib.urlretrieve (probs[i]['domain_url'], os.path.join(OUT_DIR,dpath))            
                urllib.urlretrieve (probs[i]['problem_url'], os.path.join(OUT_DIR,ppath))            
       