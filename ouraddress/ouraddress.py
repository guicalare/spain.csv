from multiprocessing import Process
from numpy import array_split
from json import load
from os import listdir
from os.path import exists as file_exists
from os.path import join as join_path
from os import remove as remove_file
from thefuzz import fuzz
from thefuzz import process
from datetime import datetime

class Ouraddress:

    def __init__(self):

        with open("config.json", "r") as f:
            self.config_parameters = load(f)

        self.instances = self.config_parameters["instances"]

        print(datetime.now().strftime("%D %H:%M:%S"), f" Loaded configuration: {self.config_parameters}")
        
    def split_input_file(self):

        input_file = join_path(self.config_parameters["input folder"], listdir(self.config_parameters["input folder"])[0])

        with open(input_file, "r") as f:
            input_file_data = f.readlines()

        headers = input_file_data[0]
        
        for line in input_file_data[1:]:

            temp_path = join_path(self.config_parameters["temp folder"], line.split("#")[0])

            if not file_exists(temp_path):

                with open(temp_path, 'w') as f:
                    f.write(headers)                

            with open(temp_path, 'a') as f:
                f.write(line)

    def file_search_fuzzy(self, id):

        search_data_path =  join_path(self.config_parameters["search folder"], id)
        input_data_path = join_path(self.config_parameters["temp folder"], id)
        output_data_path = join_path(self.config_parameters["output folder"], id)

        with open(search_data_path, "r") as f:
            search_data = f.readlines()

        with open(input_data_path, "r") as f:
            input_data = f.readlines()
        
        remove_file(input_data_path)

        data_headers = input_data[0].strip()
        search_headers = search_data[0].strip()

        with open(output_data_path, "w") as f:
            f.write(f"{data_headers}#{search_headers}#score \n")        

        for data in input_data[1:]:

            data = data.strip()

            data_address = data.split("#")[1]
            best_address_data, score_adress = "", 0

            for search in search_data:

                search = search.strip()
                search_address = search.split("#")[0]

                score = fuzz.token_sort_ratio(data_address, search_address)

                if score > score_adress:
                    best_address_data, score_adress = search, score, 
                
                if score_adress >= self.config_parameters["early stop"]:
                    break

            if score_adress >= self.config_parameters["min match valid"]:

                with open(output_data_path, "a") as f:
                    data = data.strip()
                    f.write(f"{data}#{best_address_data}#{score_adress}\n")

    def file_search_fuzzy_multiprocessing(self, temp_files, index):

        print(datetime.now().strftime("%D %H:%M:%S"), f" Thread {index} entry [file_search_fuzzy_multiprocessing] {temp_files}")
        
        for file in temp_files:

            print(datetime.now().strftime("%D %H:%M:%S"), f" Thread {index} file {file} started")
            start = datetime.now()

            self.file_search_fuzzy(file)

            end = datetime.now()
            print(datetime.now().strftime("%D %H:%M:%S"), f" Thread {index} file {file} ended [", end-start, "]")

    def file_search_fuzzy_multiprocessing_init(self):

        self.split_input_file()

        temp_files = listdir(self.config_parameters["temp folder"])

        temp_files_splits = array_split(temp_files, self.instances)

        print(datetime.now().strftime("%D %H:%M:%S"), f" Files splited distribution: [{temp_files_splits}]")

        threads = []

        for index in range(len(temp_files_splits)):

            temp_files_thread = temp_files_splits[index]

            if len(temp_files_thread) != 0:

                print(datetime.now().strftime("%D %H:%M:%S"), f" Thread {index} call with parameters: {temp_files_thread}")

                x = Process(target=self.file_search_fuzzy_multiprocessing, args=(temp_files_thread, index, ))

                threads.append(x)

                x.start()

        start = datetime.now()

        for index, thread in enumerate(threads):
            thread.join()

        end = datetime.now()

        print(datetime.now().strftime("%D %H:%M:%S"), " Total time used in threads calculations: ", end-start)

        start = datetime.now()

        print(datetime.now().strftime("%D %H:%M:%S"), " Output join started")

        output_files = listdir(self.config_parameters["output folder"])

        for output_file in output_files:

            with open(join_path(self.config_parameters["output folder"], output_file), "r") as f:
                data = f.readlines()         

            if not file_exists(join_path(self.config_parameters["output folder"], "ouradress.csv")):

                with open(join_path(self.config_parameters["output folder"], "ouradress.csv"), "w") as f:

                    for line in data:

                        if line != "\n":

                            f.write(line)
            
            else:

                with open(join_path(self.config_parameters["output folder"], "ouradress.csv"), "a") as f:

                    for line in data[1:]:

                        if line != "\n":

                            f.write(line)
            
            if ".csv" not in output_file:
            
                remove_file(join_path(self.config_parameters["output folder"], output_file))

        end = datetime.now()

        print(datetime.now().strftime("%D %H:%M:%S"), " Output join ended [", end-start, "]")

        output_file_end = join_path(self.config_parameters["output folder"], "ouradress.csv")

        print(datetime.now().strftime("%D %H:%M:%S"), f" Output file: {output_file_end}")    

#Ouraddress().file_search_fuzzy_multiprocessing_init()