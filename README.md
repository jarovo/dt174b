dt174b
======

This is a tool for interfacing the [CEM DT-174B](device_info.md) Weather Datalogger that is talking on USB by some [specific protocol](protocol.md).

USB permissions
---------------
When the datalogger is plugged-in, OS have to create a device in `/dev`. By default, only root has write access there. This tool is an userspace USB driver which needs `rw` permissions to such file. To be able to access the datalogger as ordinary user,
 add an udev rule that says the `datalogger` group may write to such device-file. I've prepared such rule in file [etc/udev/rules.d/10-dt174b.rules](etc/udev/rules.d/10-dt174b.rules) for you, so you just need to copy it:
 
    sudo cp etc/udev/rules.d/10-dt174b.rules /etc/udev/rules.d
    
Then you should create the `datalogger` group and add yourself there.

    sudo groupadd datalogger
    sudo usermod -a -G datalogger `whoami`
    
Don't forget to logioff/login after this as your presence in the group is determined upon login only. You may also do ``su `whoami` -``.
