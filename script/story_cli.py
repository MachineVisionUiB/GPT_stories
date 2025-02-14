import click
from generate_stories import main as generate_stories
from name_extraction import main as extract_names
from noun_phrases import main as extract_noun_phrases
from sentiment_huggingface import main as sentiment
from word_freq import main as word_freq
from summary_gen import main as generate_summary
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
            if startfrom != "" and startfrom != line[0]: # Skip countries until startfrom country
                continue

            startfrom = "" 
            if line [3] != "": # Skip countries without demonym
                country_code = line[0]
                country_name = line[1]
                demonym = line[3]
                if 'all' in countries and len(countries) == 1: 
                    generate_stories(num_story_per_topic, demonym, country_code, country_name)

                elif country_code in countries:
                     generate_stories(num_story_per_topic, demonym, country_code, country_name)
                
                    



@cli.command()
@click.argument('countries', nargs=-1, type=str) # country codes or 'all' for all countries
@click.option('-a', '--analysis', type=str, multiple=1, default=['all'], help='Type of analysis to perform: names, noun_phrases, tb_sentiment, word_freq')
@click.option('-s', '--startfrom', type=str, default='', help='Start from a specific country code when analysing all')
def analyze(analysis, countries, startfrom):
    
    if "summary" in analysis or "all" in analysis:
        generate_summary(countries, startfrom)
    if "names" in analysis or "all" in analysis:
        extract_names(countries, startfrom)
    if "nouns" in analysis or "all" in analysis:
        extract_noun_phrases(countries, startfrom)
    if "words" in analysis or "all" in analysis:
        word_freq(countries, startfrom)
    if "sentiment" in analysis or "all" in analysis:
        sentiment(countries, startfrom)




cli.add_command(generate)
cli.add_command(analyze)



if __name__ == '__main__':
    cli()