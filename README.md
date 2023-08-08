# Test technique (ELK – Scraping)
## Installing Elasticsearch and kibana on ubuntu 22.04
From the link provided, click https://www.elastic.co/fr/downloads/elasticsearch to download Elasticsearch.
Do the same for kibana https://www.elastic.co/fr/downloads/kibana

Elasticsearch requires Java to run. I'm going to install the latest version (Elasticsearch-8.9.0) which needs java 11.

### Installation Steps

1. **Install Java:**
   Open a terminal and run the following commands based on your Linux distribution:

   ```
   sudo apt update
   sudo apt install default-jre
   ```
2. **Extract the Archive:**

   Navigate to the directory where you downloaded the Elasticsearch package and use the following command to extract the archive:

   ```
   tar -xzf elasticsearch-8.9.0-linux-x86_64.tar.gz
   ```

3. **Configure Elasticsearch:**

   Navigate into the extracted directory:

   ```
   cd elasticsearch-8.9.0
   nano config/elasticsearch.yml
   ```
   Change these configurations:
   - `cluster.name`: Ml_sentiment (use any name you want, I used Ml_sentiment).

   - `node.name`: [ ml_node1, node-2]

   - `node.roles`: [ ml, master, remote_cluster_client, data] (ml is necessary and remote_cluster_client is recommended to work on machine learning for Q2)

   - `cluster.initial_master_nodes`: ["ml_node1", "node-2"]

   - `xpack.ml.enabled`: true (required for machine learning)

   These are the only modifications that I made.

4. **Start Elasticsearch:**

   To start Elasticsearch, run the following command from the Elasticsearch directory:
   ```
   ./bin/elasticsearch
   ```
   When running for the first time, this will return password, HTTP CA certificate and kibana enrollement token. Save them in a secure place.

5. **Extract the Archive for Kibana**

   Open a new terminal, navigate to the directory where kibana is downloaded, and extract the archive
   ```
   tar -xzf kibana-8.9.0-linux-x86_64.tar.gz
   ```
6. **Start Kibana:**

   Move to the extracted directory and run kibana as follows:
   ```
   cd kibana-8.9.0
   ./bin/kibana
   ```
   Click in the link provided (http://localhost:5601/ in my case) and login with the username (default `elastic`) and the password saved from elasticsearch.
   
   ![User interface](images/user_interface.png)

   
