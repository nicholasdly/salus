# Security Identifier Search Engine (SISE)

Sleek yet simple; a security identifier search engine in Python using dynamic programming and sequence matching.

- What is this project?
  - This project is a financial security identifier search engine with dynamic priority.
  - Utilizing provided data on security and "street" IDs, this program acts as a search engine for the user by searching a term/query and returning the 10 most relevant financial securities.
  - The user is then allowed to select a security and save it as high priority, which updates the priority order to favor the selected "street" ID of most relevance.

- Why did I choose this project?
  - I have never attempted making a search engine before, nor have I ever made user interfaces using Python. I knew it would challenge me, and I knew there was a lot to learn. With it being my first hackathon, I wanted to get out of my comfort zone. I've made games for fun, but this project felt a lot more like a real world problem I was trying to solve!

- A quick summary of my process
  1. Hand written planning and string similarity computation research
  2. Implementation of a variety of similarity calculating algorithms for both individual understanding and project testing
  5. Implementation of a completely functioning search engine within a terminal
  6. Research and implementation of the search engine user interface

- What did I learn from this project?
  - String metrics and sequence similarity algorithms ([Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance), [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance), [Gestalt pattern matching](https://en.wikipedia.org/wiki/Gestalt_Pattern_Matching)).
  - Builtin Python "difflib" module
  - Builtin Python "tkinter" module
  - .CSV file reading
  - .TXT file reading and writing
  - Dynamic programming

_This is my submission to my first hackathon, ShellHacks 2022, which I attended virtually!_
