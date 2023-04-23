import subprocess
from multiprocessing import Process
from multiprocessing import Pool

def run_command(command):
    """Function to run a command in a subprocess."""
    subprocess.run(command, shell=True)
    
def createCommands (info):
    commands = []
    folder = 'cd videos &&'
    for key, value in info.items():
        commands.append('{} ffmpeg -i {} -c copy "{}.mp4"'.format(folder, value, key))
    return commands

def callProcess(info):
    commands = createCommands(info)
    subprocess.run("mkdir videos", shell=True)
    subprocess.run("cd videos", shell=True)
    # Create a pool of 3 worker processes
    processNumber = 3
    pool = Pool(processes=processNumber)
    # Divide the commands into groups of processNumber and run them in parallel
    for i in range(0, len(commands), processNumber):
        group = commands[i:i+processNumber]
        pool.map(run_command, group)
        print(f"Group {i//processNumber + 1} completed")

    # Close the pool and wait for all processes to complete
    pool.close()
    pool.join()

