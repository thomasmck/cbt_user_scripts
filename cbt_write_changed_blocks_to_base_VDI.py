#!/usr/bin/env python

def write_changed_blocks_to_base_VDI(vdi_path, changed_block_path, bitmap_path, output_path):
	bitmap = open(bitmap_path, 'r')
	vdi = open(vdi_path, 'r+b')
	blocks = open(changed_block_path, 'r+b')
	combined_vdi = open(output_path, 'wb')

	try:
		bitmap_r = bitmap.read()
		vdi_r = vdi.read()
		blocks_r = blocks.read()
		BLOCK_SIZE = 64 * 1024
		cb_offset = 0
		for x in range(0, len(bitmap_r)):
			offset = x * BLOCK_SIZE
			if bitmap_r[x] == "1":
				combined_vdi.write(blocks_r[offset:offset+BLOCK_SIZE])
				cb_offset += BLOCK_SIZE
			else:
				combined_vdi.write(vdi_r[offset:offset+BLOCK_SIZE])
	finally:
		bitmap.close()
		vdi.close()
		blocks.close()
		combined_vdi.close()

base_vdi_path = './testvdi.vhd'
changed_blocks_path = './testblocks.vhd'
bitmap_path = './bitmap'
output_path = './combined_vdi.vhd'

write_changed_blocks_to_base_VDI(base_vdi_path, changed_blocks_path, bitmap_path, output_path)
