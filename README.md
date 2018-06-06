# Intelligems Url Shortener

This is a test project.

## Overview

This Django app provides an API for shortening URLs with the following format:

    <scheme>://<host>/<path>

The shortening uses the first letter of the `<path>` to search in a table of
available URLs, for those starting with the same letter.

Choosing the first of the available URL list, a shortened URL is created:

    http://www.example.com/<available_url>
    
If such a correlation is not possible, the app repeats the process with the second 
letter of the `<path>` and so on.

### Example:

Assume as available URL paths the following:

    s, sa, oaf

and the (non-secure, https) host: `http://www.example.com`.

Then:

    input: `https://www.techcrunch.com/some-slug-here-starting-from-s`  
    output: `http://www.example.com/s`

    input: `https://www.techcrunch.com/some-other-slug-here-starting-from-s`  
    output: `http://www.example.com/sa`

    # At this point the available URLs starting with 's' have been used.
    # so the next letter ('o') of the path is used for correlation.
    input: `https://www.techcrunch.com/some-third-long-slug`  
    output: `http://www.example.com/oaf`


## Install

1. Copy the contents of the `env.example` file into a file named `.env` 
and fill the environmental variables accordingly (follow the guideline 
of the `env.example` file).

2. Create and activate a virtual environment with Python 3 and install 
the project requirements in it:

        pip install -r requirements.txt
        
3. Apply the database migrations:

        ./manage.py migrate
        
4. For the population of the database with the initial provided available
URLs, a management command has been created (can be found at 
`intelligems/url_shortener/management/commands/populate_db.py` and needs the
 file `initial_resources/wordlist.txt` at the root of the project.):
 
        ./manage.py populate_db
        
    *This takes some time, so grab some refreshment* 
    
5. Start the server:

        ./manage.py runserver
        
        
#### Run Tests:
 
 To run the unittests, execute the following:
 
    ./manage.py test


## API

The app makes the following endpoint available:

|    Endpoint    | Method |   Description    | 
|:--------------:|:------:|:----------------:|
| /url_shortener |  POST  |  Shortens a URL  |

#### Codes

| Code  |           Description              |
|:-----:|:----------------------------------:|
|  200  | Url Already Succesfully Shortened. |
|  201  | Url Succesfully Shortened.         |
|  400  | Bad Request: Url invalid/malformed.| 
|  409  | Conflict: Url cannot be shortened. |

### Shorten a URL process:

**Request:** 

    POST http://localhost:8000/url_shortener
    
with payload:
    
    { 'url': 'http://www.some-host.com/a_path_slug' }
    
**Response:**

    {
        "message": "The url has been succesfully shortened!",
        "url": "http://www.some-host.com/a_path_slug",
        "shortened_url": "http://www.example.com/a"
    }