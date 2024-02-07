# GPT PDF Organizer

GPT Pdf Organizer is an automatic pdf file organizer that will query chat gpt apis to perform information retrieval about the contents of the files in order to properly classify them and organize them into folders.

The organization process can be customized using a config file in yaml format. The customization process involves how the new organized pdf file names will be constructed from extracted properties, and how pdf files will be grouped into folders also based on those extracted properties.

The available properties that will be extracted from files are:
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

# Usage

```
gpt-pdf-organizer --input-path INPUT_PATH \
 --output-folder OUTPUT_FOLDER \
 [--config-file CONFIG_FILE]
```

Default `config-file` used will be a local './config.yaml' file if no other is passed as argument.


## Example of Usage

### Classifying a Single File

```
gpt-file-organizer --input-path=/home/me/Documents/afile.pdf  --output-folder="/home/me/Documents/classified/"
```

### Classifying All Files in a Folder

To classify a whole folder, just use same command passing a folder instead of a file. The application will automatically detect if the input is a folder or a file.

```
gpt-file-organizer --input-path=/home/me/Documents/pdfs/  --output-folder="/home/me/Documents/classified/"
```


### Example of Classified File Structure

The above example is an theoretical output for classified files that uses only year and title in output filename, and content_type/topic/sub_topic as subfolders:

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
```
## Configuration File

The configuration file is an yaml file that supports the following properties:

| Property                          | Description                                                                                                                                                                                                                                                                                                                                                               |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apiKey`                          | The API key used for authentication. If the `OPENAI_API_KEY` environment variable is set, it will take precedence over this configuration.                                                                                                                                                                                                                               |
| `maxNumTokens`                    | The maximum number of tokens to generate in the output.                                                                                                                                                                                                                                                                                                                  |
| `llmModelName`                    | The name of the language model to use, e.g., "gpt-3.5-turbo".                                                                                                                                                                                                                                                                                                            |
| `logLevel`                        | The level of logging to output, e.g., "info".                                                                                                                                                                                                                                                                                                                            |
| `organizer.moveInsteadOfCopy`     | When set to true, files in the original folder are moved to the output destination instead of being copied. The default is false.                                                                                                                                                                                                                                        |
| `organizer.subfoldersFromAttributes` | Determines the structure of subfolders in the output directory based on content attributes such as "content_type", "author", "topic", "sub_topic", and "year". If an attribute is null, it will be replaced with "unknown_<attribute_name>" in the folder path. The default is "content_type" if this property is not specified.                                             |
| `organizer.filenameFromAttributes` | Configures the filename based on content attributes like "title", "content_type", "author", "topic", "sub_topic", and "year". The original title attribute is always used, and if not set, other attributes are appended to the left of the title. If an attribute is null, it is replaced with "unknown_<attribute_name>". The default is ["title"] if not specified. |
| `organizer.filenameAttributeSeparator` | Specifies the separator used to join attributes in the filename. The default is "-", but any string not containing invalid filename characters is supported.                                                                                                                                                                                                             |


# Installation
```
pip install gpt-pdf-organizer
```
