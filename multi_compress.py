#!/usr/bin/env python3
import multiprocessing
import subprocess
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(process)s %(processName)s %(message)s',
    filename='imageoptimizer_finished.log',
    filemode='a'
)

i = multiprocessing.Value('i', 0)
total = 0


def __get_new_path(old_path):
    directory = os.path.dirname(old_path)
    file_name = os.path.basename(old_path)
    new_directory = directory.replace('/data/var/www/', '/data/var/img_processed/')
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    return os.path.join(new_directory, file_name)


def compress(args: list):
    global i, total
    i.value += 1
    if i.value % 10 is 0:
        percentage = round(100 * i.value / total, 2)
        print("{0} of {1} processed; Progress: {2}%".format(i.value, total, percentage))

    path = args[1]
    new_path = __get_new_path(path)
    command_called = False
    if not os.path.isfile(new_path):
        command = 'guetzli --quality 84 {0} {1}'.format(path, new_path)
        # print("Processing image:", path)
        subprocess.run(command, shell=True)
        command_called = True
    filetime = str(int(os.path.getmtime(new_path)))
    new_line = '|'.join([args[0], path, filetime])
    if command_called:
        logging.debug(new_line)
    return new_line


if __name__ == "__main__":
    # imgPath = '/data/var/www/mocka.co.nz/htdocs/media/product/f4/belle-kids-chair-90.jpg'
    # result = str(int(os.path.getmtime(imgPath)))
    # print(result)

    f = open('apptrian_imageoptimizer_index.data', 'r')  # read mode open the index file
    path_arguments = list()
    for line in f.readlines():  # Read all lines one time
        line = line.strip()  # trim each line's blank
        if not len(line) or line.startswith('#'):  # Check if the line is empty or being commented
            continue  # Skip the line if invalid

        line_data = line.split('|')
        path_arguments.append([line_data[0], line_data[1]])

    total = len(path_arguments)
    pool = multiprocessing.Pool(32)
    # with open('imageoptimizer_finished.data', 'a') as result_file:
    pool.map(compress, path_arguments)


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
