# kanji-test-maker

This can be deployed to a gunicorn docker image for 'production'.

In dev, run:

     python main.py

 If the SQLLite DB is not there, you can build it with

     flask db Migrate
     flask db upgrade

This project uses PyBabel for translation. If you add any new strings please make sure to run

    pybabel extract -F babel.cfg -o messages.pot  --input-dirs=.
    pybabel update -i messages.pot -d translations -l ja

and
    pybabel compile -d translation

top implement the translations
