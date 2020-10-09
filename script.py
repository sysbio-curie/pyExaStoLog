import exastolog, sys
from memory_profiler import profile

@profile
def my_func(model):
    if model == "emt":
        model_exastolog = exastolog.Model("notebooks/model_files/EMT_cohen_ModNet.bnet", profiling=True)
        nonrand_species = ['ECMicroenv','DNAdamage','Metastasis','Migration','Invasion','EMT','Apoptosis','Notch_pthw','p53']
        sim = exastolog.Simulation(model_exastolog,nonrand_species, [1, 1, 0, 0, 0, 0, 0, 1, 0], profiling=True)
        
        
    elif model == "ras":
        model_exastolog = exastolog.Model("notebooks/model_files/krasmodel15vars.bnet", profiling=True)
        nonrand_species = ['cc','KRAS','DSB','cell_death'], [1, 1, 1, 0]
        sim = exastolog.Simulation(model_exastolog,nonrand_species, [0]*len(nonrand_species), profiling=True)
    
    elif model == "toy":    
        model_exastolog = exastolog.Model("notebooks/model_files/toy.bnet", profiling=True)
        sim = exastolog.Simulation(model_exastolog,["A", "C", "D"], [0, 0, 0], profiling=True)
    
    elif model == "toy2":
        model_exastolog = exastolog.Model("notebooks/model_files/toy2.bnet", profiling=True)
        sim = exastolog.Simulation(model_exastolog, ["A", "B", "C"], [0,0,0])
        
    elif model == "toy3":
        model_exastolog = exastolog.Model("notebooks/model_files/toy3.bnet", profiling=True)
        sim = exastolog.Simulation(model_exastolog, ["A", "B"], [0,0])        
    else:
        return
        
    print(sim.get_last_states_probtraj())

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 2:
        print("Usage: profile <emt|ras|toy|toy2|toy3>\m- emt : Big example, needs at least 30G of memory")
        print("")
        exit(1)
        
    my_func(sys.argv[1])