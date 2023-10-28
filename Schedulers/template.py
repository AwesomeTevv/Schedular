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

    print("Multi-Level Frequency Queue")

    output = ""

    total_duration = 0  # Stores the total duration of all process durations combined
    for process in data_set:
        total_duration += (
            process.duration
        )  # Adding each process duration to the total duration
    # At this point, total_duration stores the total scheduler runtime

    outs = {process: [] for process in data_set}

    of = {process: 0 for process in data_set}

    for process in data_set:
        for _ in range(process.duration):
            outs[process].append(f"{process.name}")
            of[process] += 1

            if of[process] < process.duration:
                if process.io_frequency != 0:
                    if of[process] % process.io_frequency == 0:
                        outs[process].append(f"!{process.name}")

    frequency = {process: 0 for process in data_set}

    arrivals = {time: [] for time in range(total_duration * 2)}

    for process in data_set:
        arrivals[process.arrival_time].append(process)

    frontier = []

    t = 0
    while True:
        mlfq = False

        frontier.extend(arrivals[t])

        chosen = data_set[0]

        for process in frontier:
            if frequency[process] == 0:
                chosen = process
                mlfq = True
                break

        if mlfq == False:
            best_duration = 9999
            for process in frontier:
                if len(outs[process]) < best_duration:
                    best_duration = len(outs[process])
                    chosen = process

        output += f"{outs[chosen].pop(0)} "
        frequency[chosen] += 1

        if len(outs[chosen]) == 0:
            frontier.remove(chosen)

        if len(frontier) == 0:
            break

        t += 1

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
