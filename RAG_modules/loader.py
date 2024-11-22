import os
from langchain_core.documents import Document

class DataLoader:
    def __init__(self, directory='Data'):
        self.directory = directory

    def load(self):
        """
        Load all .txt and .md files from the specified directory.
        
        Returns:
            list of Document with metadata:
            - filename 
        """
        data = {}
        
        # Check if the directory exists
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"The directory {self.directory} does not exist.")
        
        # Iterate through the files in the directory
        for filename in os.listdir(self.directory):
            if filename.endswith('.txt') or filename.endswith('.md'):
                file_path = os.path.join(self.directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    #take only the filename
                    filename = os.path.basename(file_path)
                    yield Document(
                        page_content=file.read(),
                        metadata={"filename": filename},
                    )

        
       


# Example usage
if __name__ == "__main__":
    loader = DataLoader()
    try:
        data = loader.load()
        for d in data:
            print(type(d))
       
    except Exception as e:
        print(f"Error loading files: {e}")