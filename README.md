# OpenAccelerator

This Python code is designed to help increase the adoption of open hardware by making documentation easier to generate, and to allow the relationships between other documents to be automatically visualized using a common diagramming framework from systems engineering.

This code is under development: as of March 15, 2023, text can be extracted from a PDF, topics automatically generated for the logical divisions of content within the PDF, and the divisions organized accordingly into nodes that can be outputted into a diagram. The diagram will likely be generated using Mermaid, which can allow GitHub to render the navigable diagrams.

## Usage Example

Say that you would like to understand how a computer system is built. There are different documents, each written by different people, but all describing one or more topics about computer memory, processors, solid state drives, graphics cards, etc. There is also a summary document describing the different parts of a computer system.

Instead of having a hundred pages of documentation to look through, it would be much more efficient to have a single diagram that provides a navigable interface to explore the rest of the content within the hundred pages of documentation. The top-level diagram would be very much a reflection of the summary document, and within that will be clickable nodes to describe the subsystems (memory, processors, storage, etc). Clicking on any subsystem will take you to a diagram about that subsystem which lists its components, and so on.

## Advantages 

How OpenAccelerator accelerates open hardware documentation upkeep, comprehensibility, and usability:

1. Whenever there is a change to any portion of the hundred pages, or when documentation is added or removed, the diagram can be updated and the connections refreshed.
2. If you want to change your storage from a magnetic hard drive to a solid state hard drive, a ton of documentation rework will not be necessary. Just replace the magnetic hard drive documentation with solid state hard drive documentation and refresh the diagram.
3. To extend your computer system for use with other systems, say, monitors, keyboards, etc., you can take the documentation for the diagrams of both systems and generate a super-diagram describing the combination of the two systems.

## Instructions

Any file that is placed in the io/input directory will be used to generate a navigable digaram as output, where the key topics in the different files are extracted and linked together by how related they are. 

Documents can consist of plain text or PDFs; if downloaded from the web, these can even be in HTML format. 

In the future, documentation can be retrieved from webpages and downloaded into io/input so that the diagram can be regenerated upon request. 

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

This is an open source project. Collaborators and derivative projects are welcomed. No license is needed to use or share the information in this repository as you wish. 
