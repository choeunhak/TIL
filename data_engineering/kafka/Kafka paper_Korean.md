Kafka: a Distributed Messaging System for Log Processing

Kafka는 로그 데이터를 수집하고 전달하는 데 사용되며, 대량의 데이터를 저지연 시간으로 처리할 수 있다
There is a large amount of “log” data generated at any sizable  internet company. This data typically includes (1) user activity  events corresponding to logins, pageviews, clicks, “likes”,  sharing, comments, and search queries; (2) operational metrics  such as service call stack, call latency, errors, and system metrics  such as CPU, memory, network, or disk utilization on each  machine. Log data has long been a component of analytics used to  track user engagement, system utilization, and other metrics.  However recent trends in internet applications have made activity  data a part of the production data pipeline used directly in site  features. These uses include (1) search relevance, (2)  recommendations which may be driven by item popularity or cooccurrence in the activity stream, (3) ad targeting and reporting,  and (4) security applications that protect against abusive behaviors  such as spam or unauthorized data scraping, and (5) newsfeed  features that aggregate user status updates or actions for their  “friends” or “connections” to read.  This production, real-time usage of log data creates new  challenges for data systems because its volume is orders of  magnitude larger than the “real” data. For example, search,  recommendations, and advertising often require computing    Permission to make digital or hard copies of all or part of this work for  personal or classroom use is granted without fee provided that copies are  not made or distributed for profit or commercial advantage and that  copies bear this notice and the full citation on the first page. To copy  otherwise, or republish, to post on servers or to redistribute to lists,  requires prior specific permission and/or a fee.  granular click-through rates, which generate log records not only  for every user click, but also for dozens of items on each page that  are not clicked. Every day, China Mobile collects 5–8TB of phone  call records [11] and Facebook gathers almost 6TB of various user  activity events [12]  Many early systems for processing this kind of data relied on  physically scraping log files off production servers for analysis. In  recent years, several specialized distributed log aggregators have  been built, including Facebook’s Scribe [6], Yahoo’s Data  Highway [4], and Cloudera’s Flume [3]. Those systems are  primarily designed for collecting and loading the log data into a  data warehouse or Hadoop [8] for offline consumption. At  LinkedIn (a social network site), we found that in addition to  traditional offline analytics, we needed to support most of the  real-time applications mentioned above with delays of no more  than a few seconds.  We have built a novel messaging system for log processing called  Kafka [18] that combines the benefits of traditional log  aggregators and messaging systems. On the one hand, Kafka is  distributed and scalable, and offers high throughput. On the other  hand, Kafka provides an API similar to a messaging system and  allows applications to consume log events in real time. Kafka has  been open sourced and used successfully in production at  LinkedIn for more than 6 months. It greatly simplifies our  infrastructure, since we can exploit a single piece of software for  both online and offline consumption of the log data of all types.  The rest of the paper is organized as follows. We revisit  traditional messaging systems and log aggregators in Section 2. In  Section 3, we describe the architecture of Kafka and its key design  principles. We describe our deployment of Kafka at LinkedIn in  Section 4 and the performance results of Kafka in Section 5. We  discuss future work and conclude in Section 6.   ### Kafka Architecture and Design Principles  Because of limitations in existing systems, we developed a new  messaging-based log aggregator Kafka. We first introduce the  basic concepts in Kafka. A stream of messages of a particular type  is defined by a topic. A producer can publish messages to a topic.  The published messages are then stored at a set of servers called  brokers. A consumer can subscribe to one or more topics from the  brokers, and consume the subscribed messages by pulling data  from the brokers.  Messaging is conceptually simple, and we have tried to make the  Kafka API equally simple to reflect this. Instead of showing the  exact API, we present some sample code to show how the API is  used. The sample code of the producer is given below. A message  is defined to contain just a payload of bytes. A user can choose  her favorite serialization method to encode a message. For  efficiency, the producer can send a set of messages in a single  publish request.

===========================

To subscribe to a topic, a consumer first creates one or more  message streams for the topic. The messages published to that  topic will be evenly distributed into these sub-streams. The details  about how Kafka distributes the messages are described later in  Section 3.2. Each message stream provides an iterator interface  over the continual stream of messages being produced. The  consumer then iterates over every message in the stream and  processes the payload of the message. Unlike traditional iterators,  the message stream iterator never terminates. If there are currently  no more messages to consume, the iterator blocks until new  messages are published to the topic. We support both the point-topoint delivery model in which multiple consumers jointly  consume a single copy of all messages in a topic, as well as the  publish/subscribe model in which multiple consumers each  retrieve its own copy of a topic.

=============================

The overall architecture of Kafka is shown in Figure 1. Since Kafka is distributed in nature, an Kafka cluster typically consists  of multiple brokers. To balance load, a topic is divided into multiple partitions and each broker stores one or more of those  partitions. Multiple producers and consumers can publish and  retrieve messages at the same time. In Section 3.1, we describe the  layout of a single partition on a broker and a few design choices  that we selected to make accessing a partition efficient. In Section  3.2, we describe how the producer and the consumer interact with  multiple brokers in a distributed setting. We discuss the delivery  guarantees of Kafka in Section 3.3.

==================================

### 3.1 Efficiency on a Single Partition
Simple storage:
카프카(Kafka)는 매우 간단한 저장소 구조를 갖습니다. 하나의 토픽(topic) 파티션(partition)은 하나의 논리적 로그(log)에 해당합니다. 물리적으로, 로그는 대략적으로 동일한 크기(예: 1GB)의 세그먼트 파일로 구현됩니다. 생산자(producer)가 파티션에 메시지를 발행할 때마다 브로커(broker)는 간단히 마지막 세그먼트 파일에 메시지를 추가합니다. 더 나은 성능을 위해, 우리는 일정한 수의 메시지가 발행되거나 일정한 시간이 경과한 후에만 세그먼트 파일을 디스크에 플러시합니다. 메시지는 플러시된 후에만 소비자(consumer)에게 노출됩니다.

일반적인 메시징 시스템과 달리, 카프카에 저장된 메시지에는 명시적인 메시지 ID가 없습니다. 대신, 각 메시지는 로그에서의 논리적 오프셋(offset)으로 주소 지정됩니다. 이렇게 함으로써, 메시지 ID를 실제 메시지 위치로 매핑하는 보조적이고 탐색 집중적인 랜덤 액세스 인덱스 구조를 유지하는 오버헤드를 피할 수 있습니다. 메시지 ID는 증가하지만 연속적이지는 않습니다. 다음 메시지의 ID를 계산하려면, 현재 메시지의 길이를 해당 ID에 추가해야 합니다. 이후부터는 메시지 ID와 오프셋을 서로 교환하여 사용합니다.

"To compute the id of the next message, we have to
add the length of the current message to its id. From now on, we will use message ids and offsets interchangeably"

소비자는 항상 특정 파티션에서 메시지를 순차적으로 소비합니다. 소비자가 특정 메시지 오프셋을 확인하면, 해당 오프셋 이전의 모든 메시지를 수신한 것으로 간주됩니다. 내부적으로, 소비자는 브로커에게 비동기식 풀 요청(asynchronous pull requests)을 보내어 애플리케이션이 소비할 수 있는 데이터 버퍼를 준비하도록 요청합니다. 각 풀 요청은 소비가 시작되는 메시지의 오프셋과 가져올 바이트 수를 포함합니다.

각 브로커는 메모리에 정렬된 오프셋 목록(offset list)을 유지하며, 각 세그먼트 파일의 첫 번째 메시지의 오프셋을 포함합니다. 브로커는 요청된 메시지가 포함된 세그먼트 파일을 오프셋 목록을 검색하여 찾은 후, 데이터를 소비자에게 보냅니다. 소비자가 메시지를 수신한 후에는, 다음 소비할 메시지의 오프셋을 계산하여 다음 풀 요청에서 사용합니다. 카프카 로그와 메모리 내 인덱스의 구조는 그림 2에서 나타내고 있습니다. 각 상자는 메시지의 오프셋을 보여줍니다.


##### 오프셋 vs id 활용 인덱스
하지만 이 방식은 메시지 ID와 메시지의 위치를 매핑하는 인덱스 구조를 필요로 하며, 이는 추가적인 오버헤드와 탐색 비용을 발생시킵니다.

오프셋으로 메시지를 주소 지정합니다. 이로 인해 메시지 ID가 연속적이지 않아도 되며, 다음 메시지의 ID를 계산할 때에는 현재 메시지의 길이를 해당 ID에 추가하여 사용합니다.

예를 들어, 토픽 내에서 첫 번째 메시지는 0번 오프셋을 가지며, 다음 메시지는 이전 메시지의 길이를 더한 값인 10번 오프셋을 가지게 됩니다. 따라서 메시지 ID와 오프셋을 서로 교환하여 사용할 수 있습니다.

##### 요약
카프카는 토픽 파티션을 논리적 로그로 구현하며, 각 로그는 동일한 크기의 세그먼트 파일로 구성됩니다. 생산자가 메시지를 발행할 때마다 브로커는 마지막 세그먼트 파일에 메시지를 추가합니다. 메시지는 플러시된 후에만 소비자에게 노출됩니다. 카프카에 저장된 메시지에는 명시적인 메시지 ID가 없으며, 각 메시지는 로그에서의 논리적 오프셋으로 주소 지정됩니다. 소비자는 항상 특정 파티션에서 메시지를 순차적으로 소비하며, 브로커는 메모리에 정렬된 오프셋 목록을 유지합니다. 소비자가 메시지를 수신한 후에는 다음 소비할 메시지의 오프셋을 계산하여 다음 풀 요청에서 사용합니다.
====================================
Efficient transfer:
Kafka는 대량의 로그 데이터를 수집하고 전송하는 분산 메시징 시스템입니다. 이 논문에서는 Kafka의 효율성과 확장성을 높이기 위해 일부 비전통적이지만 실용적인 설계 선택 사항에 대해 설명합니다.

Kafka는 여러 개의 메시지를 한 번에 전송할 수 있는 기능과, 한 번에 여러 개의 메시지를 가져올 수 있는 기능을 제공하여 전송 및 수신의 효율성을 높입니다. 또한, 메모리 캐싱을 사용하지 않고 파일 시스템 페이지 캐시를 사용하여 메시지를 저장하고 전송하므로 메모리 할당 및 가비지 컬렉션의 부담을 줄입니다.

또한, Kafka는 다중 구독자 시스템으로서, 하나의 메시지가 여러 개의 소비자 애플리케이션에서 여러 번 소비될 수 있습니다. 이 때, sendfile API를 이용하여 데이터 복사 및 시스템 호출 횟수를 줄이고 네트워크 액세스를 최적화합니다.

Kafka는 상태 정보를 관리하는 브로커가 없으며, 각 소비자가 자신이 얼마나 많은 메시지를 소비했는지를 관리합니다. 이를 통해 브로커의 복잡성과 부담을 줄일 수 있습니다. 그러나 이로 인해 메시지를 삭제하는 것이 복잡해지는데, Kafka는 간단한 시간 기반 SLA를 사용하여 메시지를 일정 기간 이상 보관하고 삭제합니다.

또한, 소비자는 이전 오프셋으로 되돌아가서 데이터를 재처리할 수 있습니다. 이것은 대부분의 메시지 큐에서 허용되지 않는 기능이지만, Kafka에서는 가능합니다. 이 기능은 데이터 처리 오류를 수정한 후 메시지를 다시 처리하거나, 데이터를 주기적으로 플러시하는 경우 유용합니다. 이러한 기능은 Kafka의 pull 모델에서 쉽게 지원할 수 있습니다.