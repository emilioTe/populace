# populace
SQL generator to populate a test database based on your own schema.. and some decorators.

## Requirements
* [python](http://python.org)

Note: This was tested against python 2.7 so YMMV. If you have an issue, submit it.

## Usage
    populace.py [-h] [-v] -i INPUT_FILE [-o OUTPUT_FILE] [-r RECORDS]

Note: The .sql file created will require that your database user have the following permissions:
* DROP
* INSERT
* CREATE

## Quick Start
If you already have a schema you'd like to use for your tables, you're golden. All you need to do next is add a few decorators. Easy-peasy!

Okay, let's say you have this schema(1):

    CREATE TABLE Users (
    id int auto_increment,
    email varchar(60) not null unique,
    password varchar(128) not null,
    firstname varchar(20) not null,
    joined_on datetime not null,
    primary key (id)
    );

Now that's a sexy schema, but you're looking for the meat and potatoes. Let's eat!

    CREATE TABLE Users (
    id int auto_increment,
    email varchar(60) not null unique @email,
    password varchar(128) not null @password,
    firstname varchar(20) not null @first_name,
    joined_on datetime not null @datetime,
    primary key (id)
    );

And just like that we've given the app enough to generate our SQL! Now you only need run the script:

    populace.py -i schema.sql -o ready.sql -r 30

Bam! You have an SQL file that's ready to be imported into your database.

(1) The example uses MySQL, but you're free to use whatever relational database you want.

## Decorators
Now here's the nifty part. Those decorators that you used in your schema.. they're not builtin. "Wait. What?!" Yep, you heard me right. Those decorators are dynamically generated from the text files included in the `lists` folder. When you see one that you want, simply add @filename (sans-extension) to your schema.

### Custom Decorators
Are you wondering if it's possible to make your own decorators? If so, I have a short answer for you: YES! "Well, well. How do I go about that, good sir?" By following these simple guidelines:

* Each value must be on its own line
* Filenames cannot contain spaces

If you're still confused, look at the files in the `lists` folder.

There is another caveat: if the number of records you want is greater than the number of values in that file you will get slapped with an exception. Since that's the case I would recommend adding at least 1000 values to your decorator file.

TL;DR

    records > custom_values = exception

## License
Copyright (C) 2012 Emilio Testa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
