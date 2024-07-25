import struct

def read_la_file(filepath):
    with open(filepath, 'rb') as file:
        content = file.read()

    offset = 0
    blocks = []

    while offset < len(content):
        block_type = content[offset:offset + 4].decode('ascii', errors='ignore')
        block_size = struct.unpack('>I', content[offset + 4:offset + 8])[0]

        if block_size <= 8 or block_size > len(content) - offset:
            print(f"Warning: Skipping potentially corrupted block {block_type} with size {block_size}")
            break

        block_data = content[offset + 8:offset + block_size]

        block = {
            'type': block_type,
            'size': block_size,
            'data': block_data
        }

        if block_type == 'LECF':
            block['sub_blocks'] = read_lecf_sub_blocks(block_data)

        blocks.append(block)
        offset += block_size

    return blocks

def read_lecf_sub_blocks(data):
    offset = 0
    sub_blocks = []

    while offset < len(data):
        if offset + 8 > len(data):
            break

        sub_block_type = data[offset:offset + 4].decode('ascii', errors='ignore')
        sub_block_size = struct.unpack('>I', data[offset + 4:offset + 8])[0]

        if sub_block_size <= 8 or sub_block_size > len(data) - offset:
            print(f"Warning: Skipping potentially corrupted sub-block {sub_block_type} with size {sub_block_size}")
            break

        sub_block_data = data[offset + 8:offset + sub_block_size]

        sub_block = {
            'type': sub_block_type,
            'size': sub_block_size,
            'data': sub_block_data
        }

        if sub_block_type == 'LFLF':
            sub_block['chunks'] = read_lflf_chunks(sub_block_data)

        sub_blocks.append(sub_block)
        offset += sub_block_size

    return sub_blocks

def read_lflf_chunks(data):
    offset = 0
    chunks = []

    while offset < len(data):
        if offset + 8 > len(data):
            break

        chunk_type = data[offset:offset + 4].decode('ascii', errors='ignore')
        chunk_size = struct.unpack('>I', data[offset + 4:offset + 8])[0]

        if chunk_size <= 8 or chunk_size > len(data) - offset:
            print(f"Warning: Skipping potentially corrupted chunk {chunk_type} with size {chunk_size}")
            break

        chunk_data = data[offset + 8:offset + chunk_size]

        chunk = {
            'type': chunk_type,
            'size': chunk_size,
            'data': chunk_data
        }

        if chunk_type == 'ROOM':
            chunk['details'] = read_room_details(chunk_data)

        chunks.append(chunk)
        offset += chunk_size

    return chunks

def read_room_details(data):
    header_format = '<HHHHHHHHHHBBBH'
    header_size = struct.calcsize(header_format)
    if len(data) < header_size:
        print("Warning: Room header is too short, skipping room details.")
        return {}

    header = struct.unpack(header_format, data[:header_size])

    room_details = {
        'room_size': header[0],
        'unknown1': header[1],
        'room_width': header[2],
        'room_height': header[3],
        'unknown2': header[4],
        'tileset_offset': header[5],
        'attribute_table_offset': header[6],
        'mask_offset': header[7],
        'unknown3': header[8],
        'unknown4': header[9],
        'num_objects': header[10],
        'num_boxes_offset': header[11],
        'num_sounds': header[12],
        'num_scripts': header[13],
        'exit_script_offset': header[14] if len(header) > 14 else None,
        'entry_script_offset': header[15] if len(header) > 15 else None,
    }

    sub_blocks = []
    offset = header_size
    while offset < len(data):
        if offset + 8 > len(data):
            break

        sub_block_type = data[offset:offset + 4].decode('ascii', errors='ignore')
        sub_block_size = struct.unpack('>I', data[offset + 4:offset + 8])[0]

        if sub_block_size <= 8 or sub_block_size > len(data) - offset:
            print(f"Warning: Skipping potentially corrupted sub-block {sub_block_type} with size {sub_block_size}")
            break

        sub_block_data = data[offset + 8:offset + sub_block_size]

        sub_block = {
            'type': sub_block_type,
            'size': sub_block_size,
            'data': sub_block_data
        }

        sub_blocks.append(sub_block)
        offset += sub_block_size

    room_details['sub_blocks'] = sub_blocks
    return room_details

# Exemplo de uso
if __name__ == "__main__":
    blocks = read_la_file(r'D:\GamingLibrary\The Curse of Monkey Island\COMI.LA2')
    for block in blocks:
        print(f"Block Type: {block['type']}, Block Size: {block['size']}")
        if block['type'] == 'LECF':
            for sub_block in block['sub_blocks']:
                print(f"  Sub Block Type: {sub_block['type']}, Sub Block Size: {sub_block['size']}")
                if sub_block['type'] == 'LFLF':
                    print("    LFLF block found")
                    for chunk in sub_block['chunks']:
                        print(f"    Chunk Type: {chunk['type']}, Chunk Size: {chunk['size']}")
                        if chunk['type'] == 'ROOM':
                            room_details = chunk['details']
                            print(f"      Room Size: {room_details.get('room_size')}")
                            print(f"      Room Width: {room_details.get('room_width')}")
                            print(f"      Room Height: {room_details.get('room_height')}")
                            print(f"      Number of Objects: {room_details.get('num_objects')}")
                            print(f"      Number of Boxes Offset: {room_details.get('num_boxes_offset')}")
                            print(f"      Number of Sounds: {room_details.get('num_sounds')}")
                            print(f"      Number of Scripts: {room_details.get('num_scripts')}")
                            print(f"      Exit Script Offset: {room_details.get('exit_script_offset')}")
                            print(f"      Entry Script Offset: {room_details.get('entry_script_offset')}")
                            for sub_block in room_details.get('sub_blocks', []):
                                print(f"        Sub Block Type: {sub_block['type']}, Sub Block Size: {sub_block['size']}")
