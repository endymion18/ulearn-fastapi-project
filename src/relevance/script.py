import re
import pandas as pd
import matplotlib.pyplot as plt


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


def create_report_by_years(filename: str, vacancy_name: str) -> [pd.DataFrame, pd.DataFrame, pd.DataFrame,
                                                                 pd.DataFrame]:
    df = get_vacancies_dataframe(filename)
    filtered_df = df[df['название'].str.contains(vacancy_name, flags=re.IGNORECASE)]

    salaries_by_years = get_vacancies_stats_by_year(df)
    salaries_by_years_for_name = get_vacancies_stats_by_year(filtered_df)
    salaries_by_years_for_name = salaries_by_years_for_name.rename(
        columns={'Средняя з/п': f'з/п {vacancy_name}',
                 'Количество вакансий': f'Количество вакансий {vacancy_name}'})

    return salaries_by_years[['Средняя з/п']], salaries_by_years[['Количество вакансий']], \
        salaries_by_years_for_name[[f'з/п {vacancy_name}']], salaries_by_years_for_name[
        [f'Количество вакансий {vacancy_name}']]


def create_plots():
    csv = 'vacancies.csv'
    vac = input()
    report_data_by_years = create_report_by_years(csv, vac)
    # report_data_by_city = create_report_by_years(csv, vac)

    fig1, sub1 = plt.subplots(2, 2)
    fig2, sub2 = plt.subplots(2, 2)

    report_data_by_years[0].plot(ax=sub1[0, 0], kind='bar')
    sub1[0, 0].set_title('Динамика уровня зарплат по годам', wrap=True)
    sub1[0, 0].grid(True, axis='y')
    sub1[0, 0].legend(fontsize=8, loc='upper left')
    sub1[0, 0].tick_params(labelsize=8)

    report_data_by_years[1].plot(ax=sub1[0, 1], kind='bar')
    sub1[0, 1].set_title('Динамика количества вакансий по годам', wrap=True)
    sub1[0, 1].grid(True, axis='y')
    sub1[0, 1].legend(fontsize=8, loc='upper left')
    sub1[0, 1].tick_params(labelsize=8)

    report_data_by_years[2].plot(ax=sub1[1, 0], kind='bar')
    sub1[1, 0].set_title(f'Динамика уровня зарплат по годам для {vac}', wrap=True)
    sub1[1, 0].grid(True, axis='y')
    sub1[1, 0].legend(fontsize=8, loc='upper left')
    sub1[1, 0].tick_params(labelsize=8)

    report_data_by_years[3].plot(ax=sub1[1, 1], kind='bar')
    sub1[1, 1].set_title(f'Динамика количества вакансий по годам для {vac}', wrap=True)
    sub1[1, 1].grid(True, axis='y')
    sub1[1, 1].legend(fontsize=8, loc='upper left')
    sub1[1, 1].tick_params(labelsize=8)

    fig1.tight_layout()
    fig1.savefig('relevance.png', dpi=200)

    return report_data_by_years[0].reset_index().values.tolist(), \
        report_data_by_years[1].reset_index().values.tolist(), \
        report_data_by_years[2].reset_index().values.tolist(), \
        report_data_by_years[3].reset_index().values.tolist()


create_plots()
