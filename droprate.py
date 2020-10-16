import numpy as np
rates = [0.23,0.33,0.46,0.67,1.00,1.20 ,2.50 ,3.4 ,3.75 ,5.7 ,6.70 ,6.90 ,7.5 ,9.3 ,10 ,11.40 ,12.50 ,13.20 ,13.5 ,14 ,15 ,16.50 ,20 ,22 ,25.00 ,29 ,30 ,33 ,33.30 ,35 ,50 ,100]
# ns = [1,5,10,15,20,30,50,100,150,200,250,300,400,500,750,1000]
ns = list(range(1,1000+1))

# bad for memory btw
def simulate(p,n,reps=40000):
    return np.sum(np.random.random((reps,n)) <= p,axis=1)

def ci95(x):
    return np.quantile(x,[0.025,0.975],interpolation='lower')

def ciJob(ratentuple):
    (rate,n) = ratentuple
    return (rate,n,*ci95(simulate(rate/100.0,n)))

import multiprocessing
from tqdm import tqdm

def prog_map(elms, f, desc="Sim", chunksize=1,procs=8,order=True,total=None):
    with tqdm(elms, desc=desc, total=total) as t:
        with multiprocessing.Pool(procs, initializer=tqdm.set_lock,
              initargs=(tqdm.get_lock(),)) as p:
            if (order):
                pool = list(p.imap(f, t, chunksize=chunksize))
            else:
                pool = list(p.imap_unordered(f, t, chunksize=chunksize))
            return pool

jobs = [(rate,n) for rate in rates for n in ns]
result = prog_map(jobs, ciJob, chunksize=128)
# result = [ciJob(job) for job in jobs]

import pickle
with open('droprate.pickle', 'wb') as f:
    pickle.dump(result,f)

from pprint import pprint
pprint(result)


