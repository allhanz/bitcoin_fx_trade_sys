import time
import multiprocessing


def worker(data):
    [calc(x) for x in data]


def calc(x):
    a = x * 2
    print(a)
    #time.sleep(2)

if __name__ == '__main__':
    split_data = [[1, 2, 3], [4, 5]]

    jobs = []
    for data in split_data:
        job = multiprocessing.Process(target=worker, args=(data, ))
        jobs.append(job)
        job.start()

    [job.join() for job in jobs]

    print('Finish')
