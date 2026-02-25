# DKC2 Trivia Database
This repo hosts a Python library for Archipelago that outputs trivia questions in DKC2's format and without format which should help to implement them in other games as long you're exporting this library into your `.apworld`.

This helps me to unlink updating the trivia database with DKC2's apworld updates in the future.

# Submitting questions
You can submit questions via a [Google Form](https://forms.gle/Wh5U2dLMTcYgB64o7) which aims to be a visual aid for understanding the required format or open a Pull Request here with your changes in a `.txt` file.
Questions uploaded by the Google Form will be merged slowly into the repo.

## Creating a txt manually
You may use as an example [this .txt file](https://github.com/TheLX5/DKC2-Trivia/blob/master/data/examples/parser_2_example.txt) to understand how the format works.

The first lines before the first set of `---` corresponds to the file's header, which populates some data about the game such as:
* Parser version (`PARSER`): Usually it's better to leave it at 2.
  * Parser version 1 only allows up to two incorrect answers, version 2 allows three incorrect answers.
  * The third incorrect question is filled as `"None are correct :)"` for Version 1.
* Game name (`GAME`): Self explanatory. It should match a valid topic.
  * Full list of supported topics can be found on the Google Form, I'll be putting docs on that later™️
  * You can only have one game type per `.txt` file
* Author (`AUTHOR`): Your name.
  * Should NOT contain special characters, only A-Z, a-z, 0-9 and underscore characters.
 
The question format should follow this:
* The very first line contains the string `QUESTION:` followed by the difficulty of said question (`EASY`, `MEDIUM`, `HARD`).
* Question goes next and should be up to 6 lines with a maximum of 32 characters each
  * Ideally you should stop at 30 characters per line, as it looks bad in DKC2 when letters reach the borders of the screen
  * The parser will stop processing the question lines until it reads `ANSWERS:` or reaches the 7th line
* Next go the answers for your question. The parser will process exactly four lines after `ANSWERS:`. It'll process three lines if version 1 is used.
  * The first line will **always** be the correct answer
  * Answers should NOT exceed 24 characters
    * However, you can trick the parser into making the answer be two lines long by adding this `°` character as a new line separator. This is mainly a DKC2 quirk. I do recommend sticking to a single line answer so the question fits into more games.
* Finally, a separator (`---`) **must** be included after entering the last incorrect answer

The filename of the `.txt` file does not matter.

# Interacting with the database as a developer
You can import the parsed trivia database with:
```
from worlds._dkc2_trivia.trivia import parse_topics

trivia_topics = parse_topics()
```
It will return a dictionary containing the entire database by topic name, with each topic contained in its own `Topic` object (`dict[str, Topic]`).

## Topic object
`Topic` objects contain every single question that falls into said topic separated by easy, medium and hard questions. Those can be accesed by the `Topic`'s attributes and they return a list:
```
easy_questions: list[TriviaQuestion]
medium_questions: list[TriviaQuestion]
hard_questions: list[TriviaQuestion]
```
Alternatively, you can also fetch every question regardless of its difficulty with the `fetch_every_question()` function.

## TriviaQuestion object
Questions are bundled with their answers (one correct, three incorrect). They also have some miscelaneous data that may be useful for someone (`author` and `topic_name`). You can access the question data via the attributes of the object:
```
question: str
author: str
topic_name: str
correct_answer: str
incorrect_answer_1: str
incorrect_answer_2: str
incorrect_answer_3: str
```
There's the `fetch_incorrect_answers()` function that returns a list of incorrect answers (`list[str]`).

Do note that most of the questions were made with DKC2 in mind, which means that most of them have an "invalid" third incorrect answer which defaults to `"None are correct :)"`.

Not so relevant note: If one passes a specific bool through `parse_topics`, `question` will return a `list[str]` instead which also has a very _different_ format. Said bool defaults to false, so there's nothing to worry about not declaring it anywhere.

## Shorter game names
In case you require short game names and don't want to create a dictionary of those, the apworld also provides those.
```
from worlds._dkc2_trivia.games import short_names
```
`short_names` is a `dict[str, str]` where the keys are the full game name (the one declared in the APWorld) and the values are the shorter names. Example: `"Super Mario World": "SMW"`

## Game aliases
Since there are games with multiple implementations, I decided to also provide within the apworld some aliases for those games.
```
from worlds._dkc2_trivia.games import aliases
```
`aliases` is a `dict[str, str]`, where keys are the full game implementation name (the one declared in the APWorld) and the values are the "common" or "shared" game name. Example: `"SMW: Spicy Mycena Waffles": "Super Mario World"`
