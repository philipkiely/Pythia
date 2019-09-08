import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import ast
import boto3
client = boto3.client('s3')


class Watcher:
    DIRECTORY_TO_WATCH = "/Users/Philip/Code/PennAppsXX/output"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.event_type == 'created':
            if 'joined' in event.src_path:
                time.sleep(1) # Race condition
                statefile = open('state.txt', 'r')
                state = ast.literal_eval(statefile.read())
                statefile.close()
                ifile = open(event.src_path, 'rb')
                video = ifile.read()
                ifile.close()
                tstamp = event.src_path.split('_')[-1][:-4]
                key = RSA.import_key(open('private.pem').read())
                try:
                    previous = state['previous'].encode('latin-1')
                except:
                    previous = get_random_bytes(256) #IV
                h = SHA256.new(str(previous).encode('utf-8') + str(tstamp).encode('utf-8') + video)
                signature = pss.new(key).sign(h)
                print(tstamp, "\n", signature)
                state['previous'] = signature
                response = client.put_object(Body=video, Bucket='pennapps-superunique-name-123', Key='vid/' + tstamp + '.mp4', Metadata={"Signature": signature, "Timestamp": str(tstamp), "Previous": str(previous)})
                print(response)
                statefile = open('state.txt', 'w')
                statefile.write(str(state))
                statefile.close()


if __name__ == '__main__':
    w = Watcher()
    w.run()
