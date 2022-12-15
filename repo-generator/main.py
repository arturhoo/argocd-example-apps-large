import os
import random
import subprocess

TRASH_DIR_PATH = "helm-guestbook/trash"
WORDS: list[str] = []


def initialize_words() -> None:
    with open("/usr/share/dict/words", "r") as f:
        global WORDS
        WORDS = f.read().splitlines()


def generate_random_message(length: int = 3) -> str:
    words = random.choices(WORDS, k=length)
    return " ".join(words)


def generate_file_contents(line_num: int = 50) -> str:
    lines = [generate_random_message(5) for _ in range(line_num)]
    return "\n".join(lines)


def git_add_and_commit(file_path: str) -> None:
    subprocess.run(f"git add {file_path}", shell=True)
    msg = generate_random_message()
    subprocess.run(f"git commit --no-gpg-sign -m '{msg}'", shell=True)


class Generator:
    def __init__(self, trash_dir_path: str):
        self.trash_dir_path = trash_dir_path

    def modify_random_file(self) -> str:
        files = os.listdir(self.trash_dir_path)
        chosen_file = random.choice(files)
        file_path = f"{self.trash_dir_path}/{chosen_file}"
        with open(file_path, "w") as f:
            f.write(generate_file_contents())
        return file_path

    def create_random_file(self) -> str:
        file_name = generate_random_message(1).lower()
        file_path = f"{self.trash_dir_path}/{file_name}"
        with open(file_path, "w") as f:
            f.write(generate_file_contents())
        return file_path


if __name__ == "__main__":
    initialize_words()
    charts = ["helm-guestbook1", "helm-guestbook2"]
    for chart in charts:
        gen = Generator(f"{chart}/trash")
        for _ in range(10):
            file = gen.create_random_file()
            git_add_and_commit(file)
            file = gen.modify_random_file()
            git_add_and_commit(file)
