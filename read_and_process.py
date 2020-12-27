import json
import logging
import pandas as pd

#class for reading data and processing it
class InputParser:
    def __init__(self):
        self.dataframe = {"Section":[],"Sub-Section":[],"Given DataType":[],"Expected DataType":[],"Given Length":[],"Expected MaxLength":[],"Error Code":[]}
        self.data = '' 
        self.val = False
        self.error_codes = ''

    #function to read description json file
    def read_desc_codes(self):
        try:
            with open('./input_files/standard_definition.json') as f:
                self.data = json.load(f)
            return True
        except Exception as e:
            logging.exception(e)
            return False

    #function to read error codes from the json file
    def read_error_codes(self):
        try:
            with open('./input_files/error_codes.json') as f:
                self.error_codes = json.load(f)
            return True
        except Exception as e:
            logging.exception(e)
            return False

    #function to read lines from input file and process it further
    def read_file_lines(self,modes,environment):
        try:
            # this is to check the mode of execution, is it to run unit tests or normal script execution
            if len(modes) <= 0:
                file1 = open('./input_files/input_file.txt', 'r') 
                lines = file1.readlines() 
                file1.close()
            else:
                lines = modes
            #checking return status of each methdod call
            if self.read_desc_codes():
                if self.process_data(lines):
                    if environment == 'test':
                        return pd.DataFrame(self.dataframe)
                    if self.write_data_to_csv():
                        self.read_error_codes()
                        if self.write_to_txt_file():
                            return True
                        else:
                            logging.error("Write to text file failed")
                    else:
                        logging.error("Write to CSV failed")
                else:
                    logging.error("Processing Data Failed")
            else:
                logging.error("reading description codes failed")
            return False
        except Exception as e:
            logging.exception(e)
            return False

    #writing data to csv file
    def write_data_to_csv(self):
        try:
            #used pandas to store the dataframe which is further used to write data to csv or 
            #can be use for further transformation
            df = pd.DataFrame(self.dataframe)
            print(df)
            df = df[df['Sub-Section'] != '']
            df.to_csv('output_files/lines_char.csv',index=False)
            return True
        except Exception as e:
            logging.exception(e)
            return False

    #function to check length of the input and return the error code accordignly
    def len_check(self,len_of_char,max_length,error_code_one,error_code_two):
        if len_of_char <= max_length and len_of_char > 0:
            self.dataframe["Error Code"].append(error_code_one)
        else:
            self.dataframe["Error Code"].append(error_code_two)
        return 1
    
    #function to write data to text file
    def write_to_txt_file(self):
        df = pd.DataFrame(self.dataframe)
        message = ''
        number_of_records = df.shape[0]
        try:
            file1 = open("output_files/summary.txt","w")
            for i in range(0,number_of_records):
                for k in range(0,len(self.error_codes)):
                    #checking from the datafrane if that error code exists, then looking for the relevant message template
                    if df['Error Code'][i] == self.error_codes[k]['code'] and df['Sub-Section'][i] != '':
                        message = self.error_codes[k]['message_template']
                        message = message.replace("LXY",df['Sub-Section'][i]).replace("LX", df['Section'][i])
                        if df['Error Code'][i] == 'E02':
                            message = message.replace(f"{{data_type}}",df['Expected DataType'][i],1).replace(f"{{max_length}}",str(df['Expected MaxLength'][i]),2)
                        elif df['Error Code'][i] == 'E03':
                            message = message.replace(f"{{data_type}}",str(df['Expected MaxLength'][i]),1).replace(f"{{data_type}}",df['Expected DataType'][i],2)
                        file1.write(message+"\n")
            file1.close()
            return True
        except Exception as e:
            logging.info(e)  
            return False

    def pass_error_codes(self,j,required_length):
        if len(j) <= required_length:
            self.dataframe["Error Code"].append("E01")
        else:
            self.dataframe["Error Code"].append("E03")
        return True

    def insert_dataframe_values(self,sub_section,data_type,given_length,max_length,section):
        self.dataframe["Sub-Section"].append(sub_section)
        self.dataframe["Expected DataType"].append(data_type)
        self.dataframe["Expected MaxLength"].append(max_length)
        self.dataframe["Given Length"].append(given_length)
        self.dataframe["Section"].append(section)
        return True

    #main logic function for checking different scenarios 
    def process_data(self,lines):
        difference = ''
        for i in lines:
            checker = False
            #splitting word with respect to &
            word = i.strip().split('&')
            key = ''
            data_length = len(self.data)
            original_len = len(word)
            self.val = False
            #loop to all the chacaters of the word
            for index,j in enumerate(word):
                len_of_char = len(j)
                if index == 0:
                    key = j
                else:
                    try:
                        for k in range(0,data_length):
                            #if condition to get the first key
                            if key in self.data[k]['key']:
                                obj = self.data[k]['sub_sections']
                                break

                        if index <= len(obj):
                            required_data_type = obj[index-1]['data_type']
                            required_length = obj[index-1]['max_length']
                            temp_j = j.replace(" ","")
                            if temp_j.isalpha():
                                self.dataframe["Given DataType"].append("word_characters")
                            elif j.isdigit():
                                self.dataframe["Given DataType"].append("digits")
                            else:
                                self.dataframe["Given DataType"].append("others")

                            if temp_j.isalpha() and required_data_type == 'word_characters':
                                self.pass_error_codes(j,required_length)
                            elif j.isdigit() and required_data_type == 'digits':
                                self.pass_error_codes(j,required_length)
                            elif len(j) == required_length:
                                given_data_type = 'others'
                                self.dataframe["Error Code"].append("E02")
                            elif j is not None:
                                self.dataframe["Error Code"].append("E04")

                            #function to insert dataframe values
                            self.insert_dataframe_values(obj[index-1]['key'],required_data_type,len_of_char,required_length,key)

                            #if character is not present in the standar description
                            if len(word)-1 < len(obj) and index == len(word)-1:
                                difference = len(obj) - (len(word) -1)
                                while(difference != 0):
                                    required_data_type = obj[index]['data_type']
                                    required_length = obj[index]['max_length']
                                    self.insert_dataframe_values(obj[index-1]['key'],required_data_type,"",required_length,key)
                                    self.dataframe["Given DataType"].append("")
                                    self.dataframe["Error Code"].append("E05")
                                    difference -= 1
                    except Exception as e:
                        logging.exception(e)
                        return False
            logging.info(checker)
        return True