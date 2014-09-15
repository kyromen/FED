# -*- coding: utf-8 -*-
import multiprocessing as mp


def multi_start(grabber_cls, browser_name='phanomjs', quantity_browsers=None):
    grabber = grabber_cls(0, browser_name)
    pages = grabber.grab_count_of_pages('future')
    grabber.driver.quit()

    nCPU = mp.cpu_count()

    if quantity_browsers is None:
        quantity_browsers = nCPU * 2

    if pages < quantity_browsers:
        tasks = pages
    else:
        tasks = pages / 2

    while 1:
        if tasks / quantity_browsers < 1:
            quantity_browsers -= 1
        else:
            break

    jobers = quantity_browsers

    q = pages / tasks
    r = pages % tasks

    jobs = []
    start_page = 0
    for i in range(tasks):
        count_of_pages = q
        if r > 0:
            count_of_pages += 1
            r -= 1
        if count_of_pages == 0:
            break
        jobs.append([start_page, count_of_pages])
        start_page += count_of_pages

    queue = mp.JoinableQueue()

    for job in jobs:
        queue.put(job)
    for i in range(jobers):
        queue.put(None)

    workers = []
    for i in range(jobers):
        worker = mp.Process(target=grabber.start, args=[queue, grabber_cls, browser_name])
        workers.append(worker)
        worker.start()
    queue.join()