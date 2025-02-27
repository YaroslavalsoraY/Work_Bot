import requests
from aiogram.fsm.state import StatesGroup, State


def get_vacancies(keyword: str):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': keyword,
        'area': 1,
        'per_page': 10
    }
    headers = {
        'User-Agent': 'Yandex'
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        variants = []
        data = response.json()
        vacancies = data.get('items', [])
        num_vacancies = len(vacancies)
        if num_vacancies > 0:
            for vacancy in vacancies:
                vacancy_id = vacancy.get('id')
                vacancy_title = vacancy.get("name")
                vacancy_url = vacancy.get("alternate_url")
                company_name = vacancy.get("employer", {}).get("name")
                variants.append(f'ID: {vacancy_id}\n'
                                f'Название: {vacancy_title}\n'
                                f'Компания: {company_name}\n'
                                f'Ссылка: {vacancy_url}\n\n')
            return variants
        else:
            return ['К сожалению, не нашлось вакансий']
    else:
        return ['Не удалось установить соединение']


class FSM_Vacancies(StatesGroup):
    choosing_vacancy = State()
    vacancy_chosen = State()
