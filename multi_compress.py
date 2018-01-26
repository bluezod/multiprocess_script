#!/usr/bin/env python3
import multiprocessing
import fcntl
import subprocess, os


def compress(path: str):
    directory = os.path.dirname(path)
    file_name = os.path.basename(path)
    new_directory = directory.replace('/data/var/www/', '/data/var/img_processed/')
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    new_path = os.path.join(new_directory, file_name)
    command = 'guetzli --quality 84 {0} {1}'.format(path, new_path)
    subprocess.run(command, shell=True)
    return new_path


imgPath = '/data/var/www/mocka.co.nz/htdocs/media/product/f4/belle-kids-chair-90.jpg'
print("Got result:", compress(imgPath))


def crawl(result_queue):
    import urllib.request
    data = urllib.request.urlopen(r"http://news.ycombinator.com/").read()

    print("Requested...")

    if "result found (for example)":
        result_queue.put(data)

    print("Read site.")


# processs = []
# result_queue = multiprocessing.Queue()
#
# # Step.1 Get the first line of the data file and update the list
# indexPath = 'apptrian_imageoptimizer_index.data';
# f = open(indexPath, 'r+');
# # fcntl.flock(f.fileno(), fcntl.LOCK_EX)
# imgInfo = f.readline()
#
# for n in range(4):  # start 4 processes crawling for the result
#     process = multiprocessing.Process(target=crawl, args=[result_queue])
#     process.start()
#     processs.append(process)
#
# print("Waiting for result...")
#
# result = result_queue.get()  # waits until any of the proccess have `.put()` a result
#
# for process in processs:  # then kill them all off
#     process.terminate()
#
# print("Got result:", result)
