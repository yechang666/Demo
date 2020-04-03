import re
import sys

if len(sys.argv) < 2:
    print "Usage: python "+sys.argv[0]+" datafile"
    sys.exit()
    
user, system, iow, irq = {}, {}, {}, {}
s1, s2, player, s1_memory, s2_memory, player_memory,  = {}, {}, {}, {}, {}, {}

i = -1
f = open(sys.argv[1])
for l in f.readlines():
    m = re.match(".*csserver:swServer.*", l)
    if m:
        v1, v2 = l.split()[2, 5]
        # v2 = l.split()[5]
        s2[i] = v1
        s2_memory[i] = v2
        continue
    m = re.match(".*silkwave.*", l)
    if m:
        v1, v2 = l.split()[2, 5]
        # v2 = l.split()[5]
        s1[i] = v1
        s1_memory[i] = v2
        continue
    m = re.match(".*vehicleplayer.*", l)
    if m:
        v1, v2 = l.split()[2, 5]
        # v2 = l.split()[5]
        player[i] = v1
        player_memory[i] = v2
        continue
    m = re.match(".*User\s(\d*%).*System\s(\d*%).*IOW\s(\d*%).*IRQ\s(\d*%).*", l)
    if m:
        i += 1
        user[i] = m.group(1)
        system[i] = m.group(2)
        iow[i] = m.group(3)
        irq[i] = m.group(4)
        # print "CPU: ", user[i], system[i], iow[i], irq[i]
        continue

f.close()

print "user,system,iow,irq,csserver1,csserver1_memory,csserver2,csserver2_memory,player,player_memory"
for i in range(len(user)):
    d = "-1"
    strbuf = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (user.get(i, d), \
                                       system.get(i, d), \
                                       iow.get(i, d), \
                                       irq.get(i, d), \
                                       s1.get(i, d), \
                                       s1_memory.get(i, d), \
                                       s2.get(i, d), \
                                       s2_memory.get(i, d), \
                                       player.get(i, d), \
                                       player_memory.get(i, d))
    print strbuf
print "Total", len(user), "records"
