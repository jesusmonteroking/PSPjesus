import time
import urllib
import threading
class FetchUrls(threading.Thread):
    def __init__(self, urls, output, lock):
        threading.Thread.__init__(self)
        self.urls = urls
        self.output = output
        self.lock = lock
    
    def run(self):
        while self.urls:
            url = self.urls.pop()
            req = urllib.Request(url)
            try:
                d = urllib.urlopen(req)
            except urllib.URLError as e:
                print("URL %s failed: %s" % (url, e.reason))
            
            # El bloqueo se adquiere por el hilo que llama a la función 
            self.lock.acquire()
            print("lock acquired by %s" % self.name)
            
            # Leemos el contenido de la URL y lo escribimos en el archivo
            self.output.write(d.read())
            print("write done by %s" % self.name)
            print("lock released by %s" % self.name)
            
            # Se libera el bloqueo para que otro hilo ejecute su función
            self.lock.release()
            print("URL %s fetched by %s" % (url, self.name))

def main():
    urls1 = ['http://www.google.com', 'http://www.facebook.com']
    urls2 = ['http://www.yahoo.com', 'http://www.youtube.com']

    lock = threading.Lock()
    f = open('output.txt', 'w+')
    t1 = FetchUrls(urls1, f, lock)
    t2 = FetchUrls(urls2, f, lock)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    f.close()

if __name__ == '__main__':
    main()




