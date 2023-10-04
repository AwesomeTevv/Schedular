import sys
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)


# Define the process data clas
class Process:
    def __init__(self, name, duration, arrival_time, io_frequency):
        self.name = name
        self.duration = duration
        self.arrival_time = arrival_time
        self.io_frequency = io_frequency

    def toString(self):
        return f"Name: {self.name}\nDuration: {self.duration}\nArrival Time: {self.arrival_time}\nI/O Frequency: {self.io_frequency}\n"


def main():
    # Check if the correct number of arguments is provided
    import sys

    if len(sys.argv) != 2:
        return 1

    # Extract the input file name from the command line arguments
    input_file_name = f"Process_List/{config['dataset']}/{sys.argv[1]}"

    # Define the number of processes
    num_processes = 0

    # Initialize an empty list for process data
    data_set = []

    # Open the file for reading
    try:
        with open(input_file_name, "r") as file:
            # Read the number of processes from the file
            num_processes = int(file.readline().strip())

            # Read process data from the file and populate the data_set list
            for _ in range(num_processes):
                line = file.readline().strip()
                name, duration, arrival_time, io_frequency = line.split(",")
                process = Process(
                    name, int(duration), int(arrival_time), int(io_frequency)
                )
                data_set.append(process)

    except FileNotFoundError:
        print("Error opening the file.")
        return 1

    """
    TODO Your Algorithm - assign your output to the output variable
    """

    """
    * Pre-Processing the Data Set into a Dictionary
    """
    processes = {}
    for process in data_set:
        name = process.name
        processes[name] = process

    fcfs = False
    stcf = True
    mlfq = False

    output = ""

    if fcfs:
        print("First Come, First Served")
        for process in data_set:
            # print(data.toString())
            name = process.name
            duration = int(process.duration)
            arrival_time = int(process.arrival_time)
            io_frequency = int(process.io_frequency)

            for i in range(1, duration):
                output += name + " "
                if io_frequency != 0:
                    if i % io_frequency == 0:
                        output += "!" + name + " "

            output += name + " "

    if stcf:
        print(
            f"""
--------------------------------------------------------------
Scheduling Scheme: Shortest Time to Completion First (stcf)
Input File:        {input_file_name}
--------------------------------------------------------------
              
              """
        )

        times = []
        for key in processes:
            process = processes[key]
            times.append(process.arrival_time)

        arrival_times = {t: [] for t in times}

        for key in processes:
            process = processes[key]
            arrival_times[process.arrival_time].append(process.name)

        queue = []

        for at in arrival_times:
            added = arrival_times[at]

            while len(added) != 0:
                best_time = 999999
                best_proc = ""

                for proc in added:
                    process = processes[proc]

                    completion_time = process.arrival_time + process.duration

                    if completion_time < best_time:
                        best_time = completion_time
                        best_proc = proc

                queue.append(best_proc)
                added.remove(best_proc)

            for q in queue:
                print()

    if mlfq:
        print("Multi-Level Frequency Queue")

    """
    End of your algorithm
    """

    # Open a file for writing
    try:
        output_path = f"Schedulers/template/{config['dataset']}/template_out_{sys.argv[1].split('_')[1]}"
        with open(output_path, "w") as output_file:
            # Write the final result to the output file
            output_file.write(output)

    except IOError:
        print("Error opening the output file.")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
