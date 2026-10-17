"""LightCraft回归的合成GPS JPEG与JPEG结构读取；不处理用户素材。"""
import struct


def jpeg_segments(data):
    assert data[:2] == b'\xff\xd8', 'Not JPEG'
    at = 2
    while at + 4 <= len(data):
        assert data[at] == 255, 'Malformed JPEG marker'
        marker = data[at + 1]
        if marker in (0xda, 0xd9):
            return
        size = int.from_bytes(data[at + 2:at + 4], 'big')
        assert size >= 2 and at + 2 + size <= len(data), 'Malformed JPEG segment'
        yield marker, data[at + 4:at + 2 + size]
        at += 2 + size


def jpeg_size(data):
    for marker, body in jpeg_segments(data):
        if marker in (0xc0, 0xc1, 0xc2):
            return int.from_bytes(body[3:5], 'big'), int.from_bytes(body[1:3], 'big')
    raise AssertionError('JPEG has no supported frame header')


def has_gps(data):
    for marker, body in jpeg_segments(data):
        if marker != 0xe1 or not body.startswith(b'Exif\0\0'):
            continue
        t = body[6:]
        assert t[:2] in (b'II', b'MM') and len(t) >= 8, 'Malformed EXIF'
        order = 'little' if t[:2] == b'II' else 'big'
        def number(pos, n):
            assert 0 <= pos and pos + n <= len(t), 'EXIF offset outside segment'
            return int.from_bytes(t[pos:pos + n], order)
        def entries(offset):
            count = number(offset, 2)
            assert count <= 1024 and offset + 2 + count * 12 <= len(t), 'Malformed EXIF IFD'
            return {number(offset + 2 + i * 12, 2): offset + 2 + i * 12 for i in range(count)}
        root = entries(number(4, 4))
        if 0x8825 in root:
            gps = entries(number(root[0x8825] + 8, 4))
            if 2 in gps and 4 in gps:
                return True
    return False


def with_synthetic_gps(jpeg):
    """只用于合成回归：加入GPS坐标及作者，不带任何用户位置。"""
    def entry(tag, kind, count, value):
        return struct.pack('<HHI', tag, kind, count) + (struct.pack('<I', value) if isinstance(value, int) else value)
    artist = b'CRAFT AUTHOR\0'
    gps_at = 38 + len(artist)
    gps_at += gps_at % 2
    values_at = gps_at + 2 + 5 * 12 + 4
    ifd = struct.pack('<H', 2) + entry(315, 2, len(artist), 38) + entry(0x8825, 4, 1, gps_at) + b'\0' * 4
    tiff = b'II*\0' + struct.pack('<I', 8) + ifd + artist
    tiff += b'\0' * (gps_at - len(tiff))
    tiff += struct.pack('<H', 5) + entry(0, 1, 4, b'\x02\x03\0\0') + entry(1, 2, 2, b'N\0\0\0') + entry(2, 5, 3, values_at) + entry(3, 2, 2, b'E\0\0\0') + entry(4, 5, 3, values_at + 24) + b'\0' * 4
    tiff += b''.join(struct.pack('<II', x, 1) for x in [31, 12, 0, 121, 30, 0])
    payload = b'Exif\0\0' + tiff
    segment = b'\xff\xe1' + struct.pack('>H', len(payload) + 2) + payload
    assert jpeg[:2] == b'\xff\xd8'
    return jpeg[:2] + segment + jpeg[2:]
