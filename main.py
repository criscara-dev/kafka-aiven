from consumer import consumer_run
from producer import producer_run
import time


def main():

    consumer_run()


if __name__ == "__main__":
    main()
    # wait 10 secs before running the producer script
    producer_run()
    time.sleep(10)
