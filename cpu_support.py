import subprocess
import os

def create_cgroup(cgroup_name, cpu_limit):
    # Creazione del cgroup
    subprocess.run(['cgcreate', '-g', f'cpu:/{cgroup_name}'], check=True)
    
    # Calcolo del valore per cpu.cfs_quota_us
    cpu_count = os.cpu_count()

    cpu_period = 10000000  # Valore predefinito in microsecondi
    cpu_quota = int(cpu_limit * cpu_count * cpu_period) #per ogni cpu usa il cpu_limit%
    
    # Impostazione del limite di CPU
    subprocess.run(['cgset', '-r', f'cpu.cfs_period_us={cpu_period}', cgroup_name], check=True)
    subprocess.run(['cgset', '-r', f'cpu.cfs_quota_us={cpu_quota}', cgroup_name], check=True)

def add_pid_to_cgroup(cgroup_name, pid):
    # Aggiunta del PID al cgroup
    with open(f'/sys/fs/cgroup/cpu/{cgroup_name}/tasks', 'w') as f:
        f.write(str(pid))

def remove_cgroup(cgroup_name):
    # Rimozione del cgroup
    subprocess.run(['cgdelete', '-g', f'cpu:/{cgroup_name}'], check=True)

def support_cpu(pid, cgroup_name):
        # Limite di CPU (percentuale in decimale, ad esempio 0.9 per il 90%)
    cpu_limit_percentage = 0.9
    # Creazione del cgroup con il limite di CPU
    create_cgroup(cgroup_name, cpu_limit_percentage)
    print(f"Cgroup '{cgroup_name}' creato con limite CPU al {int(cpu_limit_percentage*100)}%")
    
    # Aggiunta del PID al cgroup
    add_pid_to_cgroup(cgroup_name, pid)
    print(f"PID {pid} aggiunto al cgroup '{cgroup_name}'")
        

