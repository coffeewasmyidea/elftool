#!/usr/bin/python

import json
import os
import sys
from pathlib import Path
from typing import Any

from elftools.elf.elffile import ELFFile


def run(args: list, to_dict: bool = False) -> list[dict[str, Any]] | str:
    """
    The definition of the section structure

    typedef struct {
        Elf32_Word sh_name;
        Elf32_Word sh_type;
        Elf32_Word sh_flags;
        Elf32_Addr sh_addr;
        Elf32_Off sh_offset;
        Elf32_Word sh_size;
        Elf32_Word sh_link;
        Elf32_Word sh_info;
        Elf32_Word sh_addralign;
        Elf32_Word sh_entsize;
    } Elf32_Shdr;

    Reference: https://refspecs.linuxbase.org/elf/elf.pdf

    """

    if len(args) < 2:
        print("Provide an elf binary file")
        sys.exit(1)

    file_path = args[1]

    if Path(file_path).is_dir():
        print("Provided file is a dir")
        sys.exit(1)

    if not Path(file_path).is_file():
        print("Provided file does not exist")
        sys.exit(1)

    with open(file_path, "rb") as raw_file:
        elffile = ELFFile(raw_file)

        segments = []

        for segment_idx in range(elffile.num_segments()):
            segments.insert(segment_idx, {})
            segments[segment_idx]["segment"] = elffile.get_segment(segment_idx)
            segments[segment_idx]["sections"] = []

        for section_idx in range(elffile.num_sections()):
            section = elffile.get_section(section_idx)
            for segment in segments:
                if segment["segment"].section_in_segment(section):
                    segment["sections"].append(section)

        jdata_list = []

        for segment in segments:
            seg_head = segment["segment"].header
            jdata = {
                "type": seg_head.p_type,
                "offset": hex(seg_head.p_offset),
                "virtual_address": hex(seg_head.p_vaddr),
                "physical_address": hex(seg_head.p_paddr),
                "size_in_file": hex(seg_head.p_filesz),
                "size_in_memory": hex(seg_head.p_memsz),
            }

            jdata["segment_sections"] = (
                [
                    (
                        s.name,
                        hex(s["sh_addr"]),
                    )
                    for s in segment["sections"]
                ]
                if segment["sections"]
                else None
            )

            jdata_list.append(jdata)

        if to_dict:
            # Return a list[dict[str, Any]]
            return jdata_list

        # Serialize obj to a JSON formatted str
        return json.dumps(jdata_list)


if __name__ == "__main__":
    to_dict = bool(os.environ.get("TO_DICT"))
    result = run(sys.argv, to_dict)

    # debug
    print(result)
