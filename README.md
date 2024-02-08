
# GPT PDF Organizer

GPT Pdf Organizer is an automatic pdf file organizer that will query chat gpt apis to perform information retrieval about the contents of the files in order to properly classify them and organize them into folders.

The organization process can be customized using a config file in yaml format. This customization involves how the new organized pdf file names will be constructed from extracted properties, and how pdf files will be grouped into folders also based on those extracted properties.


## Table of Contents

- [Usage](#section-id-7)
- [API Cost of Usage and Tokens](#section-id-17)
  - [Selecting an LLM Model](#section-id-34)
 - [Configuration File](#section-id-48)
 - [Example of Usage](#section-id-101)
   - [Classifying a Single File](#section-id-103)
   - [Classifying All Files in a Folder](#section-id-109)
   - [Example of Output File Structure](#section-id-117)
- [Limitations](#section-id-152)
- [Installation](#section-id-158)
- [Development](#section-id-162)
  - [Prompt Customization](#section-id-164)



<div id='section-id-1'/>

## Usage

```
gpt-pdf-organizer --input-path INPUT_PATH \
 --output-folder OUTPUT_FOLDER \
 [--config-file CONFIG_FILE]
```

Default `config-file` used will be a local './config.yaml' file if no other is passed as argument.

<div id='section-id-17'/>

## API Cost of Usage and Tokens

The ChatGpt API uses [tokens](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them) to calculate the API request call cost. Tokens are not always the same as words.
This tool performs a query to ChatGpt API to ask questions about the content of a PDF file, and will use tokens in two ways:

- The query prompt, sent to GPT to ask about the PDF content.
- The PDF content

The PDF content is not the full PDF but rather the first `config.maxNumTokens` tokens that will be extracted from the PDF file.

The total amount of tokens spent during a single request for each file is then `config.maxNumTokens` + `promptTokenSize`, where `promptTokenSize` is the constant total size of the prompt and spans `281` tokens.

Make sure to add enough credits to your ChatGpt account and setting up your [apiKey](#configuration-file) before using.

The `apiKey` can be set via configuration file or (by setting `OPENAI_API_KEY` environment variable - it will override the config `apiKey` value).


<div id='section-id-34'/>

### Selecting an LLM Model

The cost of usage also depends on the model used. One can configure the model by setting `llmModelName` in the [apiKey](#configuration-file) file.


In summary, the total cost for organizing your files will depend on 3 factors:

- The total number of files to organize
- The chosen model (e.g: `gpt-4` or `gpt-3.5-turbo`, etc). See [OpenAPI Models](https://platform.openai.com/docs/models/overview) for all the models.
- The number of tokens to use for extracting PDF content (see [maxNumTokens](#configuration-file)). The larger `maxNumTokens` value, the more accurate will be the classification of the content, but also more costly the api call will be.


Optionally, one can also try to customize the prompt. See [Prompt Customization](#prompt-customization).

<div id='section-id-48'/>

## Configuration File

The configuration file is an yaml file that supports the following properties:

| Property                          | Description                                                                                                                                                                                                                                                                                                                                                               |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apiKey`                          | The API key used for authentication. If the `OPENAI_API_KEY` environment variable is set, it will take precedence over this configuration.                                                                                                                                                                                                                               |
| `maxNumTokens`                    | The maximum number of tokens to use for extracting content from the PDF file. Only the first `maxNumTokens` tokens will be extract from the PDF file. The larger the number of tokens, the more accurate the results for classification, but more costly will be the request.                                                                                                                                                                                                                                                                                                                |
| `llmModelName`                    | The name of the language model to use, e.g., "gpt-3.5-turbo".                                                                                                                                                                                                                                                                                                            |
| `logLevel`                        | The level of logging to output, e.g., "info".                                                                                                                                                                                                                                                                                                                            |
| `organizer.moveInsteadOfCopy`     | When set to true, files in the original folder are moved to the output destination instead of being copied. The default is false. Be aware that will remove the original file after moving it to the classified folder structure                                                                                                                                                                                                                                        |
| `organizer.subfoldersFromAttributes` | Determines the structure of subfolders in the output directory based on content attributes such as "content_type", "author", "topic", "sub_topic", and "year". If an attribute is null, it will be replaced with "unknown_<attribute_name>" in the folder path. The default is "content_type" if this property is not specified.                                             |
| `organizer.filenameFromAttributes` | Configures the filename based on content attributes like "title", "content_type", "author", "topic", "sub_topic", and "year". The original title attribute is always used, and if not set, other attributes are appended to the left of the title. If an attribute is null, it is replaced with "unknown_<attribute_name>". The default is ["title"] if not specified. |
| `organizer.filenameAttributeSeparator` | Specifies the separator used to join attributes in the filename. The default is "-", but any string not containing invalid filename characters is supported.                                                                                                                                                                                                             |

The attributes used in config `organizer.subfoldersFromAttributes` and `organizer.filenameFromAttributes` are:

- Title
- Year of Publication
- Author(s)
- Main Topic
- Content Type: Can be 'Book' or 'Article'
- Sub Topic (or Sub Area within Main Topic).

Main Topic and Sub Topic are always classified according to the following list, following Topic/Sub Topic nesting:

- **Natural Sciences**
  - Physics
  - Chemistry
  - Biology
  - Earth Sciences
- **Formal Sciences**
  - Mathematics
  - Computer Science
  - Statistics
- **Applied Sciences**
  - Engineering
  - Medicine
  - Agriculture
- **Social Sciences**
  - Psychology
  - Economics
  - Sociology
- **Interdisciplinary Fields**
  - Environmental Science
  - Biotechnology
  - Neuroscience
- **Humanities**
  - Science and technology studies
  - History and philosophy of science
  - Digital humanities


<div id='section-id-101'/>

## Example of Usage

<div id='section-id-103'/>

### Classifying a Single File

```
gpt-file-organizer --input-path=/home/me/Documents/afile.pdf  --output-folder="/home/me/Documents/classified/"
```

<div id='section-id-109'/>

### Classifying All Files in a Folder

To classify a whole folder, just use same command passing a folder instead of a file. The application will automatically detect if the input is a folder or a file.

```
gpt-file-organizer --input-path=/home/me/Documents/pdfs/  --output-folder="/home/me/Documents/classified/"
```

<div id='section-id-117'/>

### Example of Output File Structure

The above example is an theoretical output for classified files that uses only year and title in output filename, and content_type/sub_topic as subfolders (this can be configured in config file):

- Original Files:
```
pdfs/
├── file1_arxiv.pdf
├── article_202_arxiv.pdf
├── dimensionality.pdf
├── afile.pdf
...
```

- Classified Output Files:

```
output_dir/
├── article/
│ ├── mathematics/
│ │     ├── minimum_curves_in_manifolds.pdf
│ │     ├── the_great_article_of_somethin.pdf
│ ├── computer_science/
│ │     ├── the_sift_algorithm.pdf
│ │     ├── viola_jones_algorithm.pdf
│ ...
├── book/
│ ├── mathematics/
│ │     ├── calculus_volume_19.pdf
│ │     ├── fourier_transforms_200.pdf
│ ...
├── unclassified/
│ ├── afile.pdf
```

<div id='section-id-152'/>

## Limitations

For some PDF files, the content may possibly not be extracted due to the quality of the scanned image or lacking of metadata. For those cases, the file will be sent to a `unclassified` folder within the output directory.

Another case where files may not be classified is due to prompt response inaccuracy: depending on the model used and the number of tokens used to extract the content (see `maxNumTokens` in [config](#configuration-file)), the prompt api may not be able to classify the content.

<div id='section-id-158'/>

## Installation
```
pip install gpt-pdf-organizer
```
<div id='section-id-162'/>

## Development

<div id='section-id-164'/>

### Prompt Customization

This step is optional and a default prompt is already tweaked to extract good results from ChatGpt API. If however, one wants to change the prompt, follow the steps bellow.

To customize the prompt that will be performed to each file, one can do it in two ways:

- By changing the prompt in the (prompt_builder)[./gpt_pdf_organizer/domain/prompt_builder.py] module: this will keep current GPT prompter but allows to change the prompt sent to the GPT api.
- By passing a different [PromptQuerier](./gpt_pdf_organizer/service/prompt_querier.py) class instance to Application when it starts on [main entrypoint](./gpt_pdf_organizer/gpt_pdf_organizer.py): this allows integrating different apis other than ChatGpt, such as bing or bard.
