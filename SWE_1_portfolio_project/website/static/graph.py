# the structure of the RabbitMQ functions calls are adapted from RabbitMQ's RPC tutorial: https://www.rabbitmq.com/tutorials/tutorial-six-python.html
import pika, sys, os
import matplotlib.pyplot as plt
import datetime


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
#  Takes a list of data from a RabbitMQ message and converts it into two separate lists #
#                                                                                       #
#  'data' should be a list in string format: '[9, 201, 3, 202]' where even number       #
#  indices are volume integers and odd number indices are Julian days                   #
#                                                                                       #
#  Returns a list of volume integers and a list of Julian days                          #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
def data_to_lists(data, volumes, dates):
    for i in range(1, len(data), 2):
        # if the current Julian day is already in dates, add its volume to the previous entry in dates
        if data[i] in dates:
            volumes[dates.index(data[i])] += int(data[i - 1])
        else:
            volumes.append(int(data[i - 1]))
            dates.append(data[i])

    return volumes, dates


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
#  Converts Julian days to standard date                          #
#                                                                 #
#  Returns the 'dates' list with dates in the format '01/01/2022' #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
def julian_to_std(dates):
    for i in range(len(dates)):
        # conversion from Julian to standard modeled after this StackOverFlow answer: https://stackoverflow.com/a/67262098
        new_date = datetime.datetime.strptime(dates[i], '%j')
        dates[i] = new_date.strftime('%m/%d/2022')

    return dates


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
#  Generates a graph based on the dates and volumes lists   #
#                                                           #
#  Returns the filename of the graph                        #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
def graph_vol(dates, volumes):
    print(dates, volumes)
    plt.bar(list(range(len(dates))), volumes, color='blue')
    plt.xticks(ticks=list(range(len(dates))), labels=dates)
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.title('Compost Volume')
    filename = 'volume_graph.png'
    plt.savefig(''+filename)  # graph is saved to the current working directory

    return filename


def main():
    # create the RabbitMQ connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # declare the queue for receiving data from the sender
    channel.queue_declare(queue='data')

    # function that runs when a message is received/consumed
    filename = ''

    def callback(ch, method, properties, body):
        # convert body from a string into a list, modeled after:
        # https://www.geeksforgeeks.org/python-convert-a-string-representation-of-list-into-list/
        print(" [x] Received %r" % body)
        data = body.decode().strip('][').split(', ')

        volumes, dates = data_to_lists(data, [], [])

        julian_to_std(dates)

        filename = graph_vol(dates, volumes)

        # send/publish the graph's filename to the sender. routing key = sender's consumer queue
        channel.basic_publish(exchange='', routing_key=properties.reply_to, body=filename)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Sending '%s'..." % filename)

    # start consuming messages, listening on the 'data' queue
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='data', on_message_callback=callback)
    print(' [x] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
