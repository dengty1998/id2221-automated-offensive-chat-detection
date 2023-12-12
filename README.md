# ID2221 Final Project: Automated offensive chat detection in multi-player games: 

This is a final project for the course [Data-Intensive Computing](https://www.kth.se/student/kurser/kurs/ID2221?l=en) in KTH.

## Introduction

Offensive chat contents can severely affect the gaming experience of players. To combat this, most game companies employ a reporting system that users can use to report other players for inappropriate speech. However, this only happens after the game ends. During game play, other players would still be affected. As a result, we decide to develop a system support not only the reporting system but also real-time detection of offensive contents. 

We believe this is a good project topic, since user's speech data need to be stored for a long period and the scale of data keeps growing. It's suitable to use HDFS to store and query these chat messages. 

## Components

Front-end: HTML,  JavaScript
Back-end: Flask, Flask-socketio
Distributed database: Cassandra
Message Broker: Kafka
Permanent storage: HDFS
Cache storage: Redis

## How to Run

1. Install HDFS, Cassandra, Kafka and Redis properly

2. Create the HDFS direcotry "/chatlogs"

3. Create the kafka topic "chatlogs"

4. Install the python libraries using "pip install -r requirements.txt"

5. Run \_init\_.py

6. Run start_kafka.py in terminal

7. Run app.py in terminal

8. Visit webpage in different browsers, here are five default account:

   | Username | Password |
   | -------- | -------- |
   | Jack     | 123456   |
   | Tom      | 123456   |
   | Aaron    | 123456   |
   | Lucas    | 123456   |
   | Anna     | 123456   |

## Group Members

Minhao Li

Tianyu Deng