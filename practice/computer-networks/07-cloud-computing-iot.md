# Set 7 — Cloud Computing and IoT (service and deployment models, virtualization, storage, SLA, IoT basics)

**50 questions** — High: 19, Medium: 30, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Service model): A. SaaS  B. PaaS  C. IaaS  
List II (Example): I. Amazon EC2  II. Gmail  III. Google App Engine

(1) A-II, B-I, C-III  
(2) A-III, B-II, C-I  
(3) A-I, B-III, C-II  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — Gmail is ready-to-use software, App Engine a development platform, EC2 raw virtual machines.

</details>

**Q2.** `High`  
In which cloud service model does the consumer manage the operating system, runtime and applications, while the provider manages virtualization, servers, storage and networking?

(1) FaaS  
(2) PaaS  
(3) IaaS  
(4) SaaS  

<details><summary>Answer</summary>

**(3)** — IaaS gives the consumer control from the operating system upwards.

</details>

**Q3.** `High`  
A developer deploys application code to a cloud service that supplies the operating system, runtime, middleware and database, without managing the servers. This is

(1) On-premises hosting  
(2) SaaS  
(3) PaaS  
(4) IaaS  

<details><summary>Answer</summary>

**(3)** — PaaS provides a managed platform; the consumer manages only applications and data.

</details>

**Q4.** `High`  
Arrange the cloud service models in increasing order of the control the consumer has over the underlying resources.  
A. IaaS  B. SaaS  C. PaaS

(1) A, C, B  
(2) B, A, C  
(3) B, C, A  
(4) C, B, A  

<details><summary>Answer</summary>

**(3)** — SaaS gives the least control and IaaS the most.

</details>

**Q5.** `High`  
Which of the following are essential characteristics of cloud computing according to NIST?  
A. On-demand self-service  B. Broad network access  C. Resource pooling  D. Rapid elasticity  E. Measured service  
Choose the correct answer from the options given below:

(1) A, B, C, D and E  
(2) A, B and C only  
(3) A, C and D only  
(4) B, D and E only  

<details><summary>Answer</summary>

**(1)** — These are the five essential characteristics in the NIST definition.

</details>

**Q6.** `High`  
Match List I with List II.  
List I (Deployment model): A. Public cloud  B. Private cloud  C. Hybrid cloud  D. Community cloud  
List II (Description): I. Shared by several organisations with common concerns  II. Composition of two or more distinct clouds bound together  III. Open for use by the general public  IV. Operated solely for a single organisation

(1) A-III, B-II, C-IV, D-I  
(2) A-IV, B-III, C-II, D-I  
(3) A-III, B-IV, C-I, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(4)** — The four NIST deployment models.

</details>

**Q7.** `Medium`  
An organisation runs its normal workload in its private cloud and automatically uses a public cloud when demand spikes. This is called

(1) multi-tenancy  
(2) vendor lock-in  
(3) cloud bursting  
(4) live migration  

<details><summary>Answer</summary>

**(3)** — Cloud bursting is a hybrid-cloud technique for handling peak loads.

</details>

**Q8.** `High`  
Given below are two statements.  
Statement I: A Type 1 hypervisor runs directly on the host hardware.  
Statement II: A Type 2 hypervisor runs as an application on top of a host operating system.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Type 1 is bare-metal (e.g. Xen, VMware ESXi, Hyper-V); Type 2 is hosted (e.g. VirtualBox, VMware Workstation).

</details>

**Q9.** `High`  
Which of the following is a Type 2 (hosted) hypervisor?

(1) Microsoft Hyper-V  
(2) Xen  
(3) VMware ESXi  
(4) Oracle VirtualBox  

<details><summary>Answer</summary>

**(4)** — VirtualBox runs on top of a conventional operating system.

</details>

**Q10.** `High`  
Given below are two statements.  
Statement I: In full virtualization the guest operating system runs unmodified and is unaware that it is virtualized.  
Statement II: In paravirtualization the guest operating system is modified to make hypercalls to the hypervisor.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Paravirtualization trades guest modification for better performance.

</details>

**Q11.** `Medium`  
The software layer that creates and runs virtual machines by multiplexing physical hardware among them is the

(1) load balancer  
(2) device driver  
(3) hypervisor (virtual machine monitor)  
(4) container registry  

<details><summary>Answer</summary>

**(3)** — It gives each VM the illusion of its own hardware.

</details>

**Q12.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Containers are more lightweight than virtual machines.  
Reason R: Containers share the host operating system kernel instead of each running a full guest operating system.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Sharing the kernel gives faster start-up and lower overhead.

</details>

**Q13.** `Medium`  
Moving a running virtual machine from one physical host to another without noticeable downtime is called

(1) live migration  
(2) snapshotting  
(3) provisioning  
(4) cloning  

<details><summary>Answer</summary>

**(1)** — Live migration is used for load balancing and maintenance.

</details>

**Q14.** `Medium`  
The property by which a single instance of software serves several customers, with their data kept isolated, is called

(1) multi-tenancy  
(2) multiprogramming  
(3) multithreading  
(4) multihoming  

<details><summary>Answer</summary>

**(1)** — Multi-tenancy is the basis of resource pooling in SaaS.

</details>

**Q15.** `High`  
Given below are two statements.  
Statement I: Vertical scaling (scaling up) adds more CPU or memory to an existing server.  
Statement II: Horizontal scaling (scaling out) adds more servers or instances to the pool.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Standard definitions of scale-up and scale-out.

</details>

**Q16.** `Medium`  
The ability of a cloud system to acquire and release resources automatically as the workload changes is called

(1) fault tolerance  
(2) interoperability  
(3) portability  
(4) elasticity  

<details><summary>Answer</summary>

**(4)** — Scalability is the ability to grow; elasticity is growing and shrinking automatically.

</details>

**Q17.** `High`  
A formal contract between a cloud provider and a consumer that specifies guaranteed levels of availability, performance and penalties is a

(1) non-disclosure agreement  
(2) service level agreement (SLA)  
(3) service catalogue  
(4) software licence  

<details><summary>Answer</summary>

**(2)** — SLAs state metrics such as uptime percentage and response time.

</details>

**Q18.** `Medium`  
An SLA guarantees 99.9% availability. The maximum permitted downtime in a 30-day month is approximately

(1) 7.2 hours  
(2) 4.3 minutes  
(3) 43 minutes  
(4) 72 hours  

<details><summary>Answer</summary>

**(3)** — 0.1% of 30 × 24 × 60 = 43,200 minutes is 43.2 minutes.

</details>

**Q19.** `High`  
Match List I with List II.  
List I (Storage type): A. Object storage  B. Block storage  C. File storage  
List II (Example or characteristic): I. Shared hierarchical file system accessed through NFS or SMB  II. Amazon S3 — data kept as objects with metadata in a flat namespace  III. Raw volumes attached to a virtual machine, e.g. Amazon EBS

(1) A-II, B-I, C-III  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — Objects in buckets, blocks as volumes, files in shared directories.

</details>

**Q20.** `Medium`  
A database offered as a managed cloud service, in which the provider handles installation, patching, backup and scaling, is called

(1) DBaaS  
(2) NaaS  
(3) a data warehouse appliance  
(4) DaaS (desktop as a service)  

<details><summary>Answer</summary>

**(1)** — Examples are Amazon RDS and Azure SQL Database.

</details>

**Q21.** `Medium`  
According to the CAP theorem a distributed data store cannot simultaneously guarantee all three of

(1) consistency, availability and partition tolerance  
(2) concurrency, atomicity and performance  
(3) consistency, atomicity and persistence  
(4) capacity, accuracy and privacy  

<details><summary>Answer</summary>

**(1)** — When a network partition occurs, a system must choose between consistency and availability.

</details>

**Q22.** `Medium`  
In the pay-as-you-go model of cloud computing

(1) billing is a fixed annual fee  
(2) the customer buys the hardware  
(3) operational expenditure is converted into capital expenditure  
(4) capital expenditure is converted into operational expenditure  

<details><summary>Answer</summary>

**(4)** — Consumers pay for measured usage instead of investing in infrastructure.

</details>

**Q23.** `Medium`  
Which of the following is a concern or disadvantage of cloud computing?

(1) On-demand self-service  
(2) Elasticity  
(3) Reduced capital cost  
(4) Vendor lock-in  

<details><summary>Answer</summary>

**(4)** — Moving data and applications between providers can be difficult.

</details>

**Q24.** `Medium`  
In serverless computing (Function as a Service)

(1) the customer must manage the virtual machines  
(2) there are no servers involved  
(3) applications run only on the client  
(4) the provider manages server provisioning and the customer is billed per function execution  

<details><summary>Answer</summary>

**(4)** — AWS Lambda is a well-known example.

</details>

**Q25.** `Medium`  
Processing data close to where it is generated, instead of sending everything to a distant data centre, is called

(1) edge (fog) computing  
(2) grid computing  
(3) utility computing  
(4) batch computing  

<details><summary>Answer</summary>

**(1)** — It reduces latency and bandwidth, which matters for IoT applications.

</details>

**Q26.** `Medium`  
Which of the following is an open-source platform for building private and public IaaS clouds?

(1) Hadoop  
(2) MongoDB  
(3) OpenStack  
(4) Kubernetes  

<details><summary>Answer</summary>

**(3)** — OpenStack provides compute (Nova), storage (Swift, Cinder) and networking (Neutron) services.

</details>

**Q27.** `Medium`  
In cloud resource management, distributing incoming requests across multiple servers so that no single server is overloaded is called

(1) load balancing  
(2) orchestration of storage  
(3) virtualization  
(4) caching  

<details><summary>Answer</summary>

**(1)** — Load balancing improves both utilisation and availability.

</details>

**Q28.** `Medium`  
Which programming model, popularised by Google and implemented in Hadoop, processes large data sets in parallel across a cluster?

(1) Publish-subscribe  
(2) Two-phase commit  
(3) MapReduce  
(4) Remote procedure call  

<details><summary>Answer</summary>

**(3)** — Map tasks process key-value pairs and reduce tasks aggregate them.

</details>

**Q29.** `Medium`  
Given below are two statements.  
Statement I: Server virtualization allows several virtual servers to run on one physical server.  
Statement II: Server consolidation through virtualization increases hardware utilisation and reduces energy consumption.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Consolidation is one of the main motivations for virtualization.

</details>

**Q30.** `High`  
The term "Internet of Things" was coined by

(1) Tim Berners-Lee  
(2) Kevin Ashton  
(3) Vint Cerf  
(4) John McCarthy  

<details><summary>Answer</summary>

**(2)** — Ashton used the term in 1999 in the context of RFID supply chains.

</details>

**Q31.** `High`  
Arrange the layers of the basic three-layer IoT architecture from bottom to top.  
A. Network layer  B. Application layer  C. Perception layer

(1) C, B, A  
(2) C, A, B  
(3) B, A, C  
(4) A, C, B  

<details><summary>Answer</summary>

**(2)** — Perception (sensing), network (transmission), application.

</details>

**Q32.** `High`  
Given below are two statements.  
Statement I: A sensor converts a physical quantity into an electrical signal.  
Statement II: An actuator converts an electrical signal into a physical action.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Sensors measure; actuators act.

</details>

**Q33.** `High`  
Which of the following statements about MQTT is correct?

(1) It is a routing protocol for sensor networks  
(2) It is a link-layer protocol for RFID  
(3) It is a request-response protocol that runs over UDP  
(4) It is a lightweight publish-subscribe protocol that runs over TCP and uses a broker  

<details><summary>Answer</summary>

**(4)** — Clients publish to topics and the broker delivers messages to subscribers.

</details>

**Q34.** `High`  
Match List I with List II.  
List I (IoT protocol): A. MQTT  B. CoAP  C. 6LoWPAN  D. ZigBee  
List II (Description): I. Adaptation layer for carrying IPv6 over IEEE 802.15.4  II. Low-power mesh networking standard built on IEEE 802.15.4  III. Publish-subscribe messaging over TCP  IV. RESTful request-response protocol over UDP

(1) A-III, B-IV, C-I, D-II  
(2) A-III, B-IV, C-II, D-I  
(3) A-III, B-I, C-IV, D-II  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(1)** — Standard roles of the four protocols.

</details>

**Q35.** `Medium`  
The default ports of MQTT and CoAP are respectively

(1) TCP 1883 and UDP 5683  
(2) TCP 80 and UDP 53  
(3) TCP 8883 and TCP 443  
(4) TCP 5683 and UDP 1883  

<details><summary>Answer</summary>

**(1)** — MQTT uses 1883 (8883 over TLS); CoAP uses UDP 5683.

</details>

**Q36.** `Medium`  
How many quality-of-service levels does MQTT define?

(1) 3  
(2) 2  
(3) 4  
(4) 5  

<details><summary>Answer</summary>

**(1)** — QoS 0 (at most once), QoS 1 (at least once), QoS 2 (exactly once).

</details>

**Q37.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: IPv6 is considered essential for the large-scale deployment of IoT.  
Reason R: The 128-bit address space of IPv6 can give a unique address to each of billions of devices.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — IPv4's 32-bit space is too small for the number of connected things.

</details>

**Q38.** `Medium`  
Given below are two statements.  
Statement I: Arduino Uno is a microcontroller-based board.  
Statement II: Raspberry Pi is a single-board computer capable of running a full operating system such as Linux.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Arduino runs a single program on a microcontroller; Raspberry Pi has a microprocessor and an operating system.

</details>

**Q39.** `Medium`  
Which of the following is a low-power wide-area network (LPWAN) technology for long-range IoT communication?

(1) ZigBee  
(2) NFC  
(3) Bluetooth Low Energy  
(4) LoRaWAN  

<details><summary>Answer</summary>

**(4)** — LoRaWAN and NB-IoT cover kilometres at low data rates; the others are short-range.

</details>

**Q40.** `Medium`  
Which technology uses electromagnetic fields to automatically identify and track tags attached to objects?

(1) OCR  
(2) LiDAR  
(3) RFID  
(4) GPS  

<details><summary>Answer</summary>

**(3)** — A reader interrogates passive or active tags; RFID was an early enabler of IoT.

</details>

**Q41.** `Medium`  
A passive RFID tag

(1) is powered by the energy of the reader's radio signal  
(2) has its own battery  
(3) uses GPS to report location  
(4) can be read from several kilometres  

<details><summary>Answer</summary>

**(1)** — Passive tags have no power source and a short read range.

</details>

**Q42.** `Medium`  
A device that connects IoT devices using protocols such as ZigBee or BLE to the Internet, performing protocol translation, is called an

(1) IoT gateway  
(2) end node  
(3) actuator  
(4) RFID tag  

<details><summary>Answer</summary>

**(1)** — Gateways bridge constrained device networks and IP networks.

</details>

**Q43.** `Medium`  
Direct communication between devices without human intervention, a precursor of IoT, is called

(1) H2M interaction  
(2) P2P file sharing  
(3) B2B commerce  
(4) M2M communication  

<details><summary>Answer</summary>

**(4)** — Machine-to-machine communication.

</details>

**Q44.** `Medium`  
A virtual representation of a physical object or system that is kept synchronised with it through sensor data is called a

(1) digital twin  
(2) hologram  
(3) data lake  
(4) virtual machine  

<details><summary>Answer</summary>

**(1)** — Digital twins are used for monitoring and simulation in industrial IoT.

</details>

**Q45.** `Medium`  
Which of the following are major challenges of IoT?  
A. Security and privacy  B. Interoperability  C. Energy constraints of devices  D. Scalability  
Choose the correct answer from the options given below:

(1) B, C and D only  
(2) A, B, C and D  
(3) A, B and C only  
(4) A and B only  

<details><summary>Answer</summary>

**(2)** — All four are well-recognised IoT challenges.

</details>

**Q46.** `Medium`  
Which of the following is NOT a characteristic of the Constrained Application Protocol (CoAP)?

(1) It is designed for constrained devices  
(2) It requires a broker to deliver messages  
(3) It runs over UDP  
(4) It follows the REST model with methods such as GET and PUT  

<details><summary>Answer</summary>

**(2)** — CoAP is a direct client-server protocol; brokers are used by MQTT.

</details>

**Q47.** `Low`  
In cloud computing, the term "utility computing" refers to

(1) free computing resources  
(2) using utility software  
(3) computing performed only by public utilities  
(4) providing computing resources as a metered service, like electricity  

<details><summary>Answer</summary>

**(4)** — Resources are packaged and billed according to usage.

</details>

**Q48.** `Medium`  
Which of the following is an example of Software as a Service?

(1) Salesforce CRM  
(2) Heroku  
(3) Google Compute Engine  
(4) Microsoft Azure Virtual Machines  

<details><summary>Answer</summary>

**(1)** — Salesforce delivers a finished application; Heroku is PaaS and the others are IaaS.

</details>

**Q49.** `Medium`  
Grid computing differs from cloud computing mainly in that a grid

(1) always belongs to one commercial provider  
(2) is a federation of loosely coupled, geographically distributed and often heterogeneous resources applied to a common task  
(3) cannot run parallel jobs  
(4) offers on-demand self-service with pay-per-use billing  

<details><summary>Answer</summary>

**(2)** — Clouds are centrally managed, virtualized and offered as a metered service.

</details>

**Q50.** `Medium`  
In the cloud shared-responsibility model for IaaS, which of the following is the responsibility of the customer?

(1) Cooling and power  
(2) Maintenance of the hypervisor  
(3) Physical security of the data centre  
(4) Patching the guest operating system and securing applications and data  

<details><summary>Answer</summary>

**(4)** — The provider secures the cloud infrastructure; the customer secures what it runs in the cloud.

</details>
