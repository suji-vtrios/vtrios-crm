from pathlib import Path


def load_knowledge():

    content = ""

    knowledge_path = (
        Path(__file__)
        .parent.parent
        / "knowledge"
    )

    print(
        "KNOWLEDGE PATH =",
        knowledge_path
    )

    for file in knowledge_path.rglob(
        "*.md"
    ):

        print(
            "LOADING =",
            file
        )

        content += file.read_text(
            encoding="utf-8"
        )

        content += "\n\n"

    return content