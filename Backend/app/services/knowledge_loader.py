from pathlib import Path


def load_knowledge():

    content = ""

    knowledge_path = Path(
        "knowledge"
    )

    for file in knowledge_path.rglob(
        "*.md"
    ):

        content += (
            file.read_text(
                encoding="utf-8"
            )
        )

        content += "\n\n"

    return content