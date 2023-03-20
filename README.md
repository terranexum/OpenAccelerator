# OpenAccelerator

This Python code is designed to help increase the adoption of open hardware by making documentation easier to generate, and to allow the relationships between other documents to be automatically visualized using a common diagramming framework from systems engineering.

This code is under development: as of March 20, 2023, text can be extracted from hardcoded URLs, topics are automatically generated for the logical divisions of content within the retrieved text, and the divisions organized accordingly into nodes that can be outputted into a diagram. The linking is still being worked on; it will be repaired in the next version.

![OpenAccelerator Demo](https://github.com/terranexum/OpenAccelerator/blob/main/viewer/openviewer/src/assets/OpenAccelerator_v1.jpg)

## Usage Example

Say that you would like to understand how a computer system is built. There are different documents, each written by different people, but all describing one or more topics about computer memory, processors, solid state drives, graphics cards, etc. There is also a summary document describing the different parts of a computer system.

Instead of having a hundred pages of documentation to look through, it would be much more efficient to have a single diagram that provides a navigable interface to explore the rest of the content within the hundred pages of documentation. The top-level diagram would be very much a reflection of the summary document, and within that will be clickable nodes to describe the subsystems (memory, processors, storage, etc). Clicking on any subsystem will take you to a diagram about that subsystem which lists its components, and so on.

## Advantages 

How OpenAccelerator accelerates open hardware documentation upkeep, comprehensibility, and usability:

1. Whenever there is a change to any portion of the hundred pages, or when documentation is added or removed, the diagram can be updated and the connections refreshed.
2. If you want to change your storage from a magnetic hard drive to a solid state hard drive, a ton of documentation rework will not be necessary. Just replace the magnetic hard drive documentation with solid state hard drive documentation and refresh the diagram.
3. To extend your computer system for use with other systems, say, monitors, keyboards, etc., you can take the documentation for the diagrams of both systems and generate a super-diagram describing the combination of the two systems.

## How to Install

### Installing OpenAccelerator

There are several dependencies that can all be installed with `pip`. A `requirements.txt` file will be generated soon so that everything can be installed at one time instead of separately. There may be more dependencies than those listed below; these are described in `src/run.py`.

* pip install spacy
* pip install pdfminer.six # to replace pdftotext in textract
* pip install textract
* python -m spacy download en_core_web_sm
* pip install python-dotenv
* pip install sentence_transformers
* pip install seaborn
* pip install bs4
* pip install pillow

Also be sure to set up an `.env` file with the `DIR_PATH` variable going to the `io` folder.

`EX1_PATH` and `EX2_PATH` are examples which are the folder names inside `io`. These paths can be edited as needed at the very bottom of `src/run.py`. Right now, both these paths output to two different folders within `io/examples` which will need to be created if these are not already present. 

Running `python run.py` from the `src` folder will allow OpenAccelerator to retrieve the information at the page provided - both text and images obtained from HTML, to be stored in the `io` folder. Right now the images are not being handled after download, just the text. PDF files are also possible to read, but downloading and reading PDFs has not been tested yet, just opening PDFs from the `io/input` folder.

The code generates a JSON output in the `io/output` folder that needs to be saved as `data.json` in `viewer/openviewer/src/assets` before the diagram can be viewed and navigated. 

Nodes are created from relevant descriptions in a file, depending on how related the descriptions are. Multiple `.txt` files saved to the same `io` folder have not been tested to see if they would generate a combined document, but this would be a good feature in the future. This would allow documentation to be retrieved from multiple webpages that may describe individual components, and the text from these documents can be downloaded into `io/input` so that an overarching diagram describing individual components can be regenerated upon request. 

### Installing OpenViewer

Make sure you have Node.js installed. Then go to the `viewer` folder and do `npm install`

Run the following command to go into the `openviewer` directory:
  `cd openviewer`

To start a development live-reload server:
  `npm run dev`

To create a production build (in `./build`):
  `npm run build`

To start a production HTTP/2 server:
  `npm run serve`

## Installation Notes

No action is needed here; this is additional information in case changes need to be made.

The `viewer` folder contains a folder called `openviewer` that was created with the following command:

`npx preact-cli create default openviewer`

After this command was run, in the `package.json` belonging to `openviewer`, the text `NODE_OPTIONS=--openssl-legacy-provider` needed to be removed from `scripts/build` and `scripts/dev`.

## How to Use the OpenViewer

To zoom in on really large diagrams, use the navigation window on the lower left of the screen.  Mousing oer it and using the scroll wheel to zoom has been tested.

This code is still under development, thus, the text in each diagram node is not in the correct logical groupings just yet. Also, diagram nodes do not presently allow the text at right to be highlighted, although when clicking on the text at the right, the reverse is true.

## How to Contribute

To contribute to this repository, you can follow these steps:

1. Fork the repository by clicking on the "Fork" button in the top right corner of this page.
2. Clone the forked repository to your local machine using Git.
3. Make changes and improvements to the codebase as needed. If you're not sure where to start, check out the "Issues" tab to see if there are any open tasks that need attention.
4. Test your changes to make sure they are working as expected.
5. Commit your changes with descriptive commit messages.
6. Push your changes to your forked repository.
7. Create a pull request (PR) to the original repository to merge your changes back in. Be sure to include a detailed description of the changes you made and why they are important.

## Free and Open Source

This is an open source project released under the Apache 2.0 license. A license file will be added in the near future. Collaborators and derivative projects are welcomed. 