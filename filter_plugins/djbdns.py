def dns_ipv6(a, *args, **kw):
    while len(a.split(':')) < 8:
        a = a.replace('::', ':::')
    octets = []
    for part in a.split(':'):
        if not part:
            octets.extend([0, 0])
        else:
            # Pad hex part to 4 digits.
            part = '%04x' % int(part, 16)
            octets.append(int(part[:2], 16))
            octets.append(int(part[2:], 16))
    return '\\' + '\\'.join(['%03o' % x for x in octets])


def dns_soa(a, *args, **kw):
    return a.replace('@', '.', 1)


class FilterModule(object):
    def filters(self):
        return {
            'dns_ipv6': dns_ipv6,
            'dns_soa': dns_soa,
        }
