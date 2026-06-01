import json


def generate(links_file, data_file, output_file):
    with open(links_file, "r", encoding="utf-8") as links_json:
        links_data = json.load(links_json)

    with open(data_file, "r", encoding="utf-8") as data_json:
        data = json.load(data_json)

    links_data = [link for link in links_data]

    content = "| Name | Id |\n| ---- | --- |\n"

    for link, character in zip(links_data, data):
        name = link.get("name")
        available = link.get("available")

        if available is True:
            data_id = f"`{character.get('id', 'None')}`"
        elif available is False:
            data_id = "None"
        else:
            continue

        if name and data_id:
            content += f"| {name} | {data_id} |\n"

    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(content)


def generate_outfits(links_file, data_file, output_file):
    with open(links_file, "r", encoding="utf-8") as f:
        links_data = json.load(f)

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    character_ids = set()
    outfit_ids = {}

    for character in data:
        char_id = character.get("id")

        if not char_id:
            continue

        character_ids.add(char_id)

        for outfit in character.get("outfits") or []:
            outfit_id = outfit.get("id")

            if outfit_id and outfit_id != "default":
                outfit_ids[outfit_id] = char_id

    content = "| Character | Name | Id | Type |\n"
    content += "| ---- | --- | --- |---- |\n"

    for link_character in links_data:
        char_name = (link_character.get("name") or "").strip()

        if not char_name:
            continue

        char_base_id = char_name[0].lower() + char_name[1:].replace(" ", "")

        for outfit in link_character.get("outfits") or []:
            outfit_name = (outfit.get("name") or "").strip()

            if not outfit_name:
                continue

            words = outfit_name.split()

            base_outfit_id = words[0].lower() + "".join(
                word.capitalize() for word in words[1:]
            )

            possible_ids = [
                base_outfit_id,
                f"{char_base_id}{base_outfit_id[0].upper()}{base_outfit_id[1:]}",
            ]

            found_id = None
            id_type = None

            for possible_id in possible_ids:
                if possible_id in character_ids:
                    found_id = possible_id
                    id_type = "character"
                    break

                if possible_id in outfit_ids:
                    found_id = possible_id
                    id_type = "outfit"
                    break

            if found_id:
                content += (
                    f"| {char_name} | {outfit_name} " f"| `{found_id}` | {id_type} |\n"
                )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)


generate(
    "temp/input/characters_links.json",
    "temp/input/characters_data.json",
    "docs/Characters.md",
)
generate(
    "temp/input/boards_links.json", "temp/input/boards_data.json", "docs/Hoverboard.md"
)
generate_outfits(
    "temp/input/characters_outfit.json",
    "temp/input/characters_data.json",
    "docs/Outfits.md",
)
