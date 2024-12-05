import click
from generate_stories import main as generate_stories
from analyze_stories import main as analyze_stories
from name_extraction import main as extract_names
from noun_phrases import main as extract_noun_phrases
from sentiment_analysis_textblob import main as tb_sentiment
from sentiment_huggingface import main as hf_sentiment
from watson_sentiment import main as watson_sentiment
from word_compare import main as word_compare
from word_freq import main as word_freq



@click.group()
@click.pass_context()
def cli(ctx):
    """CLI for story processing tasks."""
    ctx.ensure_object(dict)
    pass

@cli.command()
@click.argument('countries')
@click.argument('num_story_per_topic', type=int)
def generate():
    """Generate stories."""
    generate_stories()

@cli.command()
def analyze():
    """Analyze stories."""
    analyze_stories()

@cli.command()
def extract_names():
    """Extract names from stories."""
    extract_names()

@cli.command()
def extract_noun_phrases():
    """Extract noun phrases from stories."""
    extract_noun_phrases()

@cli.command()
def tb_sentiment_analysis():
    """Perform sentiment analysis using TextBlob."""
    tb_sentiment()

@cli.command()
def hf_sentiment_analysis():
    """Perform sentiment analysis using HuggingFace."""
    hf_sentiment()

@cli.command()
def watson_sentiment_analysis():
    """Perform sentiment analysis using Watson."""
    watson_sentiment()

@cli.command()
def compare_words():
    """Compare words in stories."""
    word_compare()

@cli.command()
def word_frequency():
    """Calculate word frequency in stories."""
    word_freq()

if __name__ == '__main__':
    cli()