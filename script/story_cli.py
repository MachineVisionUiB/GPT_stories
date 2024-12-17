import click
from generate_stories import main as generate_stories
from name_extraction import main as extract_names
from noun_phrases import main as extract_noun_phrases
from sentiment_analysis_textblob import main as tb_sentiment
from word_freq import main as word_freq
import csv



@click.group()
def cli():
    pass
    

@cli.command()
@click.argument('countries', nargs=-1, type=str) # country codes or 'all' for all countries
@click.argument('num_story_per_topic', type=int)
@click.option('-s', '--startfrom', type=str, default='', help='Start from a specific country code when generating all')
def generate(countries, num_story_per_topic, startfrom):
    """Generate stories."""
    print("Generating stories...")
    # Read the country codes from the CSV file

    with open ("country_codes.csv", 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader) 
        for line in reader:
            if startfrom != "" and startfrom != line[0]:
                continue

            startfrom = ""
            if line [3] != "":
                country_code = line[0]
                country_name = line[1]
                demonym = line[3]
                if 'all' in countries and len(countries) == 1:
                    generate_stories(num_story_per_topic, demonym, country_code, country_name)

                elif country_code in countries:
                     generate_stories(num_story_per_topic, demonym, country_code, country_name)
                
                    



@cli.command()
@click.argument('countries', nargs=-1, type=str) # country codes or 'all' for all countries
@click.option('-a', '--analysis', type=str, default='all', help='Type of analysis to perform: names, noun_phrases, tb_sentiment, word_freq')
@click.option('-s', '--startfrom', type=str, default='', help='Start from a specific country code when analysing all')
def analyze(analysis, countries, startfrom):
    if analysis == 'names' or analysis == 'all':
        extract_names(countries, startfrom)
    if analysis == 'nouns' or analysis == 'all':
        extract_noun_phrases(countries, startfrom)
    if analysis == 'textblob' or analysis == 'all':
        tb_sentiment(countries, startfrom)
    if analysis == 'words' or analysis == 'all':
        word_freq(countries, startfrom) 




# @cli.command()
# @click.pass_context
# def extract_names(ctx):
#     """Extract names from stories."""
#     extract_names(ctx)

# @cli.command()
# @click.pass_context
# def extract_noun_phrases(ctx):
#     """Extract noun phrases from stories."""
#     extract_noun_phrases(ctx)

# @cli.command()
# @click.pass_context
# def tb_sentiment_analysis(ctx):
#     """Perform sentiment analysis using TextBlob."""
#     tb_sentiment(ctx)

# @cli.command()
# @click.pass_context
# def word_frequency(ctx):
#     """Calculate word frequency in stories."""
#     word_freq(ctx)

# @cli.command()
# @click.pass_context
# def check_context(ctx):
#     """Check the current context."""
#     click.echo(f"Context contents: {ctx.obj}")


cli.add_command(generate)
cli.add_command(analyze)
# cli.add_command(extract_names)
# cli.add_command(extract_noun_phrases)
# cli.add_command(tb_sentiment_analysis)
# cli.add_command(word_frequency)
# cli.add_command(check_context)


if __name__ == '__main__':
    cli()