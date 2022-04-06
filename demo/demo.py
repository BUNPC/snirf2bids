# A demo to use the fnirs-bids converter
import snirf2bids
import pysnirf2

def convert():
    """ To demonstrate 2 methods of using the fnirs-bids converter

    """

    #####################
    # Variable initialization

    # a snirf file (input) path
    snirf_file_path = '[path to folder]/Demo/sub-02_task-test_nirs.snirf'

    # a bids (output) destination directory
    bids_path = '[path to folder]/Demo'

    # a dictionary that holds the participant (subject) information
    subj1 = {"participant_id": 'sub-01',
             "age": 34,
             "sex": 'M'}

    #####################
    # The easiest way to convert the snirf file is to use the "snirf_to_bids" method,
    # which requires an input snirf file and output directory.
    # This function will write a bids subject folder.
    # The participant information is optional, and the default is None.
    # When the participant information is present, the function will also create a participant.tsv file

    snirf2bids.snirf_to_bids(snirf=snirf_file_path,
                             output=bids_path,
                             participants=subj1)

    #####################
    # The user can also create a subject object in the memory by using the "Subject" class.

    # The user can create the subject object by passing a snirf file into the instance.
    # The constructor will pull required subject, session, task, run and participant-related
    #   information from the snirf file
    subject1 = snirf2bids.Subject(fpath=snirf_file_path)

    # There are two ways to output this instance to local file!
    # First one is to output the instance to a series of string in form of a json-like format
    subject1.export(outputFormat='Text',
                    fpath=bids_path)

    # Second choice is to output locally as a subject folder, same as calling "snirf_to_bids"
    subject1.export(outputFormat='Folder',
                    fpath=bids_path)

convert()