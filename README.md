dt174b
======

This is a tool for interfacing the [CEM DT-174B](device_info.md) Weather Datalogger that is talking on USB by some [specific protocol](protocol.md).

USB permissions
---------------
When the datalogger is plugged-in, OS have to create a device in `/dev`. By default, only root has write access there. This tool is an userspace USB driver which needs `rw` permissions to such file. To be able to access the datalogger as ordinary user,
 add yourself to the `dialout` user group:
 
     sudo usermod --append --group dialout $(whoami)
    
Don't forget to logioff/login after this as your presence in the group is determined upon login only. You may also do `su $(whoami) -`.
