import pickle

class Pickle:
    def __init__(self, file_path) :
        self.file_path = file_path

    def read_pkl(self):
        try:
            with open(self.file_path, 'rb') as pickle_file:
                existing_documents = pickle.load(pickle_file)
        except FileNotFoundError as e:
            print(e)

        return existing_documents

    def write_pkl(self, docs):
        with open(self.file_path, 'wb') as pickle_file:
            pickle.dump(docs, pickle_file)