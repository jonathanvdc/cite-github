# `cite-github`

`cite-github` is a Python script that takes a GitHub file URL as input and generates a BibTeX entry that cites that file.

Here's how it works: suppose that we want to cite ["Fundamentals of garbage collection,"](https://github.com/dotnet/docs/blob/master/docs/standard/garbage-collection/fundamentals.md) an article on the garbage collector for the .NET framework.
Quite a few people have contributed to that article. Manually looking up their names and adding those names to the `author` field of a BibTeX entry is a chore.
For completeness' sake, we also want to note the month and year of the last commit and extract the title from the article we want to cite.
Finally, we should include the file's URL in the BibTeX entry so readers can easily find it, as well as a note that discloses when we accessed the file.

This whole workflow gets old fast. Enter `cite-github`, a Python script that automates the whole process. You provide `cite-github` with a GitHub file URL and `cite-github` generates a BibTeX entry.
```console
$ python3 cite-github.py https://github.com/dotnet/docs/blob/master/docs/standard/garbage-collection/fundamentals.md
@misc{wenzel2019fundamentals,
	title={Fundamentals of garbage collection},
	author={Maira Wenzel and Next Turn and Nick Schonning and Dan Mabee and Ron Petrusha and Mike B and Jan Kotas and Aymeric A and xaviex and Mike Jones and Michal Ciechan and Alan and Luke Latham and tompratt-AQ},
	month={May},
	year={2019},
	howpublished={\url{https://github.com/dotnet/docs/blob/master/docs/standard/garbage-collection/fundamentals.md}},
	note={Accessed on June 1, 2019.},
}
```

Note that this is subject to the GitHub API's rate-limit of 60 requests per hour. If you need to perform more requests, then you can provide a GitHub OAuth token as a second argument to `cite-github`:
```console
$ python3 cite-github.py https://github.com/dotnet/docs/blob/master/docs/standard/garbage-collection/fundamentals.md <token>
@misc{wenzel2019fundamentals,
	title={Fundamentals of garbage collection},
	author={Maira Wenzel and Next Turn and Nick Schonning and Dan Mabee and Ron Petrusha and Mike B and Jan Kotas and Aymeric A and xaviex and Mike Jones and Michal Ciechan and Alan and Luke Latham and tompratt-AQ},
	month={May},
	year={2019},
	howpublished={\url{https://github.com/dotnet/docs/blob/master/docs/standard/garbage-collection/fundamentals.md}},
	note={Accessed on June 1, 2019.},
}
```
