# A demo to use the fNIRS-BIDS converter
import snirf2bids
import os


def convert():
    """
    To demonstrate 3 methods of using the fNIRS-BIDS converter
    """

    #####################
    # Variable initialization

    # a SNIRF file (input) path
    cwd = os.getcwd()
    snirf_file_path = cwd + '\sub-02_task-test_nirs.snirf'

    # a BIDS (output) destination directory
    bids_path = cwd

    # a dictionary that holds the participant (subject) information
    subj1 = {"participant_id": 'sub-01',
             "age": 34,
             "sex": 'M'}

    #####################
    # The easiest way to convert the SNIRF file is to use the "snirf_to_bids" method,
    # which requires an input SNIRF file and output directory.
    # This function will write a BIDS subject folder.
    # The participant information is optional, and the default is None.
    # When the participant information is present, the function will also create a participant.tsv file

    snirf2bids.snirf_to_bids(inputpath=snirf_file_path,
                             outputpath=bids_path,
                             participants=subj1)

    #####################
    # The user can also create a SNIRF 'subject' object in the memory by using the "Subject" class.

    # The user can create the subject object by passing a snirf file into the instance.
    # The constructor will pull required subject, session, task, run and participant-related
    #   information from the snirf file
    subject1 = snirf2bids.Subject(fpath=snirf_file_path)

    # There are two ways to output this instance to local file!
    # First one is to output the instance to a series of string in form of a json-like format
    textStreamOutput = subject1.json_export()
    # with open('TextStreamOutput.txt', 'w') as f:
    #     f.write(textStreamOutput)

    # Second choice is to output locally as a subject folder, same as calling "snirf_to_bids"
    subject1.directory_export(fpath=bids_path)


convert()
