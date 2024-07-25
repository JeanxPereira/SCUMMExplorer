import struct

def read_la_file(filepath):
    with open(filepath, 'rb') as file:
        content = file.read()

    offset = 0
    blocks = []

    while offset < len(content):
        block_type = content[offset:offset + 4].decode('ascii', errors='ignore')
        block_size = struct.unpack('>I', content[offset + 4:offset + 8])[0]

        # Check if block_size is reasonable
        if block_size <= 8 or block_size > len(content) - offset:
            print(f"Warning: Skipping potentially corrupted block {block_type} with size {block_size}")
            break

        block_data = content[offset + 8:offset + block_size]

        block = {
            'type': block_type,
            'size': block_size,
            'data': block_data
        }

        # Handle LECF sub-blocks
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

        # Check if sub_block_size is reasonable
        if sub_block_size <= 8 or sub_block_size > len(data) - offset:
            print(f"Warning: Skipping potentially corrupted sub-block {sub_block_type} com tamanho {sub_block_size}")
            break

        sub_block_data = data[offset + 8:offset + sub_block_size]

        if sub_block_type == 'LFLF':
            sub_blocks.append({
                'type': sub_block_type,
                'size': sub_block_size,
                'sub_blocks': read_lflf_chunks(sub_block_data)
            })
        else:
            sub_blocks.append({
                'type': sub_block_type,
                'size': sub_block_size,
                'data': sub_block_data
            })

        offset += sub_block_size

    return sub_blocks

def read_lflf_chunks(data):
    offset = 0
    chunks = []

    while offset < len(data):
        if offset + 8 > len(data):
            break

        chunk_type = data[offset:offset + 4].decode('ascii', errors='ignore')
        chunk_size = struct.unpack('<I', data[offset + 4:offset + 8])[0]

        # Ensure chunk_size is reasonable
        if chunk_size <= 0 or chunk_size > len(data) - offset - 8:
            print(f"Warning: Skipping potentially corrupted chunk {chunk_type} with size {chunk_size}")
            break

        chunk_data = data[offset + 8:offset + 8 + chunk_size]

        chunk = {
            'type': chunk_type,
            'size': chunk_size,
            'data': chunk_data
        }

        if chunk_type == 'ROOM':
            chunk['details'] = read_room_chunk(chunk_data)
        elif chunk_type == 'RMSC':
            chunk['details'] = read_rmsc_chunk(chunk_data)
        elif chunk_type == 'SCRP':
            chunk['details'] = read_scrp_chunk(chunk_data)
        elif chunk_type == 'SOUN':
            chunk['details'] = read_soun_chunk(chunk_data)
        elif chunk_type == 'AKOS':
            chunk['details'] = read_akos_chunk(chunk_data)

        chunks.append(chunk)
        offset += 8 + chunk_size

    return chunks

def read_room_chunk(data):
    room = {
        'type': 'ROOM',
        'size': len(data),
        'layers': [],
        'objects': []
    }
    
    # Parsing ROOM chunk specific data
    offset = 0
    while offset < len(data):
        if offset + 8 > len(data):
            break
        layer_type = data[offset:offset + 4].decode('ascii', errors='ignore')
        layer_size = struct.unpack('<I', data[offset + 4:offset + 8])[0]

        if layer_size <= 0 or layer_size > len(data) - offset - 8:
            print(f"Warning: Skipping potentially corrupted layer {layer_type} with size {layer_size}")
            break

        layer_data = data[offset + 8:offset + 8 + layer_size]

        room['layers'].append({
            'type': layer_type,
            'size': layer_size,
            'data': layer_data
        })

        offset += 8 + layer_size

    return room

def read_rmsc_chunk(data):
    rmsc = {
        'type': 'RMSC',
        'size': len(data),
        # Adicione outros detalhes específicos para RMSC aqui
    }
    return rmsc

def read_scrp_chunk(data):
    scrp = {
        'type': 'SCRP',
        'size': len(data),
        # Adicione outros detalhes específicos para SCRP aqui
    }
    return scrp

def read_soun_chunk(data):
    soun = {
        'type': 'SOUN',
        'size': len(data),
        # Adicione outros detalhes específicos para SOUN aqui
    }
    return soun

def read_akos_chunk(data):
    akos = {
        'type': 'AKOS',
        'size': len(data),
        # Adicione outros detalhes específicos para AKOS aqui
    }
    return akos

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
                    for chunk in sub_block['sub_blocks']:
                        print(f"    Chunk Type: {chunk['type']}, Chunk Size: {chunk['size']}")
                        if chunk['type'] == 'ROOM':
                            print(f"    ROOM chunk with {len(chunk['details']['layers'])} layers")
                        else:
                            print(f"    Data Sample: {chunk['data'][:20]}...")
