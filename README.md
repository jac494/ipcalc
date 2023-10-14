# ipcalc

The intention was extending my learning of python and also to verify
IPv4 subnetting skills. This could all be greatly condensed with the
use of python modules.

So long, and thanks for all the fish.

A basic IPv4 subnetting calculator that is intended to provide a small interface for validating IPv4 network addresses, subnet masks, and host address membership within a given subnet.

## 20231014

Picking this back up and just doing a refactor to clean it up and polish a bit since I don't have any other major current project going on. I still realize I could just `import ipaddress` but that's still not the point here. I might one day make an alternate version that would be more of a production-ready commandline utility and in that case I'd likely just use the ipaddress imports but even then (as far as I'm aware) the python builtin doesn't do membership checks within subnets which is intended to be a main feature of this calcualtor. Might fork it into a new repo for that one day. Today is not that day.