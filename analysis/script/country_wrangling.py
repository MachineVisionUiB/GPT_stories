import pandas as pd


def construct_country_data():
    """
    Construct a DataFrame containing country data to use in analysis of stories.

    Data is merged from three sources:
    1. ISO-3361 country codes with demonym and emoji flags - from Statistics Norway's list
    2. World Bank population numbers - from the World Bank (https://data.worldbank.org/indicator/SP.POP.TOTL)
    3. ISO-3166 country codes with regional codes - to match alpha-2 codes to alpha-3 codes and add regions and sub-regions
        This file is downloaded directly from https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the columns 'alpha-2', 'alpha-3', 'country_name', 'flag_emoji', 'demonym', 'region', 'sub-region', and 'population'.
    """

    pd.options.display.float_format = (
        "{:.0f}".format
    )  # Display numbers without decimals

    # read first csv file from SSB (Statistics Norway) - we want to use these countries and country names as defined here
    countries = pd.read_csv(
        "support_data/ISO-3361-country-codes-with-demonyms-and-emoji.csv",
        usecols=["code", "name", "Emoji", "Demonym 1"],
    )

    countries = countries.rename(
        columns={
            "code": "alpha-2",
            "name": "country_name",
            "Emoji": "flag_emoji",
            "Demonym 1": "demonym",
        }
    )

    # read second csv file from World Bank (population numbers)
    population = pd.read_csv(
        "support_data/World_Bank_population_numbers.csv",
        skiprows=4,
        usecols=["Country Code", "2023"],
        #dtype={"2023": int}    # Can set datatype to integer to avoid decimals but then it can't handle empty values (NaN) so keeping as float - add back if needed later
)

    population = population.rename(
        columns={
            "Country Name": "country_name",
            "Country Code": "alpha-3",
            "2023": "population",
        }
    )

    # read third csv file from github (connects alpha-2 to alpha-3 codes and adds regions and subregions)
    codes_and_regions = pd.read_csv(
        "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/refs/heads/master/all/all.csv",
        usecols=["alpha-2", "alpha-3", "region", "sub-region"],
    )

    df = pd.merge(countries, codes_and_regions, on="alpha-2", how="left")
    df = pd.merge(df, population, on="alpha-3", how="left")
 
    df.to_csv("support_data/country_data.csv", index=False)
  
    return df


if __name__ == "__main__":

    construct_country_data()
