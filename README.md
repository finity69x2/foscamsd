# FoscasmSD

Support for older Standard Definition models of Foscam Security cameras

## installation:

copy the foscamsd files to the custom components directory of your home assistant config folder

## usage:

```
camera:
  - platform: foscamsd
    ip: 192.168.1.51
    port: 8001
    username: !secret cam_user
    password: !secret new_cam_pw
    name: Kitchen
```
