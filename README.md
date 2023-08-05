## ELFtool

Tiny universal tool for exploring executable ELF files (Executable and Linkable
Format). 

```shell
python elftool.py /bin/bash
```

As an optional parameter, you can set `TO_DICT=true`

```shell
TO_DICT=true python elftool.py /bin/bash
```

To parse output I use [jq](https://github.com/jqlang/jq):

```shell
python elftool.py /bin/bash | jq
```

Example output:

```shell
[
  {
    "type": "PT_PHDR",
    "offset": "0x40",
    "virtual_address": "0x40",
    "physical_address": "0x40",
    "size_in_file": "0x2d8",
    "size_in_memory": "0x2d8",
    "segment_sections": null
  },
  {
    "type": "PT_INTERP",
    "offset": "0x318",
    "virtual_address": "0x318",
    "physical_address": "0x318",
    "size_in_file": "0x1c",
    "size_in_memory": "0x1c",
    "segment_sections": [
      [
        ".interp",
        "0x318"
      ]
    ]
},
... 
]
```

Or get only the desired section

```shell
python elftool.py /bin/bash | jq '.[0]'
```

Example output:

```shell
{
  "offset": "0x40",
  "physical_address": "0x40",
  "segment_sections": null,
  "size_in_file": "0x2d8",
  "size_in_memory": "0x2d8",
  "type": "PT_PHDR",
  "virtual_address": "0x40"
}
```

Or just one value

```shell
python elftool.py /bin/bash | jq '.[0] | .size_in_memory'
```

Example output:

```shell
"0x2d8"
```

More jq usage examples can be found [here](https://jqlang.github.io/jq/tutorial/).
