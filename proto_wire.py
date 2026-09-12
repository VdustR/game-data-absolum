"""Schema-less protobuf wire reader/writer for local Absolum save research."""

def read_varint(buf, pos):
    value = shift = 0
    while pos < len(buf):
        byte = buf[pos]
        pos += 1
        value |= (byte & 127) << shift
        if byte < 128:
            return value, pos
        shift += 7
        if shift > 70:
            break
    raise ValueError('invalid varint')


def encode_varint(value):
    out = bytearray()
    while value > 127:
        out.append((value & 127) | 128)
        value >>= 7
    out.append(value)
    return bytes(out)


def fields(buf):
    pos = 0
    out = []
    while pos < len(buf):
        start = pos
        tag, pos = read_varint(buf, pos)
        number, wire = tag >> 3, tag & 7
        if not 1 <= number <= 100000:
            raise ValueError(f'invalid field number {number}')
        if wire == 0:
            value, pos = read_varint(buf, pos)
        elif wire == 1:
            value = buf[pos:pos+8]; pos += 8
        elif wire == 2:
            length, pos = read_varint(buf, pos)
            value = buf[pos:pos+length]; pos += length
        elif wire == 5:
            value = buf[pos:pos+4]; pos += 4
        else:
            raise ValueError(f'invalid wire type {wire}')
        if pos > len(buf):
            raise ValueError('truncated field')
        out.append((number, wire, value, start, pos))
    return out


def encode_fields(items):
    out = bytearray()
    for number, wire, value in items:
        out += encode_varint((number << 3) | wire)
        if wire == 0:
            out += encode_varint(value)
        elif wire == 2:
            out += encode_varint(len(value)) + value
        elif wire in (1, 5):
            out += value
        else:
            raise ValueError(wire)
    return bytes(out)


def strings_deep(buf, depth=0):
    if depth > 25:
        return
    try:
        nodes = fields(buf)
    except ValueError:
        return
    for number, wire, value, _, _ in nodes:
        if wire != 2:
            continue
        try:
            decoded = value.decode('utf-8')
            if decoded.isprintable():
                yield decoded
        except UnicodeDecodeError:
            pass
        yield from strings_deep(value, depth+1)
