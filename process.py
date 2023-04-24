import subprocess
from multiprocessing import Process
from multiprocessing import Pool



def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    exit_code = process.returncode
    if exit_code == 0:
        return (f'Conversion succeeded for {command}')
    else:
        return (f'Conversion failed with exit code {exit_code} for {command}')
    
def createCommands (info):
    commands = []
    folder = 'cd videos &&'
    i = 0
    for key, value in info.items():
        if (i==1) :
            commands.append('{} ffmpeg -i {}d -c copy "{}.mp4"'.format(folder, value, key))
        else:
            commands.append('{} ffmpeg -i {} -c copy "{}.mp4"'.format(folder, value, key))
        i = i + 1
    return commands

def callProcess(info):
    commands = createCommands(info)
    subprocess.run("mkdir videos", shell=True)
    subprocess.run("cd videos", shell=True)
    # Create a pool of 3 worker processes
    processNumber = 3
    pool = Pool(processes=processNumber)
    results = []
    # Divide the commands into groups of processNumber and run them in parallel
    for i in range(0, len(commands), processNumber):
        group = commands[i:i+processNumber]
        results.append(pool.map(run_command, group))
        #check if the results have failed 
        count = 0
        for sublist in results:
            for element in sublist:
                if 'failed' in element:
                    count += 1
        print(f"Group {i//processNumber + 1} completed with {count} failed conversions")

    # Close the pool and wait for all processes to complete
    print(results)
    pool.close()
    pool.join()

