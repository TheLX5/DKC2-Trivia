from importlib import resources
from importlib.resources.abc import Traversable
from .parser import parser_version_1, parser_version_2
from .types import Topic


def parse_single_topic(topic_data: list[str], is_dkc2: bool) -> Topic | None:
    if "PARSER:" not in topic_data[0]:
        print (f"Failed to fetch the game name.")
        return None
    parser_version = int(topic_data[0].split(": ")[1].rstrip())
    if parser_version == 1:
        return parser_version_1(topic_data, is_dkc2)
    elif parser_version == 2:
        return parser_version_2(topic_data, is_dkc2)
    else:
        print (f"Invalid or non supported parser version.")
        return None


def parse_topics(is_dkc2: bool = False) -> dict[str, Topic]:
    trivia_topics: dict[str, Topic] = {}

    root = resources.files(__package__).joinpath("data")
    topic_index: list[Traversable] = []

    def search_folder(path: Traversable) -> None:
        for item in path.iterdir():
            if item.is_file() and item.name.endswith(".txt"):
                topic_index.append(item)
            elif item.is_dir():
                search_folder(item)

    search_folder(root)

    for topic_file in topic_index:
        topic_data = topic_file.read_text(encoding='utf-8')
        parsed_topic = parse_single_topic(topic_data.splitlines(), is_dkc2)
        if parsed_topic is None:
            continue
        topic_name = parsed_topic.topic_name
        if topic_name not in trivia_topics.keys():
            trivia_topics[topic_name] = parsed_topic
        else:
            trivia_topics[topic_name].easy_questions += parsed_topic.easy_questions
            trivia_topics[topic_name].medium_questions += parsed_topic.medium_questions
            trivia_topics[topic_name].hard_questions += parsed_topic.hard_questions

    return trivia_topics
