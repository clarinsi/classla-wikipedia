# Scripts for linguistic processing of the Wikipedia dumps

The classlisize.py script is the main script, reading the Wikipedia extracts at `../output/[wiki]` and producing a conllu output, `[wiki].prelim.conllu`.

Given specific issues in the conllu output, (NER does not conform with IOB etc.), one should run the `patch_conllu.py` script afterwards, like this: `python patch_conllu.py < [wiki].prelim.conllu > [wiki].conllu`.
