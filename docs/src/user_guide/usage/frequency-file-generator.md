# Frequency File Generator

![frequency-file-generator.png](../../img/frequency-file-generator.png)

The Frequency File Generator creates a csv file (comma delimited) containing the morphs found in the selected files. The
morphs are placed in descending order based on frequency; the most frequent morph is on line 2, the 2nd most frequent
is on line 3, etc.

![csv-file.png](../../img/csv-file.png)

### Morph Collision

Inflected morphs can be identical even if they are derived from different bases, e.g:

```
Base : Inflection
有る    ある
或る    ある
```

To prevent misinterpretation of the inflected morphs we also store the base.

### Select Input

Here you have to select a folder. Any files that match your selected file formats and are in this folder or sub-folders,
will be used by the frequency file generator.

Take for example the following folders and their files:

```
english_texts/
    - books/
        - The Wise Man's Fear/
            - The Wise Man's Fear.epub
            - The Wise Man's Fear.txt
    - subs/
        - Game-of-Thrones/
            - episode_1.srt
        - Lord_of_the_Rings/
            - The_Fellowship_of_the_Ring.vff

```

If you were to select the `books` folder and you checked the .txt file format, then the frequency file analyzer would
only use the `The Wise Man's Fear.txt` file.

If you were to select the folder `english_texts` and you checked all the file format options, then the frequency file analyzer would
use the files:
- `The Wise Man's Fear.txt`
- `episode_1.srt`
- `The_Fellowship_of_the_Ring.vff`

### Select Output

The output file is automatically set to be `[anki profile folder]/frequency-files/frequency.csv`. You can set it to be
what ever you want.

### Minimum Occurrence

You can limit the morphs to only those that occur at least this many times.

### Ignore

The 'ignore'-options are the equivalent to those found in ['Parse' settings](../setup/settings/parse.md).