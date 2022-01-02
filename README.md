# Nagios-Discord
This is a very simple Python script which will allow Nagios notifications to be announced on Discord.

You'll need to make some modifications to your Nagios installation. The steps are quite easy.

First, we need to make sure we have dependencies installed.  
On your cli: `pip3 install discord-webhook`

Place the scripts in your plugins directory on the Nagios server.

Now we need to create the Nagios commands to call these scripts. These should probably go in your `commands.cfg` file.
```
define command {
  command_name notify-host-by-discord
  command_line /usr/lib/nagios/plugins/send-discord-host.sh
}

define command {
  command_name notify-service-by-discord
  command_line /usr/lib/nagios/plugins/send-discord-service.sh
}
```

Next, we should create a Nagios contact. This is usually found in your `contacts.cfg` file
```
define contact {
  contact_name discord
  use discord-contact
  alias Discord Contact
  email some@example.com
}
```

Add your new contact to your appropriate contact group too!

```
define contactgroup {
  contactgroup_name everyone
  alias Everyone
  members alice,bob,discord
}
```

Finally, add a template in your `templates.cfg` file.
```
define contact {
  name discord-contact
  service_notification_period 24x7
  host_notification_period 24x7
  service_notification_options w,u,c,r,f,s
  host_notification_options d,u,r,f,s
  service_notification_commands notify-service-by-discord
  host_notification_commands notify-host-by-discord
  register 0
}
```