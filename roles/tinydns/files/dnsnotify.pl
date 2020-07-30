#!/usr/bin/perl -w

# usage: dnsnotify zone slave [...]
# example: dnsnotify example.org 1.2.3.4 1.2.3.5
# requires Net::DNS >= 0.20

use Net::DNS;
#use Data::Dumper;
use strict;

my $zone   = shift;

die "usage: dnsnotify zone slave [...]\n"
  unless defined $zone and @ARGV;

my $res = new Net::DNS::Resolver;

for my $slave ( @ARGV ) {
  my $packet = new Net::DNS::Packet($zone, "SOA", "IN")
    or die "new Net::DNS::Packet failed\n";

  $packet->header->opcode("NS_NOTIFY_OP");
  $packet->header->aa(1);
  $packet->header->rd(0);

  $res->nameservers($slave);
  #print STDERR Dumper($packet);
  my $reply = $res->send($packet);
  if ( defined $reply ) {
    # print "Received NOTIFY answer from " . $reply->answerfrom . "\n";
    $reply->print;
  } else {
    warn "\n;; TIMED OUT\n";
  }
}

exit 0;
