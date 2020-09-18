from datetime import datetime
import os, glob

# use the elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers

# declare a client instance of the Python Elasticsearch library


# posix uses "/", and Windows uses ""
if os.name == 'posix':
    slash = "/"  # for Linux and macOS
else:
    slash = chr(92)  # '\' for Windows


def current_path():
    return os.path.dirname(os.path.realpath(__file__))


# default path is the script's current dir
def get_files_in_dir(self=current_path()):
    # declare empty list for files
    file_list = []

    # put a slash in dir name if needed
    if self[-1] != slash:
        self = self + slash

    # iterate the files in dir using glob
    for filename in glob.glob(self + '*.*'):
        # add each file to the list
        file_list += [filename]

    # return the list of filenames
    return file_list


def get_data_from_pdf_file(file):
    from pdfminer.high_level import extract_text
    return extract_text(file)


def get_data_from_text_file(file):
    # declare an empty list for the data
    data = []

    # get the data line-by-line using os.open()
    for line in open(file, encoding="utf8", errors='ignore'):
        # append each line of data to the list
        data += [str(line)]

    # return the list of data
    return "".join(data)


# pass a directory (relative path) to function call
all_files = get_files_in_dir("/app/files")

# total number of files to index
print("TOTAL FILES:", len(all_files))

"""
PART 2 STARTS HERE
"""


# define a function that yields an Elasticsearch document from file data
def yield_docs(all_files):
    # iterate over the list of files
    for _id, _file in enumerate(all_files):
        # use 'rfind()' to get last occurence of slash
        file_name = _file[_file.rfind(slash) + 1:]
        # get the file's statistics
        stats = os.stat(_file)
        # timestamps for the file
        create_time = datetime.fromtimestamp(stats.st_ctime)
        modify_time = datetime.fromtimestamp(stats.st_mtime)

        # get the data inside the file
        file_extention = _file.split('.')[-1]
        print(_file)
        if file_extention == "txt":
            data = get_data_from_text_file(_file)
        elif file_extention == "pdf":
            data = get_data_from_pdf_file(_file)
        else:
            data = "".join(get_data_from_text_file(_file))
        # create the _source data for the Elasticsearch doc
        doc_source = {
            "file_name": file_name,
            "create_time": create_time,
            "modify_time": modify_time,
            "data": data
        }
        # use a yield generator so that the doc data isn't loaded into memory
        yield doc_source

def add_files_to_elasticsearch():
    client = Elasticsearch("http://192.168.0.218:9200", http_auth=("elastic", "changeme"), )
    for doc in yield_docs(all_files):
        res = client.search(index="test-index", body={"query": {"match": {"file_name": doc['file_name']}}})
        print(res['hits']['total']['value'])
        if res['hits']['total']['value'] == 0:
            res = client.index(index="test-index", body=doc)
            print(res['result'])
            client.indices.refresh(index="test-index")
# res = client.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(data)s" % hit["_source"])