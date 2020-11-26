# CV Generator

This python program generates a cv using the library fpdf, using a json file to store the personal information. The advantage of this is mainly the separation between data and representation, and being able to modify the CV easily

## Requeriments
The generator requires the installation of the following libraries in order to work:
- _fpdf_ for the pdf generation primitives
- _pillow_ for the logos of the companies
- A valid data file with the name _cv-data.json_  inside the directory _config_. Explanation of the structure of this file in the section "Structure of the file cv-data.json"
- Logos of the previous employers in the directory _config/logos_. These logos must use .png format and have a recommended width of 84 pixels. Their name must be the id of each employer, i.e: _microsoft.png_

## Execution of the program
We can execute the program running the following command:

```
python generate-cv.py [Company name]
```

It will generate a CV in pdf format, in the root directory of the project. The company name is used for the generation of the customized company text, but the parameter can be ignored when the program is executed.

## Structure of the file cv-data.json
The specification of the fields in the _cv-data.json_ is as follows:

Field path | Explanation
--- | ---
hola | quease

## Configuration of the fonts
