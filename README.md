# WikiNews Sentiment Analysis, Translation, Summarization Tool

## sacreBLEU

sacreBLEU is used in this project to get a gauge of the accuracy of a few models which were used in the translation step.

```text
@inproceedings{post-2018-call,
  title = "A Call for Clarity in Reporting {BLEU} Scores",
  author = "Post, Matt",
  booktitle = "Proceedings of the Third Conference on Machine Translation: Research Papers",
  month = oct,
  year = "2018",
  address = "Belgium, Brussels",
  publisher = "Association for Computational Linguistics",
  url = "https://www.aclweb.org/anthology/W18-6319",
  pages = "186--191",
}
```

[Post, Matt. "A Call for Clarity in Reporting BLEU Scores." Proceedings of the Third Conference on Machine Translation: Research Papers, Belgium, Brussels, Association for Computational Linguistics, Oct. 2018, pp. 186-191.](https://www.aclweb.org/anthology/W18-6319)

## Data Source: CCMatrix v1

The CCMatrix v1 is data used to create a source and reference set for the use of the sacreBLEU scoring.

[CCMatrix: Mining Billions of High-Quality Parallel Sentences on the WEB](https://arxiv.org/abs/1911.04944) by Holger Schwenk, Guillaume Wenzek, Sergey Edunov, Edouard Grave and Armand Joulin.

[Beyond English-Centric Multilingual Machine Translation](https://arxiv.org/abs/2010.11125) by Angela Fan, Shruti Bhosale, Holger Schwenk, Zhiyi Ma, Ahmed El-Kishky, Siddharth Goyal, Mandeep Baines, Onur Celebi, Guillaume Wenzek, Vishrav Chaudhary, Naman Goyal, Tom Birch, Vitaliy Liptchinsky, Sergey Edunov, Edouard Grave, Michael Auli, and Armand Joulin.
This HuggingFace CCMatrix dataset is a wrapper around the service and files prepared and hosted by OPUS:

[Parallel Data, Tools and Interfaces in OPUS](https://www.aclweb.org/anthology/L12-1246/) by Jörg Tiedemann.
