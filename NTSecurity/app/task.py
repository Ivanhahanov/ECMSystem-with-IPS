def background_task(n):
    from time import sleep
    """ Function that returns len(n) and simulates a delay """

    delay = 2

    print("Task running")
    print(f"Simulating a {delay} second delay")

    sleep(delay)
    print(len(n))
    print("Task complete")

    return len(n)