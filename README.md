# crypto-websocket-visualisation
Websocket to listen to crypto prices and visualise the trends


## Dev Log
✅ Goal 1: Create websock connection and listen to crypto data for 
a few minutes. Stop listening automatically, create a pandas dataframe
and plot this on a graph. 

<p align="center" width="100%">
 <img align="center" width="700" alt="Screenshot 2023-06-10 at 13 09 55" src="https://github.com/ZaynRassam/crypto-websocket-visualisation/assets/112281021/1cd44217-91f5-40ec-96d3-fc3fb07de938">
<p/>


✅ Goal 2: Create a data visualisation that updates as the websocket is 
listening to the feed. 

![ezgif com-video-to-gif (3)](https://github.com/ZaynRassam/crypto-websocket-visualisation/assets/112281021/ed7e880e-ca38-4355-8139-c0326a1eac3c)


✅ Goal 3: Currently, everything is running in the same script. If we introduce Kafka, the on_message function
could send the messages to a Kafka topic (producer), another script could then listen to the topic and use
the data (consumer)

![ezgif.com-video-to-gif (4).gif](..%2F..%2FDownloads%2Fezgif.com-video-to-gif%20%284%29.gif)


Below is a video where the graph only plots the last 10 values (similar to Goal 2's graph). The x-axis still
can't handle this many values.

![ezgif.com-video-to-gif (5).gif](..%2F..%2FDownloads%2Fezgif.com-video-to-gif%20%285%29.gif)


Goal 4: We're redrawing the plot every time you matplotlib. Find a better way of drawing the graph.