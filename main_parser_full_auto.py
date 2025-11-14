
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import sqlite3
import time
import re


def init_database():
    conn = sqlite3.connect('regulation_projects.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            link TEXT,
            views INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            authority TEXT,
            type TEXT,
            status TEXT,
            procedure TEXT,
            okveds TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn

def save_project_to_db(conn, project_data):
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO projects 
            (id, title, link, views, comments, authority, type, status, procedure, okveds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_data.get('id'),
            project_data.get('title'),
            project_data.get('link'),
            project_data.get('views', 0),
            project_data.get('comments', 0),
            project_data.get('authority'),
            project_data.get('type'),
            project_data.get('status'),
            project_data.get('procedure'),
            project_data.get('okveds')
        ))
        
        conn.commit()
        
    except Exception as e:
        print(f'Ошибка при сохранении в БД: {e}')

def get_all_projects_from_db(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects')
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    
    projects = []
    for row in rows:
        project = dict(zip(columns, row))
        projects.append(project)
    
    return projects

def get_filtered_projects_from_db(conn, min_views=100):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE views >= ?', (min_views,))
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    
    projects = []
    for row in rows:
        project = dict(zip(columns, row))
        projects.append(project)
    
    return projects

def get_statistics_from_db(conn):
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM projects')
    total_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM projects WHERE views >= 100')
    filtered_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(views), SUM(comments), AVG(views), AVG(comments) FROM projects')
    stats = cursor.fetchone()
    
    return {
        'total_count': total_count,
        'filtered_count': filtered_count,
        'total_views': stats[0] or 0,
        'total_comments': stats[1] or 0,
        'avg_views': stats[2] or 0,
        'avg_comments': stats[3] or 0
    }

def open_settings_modal(driver):
    try:
        print('\nИщу кнопку "Настроить"...')
        
        settings_button = None
        
        try:
            print('  Способ 1: Поиск через h1 "Проекты"...')
            h1_projects = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.MuiTypography-root.MuiTypography-h1"))
            )
            print(f' Найден h1: "{h1_projects.text}"')
            
            parent = h1_projects.find_element(By.XPATH, "./ancestor::div[contains(@class, 'MuiGrid-container')]")
            print('  Найден родительский контейнер')
            
            buttons_container = parent.find_element(By.CSS_SELECTOR, "div.MuiGrid-container.mui-1sv05q9")
            print('  Найден контейнер с кнопками')
            
            settings_button = buttons_container.find_element(By.CSS_SELECTOR, "button.MuiButton-outlined.MuiButton-outlinedPrimary")
            print('  Найдена кнопка "Настроить" (способ 1)')
            
        except Exception as e:
            print(f'  Способ 1 не сработал: {e}')
            
            try:
                print('  Способ 2: Прямой поиск по классам кнопки...')
                settings_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mui-1ki8qzm"))
                )
                print('  Найдена кнопка "Настроить" (способ 2)')
                
            except Exception as e2:
                print(f'  Способ 2 не сработал: {e2}')
                
                try:
                    print('  Способ 3: Поиск по тексту "Настроить"...')
                    all_buttons = driver.find_elements(By.CSS_SELECTOR, "button.MuiButton-outlined")
                    
                    for i, btn in enumerate(all_buttons):
                        btn_text = btn.text.strip().lower()
                        print(f'    [{i}] Кнопка: "{btn_text}"')
                        
                        if 'настроить' in btn_text or 'настройки' in btn_text:
                            settings_button = btn
                            print(f'  Найдена кнопка "Настроить" (способ 3) [{i}]')
                            break
                            
                except Exception as e3:
                    print(f'  Способ 3 не сработал: {e3}')
        
        if settings_button:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", settings_button)
            time.sleep(1)
            
            is_displayed = settings_button.is_displayed()
            is_enabled = settings_button.is_enabled()
            print(f'  Кнопка видима: {is_displayed}, активна: {is_enabled}')
            
            if is_displayed and is_enabled:
                try:
                    settings_button.click()
                    print('  Клик по кнопке "Настроить" (обычный клик)')
                except:
                    try:
                        driver.execute_script("arguments[0].click();", settings_button)
                        print('  Клик по кнопке "Настроить" (JavaScript клик)')
                    except:
                        actions = ActionChains(driver)
                        actions.move_to_element(settings_button).click().perform()
                        print('  Клик по кнопке "Настроить" (ActionChains)')
                
                time.sleep(3)
                
                modal = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.MuiDialog-paper.mui-12ca0yz"))
                )
                print('  Модальное окно настроек открыто')
                return modal
            else:
                print('  Кнопка "Настроить" не активна или не видима')
                return None
        else:
            print('Не удалось найти кнопку "Настроить"')
            return None
            
    except Exception as e:
        print(f'Ошибка при открытии модального окна: {e}')
        import traceback
        traceback.print_exc()
        return None

def toggle_option(driver, option_element, option_name):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option_element)
        time.sleep(0.5)
        
        for i in range(1):
            try:
                option_element.click()
            except:
                driver.execute_script("arguments[0].click();", option_element)
            time.sleep(0.3)
        
        print(f'  Опция "{option_name}" обработана')
        return True
        
    except Exception as e:
        print(f'  Ошибка при обработке опции "{option_name}": {e}')
        return False

def click_apply_button(modal):
    try:
        print('\n  Ищу кнопку "Применить"...')
        
        apply_button = modal.find_element(
            By.CSS_SELECTOR, 
            "button.MuiButton-contained.MuiButton-containedPrimary.mui-5l8cti"
        )
        print('  Найдена кнопка "Применить"')
        
        driver = modal.parent
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", apply_button)
        time.sleep(1)
        
        try:
            apply_button.click()
            print('    Клик по кнопке "Применить" (обычный клик)')
        except:
            driver.execute_script("arguments[0].click();", apply_button)
            print('    Клик по кнопке "Применить" (JavaScript клик)')
        
        time.sleep(3)
        print('\nНастройки таблицы применены успешно!')
        return True
        
    except Exception as e:
        print(f'  Не удалось найти или нажать кнопку "Применить": {e}')
        import traceback
        traceback.print_exc()
        return False

def configure_table_columns(driver):
    try:
        print('\n' + '='*60)
        print('НАСТРОЙКА ОТОБРАЖЕНИЯ ТАБЛИЦЫ')
        print('='*60)
        
        modal = open_settings_modal(driver)
        if not modal:
            return False
        
        print('\n  Работаю с опцией "Идентификатор"...')
        try:
            identifier_option = driver.find_element(
                By.CSS_SELECTOR, 
                'div[data-rbd-drag-handle-draggable-id="id"]'
            )
            toggle_option(driver, identifier_option, "Идентификатор")
        except Exception as e:
            print(f'  Не удалось работать с опцией "Идентификатор": {e}')
        
        print('\n  Работаю с опцией "Статистика"...')
        try:
            statistics_option = driver.find_element(
                By.CSS_SELECTOR, 
                'div[data-rbd-drag-handle-draggable-id="npaStatistics"]'
            )
            toggle_option(driver, statistics_option, "Статистика")
        except Exception as e:
            print(f'  Не удалось работать с опцией "Статистика": {e}')


        print('\n  Работаю с опцией "ОКВЭД"...')
        try:
            identifier_option = driver.find_element(
                By.CSS_SELECTOR, 
                'div[data-rbd-drag-handle-draggable-id="okveds"]'
            )
            toggle_option(driver, identifier_option, "ОКВЭД")
        except Exception as e:
            print(f'  Не удалось работать с опцией "ОКВЭД": {e}')
        
        return click_apply_button(modal)
        
    except Exception as e:
        print(f'Ошибка при настройке отображения таблицы: {e}')
        import traceback
        traceback.print_exc()
        return False

def open_advanced_filter(driver):
    try:
        print('\n' + '='*60)
        print('ОТКРЫТИЕ РАСШИРЕННОГО ФИЛЬТРА')
        print('='*60)
        
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Расширенный фильтр') or contains(., 'фильтр')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_button)
        time.sleep(1)
        filter_button.click()
        print('Расширенный фильтр открыт')
        time.sleep(3)
        return True
    except Exception as e:
        print(f'Не удалось открыть расширенный фильтр: {e}')
        return False

def select_procedure_filter(driver):
    try:
        print('\n' + '='*60)
        print('ВЫБОР ФИЛЬТРА "ПРОЦЕДУРА"')
        print('='*60)
        
        print('Ищу поле "Процедура"...')
        
        procedure_select = None
        
        try:
            procedure_label = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//label[contains(., 'Процедура')]"))
            )
            label_for = procedure_label.get_attribute('for')
            print(f'Найден label "Процедура" с for="{label_for}"')
            
            procedure_select = driver.find_element(By.ID, label_for)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", procedure_select)
            time.sleep(1)
            procedure_select.click()
            print('Клик по полю "Процедура"')
            time.sleep(2)
            
        except Exception as e:
            print(f'  Способ 1 не сработал: {e}')
            
            print('  Пробую способ 2: поиск через MuiGrid-item...')
            all_grid_items = driver.find_elements(By.CSS_SELECTOR, "div.MuiGrid-item")
            print(f'  Найдено grid items: {len(all_grid_items)}')
            
            for i, grid_item in enumerate(all_grid_items):
                grid_text = grid_item.text
                if 'Процедура' in grid_text and 'Выберите значение' in grid_text:
                    print(f'  Найден grid item [{i}] с "Процедура"')
                    
                    procedure_select = grid_item.find_element(By.CSS_SELECTOR, "div.MuiSelect-select")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", procedure_select)
                    time.sleep(1)
                    procedure_select.click()
                    print('Клик по полю "Процедура"')
                    time.sleep(2)
                    break
        
        if not procedure_select:
            print('Не удалось найти поле "Процедура"')
            return False
        
        aria_expanded = procedure_select.get_attribute('aria-expanded')
        print(f'  aria-expanded: {aria_expanded}')
        
        if aria_expanded == 'true':
            print('Выпадающий список открыт')
            
            print('\nИщу опцию "Оценка регулирующего воздействия"...')
            
            all_options = driver.find_elements(By.CSS_SELECTOR, "li.MuiMenuItem-root")
            print(f'Найдено опций: {len(all_options)}')
            
            for i, option in enumerate(all_options):
                option_text = option.text
                option_value = option.get_attribute('data-value')
                
                if 'Оценка регулирующего воздействия' in option_text or option_value == '2':
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                    time.sleep(0.5)
                    option.click()
                    print(f'Выбрана опция "Оценка регулирующего воздействия" [{i}]')
                    time.sleep(2)
                    return True
            
            print('Опция "Оценка регулирующего воздействия" не найдена')
            return False
        else:
            print('Выпадающий список не открылся')
            return False
            
    except Exception as e:
        print(f'Ошибка при выборе фильтра "Процедура": {e}')
        import traceback
        traceback.print_exc()
        return False

def select_status_filter(driver):
    try:
        print('\n' + '='*60)
        print('ВЫБОР ФИЛЬТРА "СТАТУС"')
        print('='*60)
        
        print('Ищу поле "Статус"...')
        
        status_select = None
        
        try:
            status_label = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//label[contains(., 'Статус')]"))
            )
            label_for = status_label.get_attribute('for')
            print(f'Найден label "Статус" с for="{label_for}"')
            
            status_select = driver.find_element(By.ID, label_for)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_select)
            time.sleep(1)
            status_select.click()
            print('Клик по полю "Статус"')
            time.sleep(2)
            
        except Exception as e:
            print(f'  Способ 1 не сработал: {e}')
            
            print('  Пробую способ 2: поиск через MuiGrid-item...')
            all_grid_items = driver.find_elements(By.CSS_SELECTOR, "div.MuiGrid-item")
            
            for i, grid_item in enumerate(all_grid_items):
                grid_text = grid_item.text
                if 'Статус' in grid_text and 'Выберите значение' in grid_text:
                    print(f'  Найден grid item [{i}] с "Статус"')
                    
                    status_select = grid_item.find_element(By.CSS_SELECTOR, "div.MuiSelect-select")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_select)
                    time.sleep(1)
                    status_select.click()
                    print('Клик по полю "Статус"')
                    time.sleep(2)
                    break
        
        if not status_select:
            print('Не удалось найти поле "Статус"')
            return False
        
        aria_expanded = status_select.get_attribute('aria-expanded')
        print(f'  aria-expanded: {aria_expanded}')
        
        if aria_expanded == 'true':
            print('Выпадающий список открыт')
            
            print('\nИщу опцию "Идет обсуждение"...')
            
            all_options = driver.find_elements(By.CSS_SELECTOR, "li.MuiMenuItem-root")
            print(f'Найдено опций: {len(all_options)}')
            
            for i, option in enumerate(all_options):
                option_text = option.text
                option_value = option.get_attribute('data-value')
                
                if 'Идет обсуждение' in option_text or option_value == '2':
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                    time.sleep(0.5)
                    option.click()
                    print(f'Выбрана опция "Идет обсуждение" [{i}]')
                    time.sleep(2)
                    return True
            
            print('Опция "Идет обсуждение" не найдена')
            return False
        else:
            print('Выпадающий список не открылся')
            return False
            
    except Exception as e:
        print(f'Ошибка при выборе фильтра "Статус": {e}')
        import traceback
        traceback.print_exc()
        return False

def apply_filters(driver):
    try:
        print('\n' + '='*60)
        print('ПРИМЕНЕНИЕ ФИЛЬТРОВ')
        print('='*60)
        
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Поиск') or contains(., 'ПОИСК')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
        time.sleep(1)
        search_button.click()
        print('Кнопка "Поиск" нажата')
        time.sleep(5)
        return True
        
    except Exception as e:
        print(f'Ошибка при применении фильтров: {e}')
        return False

def parse_regulation_projects(driver, conn):
    projects_count = 0
    
    try:
        print('\n' + '='*60)
        print('НАЧАЛО ПАРСИНГА ПРОЕКТОВ')
        print('='*60)
        
        page_num = 1
        MAX_PAGES = 4
        
        while page_num <= MAX_PAGES:
            print(f'\n{"="*60}')
            print(f'Страница {page_num}/{MAX_PAGES}')
            print(f'{"="*60}')
            
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            tbody = soup.find('tbody')
            if not tbody:
                print('Таблица не найдена!')
                break
            
            rows = tbody.find_all('tr', class_='MuiTableRow-root')
            print(f'Найдено строк в таблице: {len(rows)}')
            
            parsed_on_page = 0
            
            for idx, row in enumerate(rows, 1):
                try:
                    project_data = {}
                    
                    cells = row.find_all('td', class_='MuiTableCell-root')
                    
                    if len(cells) < 3:
                        continue

                    first_cell = cells[0]
                    title_div = first_cell.find('div')
                    if title_div:                        project_data['title'] = title_div.get_text(strip=True)
                    else:
                        project_data['title'] = first_cell.get_text(strip=True)

                    second_cell = cells[1]
                    project_id_text = second_cell.get_text(strip=True)
                    if project_id_text.isdigit():
                        project_data['id'] = project_id_text
                        project_data['link'] = f'https://regulation.gov.ru/projects/{project_id_text}/'

                    third_cell = cells[2]
                    
                    stats_divs = third_cell.find_all('div', class_='MuiGrid-root MuiGrid-item mui-sq014x')
                    
                    if len(stats_divs) >= 2:
                        views_text = stats_divs[0].get_text(strip=True)
                        views_match = re.search(r'(\d+)', views_text)
                        if views_match:
                            project_data['views'] = int(views_match.group(1))
                        
                        comments_text = stats_divs[1].get_text(strip=True)
                        comments_match = re.search(r'(\d+)', comments_text)
                        if comments_match:
                            project_data['comments'] = int(comments_match.group(1))
                    else:
                        stats_text = third_cell.get_text()
                        numbers = re.findall(r'\d+', stats_text)
                        if len(numbers) >= 1:
                            project_data['views'] = int(numbers[0])
                        if len(numbers) >= 2:
                            project_data['comments'] = int(numbers[1])

                    okveds_cell = row.find('td', {'data-index': '3'})
                    if okveds_cell:
                        okveds_text = okveds_cell.get_text(strip=True)
                        if okveds_text:
                            project_data['okveds'] = okveds_text

                    authority_cell = row.find('td', {'data-index': '4'})
                    if authority_cell:
                        authority_text = authority_cell.get_text(strip=True)
                        if authority_text:
                            project_data['authority'] = authority_text
                    if authority_cell:
                        authority_text = authority_cell.get_text(strip=True)
                        if authority_text:
                            project_data['authority'] = authority_text

                    type_cell = row.find('td', class_='mui-1tuqlbi')
                    if type_cell:
                        type_text = type_cell.get_text(strip=True)
                        if type_text:
                            project_data['type'] = type_text

                    project_data['status'] = 'Идет обсуждение'
                    project_data['procedure'] = 'Оценка регулирующего воздействия'

                    if 'title' in project_data and 'id' in project_data:
                        views = project_data.get('views', 0)
                        
                        if views >= 100:
                            save_project_to_db(conn, project_data)
                            projects_count += 1
                            parsed_on_page += 1
                            
                            title_display = project_data['title'][:60]
                            print(f'  [{projects_count}] {title_display}...')
                            print(f'    ID: {project_data["id"]} | Просмотры: {views} | Комментарии: {project_data.get("comments", 0)}')
                            if 'authority' in project_data:
                                print(f'    Орган: {project_data["authority"]}')
                            if 'okveds' in project_data:
                                print(f'    ОКВЭД: {project_data["okveds"]}')
                            if 'type' in project_data:
                                print(f'    Вид: {project_data["type"]}')
                        else:
                            print(f'  Пропущен (просмотров: {views}): {project_data["title"][:60]}...')
                    
                except Exception as e:
                    print(f'  Ошибка при обработке строки {idx}: {e}')
                    continue
            
            print(f'\nНа странице {page_num} обработано проектов: {parsed_on_page}')
            print(f'Всего сохранено в базу данных: {projects_count}')

            if page_num < MAX_PAGES:
                print(f'\nПереход на страницу {page_num + 1}...')
                
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    
                    next_page_num = page_num + 1
                    next_button = None
                    
                    try:
                        next_button = driver.find_element(
                            By.XPATH,
                            f"//button[contains(@class, 'MuiPaginationItem-root') and text()='{next_page_num}']"
                        )
                    except:
                        pass
                    
                    if not next_button:
                        try:
                            next_button = driver.find_element(
                                By.CSS_SELECTOR,
                                "button[aria-label*='next'], button[aria-label*='Next'], button[aria-label*='следующ']"
                            )
                        except:
                            pass
                    
                    if not next_button:
                        try:
                            all_buttons = driver.find_elements(By.CSS_SELECTOR, "button.MuiPaginationItem-root")
                            for btn in all_buttons:
                                if btn.text == str(next_page_num):
                                    next_button = btn
                                    break
                        except:
                            pass
                    
                    if next_button and next_button.is_enabled() and next_button.is_displayed():
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", next_button)
                        time.sleep(4)
                        page_num += 1
                        print(f'Переход на страницу {page_num} выполнен')
                    else:
                        print('Кнопка следующей страницы не найдена')
                        break
                        
                except Exception as e:
                    print(f'Ошибка при переходе на следующую страницу: {e}')
                    break
            else:
                print(f'\nОбработаны все {MAX_PAGES} страницы')
                break
        
        return projects_count
        
    except Exception as e:
        print(f'\nКритическая ошибка при парсинге: {e}')
        import traceback
        traceback.print_exc()
        return projects_count


def main():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    conn = None
    
    try:
        conn = init_database()
        
        url = 'https://regulation.gov.ru/projects/?type=Grid'
        print(f'\n{"="*60}')
        print('ЗАПУСК ПОЛНОСТЬЮ АВТОМАТИЗИРОВАННОГО ПАРСЕРА')
        print(f'{"="*60}')
        print(f'\nОткрываю: {url}')
        driver.get(url)
        
        print('\nЖду загрузки страницы...')
        time.sleep(5)

        if not open_advanced_filter(driver):
            print('\nНе удалось открыть расширенный фильтр. Продолжаю без фильтров...')
        else:

            if not select_procedure_filter(driver):
                print('\nНе удалось выбрать фильтр "Процедура"')

            if not select_status_filter(driver):
                print('\nНе удалось выбрать фильтр "Статус"')

            if not apply_filters(driver):
                print('\nНе удалось применить фильтры')

        time.sleep(3)
        if not configure_table_columns(driver):
            print('\nНе удалось настроить отображение таблицы. Продолжаю с текущими настройками...')

        time.sleep(3)
        projects_count = parse_regulation_projects(driver, conn)

        print('\n' + '='*60)
        print('ПОЛУЧЕНИЕ СТАТИСТИКИ ИЗ БАЗЫ ДАННЫХ')
        print('='*60)

        stats = get_statistics_from_db(conn)
        
        print(f'\nВсего проектов в базе: {stats["total_count"]}')
        print(f'Проектов с 100+ просмотров: {stats["filtered_count"]}')
        
        if stats['total_count'] > 0:
            print(f'\nОбщая статистика:')
            print(f'  Всего просмотров: {stats["total_views"]}')
            print(f'  Всего комментариев: {stats["total_comments"]}')
            print(f'  Средние просмотры: {stats["avg_views"]:.1f}')
            print(f'  Средние комментарии: {stats["avg_comments"]:.1f}')
        
        print('\n' + '='*60)
        print('ПАРСИНГ ЗАВЕРШЕН УСПЕШНО!')
        print('='*60)
        print(f'\nДанные сохранены в базу: regulation_projects.db')
        print(f'Всего записей: {projects_count}')
        
        return conn
        
    except KeyboardInterrupt:
        print('\n\nПарсинг прерван пользователем')
        
        if conn:
            stats = get_statistics_from_db(conn)
            print(f'Сохранено {stats["total_count"]} проектов в базу данных')
        
        return conn
        
    except Exception as e:
        print(f'\nКритическая ошибка: {e}')
        import traceback
        traceback.print_exc()
        return conn
        
    finally:
        print('\n' + '='*60)
        print('Закрываю браузер через 5 секунд...')
        print('='*60)
        time.sleep(5)
        driver.quit()
        
        if conn:
            conn.close()
            print('Соединение с базой данных закрыто')

if __name__ == '__main__':
    conn = main()
    
    print('\n' + '='*60)
    print('БАЗА ДАННЫХ:')
    print('='*60)
    print('- regulation_projects.db (SQLite база данных)')
    print('='*60)