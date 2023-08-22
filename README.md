# IoT-DNS-Replication
## Filtering commands used for wireshark
```
ip.addr == 192.168.0.7
frame.time >= "2019-08-01 00:00:00" && frame.time <= "2019-08-01 23:59:59"
```
## Steps of the method
#### 1.  Compute the Domain Query Probability (code in **domain_probability.py**)
   
  * We have IoT traffic traces collected over a period of T = 2 consecutive weeks from 53 different IoT devices.

* We extract the set of domain names queried by each device.

* Let’s say device Q_1 queries three distinct domain names:{q11, q12, q13}, and device Q_2 queries two distinct domain names: {q21, q22}

* We divide the observation time T into non-overlapping time windows of length w=1 hour. Therefore, we have N=T/w = 2*7*24/1 = 336 time windows.

* For each domain q, for each of the N time windows, we determine whether q was queried or not during that window.

* Now, we assume we observed at least one DNS query to q in n out of N time windows. We then say that device Q queries q with probability p = n/N

Here is an example:
| Time Windoe   | Device Q1 Domains queried | Device Q2 Domains queried |
| ------------- |:-------------:| -----:|
| 0-1 hour      | q11, q12      | q21 |
| 1-2 hour      | q11           |   q21, q22 |
| 2-3 hour      | q13           |    q21 |
| 3-4 hour      | q11,q13       |    q21, q22 |
Now compute the probabilities:

Device Q1:

q11 was queried in 3 out of 4 time windows: p11 = 3/4

q12  was queried in 1 out of 4 time windows: p12 = 1/4

q13 was  queried in 2 out of 4 time windows: p13 = 2/4

Device Q2:

q21 was queried in 4out of 4 time windows: p21 = 4/4

q22 was queried in  2 out of 4 time windows: p22 = 2/4

#### 2. Compute the domain IDF (code in **IoT_idf.py**)
   
* Count the number of clients Nc(q_i) for each domain q_i during the observation period Tp.
* Count the total number of client Nc.
* Compute the IDF for each domain
  
  IDF(q_i) = $log (1 + \frac{Nc}{Nc(q_i)+1})$

#### 3. Compute the threasholds for each IoT device(code in threashold.py)  

* Find similarity score between IoT and non-IoT devices and treat them as negetive scores.
* Find similarit score between IoT and IoT devices and treat them as positive scores.
* Generate ROC curve
* Use 0.1% as a tolerable flase positve rate to find a threashold
