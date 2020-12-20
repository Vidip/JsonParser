import read_and_process as read_file

#runner class to run the main read_file script execution for the production or direct mode
class Runner:
    def __init__(self):
        process = read_file.InputParser()
        process.read_file_lines([],'production')

runner_object = Runner()