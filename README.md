# JsonParser

To Run the Application:

1. First have to activate the virtual environment using following command:
   `source env/bin/activate`

2. To run the Main Class - Runner class using following command:
	`python runner.py`

3. To run the Test Cases, following command can be used:
	`python test/testscript.py TestData`


Folder Structure:

1. runner.py -> Main file to execute all the read, process and write operation
2. read_and_process.py -> Having Class with all the read,process and write logic in it.
3. test/testscript.py -> Having all the unit test cases


Test Cases:

1. Test Case to check length of the given string with the standard description schema.
2. Test Case to check the complete execution of all the given input string (this can be customized from the unit test function).
3. Test Case to check the data type of the given string
4. Test Case to check the error code of the given string

Exception Handling and Logging:

Exception handling and logging is maintained throughout the code and if any excpetion is encoutered it is logged. Different types of logs were used.