import re
import time

import pandas as pd
import matplotlib.pyplot as plt


def create_relevance_table(df: pd.DataFrame, vacancy_name: str) -> list:
    indexes = ['Год',
               'Средняя зарплата',
               'Количество вакансий',
               f'Средняя зарплата - \n{vacancy_name}',
               f'Количество вакансий - \n{vacancy_name}']

    df = df.reset_index()
    table_data = list(df.values.tolist())
    for i in range(len(table_data)):
        table_data[i] = [int(item) for item in table_data[i]]
    table_data.insert(0, indexes)

    return table_data


def create_salary_table(series: pd.Series):
    indexes = ['Город', 'Уровень зарплат']
    table_data = series.reset_index()
    table_data = table_data.values.tolist()
    table_data.insert(0, indexes)

    return table_data


def create_rate_table(series: pd.Series):
    indexes = ['Город', 'Доля вакансий']
    table_data = series.apply(lambda x: f"{x}%").reset_index()
    table_data = table_data.values.tolist()
    table_data.insert(0, indexes)

    return table_data


def get_vacancies_dataframe(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, names=['название', 'навыки', 'от', 'до', 'валюта', 'Город', 'Год'], dtype={
        'название': 'string',
        'навыки': 'string',
        'от': float,
        'до': float,
        'валюта': 'string',
        'город': 'string',
        'год': 'string',
    }, skiprows=1)

    df['Год'] = df['Год'].apply(
        lambda published_at: int(re.sub(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):([0-9+]{7})', r'\1', published_at)))
    df['Средняя з/п'] = df[['от', 'до']].fillna(0).mean(axis=1).astype(int)

    end_time = time.time()
    print(f"csv считан за {end_time-start_time}")

    return df


def get_vacancies_stats_by_year(vacancies_df: pd.DataFrame) -> pd.DataFrame:
    vacancies_by_years = vacancies_df.groupby(['Год']).agg({
        "Средняя з/п": lambda x: round(x.mean(axis=0)),
    })
    vacancies_by_years['Количество вакансий'] = vacancies_df['Год'].value_counts()
    return vacancies_by_years


def get_stats_by_city(vacancies_df: pd.DataFrame) -> [pd.DataFrame, pd.DataFrame]:
    vacancies_by_cities = vacancies_df.groupby('Город', sort=False).agg({
        "Средняя з/п": lambda x: round(x.mean(axis=0)),
    })
    vacancies_by_cities = vacancies_by_cities.rename(columns={'Средняя з/п': 'Уровень зарплат'})
    vacancies_by_cities['count'] = vacancies_df['Город'].value_counts()
    cities_count = vacancies_by_cities['count'].sum(axis=0)
    vacancies_by_cities['Доля вакансий, %'] = pd.Series(vacancies_by_cities['count'] / cities_count * 100).apply(
        lambda x: float("%.2f" % x))
    vacancies_by_cities = vacancies_by_cities[vacancies_by_cities['Доля вакансий, %'] >= 1]
    salaries_by_cities = vacancies_by_cities.sort_values(['Уровень зарплат', 'Город'], ascending=[False, True])[
        'Уровень зарплат'] \
        .head(10)
    vacancies_rates = vacancies_by_cities.sort_values(['Доля вакансий, %', 'Город'], ascending=[False, True])[
        'Доля вакансий, %'].head(10)
    vacancies_rates.loc['Другие'] = float("%.2f" % (100 - vacancies_rates.sum()))
    vacancies_rates.sort_values(inplace=True, ascending=False)

    salaries_by_cities.index.name = None
    index = salaries_by_cities.index.tolist()
    index = [i.replace('-', '-\n') for i in index]
    index = [i.replace(' ', ' \n') for i in index]
    salaries_by_cities.index = pd.Index(index)
    vacancies_rates.name = None
    return salaries_by_cities, vacancies_rates


def get_skills_stats(df: pd.DataFrame) -> dict:
    tables_data = {}
    df = df.copy()
    df = df.dropna(subset=['навыки'])
    df['навыки'] = df['навыки'].apply(lambda x: (x.split('\n')))
    df = df.explode('навыки')[['навыки', 'Год']].groupby('Год', as_index=False).value_counts()
    for year in df['Год'].unique():
        tables_data[str(year)] = df.loc[df['Год'] == year][['навыки', 'count']].head(20).to_numpy().tolist()

    return tables_data


def create_report(filename: str, vacancy_name: str) -> [pd.DataFrame]:
    df = get_vacancies_dataframe(filename)
    if vacancy_name not in vacancies_names:
        filtered_df = df[df['название'].str.contains(vacancy_name, flags=re.IGNORECASE)]
    else:
        filtered_df = df[df['название'].str.contains("|".join(vacancies_names[vacancy_name]), flags=re.IGNORECASE)]

    salaries_by_years = get_vacancies_stats_by_year(df)
    salaries_by_years_for_name = get_vacancies_stats_by_year(filtered_df)
    salaries_by_years_for_name = salaries_by_years_for_name.rename(
        columns={'Средняя з/п': f'з/п {vacancy_name}',
                 'Количество вакансий': f'Количество вакансий {vacancy_name}'})

    combined_stats_by_years = pd.merge(salaries_by_years, salaries_by_years_for_name, on='Год', how='outer').fillna(0)

    salaries_by_cities = get_stats_by_city(df)
    salaries_by_cities_for_name = get_stats_by_city(filtered_df)

    skills_stats = get_skills_stats(df)
    skills_stats_for_name = get_skills_stats(filtered_df)

    return combined_stats_by_years, salaries_by_cities, salaries_by_cities_for_name, skills_stats, skills_stats_for_name


def create_relevance_data(report_data_by_years: pd.DataFrame, vacancy_name: str):
    fig, sub = plt.subplots(2, 2)

    report_data_by_years[['Средняя з/п']].plot(ax=sub[0, 0], kind='bar')
    sub[0, 0].set_title('Динамика уровня зарплат по годам', wrap=True)
    sub[0, 0].grid(True, axis='y')
    sub[0, 0].legend(fontsize=8, loc='upper left')
    sub[0, 0].tick_params(labelsize=8)

    report_data_by_years[['Количество вакансий']].plot(ax=sub[0, 1], kind='bar')
    sub[0, 1].set_title('Динамика количества вакансий по годам', wrap=True)
    sub[0, 1].grid(True, axis='y')
    sub[0, 1].legend(fontsize=8, loc='upper left')
    sub[0, 1].tick_params(labelsize=8)

    report_data_by_years[[f'з/п {vacancy_name}']].plot(ax=sub[1, 0], kind='bar')
    sub[1, 0].set_title(f'Динамика уровня зарплат по годам для {vacancy_name}', wrap=True)
    sub[1, 0].grid(True, axis='y')
    sub[1, 0].legend(fontsize=8, loc='upper left')
    sub[1, 0].tick_params(labelsize=8)

    report_data_by_years[[f'Количество вакансий {vacancy_name}']].plot(ax=sub[1, 1], kind='bar')
    sub[1, 1].set_title(f'Динамика количества вакансий по годам для {vacancy_name}', wrap=True)
    sub[1, 1].grid(True, axis='y')
    sub[1, 1].legend(fontsize=8, loc='upper left')
    sub[1, 1].tick_params(labelsize=8)

    fig.tight_layout()
    fig.savefig('relevance.png', dpi=200)

    return create_relevance_table(report_data_by_years, vacancy_name)


def create_geography_data(report_data_by_cities: [pd.Series], vacancy_name: str):
    salaries_by_cities, salaries_by_cities_for_name = report_data_by_cities

    fig, sub = plt.subplots(2, 2)

    salaries_by_cities[0].plot(ax=sub[0, 0], kind='barh').invert_yaxis()
    sub[0, 0].set_title('Уровень зарплат по городам', wrap=True)
    sub[0, 0].grid(True, axis='x')
    sub[0, 0].tick_params(axis='y', labelsize=6)
    sub[0, 0].tick_params(axis='x', labelsize=8)
    ticklabels = sub[0, 0].get_yticklabels()
    for ticklabel in ticklabels:
        ticklabel.set_ha('right')
        ticklabel.set_va('center')

    salaries_by_cities[1].plot(ax=sub[0, 1], kind='pie', textprops={'fontsize': 6})
    sub[0, 1].set_title('Доля вакансий по городам', wrap=True)
    sub[0, 1].tick_params(labelsize=6)

    salaries_by_cities_for_name[0].plot(ax=sub[1, 0], kind='barh').invert_yaxis()
    sub[1, 0].set_title(f'Уровень зарплат по городам\nдля вакансии {vacancy_name}', wrap=True)
    sub[1, 0].grid(True, axis='x')
    sub[1, 0].tick_params(axis='y', labelsize=6)
    sub[1, 0].tick_params(axis='x', labelsize=8)
    ticklabels = sub[1, 0].get_yticklabels()
    for ticklabel in ticklabels:
        ticklabel.set_ha('right')
        ticklabel.set_va('center')

    salaries_by_cities_for_name[1].plot(ax=sub[1, 1], kind='pie', textprops={'fontsize': 6})
    sub[1, 1].set_title(f'Доля вакансий по городам\nдля вакансии {vacancy_name}', wrap=True)
    sub[1, 1].tick_params(labelsize=6)

    fig.tight_layout()
    fig.savefig('geography.png', dpi=200)

    first_table_data = create_salary_table(salaries_by_cities[0])
    second_table_data = create_salary_table(salaries_by_cities_for_name[0])
    third_table_data = create_rate_table(salaries_by_cities[1])
    fourth_table_data = create_rate_table(salaries_by_cities_for_name[1])

    return [first_table_data, second_table_data, third_table_data, fourth_table_data]


def parse_csv():
    csv = 'vacancies.csv'
    vac = input()
    report = create_report(csv, vac)
    report_by_years = report[0]
    report_by_city = report[1:3]
    skills_stats_by_years = list(report[3:5])

    with open('table_list.txt', mode='w', encoding='utf-8') as file:
        geography = str(create_geography_data(report_by_city, vac)).replace('\'', '\"')
        relevance = str(create_relevance_data(report_by_years, vac)).replace('\'', '\"')
        skills = str(skills_stats_by_years).replace('\'', '\"')
        file.write('JSON для востребованности\n')
        file.write('{"data": %s}\n' % relevance)
        file.write('JSON для географии\n')
        file.write('{"data": %s}\n' % geography)
        file.write('JSON для навыков\n')
        file.write('{"data": %s}\n' % skills)

    end_time = time.time()
    print(f"Время выполнения: {end_time-start_time}")


vacancies_names = {
    "Devops-инженер": ('devops', 'development operations')
}

start_time = time.time()
parse_csv()
