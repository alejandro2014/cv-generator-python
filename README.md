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

| Field path | Field type | Explanation |
| --- | --- | --- |
| _$.header_ | object | Header data |
| _$.header.name_ | string | Name and surname(s) of the user |
| _$.header.position_ | string | Position that will be used as a subtitle |
| _$.header.address_ | string | Physical address |
| _$.header.mail_ | string | Email address |
| _$.header.phone_ | string | Phone number |
| _$.header.birth_ | object | Birth data |
| _$.header.birth.place_ | string | Place of birth |
| _$.header.birth.date_ | string | Date of birth |
| _$.header.repo_ | string | Repository with the projects of the user |
| _$.profile_ | object | Introduction of the candidate |
| _$.profile.introduction_ | string | Text of introduction of the candidate to the company |
| _$.experiences_ | array | List of previous experiences. They are no sorted, you choose the order |
| _$.experiences[*]_ | object | Object containing fields of the experience |
| _$.experiences[*].company_ | object | Data of the company |
| _$.experiences[*].company.id_ | string | Id. of the company. **This name must be coincident with the png logo (without the extension)** |
| _$.experiences[*].company.name_ | string | Full name of the company |
| _$.experiences[*].company.location_ | string | Location of the company |
| _$.experiences[*].company.type_ | string | Type of business of the company |
| _$.experiences[*].start_ | integer | Year when the experience begins |
| _$.experiences[*].end_ | integer | Year when the experience ends |
| _$.experiences[*].position_ | string | Explanation of the performed role, projects, type of work, etc |
| _$.experiences[*].technologies_ | array | List of technologies used in the project |
| _$.experiences[*].technologies[*]_ | string | Technology used |
| _$.skills_ | array | List of skills that will be enumerated |
| _$.skills[*]_ | string | Skill as a string |

## Configuration of the fonts
The fonts are located in the file _config/fonts.json_ and the fields are quite self-explanatory, you can configure them here.

## TODO
- Improvement of the layout: Better calculations
- Improvement of the layout: More beautiful document
- Unit testing
- More refactoring
- Better region management
