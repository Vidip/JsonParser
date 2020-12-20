import unittest
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import read_and_process as read_file


class TestData(unittest.TestCase):

    #setUp function
    def setUp(self):
        self.process = read_file.InputParser()

    #test function to check the function running
    def test_complete_function(self):
        data = ['L1&1&AB', 'L2&NB&2&34']
        result  = self.process.read_file_lines(data,'test_integrated')
        self.assertEqual(result, True)

    #test function to check the error codes
    def test_specific_error_code(self):
        data = ['L1&1&AB']
        expected_error_code = ['E01','E01','E05']
        res = self.process.read_file_lines(data,'test')
        length = len(res)
        for i in range(0,length):
            self.assertEqual(res['Error Code'][i],expected_error_code[i])

    #test function to check the data type
    def test_check_data_type(self):
        data = ['L2&NB&2&34']
        given_data_type = ['word_characters','digits','digits']
        res = self.process.read_file_lines(data,'test')
        length = len(res)
        for i in range(0,length):
            self.assertEqual(res['Given DataType'][i],given_data_type[i])

    #test function to check the length of the input string and the length of the standard description section schema
    def test_check_array_length(self):
        data = ['L2&NB&2&34']
        given_word_length = len(data[0].split('&')) -1 
        res = self.process.read_file_lines(data,'test')
        length = res.shape[0]
        difference = length - given_word_length
        self.assertEqual(difference,0)


if __name__ == '__main__':
    unittest.main()