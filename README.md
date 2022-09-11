# shellhacks-2022

This is my submission to my first hackathon, ShellHacks 2022, which I attended virtually!

- What is this project?
  - This project is a financial security identifier search engine with dynamic priority.
  - Utilizing provided data on security and "street" IDs, this program prompts the user for a search term/query and returns the 5 most relevant financial securities.
  - The user is then allowed to select a security, which updates the priority order to favor the selected "street" ID of most relevance.
  - The program will prompt the user for another query after each selection, but the user can exit the program anytime they are prompted for input.

- Why did I choose this project?
  - I have never attempted making a search engine before--I knew it would challenge me, and I knew there was a lot to learn. With it being my first hackathon, I wanted to get out of my comfort zone. I've made games for fun, but this project felt a lot more realistic to what I might end up doing in my field of work after college.

- What did I learn from this project?
  - I learned _**a lot**_ about string metrics and sequence similarity calculations, which is something I have never really looked into.
  - I knew there was always going to be a library I could use, and I was sure Python also had built-in modules for similarity computation, but I wanted to at least start by doing my own research and learn about how it all worked, rather than just accepting the easy route.

- How did I make this project?
  - Nearly my entire first night of programming during the hackathn was spent researching string metrics, edit distance, and sequence matching. I had looked at the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance), the [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance), a combination of the two, but I eventually settled on the [Gestalt pattern matching](https://en.wikipedia.org/wiki/Gestalt_Pattern_Matching) algormithm.
  - After implementing all of them, the Gestalt method produced the closest product to my envision of similarity. It was during my research into the Gestalt matching algorithm where I discovered the Python builtin difflab module utilized Gestalt method almost exactly!
