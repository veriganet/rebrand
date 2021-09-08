number_of_peers = "3"

peers = ''
preconfigured_peers = ""
for p in range(int(number_of_peers)):
    peer = "%s-peering%s.%s" % ("kor", str(p), "domainsvc")
    peers = peers + 'const char * default_live_peer_network%s' % str(p) + ' = "' + peer + '";' + "\n"
    preconfigured_peer = "preconfigured_peers.emplace_back(default_live_peer_network%s);" % str(p)
    preconfigured_peers = preconfigured_peers + preconfigured_peer + "\n"

#'const char * default_live_peer_network = "peering.nano.org";'

print(peers)
print(preconfigured_peers)
