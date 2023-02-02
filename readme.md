# MQTT v5 Demos

## Prerequisites

```sh
# Install mosquitto, mosquitto_sub, mosquitto_pub
brew install mosquitto
```

## New Features

- Shared Subscriptions

  - Open 4 terminals
  - Terminal 1
    - Run a mosquitto broker instance using Docker Desktop with `mosquitto`
  - Terminal 2
    - First subscriber subscribes to the shared topic 'topic1' with `mosquitto_sub -t '$share/group1/topic1'`
  - Terminal 3
    - Second subscriber subscribes to the shared topic 'topic1' with `mosquitto_sub -t '$share/group1/topic1'`
  - Terminal 4
    - Lastly, publish messages to the shared topic with `mosquitto_pub -t topic1 -m hello1` then `mosquitto_pub -t topic1 -m hello2`
  - Expected result is only one subscriber gets the first published message 'hello1', and only the other subscriber gets the second published message 'hello2'.
  - More info, see [Oasis MQTT 5 Docs](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901250)

    ![MQTT5 Shared Subscription](./media/shared-subscription.png)
