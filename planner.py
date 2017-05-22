
import urllib.request as urllib2
# import urllib2
import os, json, sys

# def make_plan(domain_path,problem_path):
    

def online(domain_path, problem_path):
    data = {'domain': open(domain_path, 'r').read(),
            'problem': open(problem_path, 'r').read()}

    req = urllib2.Request('http://solver.planning.domains/solve')
    req.add_header('Content-Type', 'application/json')
    resp = json.loads(urllib2.urlopen(req, json.dumps(data).encode('utf-8')).read().decode('utf-8'))
    return [act['name'] for act in resp['result']['plan']]

def local(domain_path, problem_path):
    out_path = 'tmp.ipc'
    os.system('cloud_solver/siw-then-bfsf --domain ' + domain_path + ' --problem ' + problem_path + ' --output ' + out_path)
    with open(out_path) as f:
        return f.read().split('\n')

use_local = False

if use_local:
    make_plan = local
else:
    make_plan = online


if __name__ == '__main__':
    plan = make_plan(sys.argv[1],sys.argv[2])
    with open(sys.argv[3], 'w') as f:
        f.write('\n'.join(plan))
    
 