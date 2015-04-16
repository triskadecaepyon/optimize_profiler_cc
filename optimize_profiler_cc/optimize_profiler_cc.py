"""
A package created for a Software Metrics class that gives optimization suggestions based upon
Cyclomatic Complexity values read in module files.

Gives flagged values based upon module mean CC, or allows for direct CC overrides
to give user additional flexibility once the data is loaded.  

"""

import numpy as np
import pandas as pd
import json
import copy


class OptimizeProfilerCC:
    """
    A class that does optimization analysis of Radon processed JSON files.  Looks for high complexity files
    within modules to flag down for further analysis by the user.
    
    Handles file parsing, loading, and management by encompassing strategy in class, and hiding class
    variables and methods. Outward facing functions to run analysis on imported dataset.
    
    """
    __FILE_NAME__ = None
    __FILE_DATA__ = None

    def __init__(self, input_file_name):
        self.__FILE_NAME__ = input_file_name
        self.__FILE_DATA__ = self.__pd_converter_radon_cc__(self.__FILE_NAME__)

    def load_new_file(self, input_file_name):
        """
        Allows loading of new JSON file, such that
        only one class needs to be instantiated for 
        analysis.
        """
        self.__FILE_NAME__ = input_file_name
        self.__FILE_DATA__ = self.__pd_converter_radon_cc__(self.__FILE_NAME__)

    @staticmethod
    def __pd_converter_radon_cc__(file_name_path):
        """
        Loads radon-formatted cc reports in JSON format.  
        Requires the file path of the json file as an argument.
        Uses the Open command and the native JSON parsing in Python.
        
        Returns a pandas dataframe with a complete listing of all files
        listed within the JSON output given.
        """
        with open(file_name_path) as data_file:
            djangocc_file = json.load(data_file)

        file_key_list=[]
        for file_keys in djangocc_file.keys():
            file_key_list.append(file_keys)

        array_of_dict_of_metrics = []
        for files in file_key_list:
            classes_json = djangocc_file.get(files)

            for classes in classes_json:
                dict_of_classes = {}
                dict_of_classes['filename'] = files
                dict_of_classes['name'] = classes.get('name')
                dict_of_classes['closures'] = classes.get('closures')
                dict_of_classes['col_offset'] = classes.get('col_offset')
                dict_of_classes['complexity'] = classes.get('complexity')
                dict_of_classes['endline'] = classes.get('endline')
                dict_of_classes['lineNumber'] = classes.get('lineno')
                dict_of_classes['rank'] = classes.get('rank')
                dict_of_classes['type'] = classes.get('type')

                array_of_dict_of_metrics.append(dict_of_classes)

        column_order = ['filename', 'name', 'closures', 'col_offset', 'complexity',
                        'endline', 'lineNumber', 'rank', 'type']
        data_frame = pd.DataFrame(array_of_dict_of_metrics, columns=column_order)
        return data_frame

    @staticmethod
    def __run_cc_opt_search__(pd_format_cc_report, force_min_cc=None):
        """
        Runs a search of the radon data provided for suitable functions and methods
        that have high cyclomatic complexity.  Reports back via text the function 
        and method details that were flagged by the search.  
        
        Adjustable forced value of CC to provide flexibility in analysis.
        
        Implementation currently ignores classes for analysis.
        Hidden method with run_cc_report() as the way of calling the method
        """
        new_data_sorted = pd_format_cc_report.sort(['filename', 'lineNumber'])
        unique_files = pd.unique(new_data_sorted.filename)

        print "Running search..."
        print "--------------------------"
        print "Module Files: " + str(len(unique_files))
        print "Module Classes: " + str(np.sum([new_data_sorted.type == 'class']))
        print "Module Methods: " + str(np.sum([new_data_sorted.type == 'method']))
        print "Module Functions: " + str(np.sum([new_data_sorted.type == 'function']))
        print "Module Complexity Mean: " + str(np.mean(new_data_sorted.complexity))
        print "Module Complexity Median: " + str(np.median(new_data_sorted.complexity))
        print "Module Complexity Standard Deviation: " + str(np.std(new_data_sorted.complexity))

        module_mean = np.mean(new_data_sorted.complexity)

        if force_min_cc is not None:
            print "Forced minimum CC value: " + str(force_min_cc)

        for file_n in unique_files:
            print "--------------------------"
            print "File name: " + str(file_n)
            print "--------------------------"

            per_file = new_data_sorted[new_data_sorted.filename == file_n]
            file_cc_mean = np.mean(per_file.complexity)
            # file_cc_median = np.mean(per_file.complexity)
            # file_cc_sd = np.mean(per_file.complexity)

            signature_count = len(per_file)
            lone_signature = True
            if signature_count > 1:
                lone_signature = False

            for sigs in range(0, signature_count):
                sig_data = per_file.iloc[sigs]
                if lone_signature is False:
                    if force_min_cc is not None:
                        if (sig_data.complexity > force_min_cc) and (sig_data.type != 'class'):
                            print "Flag Optimize - Sig name: " + str(sig_data[1]) + " | Type: " + str(sig_data.type) + \
                                  " | CC: " + str(sig_data.complexity) + " | LineNum: " + str(sig_data.lineNumber) + \
                                  " | Force: " + str(force_min_cc)
                    else:
                        if (sig_data.complexity > file_cc_mean) and (sig_data.type != 'class'):
                            print "Flag Optimize - Sig name: " + str(sig_data[1]) + " | Type: " + str(sig_data.type) + \
                                  " | CC: " + str(sig_data.complexity) + " | LineNum: " + str(sig_data.lineNumber)
                else:
                    if force_min_cc is not None:
                        if (sig_data.complexity > force_min_cc) and (sig_data.type != 'class'):
                            print "Flag Optimize - Sig name: " + str(sig_data[1]) + " | Type: " + str(sig_data.type) + \
                                  " | CC: " + str(sig_data.complexity) + " | LineNum: " + str(sig_data.lineNumber) + \
                                  " | Force: " + str(force_min_cc)
                    else:
                        if (sig_data.complexity > module_mean) and (sig_data.type != 'class'):
                            print "Flag Optimize - Sig name: " + str(sig_data[1]) + " | Type: " + str(sig_data.type) + \
                                  " | CC: " + str(sig_data.complexity) + " | LineNum: " + str(sig_data.lineNumber)

    def run_cc_report(self, force_min_cc=None):
        """
        Runs the CC report of the optimise-capable functions and methods.
        Openly callable in this format.
        """
        self.__run_cc_opt_search__(self.__FILE_DATA__, force_min_cc=force_min_cc)

    def get_raw_cc_data(self):
        """
        Gets the raw dataframe that was created by the class
        for advanced usage or export.  Creates a shallow 
        copy for proper operation within original class.
        """
        return copy.copy(self.__FILE_DATA__)

    def get_file_name(self):
        """
        A helper function that returns the name of the file being processed.
        """
        return self.__FILE_NAME__