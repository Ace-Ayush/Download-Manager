import os
import requests
from threading import Thread

class DownloadThread(Thread):
    def __init__(self, url, save_dir):
        super().__init__()
        self.url = url
        self.save_dir = save_dir
    
    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            file_name = os.path.basename(self.url)
            save_path = os.path.join(self.save_dir, file_name)
            with open(save_path, "wb") as f:
                f.write(response.content)
                print(f"Downloaded {self.url}")
        else:
            print(f"Failed to download {self.url}")
        
class DownloadManager:
    def __init__(self, urls, num_threads=1, save_dir="."):
        self.urls = urls
        self.num_threads = num_threads
        self.save_dir = save_dir
    
    def start_download(self):
        threads = []
        for url in self.urls:
            thread = DownloadThread(url, self.save_dir)
            threads.append(thread)
        
        # Start threads
        for i in range(0, len(threads), self.num_threads):
            thread_slice = threads[i:i+self.num_threads]
            for thread in thread_slice:
                thread.start()
            
            for thread in thread_slice:
                thread.join()
            
        print("Download complete.")
