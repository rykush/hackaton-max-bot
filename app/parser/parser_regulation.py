import requests
import xml.etree.ElementTree as ET
from app.database.session import get_db
from app.database.models import Parser_data


url = "https://regulation.gov.ru/api/npalist/"
filters = {
    'limit': 50,
    'fields': 'title,department,kind,procedure,date,startDiscussion,endDiscussion,status',
    'sort':'desc'
}

async def parsing(filters: dict = filters, url: str = url):
    print('Начало парсинга')
    try:
        response = requests.get(url, params=filters)
        response.raise_for_status()
        
        content_type = response.headers.get('content-type', '').lower()
        
        if 'application/xml' in content_type or 'text/xml' in content_type:
            print('parsing: yes')
            await add_data(response=response.content)
            # await check_parser_data_in_db()
            # await print_xml_response(response)
        else:
            print(response.text)
        
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except Exception as e:
        print(f"Ошибка обработки ответа: {e}")

async def parsing_project(id):
    try:
        response = requests.get(url+str(id))
        response.raise_for_status()
        content_type = response.headers.get('content-type', '').lower()

        if 'application/xml' in content_type or 'text/xml' in content_type:
            root = ET.fromstring(response.content)
            project = root.find('project')
            title_elem = project.find('title')
            kind_elem = project.find('kind')
            department_elem = project.find('department')
            start_discussion = project.find('startDiscussion')
            end_discussion = project.find('endDiscussion')
            message_text = {
                'url': f'https://regulation.gov.ru/projects/{id}',
                'title': title_elem.text if title_elem is not None else None,
                'kind': kind_elem.text if kind_elem is not None else None,
                'department': department_elem.text if department_elem is not None else None,
                'startDiscussion': start_discussion.text if start_discussion is not None else None,
                'endDiscussion': end_discussion.text if end_discussion is not None else None
            }
            return message_text
        else:
            print(response.text)
    except Exception as e:
        print("Ошибка Parser.parsing_project(): ", e)

async def add_data(response: bytes):
    try:
        print('add_data: start')
        root = ET.fromstring(response)
        db = next(get_db())
        for project in root.findall('project'):
            procedure = project.find('procedure')
            if str(project.find('status').text) == 'Идет обсуждение':
                if db.query(Parser_data).filter_by(document_id=project.get('id')).first() is None:
                    if procedure is not None and procedure.get('id') == '2':
                        kind_elem = project.find('kind')
                        department_elem = project.find('department')
                        start_discussion = project.find('startDiscussion')
                        end_discussion = project.find('endDiscussion')
                        filters = {
                            'kind': kind_elem.get('id') if kind_elem is not None else None,
                            'department': department_elem.get('id') if department_elem is not None else None,
                            'startDiscussion': start_discussion.text if start_discussion is not None else None,
                            'endDiscussion': end_discussion.text if end_discussion is not None else None
                        }
                        print(project.get('id'))
                        parser_data = Parser_data(
                            document_id=project.get('id'),
                            document_filters=filters
                        )
                        db.add(parser_data)
                        db.commit()
                        print('commit')
        print('add_data: end')
    except Exception as e:
        print('Ошибка add_data:', e)

async def check_parser_data_in_db():
    db = next(get_db())
    data = db.query(Parser_data).all()
    for u in data:
        print(u.document_id, u.document_filters)


async def print_xml_response(response: requests.Response) -> None:
    try:
        root = ET.fromstring(response.content)
        
        def print_element(element, indent=0):
            spaces = "  " * indent
            attrs = " ".join([f'{k}="{v}"' for k, v in element.attrib.items()])
            attrs_str = f" {attrs}" if attrs else ""
            
            if len(element) == 0 and element.text and element.text.strip():
                print(f"{spaces}<{element.tag}{attrs_str}>{element.text.strip()}</{element.tag}>")
            elif element.attrib:
                print(f"{spaces}<{element.tag}{attrs_str}>")
                for child in element:
                    print_element(child, indent + 1)
                print(f"{spaces}</{element.tag}>")
            else:
                print(f"{spaces}<{element.tag}>")
                for child in element:
                    print_element(child, indent + 1)
                print(f"{spaces}</{element.tag}>")
        
        print_element(root)
        
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML: {e}")
        print("Сырой ответ:")
        print(response.text)

# pars.check_parser_data_in_db()