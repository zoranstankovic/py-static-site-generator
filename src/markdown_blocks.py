def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        clean_block = block.strip()
        if not clean_block:
            continue
        blocks.append(clean_block)

    return blocks
