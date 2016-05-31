# Relational databases and SQL basics: Part 1

A relational database contains a number of tables consisting of rows and
columns. Each row in the table represents some entity, with each column giving
information about that entity. For example, let's take on the data storage
needs of an imaginary news organization. A news organization might need to keep
track of all the writers they have on staff. We'll create a "writers" table
to hold this information:

| name | title | start_year |
| ---- | ----- | ---------- |
| Gabriella McCullough | reporter | 2009 |
| Steven Kennedy | drama critic | 2012 |
| Jalen Shaara | columnist | 2002 |

... and then a table of articles that those writers are responsible for:

| author | title | published_date |
| ------ | ----- | -------------- |
| Gabriella McCullough | Man, opossum reach garbage accord | 2015-07-01 |
| Steven Kennedy | "The Deceit of Apricot" opens to rave reviews | 2015-07-15 |
| Jalen Shaara | What's the Big Data? Why I'm a data skeptic | 2015-07-16 |
| Gabriella McCullough | Traffic signals restored on Tunguska Ave | 2015-07-01 |

Looks pretty okay so far! You can easily imagine using this data for any
number of purposes: to generate the home page of the publication; to do
metric evaluations on employee performance; to do text analysis on article
titles, etc.

The decisions you make about how to separate your data into tables, and how to
decide what columns to put into those tables, is called the database *schema*.
The schema above isn't an okay start, but has some problems---which we'll
discuss as the tutorial progresses.

## Relational database management software (RDBMS)

The concept of the "relational database" stretches back many decades, and over
the years a number of programmers and vendors have made available software that
implements the basic idea. The most popular that you're likely to come across:

* MySQL, an open-source RDBMS widely used in web applications
* Oracle and Microsoft's SQL Server, enterprise-grade software used in large
organizations
* SQLite, a tiny, embeddable RDMBS that you can include in essentially any
  application (the Python standard library includes a SQLite module)
* PostgreSQL, another open-source RDBMS

If you're developing an application from scratch, it can be tricky to decide
which RDBMS to use. There are many criteria that might play into your decision
(such as: How much does it cost? How does it perform with large amounts of
data? How does it perform with a large number of users?). (If you're working
with an existing database (say, a database already present in your
organization), you'll just have to learn to work with what you're given.)

In this tutorial, we're going to use PostgreSQL (sometimes called "Postgres"
for short). It's freely available, open-source software that strikes a good
balance between ease of use and being usable at serious scale.

For the remainder of this tutorial, I'm going to assume that you're using
OS X and you've installed Postgres.app on your local machine. You can easily
install PostgreSQL on other operating systems; on Linux it should be as easy
as using your package manager. If you're having trouble, let me know and I can
help you out!

## SQL

Although the details of how any given RDBMS stores its data can differ wildly,
nearly every RDBMS you use supports one computer language for data input and
data access: SQL.  SQL ("Structured Query Language," often pronounced as
"sequel" and sometimes by naming its initials) is a language that is
*specifically built* for specifying and retrieving combinations of rows and
columns from relational data. It's an extraordinarily powerful language, and
of what follows in this tutorial is learning how SQL works and what it looks
like.

In the same way that you can write HTML and have it appear basically the same
way on every web browser, you can write SQL and expect it to behave more or
less the same in every RDBMS. Or, at least, that's the ideal. But beware: every
RDBMS has slightly different rules for how to write SQL, and even if you're an
expert with one RDBMS, it can be non-trivial to learn how to work with another
one. This tutorial shows how to use PostgreSQL, and the concepts shown here
should carry to any other system. But if you do end up using another RDBMS, be
aware that you may need to consult the documentation for that RDBMS and fiddle
around with the syntax.

###A quick taste

Here's a little preview of how SQL works. Here are the tables of data that we
created above for our imaginary news organization:

| name | title | start_year |
| ---- | ----- | ---------- |
| Gabriella McCullough | reporter | 2009 |
| Steven Kennedy | drama critic | 2012 |
| Jalen Shaara | columnist | 2002 |

... and then a table of articles that those writers are responsible for:

| author | title | published_date |
| ------ | ----- | -------------- |
| Gabriella McCullough | Man, opossum reach garbage accord | 2015-07-01 |
| Steven Kennedy | "The Deceit of Apricot" opens to rave reviews | 2015-07-15 |
| Jalen Shaara | What's the Big Data? Why I'm a data skeptic | 2015-07-16 |
| Gabriella McCullough | Traffic signals restored on Tunguska Ave | 2015-07-01 |

The SQL commands for creating these tables in the database looks like this:

    create table reporters (name varchar(80), title varchar(80), start_year int);

    create table articles (author varchar(80), title varchar(140), published_date date);

The SQL commands for populating those tables with data looks like this:

    insert into reporters (name, title, start_year) values
        ('Gabriella McCullough', 'reporter', 2009),
        ('Steven Kennedy', 'drama critic', 2012),
        ('Jalen Shaara', 'columnist', 2002);

    insert into articles (author, title, published_date) values
        ('Gabriella McCullough', 'Man, opossum reach garbage accord', '2015-07-01'),
        ('Steven Kennedy', '"The Deceit of Apricot" opens to rave reviews', '2015-07-15'),
        ('Jalen Shaara', 'What''s the Big Data? Why I''m a data skeptic', '2015-07-16'),
        ('Gabriella McCullough', 'Traffic signals restored on Tunguska Ave', '2015-07-01'); 

Here are some example queries we can run on the data, along with their results.
To get a list just of reporter's names:

    select name from reporters;

            name         
    ---------------------
    Gabriella McCullough
    Steven Kennedy
    Jalen Shaara

To find out how many articles a particular writer has written:

    select count(title) from articles where author = 'Gabriella McCullough';

    count 
    -------
        2

To get a list of articles and authors, along with the titles of those authors:

    select articles.author, reporters.title, articles.title
        from articles
        join reporters on reporters.name = articles.author;

        author        |    title     |                     title                     
    ---------------------+--------------+-----------------------------------------------
    Gabriella McCullough | reporter     | Traffic signals restored on Tunguska Ave
    Gabriella McCullough | reporter     | Man, opossum reach garbage accord
    Steven Kennedy      | drama critic | "The Deceit of Apricot" opens to rave reviews
    Jalen Shaara        | columnist    | What's the Big Data? Why I'm a data skeptic

It's like magic! 

## Clients, servers and `psql`

An RDBMS generally runs on a computer in the background, as a long-running
process (or "daemon"). This process listens on the network for incoming
requests, and then delivers responses to those requests. Software that operates
in this manner is often called "server" software. When we talk about the
"PostgreSQL server," we're specifically talking about the *software* running
on the computer. (In the case of this tutorial, you'll be running that server
software on your own computer. In the "real world," organizations will often
dedicate an entire computer, or cluster of computers, to the task of running
this software.)

Software that makes requests to and interprets responses from a server is
called "client" software. You can write SQL client software in any number
of languages (we'll see how to use Python for this purpose in a bit), but
there's one piece of client software that we'll be using a lot for learning
how to use SQL and PostgreSQL: `psql`. You can think of `psql` as being a
kind of "interactive shell" (like IPython) for SQL requests. You run `psql` and
type in a query; `psql` sends that query to the server and then displays the
response. It's a convenient way to experiment with SQL.

There are two different kinds of command you can type into `psql`: SQL
statements and `psql` "meta-commands." The "meta-commands" are for doing things
specific to the `psql` interactive shell---tasks that are outside the purview
of SQL proper, like setting the format of the input, or listing available
tables. Meta-commands always begin with a backslash (`\`).

## Using PostgreSQL

We know enough now to get started. First, run `Postgres.app` on your
computer by double-clicking on its icon. This is the Postgres "server"; as
long as it's running, you can connect to it with client software and make
requests. (You can stop the server by quitting the app: go to the elephant icon
in your menu bar and select "Quit.")

Postgres.app provides an easy way to launch the `psql` tool: simply click on
the elephant icon in the menu bar and select "Open psql." It'll open up a
Terminal window with `psql` already running. You should see something like
this:

![screenshot](http://static.decontextualize.com/snaps/psql_screen.png)

###Importing data

For the purposes of this tutorial, I'm going to have you *import* some data 
into your database. In particular, we're going to use data from the [MONDIAL project](http://www.dbis.informatik.uni-goettingen.de/Mondial/), which is a
database of geographical facts gleaned from various freely available sources.
There are a number of ways to get data into a relational database; conveniently, MONDIAL makes their database available in SQL format. Download the [statements
for the table schemas here](http://www.dbis.informatik.uni-goettingen.de/Mondial/OtherDBMSs/mondial-schema-postgresql-2010.sql) and [the statements to insert the data here](http://www.dbis.informatik.uni-goettingen.de/Mondial/OtherDBMSs/mondial-inputs-postgresql-2010.sql). Remember where you put these files!

To import the data into PostgreSQL, start `psql` as described in the previous section. Type the following command at the `psql` prompt:

    create database mondial;

... and hit Return. This command creates a new "database." A "database," by the
way, is just a name for a collection of tables. Your PostgreSQL server software
can manage multiple databases.) server can contain and manage multiple such
databases.

> Don't forget the semi-colon at the end of the `create` line! Every SQL
> statement ends with a semi-colon.

You can get a list of all the databases that are currently on your server with
the `\l` meta-command (short for "list"):

    \l

You'll see something that looks like this:

                                    List of databases
    Name    |  Owner  | Encoding |   Collate   |    Ctype    |  Access privileges  
    -----------+---------+----------+-------------+-------------+---------------------
    allison   | allison | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
    mondial   | allison | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
    postgres  | allison | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
    template0 | allison | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/allison         +
            |         |          |             |             | allison=CTc/allison
    template1 | allison | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/allison         +
            |         |          |             |             | allison=CTc/allison

The `postgres` database and the `template` databases (if present) are for
internal PostgreSQL use---you don't need to mess with them. Postgres.app also
creates a "default" database named after your OSX user. You can use this as
"scratch" space for experimentation, or just leave it alone.

Now that you've created the `mondial` database, you need to "connect" to it. To
accomplish this, use the `\c` meta-command like so:

    \c mondial

Once you've connected to a database, you can list the tables in the database
with the `\d` meta-command, like so:

    \d

At this point, you should get an error message saying "No relations found."
Which makes sense---we haven't added any data yet! In order to populate our
database, we're going to import the SQL statements from MONDIAL that we
downloaded earlier. The meta-command for importing SQL statements is `\i`.
You need to give the `\i` meta-command a parameter, which should be the
location of the file you want to import. You'll need to import the `schema`
file first. I downloaded the SQL files from above into my `~/Downloads`
directory, so I might type:

    \i /Users/allison/Downloads/mondial-schema-postgresql-2010.sql

You'll see a whole list of "CREATE TABLE" lines, which acknowledge the fact
that tables have been created. Now you can import the data itself:

    \i /Users/allison/Downloads/mondial-inputs-postgresql-2010.sql 

A bunch of `INSERT 0 1` lines will fly by, one for every record that has been
inserted.

> OSX Pro-Tip: If you drag and drop a file from Finder to a terminal window,
> the path to the file you dropped will be pasted into the program you're
> using. Handy!

Now try using the `\d` meta-command again. You'll see something that looks
like this:

                  List of relations
     Schema |       Name        | Type  |  Owner  
    --------+-------------------+-------+---------
     public | airport           | table | allison
     public | borders           | table | allison
     public | city              | table | allison
     public | cityothername     | table | allison
     public | citypops          | table | allison
     public | continent         | table | allison
     public | country           | table | allison
     public | countryothername  | table | allison
     public | countrypops       | table | allison
     public | desert            | table | allison
     public | economy           | table | allison
     public | encompasses       | table | allison
     public | ethnicgroup       | table | allison
     public | geo_desert        | table | allison
     public | geo_estuary       | table | allison
     public | geo_island        | table | allison
     public | geo_lake          | table | allison
     public | geo_mountain      | table | allison
     public | geo_river         | table | allison
     public | geo_sea           | table | allison
     public | geo_source        | table | allison
     public | island            | table | allison
     public | islandin          | table | allison
     public | ismember          | table | allison
     public | lake              | table | allison
     public | language          | table | allison
     public | located           | table | allison
     public | locatedon         | table | allison
     public | mergeswith        | table | allison
     public | mountain          | table | allison
     public | mountainonisland  | table | allison
     public | organization      | table | allison
     public | politics          | table | allison
     public | population        | table | allison
     public | province          | table | allison
     public | provinceothername | table | allison
     public | provpops          | table | allison
     public | religion          | table | allison
     public | river             | table | allison
     public | riverthrough      | table | allison
     public | sea               | table | allison
    (41 rows)

Awesome work! You've successfully imported some data into your database.

###Examining tables

The `\d` meta-command on its own shows a list of all tables. If you provide
a table name after the `\d`, you'll get a description of just that table.
For example, let's see what's in the `city` table:

    \d city

Here's what you'll see:

                  Table "public.city"
       Column   |         Type          | Modifiers 
    ------------+-----------------------+-----------
     name       | character varying(50) | not null
     country    | character varying(4)  | not null
     province   | character varying(50) | not null
     population | numeric               | 
     latitude   | numeric               | 
     longitude  | numeric               | 
     elevation  | numeric               | 
    Indexes:
        "citykey" PRIMARY KEY, btree (name, country, province)
    Check constraints:
        "citylat" CHECK (latitude >= (-90)::numeric AND latitude <= 90::numeric)
        "citylon" CHECK (longitude >= (-180)::numeric AND longitude <= 180::numeric)
        "citypop" CHECK (population >= 0::numeric)

This shows you what columns are present in the table, and what *data types*
those columns contain. We see above, for example, that the `city` table
has a column called `name` whose type is `character varying(35)`. There's
also a `population` column whose type is `numeric`.

> The `\d` command also displays a list of table *indexes* and *constraints*.
> An index is a way to make a queries on a table faster by storing extra
> information about each record when it's inserted or updated. A constraint is
> an automatic "check" you can set up that ensures any data you put into the
> table meets certain criteria. We're not going to talk about indexes or
> constraints in any detail in this tutorial, but you can read more about them
> in the PostgreSQL documentation.

###Data types

Every column in a table has a *data type*. There are a number of core SQL data
types supported by nearly every RDBMS, and individual vendors may also supply
data types specific to their own software. Some of the most common data types
in SQL are:

| type | description |
| ---- | ----------- |
| `varchar(n)` or `character varying(n)` | a string that is at most *n*
characters long |
| `integer` or `int` | integer numbers |
| `float` | floating-point numbers |
| `numeric` | fractional numbers with a fixed precision |
| `date` | stores a year, month and day |
| `timestamp` | stores a year, month, day, hour, minute, and second |
| `boolean` | either `true` or `false` |

[Here's a full-list of data types supported by
PostgreSQL](http://www.postgresql.org/docs/9.4/static/datatype.html). It's
important to recognize what data types you're working with, since it changes
the way you write queries against the data, and how some features (like
sorting) will behave.

###Writing a query with `SELECT`

Enough with the preliminaries! Let's actually get some data out of the
database. The way you get data out of a SQL table is to write a `SELECT`
statement. The `SELECT` statement allows you to specify (among other things):

* which rows you want
* for the rows selected, which columns you want
* the number of rows to return
* how to sort the rows

The basic syntax for `SELECT` is this:

    SELECT fields
    FROM table
    WHERE criterion
    ORDER BY order_fields
    LIMIT number;

... where:

* `fields` is a comma-separated list of fields that you want to retrieve
* `table` is the name of the table you want to query;
* `criterion` is a SQL expression that determines with rows will be included
  (more on SQL expressions in a bit);
* `order_fields` is a comma-separated list of fields to use as the basis for
  sorting the results (e.g., if you want to sort alphabetically by the `name`
  field, put `name` here); you can optionally include the `DESC` keyword here
  to sort in reverse order.
* `number` is the maximum number of records to return.

The `WHERE`, `ORDER BY` and `LIMIT` lines are all optional: the only thing
you need for a `SELECT` statement is a list of fields and a table. SQL is
also not white-space sensitive; I wrote each clause on a separate line above,
but you're free to include new lines and extra whitespace where you will. You
could also potentially write the whole statement on a single line, if you
wanted to. (Just remember to end the statement with a semicolon.)

> NOTE: This is only a small subset of the `SELECT` statement's capabilities,
> presented for pedagogical purposes only! The actual syntax is [much more
> complicated](http://www.postgresql.org/docs/9.0/static/sql-select.html).

So, for example, let's select the `name` and `population` columns from the
`city` table, displaying only the rows where the value for `population` is
greater than nine million. Type the following query into your `psql` session
and hit return.

    SELECT name, population
    FROM city
    WHERE population > 9000000;

You'll see results that look like this:

       name    | population 
    -----------+------------
     Moskva    |   11979529
     Istanbul  |   13710512
     Guangzhou |   11071424
     Shenzhen  |   10358381
     Wuhan     |    9785388
     Beijing   |   11716620
     Shanghai  |   22315474
     Tianjin   |   11090314
     Karachi   |    9339023
     Mumbai    |   12442373
     Delhi     |   11034555
     Jakarta   |    9607787
     Seoul     |    9708483
     São Paulo |   11152344
    (14 rows)

To order these cities alphabetically, we can add an `ORDER BY` clause:

    SELECT name, population
    FROM city
    WHERE population > 9000000
    ORDER BY name;

Results:

       name    | population 
    -----------+------------
     Beijing   |   11716620
     Delhi     |   11034555
     Guangzhou |   11071424
     Istanbul  |   13710512
     Jakarta   |    9607787
     Karachi   |    9339023
     Moskva    |   11979529
     Mumbai    |   12442373
     Seoul     |    9708483
     Shanghai  |   22315474
     Shenzhen  |   10358381
     São Paulo |   11152344
     Tianjin   |   11090314
     Wuhan     |    9785388
    (14 rows)

To order these cities by descending population:

    SELECT name, population
    FROM city
    WHERE population > 9000000
    ORDER by population DESC;

Results:

       name    | population 
    -----------+------------
     Shanghai  |   22315474
     Istanbul  |   13710512
     Mumbai    |   12442373
     Moskva    |   11979529
     Beijing   |   11716620
     São Paulo |   11152344
     Tianjin   |   11090314
     Guangzhou |   11071424
     Delhi     |   11034555
     Shenzhen  |   10358381
     Wuhan     |    9785388
     Seoul     |    9708483
     Jakarta   |    9607787
     Karachi   |    9339023
    (14 rows)

Finally, to limit our result set to only the top five cities, we can include
the `LIMIT` keyword. Let's change the fields to include the country as well:

    SELECT name, country, population
    FROM city
    WHERE population > 7000000
    ORDER by population DESC
    LIMIT 5;

Results:

       name   | country | population 
    ----------+---------+------------
     Shanghai | CN      |   22315474
     Istanbul | TR      |   13710512
     Mumbai   | IND     |   12442373
     Moskva   | R       |   11979529
     Beijing  | CN      |   11716620

###Exploring tables with `*` and `LIMIT`

Occasionally it's useful to just "take a peek" at the data that's in a table,
without having to specify which columns and rows you want in particular. For
these purposes, you can put a `*` in the field parameter (right after the
word `SELECT`), which will include *all* of the fields in the table in your
search result. Combined with the `LIMIT` clause, you can use this to take
a look at what's in the first few rows of the table `country`:

    SELECT *
    FROM country
    LIMIT 10;

Result:

        name    | code |     capital      |   province    |  area  | population 
    ------------+------+------------------+---------------+--------+------------
     Albania    | AL   | Tirana           | Albania       |  28750 |    2800138
     Greece     | GR   | Athina           | Attikis       | 131940 |   10816286
     Macedonia  | MK   | Skopje           | Macedonia     |  25333 |    2059794
     Serbia     | SRB  | Beograd          | Serbia        |  77474 |    7120666
     Montenegro | MNE  | Podgorica        | Montenegro    |  14026 |     620029
     Kosovo     | KOS  | Prishtine        | Kosovo        |  10887 |    1733872
     Andorra    | AND  | Andorra la Vella | Andorra       |    450 |      78115
     France     | F    | Paris            | Île-de-France | 547030 |   64933400
     Spain      | E    | Madrid           | Madrid        | 504750 |   46815916
     Austria    | A    | Wien             | Wien          |  83850 |    8499759
    (10 rows)

A quick (but, in PostgreSQL, potentially [slow](https://wiki.postgresql.org/wiki/Slow_Counting)) way to count the total number of records in a table is to use
the `count()` aggregate function:

    SELECT count(*) FROM city;

Result:

     count 
    -------
      3375
    (1 row)
    
This tells us that there are 3111 rows in the `city` table. (More on
aggregation below.)

##SQL expressions in WHERE clauses

As we saw in one of the above examples, the `WHERE` clause requires an
expression that returns true or false. Rows in the table for which this
expression is true will be included in the result set; rows for which this
expression evaluates to false will be skipped.

The syntax for SQL expressions is, in general, very similar to the syntax for
writing expressions in (e.g.) Python (the analog for the `WHERE` clause in
Python would be the expression following `if` in a list comprehension). There
are a number of operators which take expressions on either side; these
expressions can be either literals (such as numbers or strings that you type
directly into the query) or column names. If the expression is a column name,
then its value is the contents of that column for the row currently being
evaluated.

The supported operators in SQL are, in some cases, slightly different from
their counterparts in Python. Here are some common SQL operators:

| operator | description |
| -------- | ----------- |
| `>`        | greater than |
| `<`        | less than |
| `>=`        | greater than or equal to |
| `<=`        | less than or equal to |
| `=`        | equal to (note: `=` and not `==`!) |
| `<>` or `!=` | not equal to |

To check to see if a value is `NULL` or missing, use the special expression `IS
NULL` (or, for the converse, `IS NOT NULL`).

> You can also use basic mathematical expressions in SQL, to check if (e.g.)
> the sum of the value in two columns is greater than a particular value.
> [Here's a
> list](http://www.postgresql.org/docs/9.0/static/functions-math.html) of the
> supported mathematical operators in PostgreSQL. 
> 

Here's a quick example of using the `>` operator to find all rows in the `lake`
table with an `area` value of greater than 30000:

    SELECT name, area, depth FROM lake WHERE area > 30000;

Results:

          name       |  area  | depth 
    -----------------+--------+-------
     Ozero Baikal    |  31492 |  1637
     Dead Sea        |  41650 |   378
     Caspian Sea     | 386400 |   995
     Lake Victoria   |  68870 |    85
     Lake Tanganjika |  32893 |  1470
     Great Bear Lake |  31792 |   446
     Lake Huron      |  59600 |   229
     Lake Michigan   |  57800 |   281
     Lake Superior   |  82103 |   405
    (9 rows)

###More sophisticated WHERE clauses with `AND` and `OR`

You can construct more sophisticated expressions in your `WHERE` clauses using
the `AND` and `OR` operators. These work just like their Python counterparts:
on either side, write an expression. If both expressions return true, then
the entire expression with `AND` returns true. If either returns true, then
the entire expression with `OR` returns true.

As a quick example, let's find all of the cities in Finland that meet a
particular level of population. The cities in the `city` table are linked to
their country with a country code in the `country` field. We can determine
what that country code is by running a `SELECT` on the `country` table:

    SELECT name, code FROM country WHERE name = 'Finland';

Results:

      name   | code 
    ---------+------
     Finland | SF

Now we can query the `city` table for Finnish cities:

    SELECT name, country, population FROM city WHERE country = 'SF';

Results:

         name     | country | population 
    --------------+---------+------------
     Mariehamn    | SF      |      10851
     Tampere      | SF      |     220678
     Lahti        | SF      |     103396
     Hämeenlinna  | SF      |      67803
     Kuopio       | SF      |     106475
     Lappeenranta | SF      |      72617
     Kotka        | SF      |      54714
     Rovaniemi    | SF      |      61244
     Mikkeli      | SF      |      54633
     Jyväskylä    | SF      |     134862
     Joensuu      | SF      |      74332
     Oulu         | SF      |     194181
     Pori         | SF      |      83457
     Turku        | SF      |     182154
     Helsinki     | SF      |     614535
     Espoo        | SF      |     261654
     Vaasa        | SF      |      66415
    (17 rows)

Let's say we want to find all Finnish cities with a population of at least 100000 people. We can write that query like so:

    SELECT name, country, population
    FROM city
    WHERE country = 'SF' AND population > 100000;

Results:

       name    | country | population 
    -----------+---------+------------
     Tampere   | SF      |     220678
     Lahti     | SF      |     103396
     Kuopio    | SF      |     106475
     Jyväskylä | SF      |     134862
     Oulu      | SF      |     194181
     Turku     | SF      |     182154
     Helsinki  | SF      |     614535
     Espoo     | SF      |     261654
    (8 rows)

Another example: the `lake` table has a list of lakes, along with (among other
things) their area and depth. Let's say that we want to find a list of Earth's
most ~remarkable lakes~, based on those lakes' depth and area. To get a list of
lakes that are either (a) 500 meters deep or (b) have a surface area of more than 30000 square meters:

    SELECT name, area, depth
    FROM lake
    WHERE depth > 500 OR area > 30000;

Results:

           name       |  area  | depth 
    ------------------+--------+-------
     Dead Sea         |  41650 |   378
     Caspian Sea      | 386400 |   995
     Issyk-Kul        |   6236 |   668
     Lake Toba        |   1103 |   505
     Ozero Baikal     |  31492 |  1637
     Lake Victoria    |  68870 |    85
     Lake Tanganjika  |  32893 |  1470
     Lake Malawi      |  29600 |   704
     Great Bear Lake  |  31792 |   446
     Great Slave Lake |  28568 |   614
     Lake Huron       |  59600 |   229
     Lake Michigan    |  57800 |   281
     Lake Superior    |  82103 |   405
     Crater Lake      |   53.2 |   594
     Lake Tahoe       |    497 |   501
    (15 rows)

##Sums, minimums, maximums and averages

Going back to the MONDIAL database, let's say you wanted to find the population
of the entire world. The `country` table is our best bet for finding this data,
having as it does a `population` field:

    mondial=# SELECT population FROM country LIMIT 10;
     population 
    ------------
        2800138
       10816286
        2059794
        7120666
         620029
        1733872
          78115
       64933400
       46815916
        8499759
    (10 rows)

Presumably, excepting the number of stateless individuals not counted among the
population of a particular country, we could determine the world's population
by adding up all of these numbers. To save us the tedium of writing a program
to perform this task, SQL provides a particular kind of syntax to calculate
sums for all of the values in a field. It looks like this:

	mondial=# SELECT sum(population) FROM country;
	 sum     
	------------
	  6971899367
	(1 row)

The new part here is `sum()`, with the field you want summed between the
parentheses. The `sum()` function is one of several so-called "[aggregate
functions](http://www.postgresql.org/docs/9.4/static/functions-aggregate.html)"
that take the all the values from a field and reduce them down to a single
value. Another such function is `avg()`, which calculates the arithmetic mean
of a column of values:

	mondial=# SELECT avg(population) FROM country;
	          avg          
	-----------------------
	 28573358.061475409836
	(1 row)

You can use a `WHERE` clause with these queries to limit which rows are
included in the aggregate. For example, the following query selects all the MONDIAL cities
in Finland:

	mondial=# SELECT population FROM city WHERE country = 'SF';
     population 
    ------------
          10851
         220678
         103396
          67803
         106475
          72617
          54714
          61244
          54633
         134862
          74332
         194181
          83457
         182154
         614535
         261654
          66415
    (17 rows)

Adding `sum()` around the `population` column yields the sum of just these values from the table:

	mondial=# SELECT sum(population) FROM city WHERE country = 'SF';
	   sum   
	---------
	 2364001
	(1 row)

We already covered another aggregate function, `count()`, which simply counts
the number of rows. To illustrate this with another example, consider the
`encompasses` table, which relates countries to the continents that encompass
them. (Browse this table with a `SELECT * FROM continents` to familiarize
yourself with the structure.) To count the number of countries at least
partially in Europe:

	mondial=# SELECT count(country) FROM encompasses WHERE continent = 'Europe';
	 count 
	-------
	    54
	(1 row)

Finally, the `min()` and `max()` aggregate functions return, respectively, the
minimum and maximum values for the given column. To find the country with the
smallest area, we might issue the following query:

	mondial=# SELECT min(area) FROM country;
	 min  
	------
	 0.44
	(1 row)

To find the are value for the country with the largest largest area:

	mondial=# SELECT max(area) FROM country;
	   max    
	----------
	 17075200
	(1 row)

The two queries can be combined into one:

	mondial=# SELECT min(area), max(area) FROM country;
	 min  |   max    
	------+----------
	 0.44 | 17075200
	(1 row)

###SELECTs with aggregate functions are different

We had been using the `SELECT` statement before as, essentially, a way to
filter and order rows from a table based on their characteristics. So you may,
at this point, notice that `SELECT` statements that include aggregate functions
operate differently from their counterparts without any aggregate functions.
Although the results of the query are returned in a tabular format, the "rows"
and "columns" in the result don't correspond to rows and columns in the
original table. (E.g., there is no column in the `country` table called `min`
and `max`; these appear only in the results of a query using those aggregate
functions.)

I bring this up because it's worth pointing out that `SELECT` with aggregates
is a little bit counterintuitive. Personally, I wish that the syntax made this
a bit clearer; everyone would benefit if, in order to use aggregate functions,
you had to use a separate statement (like `AGGREGATE table CALCULATE min(x)`
or something like that, sort of like [how MongoDB does
it](http://docs.mongodb.org/manual/reference/method/db.collection.aggregate/)).
But that's not the way SQL works, and so we close our eyes, take a deep breath,
and entrust ourselves to the solutions and abstractions so carefully invented
by the standards-makers of government and industry.

###Aggregating with `GROUP BY`

There's a particular pattern for using aggregate function that happens over and
over frequently enough that there is a special syntax for it: grouping. To
illustrate, consider the following task: we want to find the population number
for the largest city in each country, using the data in the `city` table. We
already know how to do this for individual countries, in separate queries; here
are two such queries for the US and Finland:

	mondial=# SELECT max(population) FROM city WHERE country = 'USA';
	   max   
	---------
	 8405837
	(1 row)
	
	mondial=# SELECT max(population) FROM city WHERE country = 'SF';
	  max   
	--------
	 614535
	(1 row)

If we wanted to do this with *every* country present in the `city` table, we'd
have a little programming task on our hands: find all of the unique countries,
iterate through them, issue a query for each, etc. etc. etc. Because this task
is so common, SQL provides a shortcut, which is the `GROUP BY` clause. If you
include a `GROUP BY` clause in your SQL statement, the aggregate that you
specify will be performed *not* on all of the rows that match the `WHERE`
clause, but for all rows having unique values for the column you specify.

For example, the following query calculates the maximum value for the `population` column for every unique country:

    mondial=# SELECT country, max(population) FROM city GROUP BY country;
     country |   max    
    ---------+----------
     NEP     |  1003285
     RA      |  2768772
     CH      |   384786
     L       |    99852
     AMSA    |         
     WD      |    14725
     LB      |  1010970
     BF      |  1475223
    [many rows omitted for brevity]
     MOC     |  1094628
     RO      |  1883425
     SSD     |   372410
     LS      |   227880
     PNG     |   318128
     BZ      |    53532
     SLB     |    49107
     NORF    |         
    (244 rows)

(Some countries have blanks, since apparently there are some countries whose
listed cities all have an empty population field.) This query tells us that,
e.g., the most populous city in Nepal has 1003285 people, that the most
populous city in Argentina (code `RA`) has 2768772 people, etc.

We can clean up the empty rows by using a `WHERE` clause to include as
candidates for aggregation only those cities that have a non-empty `population`
field:

	mondial=# SELECT country, max(population)
	    FROM city
	    WHERE population IS NOT NULL
	    GROUP BY country;
     country |   max    
    ---------+----------
     NEP     |  1003285
     RA      |  2768772
     CH      |   384786
    [many rows omitted for brevity]
     MOC     |  1094628
     RO      |  1883425
     SSD     |   372410
     LS      |   227880
     PNG     |   318128
     BZ      |    53532
     SLB     |    49107
    (211 rows)
	
Queries with `GROUP BY` also allow you to use the `ORDER BY` and `LIMIT`
clauses. Here's an example that sorts the results of the query in alphabetical
order by country, limited to just the first five rows:

	mondial=# SELECT country, max(population)
        FROM city
        WHERE population IS NOT NULL
        GROUP BY country
        ORDER BY country
        LIMIT 5;
    country |   max   
    ---------+---------
    A       | 1761738
    AFG     | 2435400
    AG      |   22219
    AL      |  418495
    AND     |   22256
    (5 rows)

To order by the aggregate field, repeat the aggregate expression in the `ORDER BY` clause:
	
	mondial=# SELECT country, max(population)
        FROM city
        WHERE population IS NOT NULL
        GROUP BY country
        ORDER BY max(population) DESC
        LIMIT 5;
     country |   max    
    ---------+----------
     CN      | 22315474
     TR      | 13710512
     IND     | 12442373
     R       | 11979529
     BR      | 11152344
    (5 rows)

> NOTE: You might think that getting the *name* of the city that has the
> largest population for each country (i.e., the row containing the group-wise
> maximum) would be easy---but, unfortunately, it isn't. [Here's a good overview
> of techniques for performing this task](http://jan.kneschke.de/projects/mysql/groupwise-max/).

Here's another example of `GROUP BY`. Consider the `island` table, which is a list of islands in the world, including their area, height, island group and type:
	
    mondial=# SELECT name, islands, area, elevation, type FROM island LIMIT 10;
           name        |     islands      |  area   | elevation |   type   
    -------------------+------------------+---------+-----------+----------
     Svalbard          | Svalbard         |   39044 |      1717 | 
     Greenland         |                  | 2175600 |           | 
     Iceland           |                  |  102829 |      2119 | volcanic
     Aust-Vagoey       | Lofotes          |     526 |      1146 | 
     Streymoy          | Faroe Islands    |     373 |       789 | 
     Ireland           | British Isles    |   84421 |      1041 | 
     Great Britain     | British Isles    |  229850 |      1344 | 
     Shetland Mainland | Shetland Islands |     970 |       449 | 
     Orkney Mainland   | Orkney Islands   |     492 |       271 | 
     South Ronaldsay   | Orkney Islands   |      50 |       118 | 
    (10 rows)

The `type` field has a few distinct values:

	mondial=# SELECT DISTINCT(type) FROM island;
	   type   
	----------
	 
	 coral
	 volcanic
	 atoll
	 lime
	(5 rows)

So, let's find the *average area* of islands belonging to each island type:

	mondial=# SELECT type, avg(area) FROM island GROUP BY type;
       type   |          avg          
    ----------+-----------------------
              |    41736.819473684211
     coral    |  211.7166666666666667
     volcanic | 9369.1248863636363636
     lime     |  298.6000000000000000
     atoll    |   64.5671428571428571
    (5 rows)

Volcanic islands are awful big, aren't they?

> EXERCISE: Find the island group (i.e., the `islands` field in the `island`
> table) with the greatest average height.

###Filter aggregations with `HAVING`

We saw above that the `WHERE` clause can be used to restrict which rows are
used when calculating an aggregate. But what if we want to restrict which rows
are present *in the response to the aggregate query* itself? It's not
difficult, but it does require a discussion of a previously undiscussed clause:
`HAVING`.

To illustrate the problem, consider the `river` table. This table has a list of
rivers, which includes the river's name and its outlet, which is either a sea,
a lake, or another river (or possibly none of these, in the case of rivers in
endorheic basins). Here's what the table looks like:

	mondial=# SELECT name, river, lake, sea FROM river LIMIT 10;
            name         |  river  |  lake   |      sea       
    ---------------------+---------+---------+----------------
     Thjorsa             |         |         | Atlantic Ocean
     Joekulsa a Fjoellum |         |         | Greenland Sea
     Glomma              |         |         | Skagerrak
     Lagen               | Glomma  |         | 
     Goetaaelv           |         |         | Kattegat
     Klaraelv            |         | Vaenern | 
     Umeaelv             |         |         | Baltic Sea
     Dalaelv             |         |         | Baltic Sea
     Vaesterdalaelv      | Dalaelv |         | 
     Oesterdalaelv       | Dalaelv |         | 
    (10 rows)

These results show that, e.g., the [Thjorsa
river](https://en.wikipedia.org/wiki/%C3%9Ej%C3%B3rs%C3%A1) empties into the
Atlantic Ocean, while the [Klaraelv
river](https://en.wikipedia.org/wiki/Klar%C3%A4lven) empties into a lake named
"Vaenern."

Let's say we're interested in knowing exactly how many rivers empty into all of
the known seas. We could find this out by issuing a query that counts the
rivers, grouped by the name of the sea:

	mondial=# select sea, count(name) from river group by sea;
            sea        | count 
    -------------------+-------
                       |   157
     Persian Gulf      |     1
     Malakka Strait    |     1
     Atlantic Ocean    |    24
     Greenland Sea     |     1
     Barents Sea       |     3
     Arabian Sea       |     1
     Pacific Ocean     |     4
     Arctic Ocean      |     1
     The Channel       |     1
     Mediterranean Sea |     9
     Black Sea         |     4
     Sea of Okhotsk    |     1
     South China Sea   |     1
     Gulf of Bengal    |     1
     East China Sea    |     1
     Hudson Bay        |     1
     Yellow Sea        |     1
     Bering Sea        |     1
     Gulf of Mexico    |     2
     Caribbean Sea     |     2
     Indian Ocean      |     4
     Kara Sea          |     2
     Sea of Azov       |     1
     Kattegat          |     1
     North Sea         |     5
     Andaman Sea       |     2
     Skagerrak         |     1
     East Sibirian Sea |     3
     Baltic Sea        |    11
    (30 rows)

This is fine, but it has a lot of noise! What if we wanted to get this list of
results, but *exclude* the rows that have a count of one or less. Is this
possible? If so, how?

The first way you might attempt to solve this would be with the `WHERE` clause.
That's what `WHERE` is for, after all, right? To exclude records from a query.
Let's try it:

	mondial=# SELECT sea, count(name) FROM river WHERE count(name) > 1 GROUP BY sea; 
	ERROR:  aggregate functions are not allowed in WHERE
	LINE 1: select sea, count(name) from river where count(name) > 1 gro...
	                                                 ^

Hmm. Weird. Apparently, and I quote, "aggregate functions are not allowed in
`WHERE`." It turns out that the `WHERE` clause can only be used to filter rows
*before* the aggregation operation happens---not afterward. To filter rows in
the aggregation, there's a different clause, (confusingly, IMO) called
`HAVING`. The `HAVING` clause works like this:

	mondial=# SELECT sea, count(name) FROM river GROUP BY sea HAVING count(name) > 1;
	        sea        | count 
	-------------------+-------
	                   |   130
	 Atlantic Ocean    |    24
	 Barents Sea       |     3
	 Pacific Ocean     |     3
	 Arctic Ocean      |     2
	 Mediterranean Sea |     8
	 Black Sea         |     3
	 Gulf of Mexico    |     2
	 Caribbean Sea     |     2
	 Indian Ocean      |     4
	 North Sea         |     5
	 Sibirian Sea      |     5
	 Andaman Sea       |     2
	 Baltic Sea        |    11
	(14 rows)

The `HAVING` clause looks just like a `WHERE` clause, except that it can refer
only to fields that are present in the aggregation (in this case,
`count(name)`).  As you can see, by including the `HAVING` clause in this
query, we've excluded results where the aggregation function didn't meet a
certain criterion. Perfect!

Let's do another example. The `religion` table is a list of records that relate
religions to countries. Each country has several records in the table, and each
record indicates the percentage of the population that adherents to the given
religion make up in the country. So, for example, this query:

	mondial=# select * from religion limit 10;
     country |        name        | percentage 
    ---------+--------------------+------------
     AL      | Muslim             |         70
     AL      | Roman Catholic     |         10
     AL      | Christian Orthodox |         20
     GR      | Christian Orthodox |         98
     GR      | Muslim             |        1.3
     MK      | Christian Orthodox |       64.7
     MK      | Muslim             |       33.3
     MK      | Roman Catholic     |        0.2
     SRB     | Christian Orthodox |         85
     SRB     | Muslim             |        3.2
    (10 rows)

... shows that in Albania (code `AL`), 70 percent of the country is Muslim, 10
percent is Roman Catholic, and 20 percent is Christian Orthodox.

We'll use this table to find religions that are present in the fewest countries.

	mondial=# SELECT name, count(country) FROM religion GROUP BY name;
                name             | count 
    -----------------------------+-------
     Buddhist                    |    23
     African Methodist Episcopal |     1
     Jehovas Witnesses           |     8
     Ekalesia Niue               |     1
     Jains                       |     1
     United                      |     1
     Mayan                       |     1
     Armenian Apostolic          |     1
     Taoist                      |     1
     Kimbanguist                 |     1
     Coptic Christian            |     1
     Presbyterian                |     2
     New Apostolic               |     1
     Hoa Hao                     |     1
     Catholic                    |     2
     Muslim                      |   115
     Sikh                        |     2
     Church Tuvalu               |     1
     United Church               |     1
     Jewish                      |    17
     Baptist                     |     4
     Episcopalian                |     1
     Christian Congregationalist |     1
     Uniting Church Australia    |     1
     Anglican                    |    17
     Seventh-Day Adventist       |     7
     Confucianism                |     1
     Church of God               |     3
     Cao Dai                     |     1
     Congregational Christian    |     1
     Church Christ               |     1
     Chondogyo                   |     1
     Adventist                   |     1
     Christian                   |    58
     Christian Orthodox          |    29
     Ukrainian Greek Catholic    |     1
     Druze                       |     1
     Methodist                   |     3
     Roman Catholic              |   116
     Mormon                      |     4
     Protestant                  |    91
     Hindu                       |    19
     Bahai                       |     2
     Yezidi                      |     1
    (44 rows)

These results show us that, e.g., Hinduism is present in 19 different
countries; Mormonism is present in 4; Islam is present in 115. Let's add a
`HAVING` clause so that we see *only* the religions that are present in a
single country:

	mondial=# SELECT name, count(country) FROM religion GROUP BY name HAVING count(country) = 1;
                name             | count 
    -----------------------------+-------
     African Methodist Episcopal |     1
     Ekalesia Niue               |     1
     Jains                       |     1
     United                      |     1
     Mayan                       |     1
     Armenian Apostolic          |     1
     Taoist                      |     1
     Kimbanguist                 |     1
     Coptic Christian            |     1
     New Apostolic               |     1
     Hoa Hao                     |     1
     Church Tuvalu               |     1
     United Church               |     1
     Episcopalian                |     1
     Christian Congregationalist |     1
     Uniting Church Australia    |     1
     Confucianism                |     1
     Cao Dai                     |     1
     Congregational Christian    |     1
     Church Christ               |     1
     Chondogyo                   |     1
     Adventist                   |     1
     Ukrainian Greek Catholic    |     1
     Druze                       |     1
     Yezidi                      |     1
    (25 rows)

(Obviously, there are adherents of these religions in more than one country!
Presumably, the `religion` table only has records if the number of adherents is
large enough that it constitutes a percentage of the general population above a
certain threshold.)

Let's make our query a bit more specific and find the religions that only occur
in one country and where that religion's percentage share in the country is
less than 5%. We can do this by filtering the rows first with `WHERE`, like so:

	mondial=# SELECT name, count(country)
	    FROM religion
	    WHERE percentage < 5
	    GROUP BY name
	    HAVING count(country) = 1;
         name      | count 
    ---------------+-------
     Confucianism  |     1
     Jains         |     1
     Cao Dai       |     1
     Church Christ |     1
     Yezidi        |     1
     Mayan         |     1
     Chondogyo     |     1
     Adventist     |     1
     New Apostolic |     1
     Hoa Hao       |     1
     Druze         |     1
     Catholic      |     1
    (12 rows)

The tricky part in this query is the *combination* of `WHERE` and `HAVING`. The
`WHERE` clause tells SQL to exclude any rows where the percentage is less than
5 *before* any aggregation happens. The `HAVING` clause tells SQL to exclude
any rows *after* the aggregation where the result of `count(country)` is not
equal to 1.

##Joins

In this section, we're going to discuss one of the things that makes SQL truly powerful: the ability to create queries that "join" tables together. 

To illustrate, let's tackle one particular task. So far, We've been running up
against a problem pretty consistently with the MONDIAL database, which is this: the
*names* of countries aren't stored in most of these tables---just their "code." When looking at the `city` table, for instance:

	mondial=# SELECT name, country FROM city ORDER BY name LIMIT 10;
           name       | country 
    ------------------+---------
     's-Hertogenbosch | NL
     A Coruña         | E
     Aachen           | D
     Aalborg          | DK
     Aarau            | CH
     Aba              | WAN
     Abadan           | IR
     Abaetetuba       | BR
     Abakaliki        | WAN
     Abakan           | R
    (10 rows)

Unless we happen to have already memorized these codes, we have to look them up one-by-one in the `country` table to find out what they mean:

	mondial=# SELECT name FROM country WHERE code = 'WAN';
	  name   
	---------
	 Nigeria
	(1 row)

That's sort of inconvenient, and it seems like computers should be able to help
with this problem. Isn't there a way to write a query so that each row returned
from the `city` table automatically gets matched up with the `country` that has
the corresponding code?

In fact, there is, and it's called `JOIN`. We'll continue with the
`city`/`country` analogy in a second, but it's a bit easier to demonstrate how
`JOIN` works with some smaller, toy tables first. Recall from Part One our tiny
database for a news organization, which consists of a table for writers:

| name | title | start_year |
| ---- | ----- | ---------- |
| Gabriella McCullough | reporter | 2009 |
| Steven Kennedy | drama critic | 2012 |
| Jalen Shaara | columnist | 2002 |

... and then a table of articles that those writers are responsible for:

| author | title | published_date |
| ------ | ----- | -------------- |
| Gabriella McCullough | Man, opossum reach garbage accord | 2015-07-01 |
| Steven Kennedy | "The Deceit of Apricot" opens to rave reviews | 2015-07-15 |
| Jalen Shaara | What's the Big Data? Why I'm a data skeptic | 2015-07-16 |
| Gabriella McCullough | Traffic signals restored on Tunguska Ave | 2015-07-01 |

Let's say we wanted to produce a *new* table, which consists of a list of
article titles and dates, along with the name of the author, the author's
title, and the author's start year. In other words, we want information from
*both* tables, and we want to automatically *align* that data so that we end up
with the correct title and start year for each author. Basically, what we want
is this:

| article.author | article.title | article.published_date | author.title | author.start_year |
| ------ | ----- | -------------- | --- | --- |
| Gabriella McCullough | Man, opossum reach garbage accord | 2015-07-01 | reporter | 2009 |
| Steven Kennedy | "The Deceit of Apricot" opens to rave reviews | 2015-07-15 |  drama critic | 2012 |
| Jalen Shaara | What's the Big Data? Why I'm a data skeptic | 2015-07-16 | columnist | 2002 |
| Gabriella McCullough | Traffic signals restored on Tunguska Ave | 2015-07-01 | reporter | 2002 |

Essentially, what we've done is taken our "articles" table, and then reshuffled
the "authors" table and glued it on to the right-hand side, making one big
monster table that joins the two together. This is what is meant by a "join"
in relational database parlance.

We're going to solve our country name problem using a join as well, and in the
process, explain the syntax for how joins work in SQL.

###Join in SQL

The syntax of a `JOIN` looks like this:

    SELECT fields
    FROM left_table
    JOIN right_table ON left_field = right_field

... where `fields` is the list of fields that you want, `left_table` is the
table you want to leave alone, and `right_table` is the table you want to
re-arrange and tack on to the left table. The `left_field` and `right_field`
values determine how the joined table will be aligned: the data from `right_table` will be joined to the 

A join consists of two tables, and a field in each table that links the two
together. In the example above, the "link" between the two tables is that the
name of the author in the articles table needs to match the name of the author
in the writers table. For the purposes of naming the countries that each city
is in, the two tables we want to join are `city` and `country`, and the "link"
between them is the country code---which is in the `country` field of the
`city` table, and the `code` field of the `country` table. Here's what the
query looks like:

	mondial=# SELECT city.name, city.population, country.code, country.name
        FROM city JOIN country ON city.country = country.code
        LIMIT 10;
       name   | population | code |  name   
    ----------+------------+------+---------
     Tirana   |     418495 | AL   | Albania
     Shkodër  |      77075 | AL   | Albania
     Durrës   |     113249 | AL   | Albania
     Vlorë    |      79513 | AL   | Albania
     Elbasan  |      78703 | AL   | Albania
     Korçë    |      51152 | AL   | Albania
     Komotini |            | GR   | Greece
     Kavala   |      58790 | GR   | Greece
     Athina   |     664046 | GR   | Greece
     Peiraias |     163688 | GR   | Greece

There's a *lot* going on in this query, and one or two new things other than
the join. So let's take it line by line. Let's start with the middle line:

    FROM city JOIN country ON city.country = country.code

This line says to select from the `city` table (this is the left table of our
join) and join it to the `country` table (the right table). The `ON` clause
tells PostgreSQL how to re-arrange the right-side table. It says, in effect:
for every row in the `city` table, find the row in the `country` table where
the country's `code` field (`country.code`) matches the city's `country` field
(`city.country`).

The dot between the name of the table and the field is something we haven't
discussed yet: when you're naming a field, the dot syntax allows you to specify
*which table* that field is found in. (This is important when the two tables
you're joining have fields with the same name---you need to be able to
disambiguate.) We see the dot again in the first line of the query:

	SELECT city.name, city.population, country.code, country.name

This line specifies *which* fields we want to see. Because we're joining two
tables, we need to be explicit about which table the field we want originates
from. In this query, we're getting the `name` field from the `city` table, the
`population` field from the `country` table, the `code` field from the
`country` table, and the `name` field from the `country` table.

> NOTE: To see what the entire joined table looks like, without any fields
> selected, try the following query: `SELECT * FROM city JOIN country ON
> city.country = country.code LIMIT 10;`

Finally, the `LIMIT 10` line works just like it does with other `SELECT`
statements: it just limits the results to the given number of lines. (You can
remove the `LIMIT` if you want to page through the results in `psql`.)

###Combining `JOIN` with `WHERE` and aggregation

Once you've created a joined table with a `JOIN` clause, you can operate on it
just like any other table---restricting selections with `WHERE` and performing
aggregates with `GROUP BY`. Let's do another example from joining the `city`
and `country` tables. Here's a query that finds every city with a population
over one million people that is found in a country with fewer than five million
people:

	mondial=# SELECT city.name, city.population, country.name,
            country.population
        FROM city JOIN country ON city.country = country.code
        WHERE city.population > 1000000 AND country.population < 5000000;
        name     | population |  name   | population 
    -------------+------------+---------+------------
     Yerevan     |    1066264 | Armenia |    3026879
     Tbilisi     |    1073345 | Georgia |    4483800
     Bayrūt      |    1100000 | Lebanon |    4341092
     Montevideo  |    1318755 | Uruguay |    3286314
     Brazzaville |    1408150 | Congo   |    4001831
     Monrovia    |    1010970 | Liberia |    3957990
    (6 rows)

A great thing about table joins is that we can use `WHERE` to establish
criteria for fields in either the left or right table. If you're having trouble
picturing how this query works, try running it without one of the expressions
in the `WHERE` clause (i.e., leave out `city.population > 1000000` or
`country.population < 5000000`).

The following example combines nearly all of the concepts we've discussed so
far. It finds the sum of the population of cities in the `city` table for all
countries, and then displays those countries having at least 20 million
individuals living in cities.

	mondial=# SELECT country.name, sum(city.population)
        FROM city JOIN country ON city.country = country.code
        WHERE city.population IS NOT NULL
        GROUP BY country.name
        HAVING sum(city.population) > 20000000
        ORDER BY sum(city.population) DESC;
          name      |    sum    
    ----------------+-----------
     China          | 326910749
     India          | 129752758
     Brazil         |  93687185
     United States  |  81816121
     Russia         |  72000673
     Japan          |  48068708
     Mexico         |  47137170
     Indonesia      |  46627466
     Turkey         |  46045206
     Iran           |  32393196
     South Korea    |  32332901
     Pakistan       |  29838311
     Colombia       |  26579496
     Germany        |  25333235
     United Kingdom |  25252422
     South Africa   |  23470701
     Nigeria        |  22757771
     Egypt          |  22364857
    (18 rows)

The tricky part here is the `GROUP BY` clause, which is grouping by a value in
the right table of the join (`country.name`).

##Joining with many-to-many relationships

So far, we've been exercising our table join chops on the `city` and `country`
tables. These two tables have a *many-to-one* relationship: one country can
contain many cities, but a city can only be in one country. It's easy to write
a `JOIN` for a one-to-many relation, since you know that the right-side table
will always have, at most, one matching record.

But the MONDIAL database (along with many other relational database schemas)
has entities that exist in a many-to-many relationship. For example, a river
can flow through multiple countries, and one country can have multiple rivers
flowing through it. Representing many-to-many relationships in SQL is a bit
tricky, and as a consequence, writing `JOIN`s for many-to-many relationships is
tricky as well.

The conventional way to model a many-to-many relationship in a relational database is with a [junction table](https://en.wikipedia.org/wiki/Junction_table) (sometimes also called a "linking table"). A junction table has rows for every instance of relationship between two tables, using a unique key to refer to the rows in those tables.

###Many writers, many articles

To illustrate, let's return to our news organization database. We have a table for writers:

| name | title | start_year |
| ---- | ----- | ---------- |
| Gabriella McCullough | reporter | 2009 |
| Steven Kennedy | drama critic | 2012 |
| Jalen Shaara | columnist | 2002 |

... and then a table of articles that those writers are responsible for:

| author | title | published_date |
| ------ | ----- | -------------- |
| Gabriella McCullough | Man, opossum reach garbage accord | 2015-07-01 |
| Steven Kennedy | "The Deceit of Apricot" opens to rave reviews | 2015-07-15 |
| Jalen Shaara | What's the Big Data? Why I'm a data skeptic | 2015-07-16 |
| Gabriella McCullough | Traffic signals restored on Tunguska Ave | 2015-07-01 |

This schema represents a simple many-to-one relationship: one writer can write
many articles, and every article has exactly one writer. But let's say that one
day, in our news organization, Gabriella McCullough and Steven Kennedy
*collaborate* on an article. How do we represent this in the database?

One option, of course, would simply be to store both of the names in the `author` field:

| author | title | published_date |
| ------ | ----- | -------------- |
| Gabriella McCullough and Steven Kennedy | Theater Chairs Uncomfortable, Experts Warn | 2015-07-28 |

There's a problem with this solution, however, which is that now a query on our database that looks like this:

    SELECT count(*) FROM articles WHERE author = 'Gabriella McCullough';

... no longer functions properly, because it won't include the article where
Gabriella collaborated with Steven. Likewise, it would be difficult to
construct a `JOIN` (like we did in the previous section) that would tell us the
title of all of the authors involved in writing the story. (We'd have to parse
out the names first in order to use them in the query, which is a hassle.)

The issue is that we've discovered that our initial modeling of the data
structure was wrong. There isn't a many-to-one relationship between articles
and writers; instead, there's a many-to-many relationship: a single writer can
write multiple stories, and any given story can be authored by more than one
writer.

To represent this relationship, we need to slightly restructure our database.
First, we'll remove the `author` field from the `articles` table and add a new
field, `article_id`, which is a unique integer assigned to each article:

| article_id | title | published_date |
| ------ | ----- | -------------- |
| 1 | Man, opossum reach garbage accord | 2015-07-01 |
| 2 | "The Deceit of Apricot" opens to rave reviews | 2015-07-15 |
| 3 | What's the Big Data? Why I'm a data skeptic | 2015-07-16 |
| 4 | Traffic signals restored on Tunguska Ave | 2015-07-01 |
| 5 | Theater Chairs Uncomfortable, Experts Warn | 2015-07-28 |

... and then create a new table, which relates author names to the articles
that they've written. We'll store one row for each instance of a relationship
between an author and an article and call it `author_article`:

| author | article_id |
| ------ | ---------- |
| Gabriella McCullough | 1 |
| Gabriella McCullough | 4 |
| Gabriella McCullough | 5 |
| Steven Kennedy | 2 |
| Steven Kennedy | 5 |
| Jalen Shaara | 3 |

This junction table tells us that Gabriella has a byline on articles 1, 4, and
5; Steven has a byline on articles 2 and 5; and Jalen has a byline on article
3. For any article, we could get a list of its authors like so:

    SELECT author FROM author_article WHERE article_id = 5;

Getting a list of titles on which a writer has a byline is slightly more
complicated, and involves a join:

    SELECT article.title
    FROM author_article JOIN article
        ON article.article_id = author_article.article_id
    WHERE author_article.author = 'Gabriella McCullough';

###Rivers and countries

Let's return to the MONDIAL database for an example with real data. As
mentioned above, rivers and countries are in a many-to-many relationship. The
MONDIAL database has a table for countries, and a table for rivers, and a table
called `geo_river` that is the junction table for their many-to-many
relationship. Here's what the table looks like:

	mondial=# SELECT river, country, province FROM geo_river ORDER BY river
	    LIMIT 20;
          river      | country |     province     
    -----------------+---------+------------------
     Aare            | CH      | Bern
     Aare            | CH      | Aargau
     Aare            | CH      | Solothurn
     Adda            | I       | Lombardia
     Akagera         | EAU     | Uganda
     Akagera         | EAT     | Kagera
     Akagera         | RWA     | Rwanda
     Allegheny River | USA     | Pennsylvania
     Allegheny River | USA     | New York
     Aller           | D       | Niedersachsen
     Alz             | D       | Bayern
     Amazonas        | BR      | Amapá
     Amazonas        | BR      | Amazonas
     Amazonas        | BR      | Pará
     Amazonas        | PE      | Loreto
     Amazonas        | CO      | Amazonas
     Ammer           | D       | Bayern
     Amudarja        | AFG     | Afghanistan
     Amudarja        | UZB     | Samarqand
     Amudarja        | UZB     | Qoraqalpogʻiston
    (20 rows)

This result shows us that, e.g., the Amazon river flows through several
different countries. (The `geo_river` table also gives us information on which
*provinces* a river flows through, so we see that the Allegheny wends its way
through both New York and Pennsylvania.)

All well and good so far. Let's exploit the many-to-many relationship to
get information about particular countries and rivers. To find all of the rivers that flow through Finland:

	mondial=# SELECT river, province FROM geo_river WHERE country = 'SF';
         river     |  province  
    ---------------+------------
     Paatsjoki     | Lappia
     Ounasjoki     | Lappia
     Kemijoki      | Lappia
     Oulujoki      | Oulu
     Kymijoki      | Haeme
     Kymijoki      | Kymi
     Kymijoki      | Mikkeli
     Kokemaeenjoki | Haeme
     Kokemaeenjoki | Turku-Pori
     Vuoksi        | Kuopio
     Vuoksi        | Kymi
    (11 rows)

A list of all the countries and provinces that the Rhine runs through:

	mondial=# SELECT river, country, province FROM geo_river WHERE river = 'Rhein';
	 river | country |      province       
	-------+---------+---------------------
	 Rhein | F       | Alsace
	 Rhein | A       | Vorarlberg
	 Rhein | D       | Baden Wurttemberg
	 Rhein | D       | Hessen
	 Rhein | D       | Nordrhein Westfalen
	 Rhein | D       | Rheinland Pfalz
	 Rhein | FL      | Liechtenstein
	 Rhein | CH      | Aargau
	 Rhein | CH      | Basel-Land
	 Rhein | CH      | Basel-Stadt
	 Rhein | CH      | Graubunden
	 Rhein | CH      | Sankt Gallen
	 Rhein | CH      | Schaffhausen
	 Rhein | CH      | Thurgau
	 Rhein | CH      | Zurich
	 Rhein | NL      | Gelderland
	 Rhein | NL      | Zuid Holland
	(17 rows)

This is a bit annoying, since we're seeing the country codes again instead of the country names. In order to get the country name, we need to `JOIN` the junction table with the `country` table to get the country name out.

	mondial=# SELECT geo_river.river, country.name, geo_river.province
        FROM geo_river JOIN country ON geo_river.country = country.code
        WHERE river = 'Rhein';
	 river |     name      |      province       
	-------+---------------+---------------------
	 Rhein | France        | Alsace
	 Rhein | Austria       | Vorarlberg
	 Rhein | Germany       | Baden Wurttemberg
	 Rhein | Germany       | Hessen
	 Rhein | Germany       | Nordrhein Westfalen
	 Rhein | Germany       | Rheinland Pfalz
	 Rhein | Liechtenstein | Liechtenstein
	 Rhein | Switzerland   | Aargau
	 Rhein | Switzerland   | Basel-Land
	 Rhein | Switzerland   | Basel-Stadt
	 Rhein | Switzerland   | Graubunden
	 Rhein | Switzerland   | Sankt Gallen
	 Rhein | Switzerland   | Schaffhausen
	 Rhein | Switzerland   | Thurgau
	 Rhein | Switzerland   | Zurich
	 Rhein | Netherlands   | Gelderland
	 Rhein | Netherlands   | Zuid Holland
	(17 rows)

Let's dig a bit deeper and select rivers based on their characteristics.
We already know how to get a list of names of rivers whose area is greater
than 50000:

    mondial=# SELECT name FROM lake WHERE area > 50000;
         name      
    ---------------
     Caspian Sea
     Lake Victoria
     Lake Huron
     Lake Michigan
     Lake Superior
    (5 rows)

But let's say that we want to know the names of the countries in which these
lakes at least partially lie.  In order to find this, we're going to `JOIN`
this statement to the `geo_lake` table. (The `geo_lake` is a linking table
analogous to `geo_river`, but, naturally, for the location of lakes instead of
the location of rivers.) Here's the query:

    mondial=# SELECT lake.name, geo_lake.country, geo_lake.province
        FROM lake JOIN geo_lake ON lake.name = geo_lake.lake
        WHERE lake.area > 50000;
         name      | country |    province    
    ---------------+---------+----------------
     Caspian Sea   | R       | Kalmykiya
     Caspian Sea   | R       | Astrakhanskaya
     Caspian Sea   | R       | Dagestan
     Caspian Sea   | IR      | Gillan
     Caspian Sea   | IR      | Mazandaran
     Caspian Sea   | IR      | Golestan
     Caspian Sea   | TM      | Balkan
     Caspian Sea   | AZ      | Azerbaijan
     Caspian Sea   | KAZ     | Atyrau
     Caspian Sea   | KAZ     | Mangistau
     Lake Victoria | EAT     | Kagera
     Lake Victoria | EAT     | Mwanza
     Lake Victoria | EAT     | Mara
     Lake Victoria | EAT     | Simiyu
     Lake Victoria | EAT     | Geita
     Lake Victoria | EAK     | Kenya
     Lake Victoria | EAU     | Uganda
     Lake Huron    | CDN     | Ontario
     Lake Huron    | USA     | Michigan
     Lake Michigan | USA     | Illinois
     Lake Michigan | USA     | Indiana
     Lake Michigan | USA     | Michigan
     Lake Michigan | USA     | Wisconsin
     Lake Superior | CDN     | Ontario
     Lake Superior | USA     | Michigan
     Lake Superior | USA     | Minnesota
     Lake Superior | USA     | Wisconsin
    (27 rows)

This join is interesting, since in the act of joining, we actually introduced
*more rows* into the search results. That's what happens when the right table
has more than one row that matches the condition in the `ON` clause.

    Of course, we still have that pesky country code! To get rid of it, we need
    to join *twice*: once on `geo_lake` and again on `country`:
    	
    mondial=# SELECT lake.name, country.name, geo_lake.province
    mondial-# FROM lake
    mondial-# JOIN geo_lake ON lake.name = geo_lake.lake
    mondial-# JOIN country ON country.code = geo_lake.country
    mondial-# WHERE lake.area > 50000;
         name      |     name      |    province    
    ---------------+---------------+----------------
     Caspian Sea   | Russia        | Kalmykiya
     Caspian Sea   | Russia        | Astrakhanskaya
     Caspian Sea   | Russia        | Dagestan
     Caspian Sea   | Iran          | Gillan
     Caspian Sea   | Iran          | Mazandaran
     Caspian Sea   | Iran          | Golestan
     Caspian Sea   | Turkmenistan  | Balkan
     Caspian Sea   | Azerbaijan    | Azerbaijan
     Caspian Sea   | Kazakhstan    | Atyrau
     Caspian Sea   | Kazakhstan    | Mangistau
     Lake Victoria | Tanzania      | Kagera
     Lake Victoria | Tanzania      | Mwanza
     Lake Victoria | Tanzania      | Mara
     Lake Victoria | Tanzania      | Simiyu
     Lake Victoria | Tanzania      | Geita
     Lake Victoria | Kenya         | Kenya
     Lake Victoria | Uganda        | Uganda
     Lake Huron    | Canada        | Ontario
     Lake Huron    | United States | Michigan
     Lake Michigan | United States | Illinois
     Lake Michigan | United States | Indiana
     Lake Michigan | United States | Michigan
     Lake Michigan | United States | Wisconsin
     Lake Superior | Canada        | Ontario
     Lake Superior | United States | Michigan
     Lake Superior | United States | Minnesota
     Lake Superior | United States | Wisconsin
    (27 rows)

This query essentially takes the table resulting from the first join and uses
it as the left table in a *second* join. Tricky! But powerful.

###Aggregates with many-to-many relations

You can use aggregates with junction tables fairly easily. For example, here's
a query that gets the total number of provinces that each river passes through:

	mondial=# SELECT river, count(province)
	    FROM geo_river GROUP BY river
	    ORDER BY count(province) DESC
        LIMIT 10;
      river  | count 
    ---------+-------
     Donau   |    32
     Niger   |    20
     Rhein   |    17
     Tigris  |    16
     Euphrat |    15
     Parana  |    13
     Zaire   |    13
     Volga   |    13
     Dnepr   |    12
     Elbe    |    12
    (10 rows)

And, the other way, the total number of rivers that pass through each province:

	mondial=# SELECT province, count(river)
        FROM geo_river
        GROUP BY province
        ORDER BY count(river) DESC
        LIMIT 10;
         province      | count 
    -------------------+-------
     Bayern            |    10
     Orientale         |     7
     Bandundu          |     7
     Xizang            |     7
     Serbia            |     7
     Katanga           |     7
     Equateur          |     6
     Baden-Württemberg |     6
     South Sudan       |     6
     Amazonas          |     6
    (10 rows)

###DISTINCT and COUNT(DISTINCT ...)

We discussed the `DISTINCT` keyword above when exploring the `island` table's
`type` field. Putting the word `DISTINCT` before a field name causes the query
to return *only the unique values* for the selected field. `DISTINCT` is an
easy way to remove duplicates from results, especially in the cases where
you're querying only on a single field.

As an example, the `ethnicgroup` table has a record that relates countries,
ethnic groups, and the percentage of the country's population that a particular
ethnic group makes up. If you simply wanted a list of *all the ethnic groups in
the world*, the one way to structure the query would be like this:

    mondial=# SELECT name FROM ethnicgroup ORDER BY name LIMIT 10;
      name   
    ---------
     Acholi
     Afar
     Afar
     African
     African
     African
     African
     African
     African
     African
    (10 rows)

This, of course, is showing us not the list of ethnic groups but the list of
ethnic groups as they relate to countries and percentages, which means we'll
see the same group multiple times. The easiest way to get the list of *unique*
ethnic groups is to simply put the word `DISTINCT` before the field in the
query:

    mondial=# SELECT DISTINCT name FROM ethnicgroup ORDER BY name LIMIT 10;
             name         
    ----------------------
     Acholi
     Afar
     African
     African descent
     African-white-Indian
     Afro-Asian
     Afro-Chinese
     Afro-East Indian
     Afro-European
     Albanian
    (10 rows)

The `DISTINCT` keyword can be used in combination with `COUNT` aggregation to
count the number of times a particular value appears in a `COUNT` aggregate. As
an example, consider the query above where we counted the number of provinces
that a particular river runs through:

	mondial=# SELECT river, count(province)
	    FROM geo_river GROUP BY river
	    ORDER BY count(province) DESC
        LIMIT 10;
      river  | count 
    ---------+-------
     Donau   |    32
     Niger   |    20
     Rhein   |    17
     Tigris  |    16
     Euphrat |    15
     Parana  |    13
     Zaire   |    13
     Volga   |    13
     Dnepr   |    12
     Elbe    |    12
    (10 rows)

You might think that you could turn this into a query that finds the number of
*countries* that a river passes through simply by switching the word `province`
to `country`:

    mondial=# SELECT river, count(country)
        FROM geo_river GROUP BY river
        ORDER BY count(country) DESC
        LIMIT 10;
      river  | count 
    ---------+-------
     Donau   |    32
     Niger   |    20
     Rhein   |    17
     Tigris  |    16
     Euphrat |    15
     Parana  |    13
     Zaire   |    13
     Volga   |    13
     Dnepr   |    12
     Elbe    |    12
    (10 rows)

But it returns the same results! The reason is that the linking table has one
entry per *province*, and that row includes the country, so counting the two
has essentially the same result. The easy way to get around this difficulty is
by putting the `DISTINCT` keyword inside the parentheses, which is a special
syntax that allows you to include only the unique values for a particular field
inside of the `COUNT` aggregation. Observe!

    mondial=# SELECT river, count(DISTINCT country)
        FROM geo_river GROUP BY river
        ORDER BY count(DISTINCT country) DESC
        LIMIT 10;
      river  | count 
    ---------+-------
     Donau   |    10
     Rhein   |     6
     Zambezi |     6
     Drau    |     5
     Jordan  |     5
     Mekong  |     5
     Mur     |     4
     Niger   |     4
     Save    |     4
     Limpopo |     4
    (10 rows)

Magic!

##Aliases

To save time and typing, the designers of SQL introduced the concept of the
*alias*. An alias is a way to give a table or column a shorter name inside of a
query, so you have less typing to do. You can also use an alias to change the
name of a column that appears in the output for a query, which can be
especially valuable when working with aggregations.

###Aliasing table names

As an example of where an alias might be useful, consider the query we wrote
earlier that finds cities with large populations in countries with small
populations:

	SELECT city.name, city.population, country.name, country.population
    FROM city JOIN country ON city.country = country.code
    WHERE city.population > 1000000 AND country.population < 5000000;

It seems verbose to write out `city` and `country` so many times. And whenever
something "seems verbose" you can count on programmers having come up with a
way to make it shorter (and maybe a bit more confusing). So, what you can do is
put an `AS` clause after the name of the table in the `FROM`. Elsewhere in the
query, you can now use whatever string you typed after `AS` to refer to the
table, as a kind of shorthand. Here's the same query using `AS`:

    mondial=# SELECT ci.name, ci.population, co.name, co.population
    mondial-# FROM city AS ci JOIN country AS co ON ci.country = co.code
    mondial-# WHERE ci.population > 1000000 AND co.population < 5000000;
        name     | population |  name   | population 
    -------------+------------+---------+------------
     Yerevan     |    1066264 | Armenia |    3026879
     Tbilisi     |    1073345 | Georgia |    4483800
     Bayrūt      |    1100000 | Lebanon |    4341092
     Montevideo  |    1318755 | Uruguay |    3286314
     Brazzaville |    1408150 | Congo   |    4001831
     Monrovia    |    1010970 | Liberia |    3957990
    (6 rows)

You can use whatever you want as an alias (as long as it's a valid [PostgreSQL
identifier](https://www.postgresql.org/docs/current/static/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS),
though in general you'll see a lot of single- and double-character aliases,
often using the first letter (or couple of letters) from the name of the table
being referenced.

If the `AS` keyword is *still* too verbose for you, you can omit it altogether, leaving just the
alias after the table name:

    mondial=# SELECT ci.name, ci.population, co.name, co.population
        FROM city ci JOIN country co ON ci.country = co.code
        WHERE ci.population > 1000000 AND co.population < 5000000;
        name     | population |  name   | population 
    -------------+------------+---------+------------
     Yerevan     |    1066264 | Armenia |    3026879
     Tbilisi     |    1073345 | Georgia |    4483800
     Bayrūt      |    1100000 | Lebanon |    4341092
     Montevideo  |    1318755 | Uruguay |    3286314
     Brazzaville |    1408150 | Congo   |    4001831
     Monrovia    |    1010970 | Liberia |    3957990
    (6 rows)

###Aliasing column names

You can specify aliases for column names as well, using the same syntax. A
column name alias simply changes the text that appears in the column header for
a given field in the query.

    mondial=# SELECT name AS moniker, population AS resident_count
        FROM city
        LIMIT 5;
     moniker | resident_count 
    ---------+----------------
     Tirana  |         418495
     Shkodër |          77075
     Durrës  |         113249
     Vlorë   |          79513
     Elbasan |          78703
    (5 rows)

The functionality is slightly more useful when working with aggregate
functions. To demonstrate, let's return to the following query, which lists
countries along with the population value for the most populous city in the
country:

	mondial=# SELECT country, max(population)
        FROM city
        WHERE population IS NOT NULL
        GROUP BY country
        ORDER BY max(population) DESC
        LIMIT 5;
     country |   max    
    ---------+----------
     CN      | 22315474
     TR      | 13710512
     IND     | 12442373
     R       | 11979529
     BR      | 11152344
    (5 rows)

This query is a bit awkward because we have to write the aggregate function
twice: once in the column list and again in the `ORDER BY` clause.  As an
alternative, you can give the aggregate a column alias, and use that alias in
subsequent clauses:

    mondial=# SELECT country, max(population) as most_people
        FROM city
        WHERE population IS NOT NULL
        GROUP BY country
        ORDER BY most_people DESC
        LIMIT 5;
     country | most_people 
    ---------+-------------
     CN      |    22315474
     TR      |    13710512
     IND     |    12442373
     R       |    11979529
     BR      |    11152344
    (5 rows)

As a perk, using a column alias for the aggregate gives the column a more
descriptive name in the output (without the alias, PostgreSQL uses the name of
the aggregate function as the column name).

##Further reading

* The [PostgreSQL tutorial](http://www.postgresql.org/docs/9.4/static/tutorial.html) is a thoughtful, thorough introduction to PostgreSQL, `psql`, and relational database concepts in general.
* [SQL Teaching](https://www.sqlteaching.com/) has a series of online, interactive tutorials about making queries.
* If you're looking to buy a book, I always recommend O'Reilly's "Head First" series. Here's [Head First SQL](http://shop.oreilly.com/product/9780596526849.do).
* For a different take on all this material, [consult Joshua Lande's excellent series, "What Every Data Scientist Needs to Know about SQL"](http://joshualande.com/data-science-sql/)
* The official PostgreSQL documentation has a [good tutorial on aggregate functions](http://www.postgresql.org/docs/9.4/static/tutorial-agg.html). See also [the list of all supported aggregate functions in PostgreSQL](http://www.postgresql.org/docs/9.4/static/functions-aggregate.html).
* The official PostgreSQL documentation also has an [introduction to the `FROM` clause](http://www.postgresql.org/docs/9.4/static/queries-table-expressions.html#QUERIES-FROM) that covers table joins in some detail.

